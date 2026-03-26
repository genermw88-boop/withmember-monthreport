import streamlit as st
import requests
from datetime import datetime

# -----------------------------------------------------------------
# 1. 네이버 블로그 검색 API (스나이퍼 타겟팅 및 날짜 필터링 로직)
# -----------------------------------------------------------------
def get_sharp_blog_data(store_name, region, campaign_key, client_id, client_secret):
    # 검색어를 정교하게 조합합니다 (예: "달서구 동경생고기 리뷰노트")
    query = f"{region} {store_name}"
    if campaign_key:
        query += f" {campaign_key}"
        
    # sort=date 를 추가하여 가장 최근에 쓰여진 글부터 가져옵니다.
    url = f"https://openapi.naver.com/v1/search/blog?query={query}&display=100&sort=date"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            
            # 1. 뾰족한 검색어로 걸러진 전체 누적 문서 수
            total_accumulated = result.get('total', 0)
            
            # 2. 이번 달 신규 발행 건수만 정확히 추출
            current_ym = datetime.now().strftime("%Y%m") # 예: "202603"
            items = result.get('items', [])
            
            # 가져온 100개의 최신 글 중, 발행일이 이번 달인 것만 카운트합니다.
            monthly_new = sum(1 for item in items if item.get('postdate', '').startswith(current_ym))
            
            return total_accumulated, monthly_new
        else:
            st.warning(f"API 호출 실패 (상태 코드: {response.status_code}) - Secrets 키를 확인해주세요.")
            return 0, 0
    except Exception as e:
        st.error(f"블로그 API 통신 에러: {e}")
        return 0, 0

# -----------------------------------------------------------------
# 2. 메인 UI 및 보고서 생성 로직 
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📊", layout="wide")

st.title("📊 WithMember 월간 마케팅 분석 보고서 생성기")
st.markdown("정교한 검색 API 로직으로 매장의 실제 블로그 리뷰를 자동 추출하고 분석합니다.")

# 서버의 Secrets에서 API 키 로드
try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 네이버 API 키가 없습니다.")
    st.stop()

with st.form("report_form"):
    st.subheader("📌 1. 타겟 매장 정보 (블로그 자동 추출용)")
    st.caption("넓은 키워드(예: 대구 맛집)가 아닌, 우리 매장만 잡힐 수 있도록 구체적으로 적어주세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("매장명 (필수)", placeholder="예: 동경생고기")
    with col2:
        region = st.text_input("세부 지역명 (필수)", placeholder="예: 달서구")
    with col3:
        campaign_key = st.text_input("캠페인 키워드 (선택)", placeholder="예: 리뷰노트 (없으면 비워두세요)")

    st.divider()

    st.subheader("📊 2. 플레이스 및 외부 매체 (수기 입력)")
    st.caption("※ 네이버 플레이스는 봇(Bot) 차단이 심해 수기로 입력하는 것이 가장 빠르고 안전합니다.")
    
    col4, col5 = st.columns(2)
    with col4:
        place_total_reviews = st.number_input("이번 달 신규 방문자 리뷰 수 (네이버)", min_value=0, value=0)
        place_replies = st.number_input("이번 달 사장님 답글 수 (네이버)", min_value=0, value=0)
    with col5:
        google_review_cnt = st.number_input("이번 달 구글/카카오 리뷰 증가 수", min_value=0, value=0)
        insta_views = st.number_input("이번 달 인스타 영상 총 조회수", min_value=0, value=0)

    submit_button = st.form_submit_button("전문가용 마케팅 보고서 추출")

# -----------------------------------------------------------------
# 3. 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not region:
        st.warning("정확한 데이터 추출을 위해 '매장명'과 '세부 지역명'을 꼭 입력해주세요.")
    else:
        with st.spinner('블로그 데이터를 자동 추출하고 분석 리포트를 작성 중입니다...'):
            
            # API 자동 추출 실행
            total_blogs, monthly_blogs = get_sharp_blog_data(store_name, region, campaign_key, naver_client_id, naver_client_secret)
            
            # 소통율 계산
            reply_rate = round((place_replies / place_total_reviews) * 100, 1) if place_total_reviews > 0 else 0
            current_month = datetime.now().month

            st.success("✅ 블로그 데이터 자동 추출 및 보고서 생성이 완료되었습니다!")
            
            # 리포트 출력
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 성과 분석 리포트")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 💬 1. 플레이스 고객 소통 및 활성도 지수")
            st.markdown(f"> **이번 달 신규 방문자 리뷰 {place_total_reviews}건 중, 사장님 답글 {place_replies}건 완료 (소통율 {reply_rate}%)**")
            st.markdown("- **로직 분석:** 네이버 알고리즘은 관리자와 고객 간의 활발한 소통이 일어나는 매장에 플레이스 지수(Place Index) 가점을 크게 부여합니다. 꾸준한 답글 관리는 검색 순위 최적화(SEO)의 가장 탄탄한 기반이 됩니다.")
            
            st.markdown("### 📝 2. 블로그 리뷰(리뷰노트) 자동 추출 현황")
            # 자동 추출된 데이터가 바로 꽂힙니다.
            st.markdown(f"> **관련 블로그 리뷰 총 {total_blogs:,}건 누적 (이번 달 신규 발행 {monthly_blogs}건 자동 확인)**")
            st.markdown(f"- **로직 분석:** '{region} {store_name}' 관련하여 양질의 C-Rank 포스팅이 지속적으로 누적되고 있습니다. 특히 이번 달 새롭게 발행된 {monthly_blogs}건의 고품질 리뷰가 모바일 스마트블록 영역에서 활동하며, 매장으로 넘어오는 '징검다리 트래픽(전환율)'을 톡톡히 견인하고 있습니다.")
            
            st.markdown("### 🗺️ 3. 로컬 SEO 및 외부 지도 플랫폼 확장성")
            st.markdown(f"> **구글맵스 및 카카오맵 신규 우수 리뷰 총 {google_review_cnt}건 확보**")
            st.markdown("- **로직 분석:** 네이버는 타 플랫폼에서의 브랜드 인지도를 간접 평가에 반영합니다. 외부 앱에서의 긍정적 평판은 길 찾기 후 바로 방문하는 '고관여 고객'의 방문 전환을 직접적으로 끌어올리는 지표입니다.")
            
            st.markdown("### 📱 4. SNS 바이럴 트래픽 및 마케팅 선순환(Flywheel)")
            st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
            st.markdown("- **로직 분석:** 폭발적인 인스타그램 조회수는 잠재 고객들이 네이버에서 매장 이름을 직접 검색하게 만드는 '브랜드 검색'을 유발합니다. 직접 검색을 통한 트래픽 유입은 네이버 로직 상 가장 강력한 순위 상승 동력으로 작용하고 있습니다.")
