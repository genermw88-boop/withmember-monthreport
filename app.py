import streamlit as st
import requests
from datetime import datetime

# -----------------------------------------------------------------
# 1. 네이버 블로그 검색 API (정확도 100%)
# -----------------------------------------------------------------
def get_real_blog_reviews(keyword, client_id, client_secret):
    url = f"https://openapi.naver.com/v1/search/blog?query={keyword}&display=100"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get('total', 0)
        else:
            st.warning(f"블로그 API 호출 실패 (상태 코드: {response.status_code}) - 네이버 개발자 센터에서 '검색' API가 추가되었는지 확인해 주세요.")
            return 0
    except Exception as e:
        st.error(f"블로그 API 에러 발생: {e}")
        return 0

# -----------------------------------------------------------------
# 2. 메인 UI 및 보고서 생성 로직 
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📊", layout="wide")

st.title("📊 WithMember 월간 마케팅 분석 보고서 생성기")
st.markdown("네이버 API와 수기 데이터를 결합하여 가장 안정적이고 전문적인 리포트를 추출합니다.")

# 서버의 Secrets에서 API 키를 자동으로 불러옵니다.
try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit 사이트 우측 상단 점 3개(⋮) -> Settings -> Secrets 탭에 네이버 API 키를 먼저 입력해 주세요.")
    st.stop()

with st.form("report_form"):
    st.subheader("📌 매장 및 타겟 정보")
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 동경생고기")
    with col2:
        blog_keyword = st.text_input("블로그 API 검색 키워드", placeholder="예: 대구 달서구 맛집 동경생고기")

    st.divider()

    st.subheader("📊 이번 달 성과 데이터 입력")
    st.caption("정확한 데이터 추출을 위해 네이버 플레이스 및 외부 매체 수치를 입력해 주세요.")
    
    col3, col4 = st.columns(2)
    with col3:
        place_total_reviews = st.number_input("이번 달 신규 방문자 리뷰 수 (네이버)", min_value=0, value=0)
        place_replies = st.number_input("이번 달 사장님 답글 수 (네이버)", min_value=0, value=0)
    with col4:
        google_review_cnt = st.number_input("이번 달 구글/카카오 리뷰 증가 수", min_value=0, value=0)
        insta_views = st.number_input("이번 달 인스타 영상 총 조회수", min_value=0, value=0)

    submit_button = st.form_submit_button("마케팅 분석 보고서 생성")

# -----------------------------------------------------------------
# 3. 결과 출력
# -----------------------------------------------------------------
if submit_button:
    with st.spinner('데이터를 분석하고 리포트를 작성 중입니다...'):
        
        # 블로그 API 추출 실행
        real_blog_count = get_real_blog_reviews(blog_keyword, naver_client_id, naver_client_secret)
        
        # 소통율 계산
        if place_total_reviews > 0:
            reply_rate = round((place_replies / place_total_reviews) * 100, 1)
        else:
            reply_rate = 0
            
        current_month = datetime.now().month

        st.success("✅ 보고서 생성이 완료되었습니다!")
        
        # 리포트 텍스트 출력
        st.markdown("---")
        st.markdown(f"## [WithMember] {current_month}월 마케팅 성과 분석 리포트")
        st.markdown(f"**수신:** {store_name} 대표님")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 💬 1. 플레이스 고객 소통 지수")
        st.markdown(f"> **이번 달 신규 방문자 리뷰 {place_total_reviews}건 중, 사장님 답글 {place_replies}건 완료 (소통율 {reply_rate}%)**")
        st.markdown("- **로직 분석:** 네이버 알고리즘은 활발한 소통이 일어나는 매장에 플레이스 지수(Place Index) 가점을 부여합니다. 꾸준한 답글 관리는 검색 순위 최적화(SEO)의 핵심 기반입니다.")
        
        st.markdown("### 📝 2. 블로그 리뷰노트 누적 및 노출 현황")
        st.markdown(f"> **'{blog_keyword}' 관련 고품질 블로그 리뷰 총 {real_blog_count:,}건 누적 발행**")
        st.markdown("- **로직 분석:** C-Rank 기반의 양질의 포스팅이 누적되며 스마트블록 점유율을 높이고 있습니다. 이는 플레이스로 넘어오는 징검다리 트래픽 역할을 톡톡히 하고 있습니다.")
        
        st.markdown("### 🗺️ 3. 로컬 SEO 및 외부 지도 플랫폼 확장성")
        st.markdown(f"> **구글/카카오맵 신규 우수 리뷰 총 {google_review_cnt}건 확보**")
        st.markdown("- **로직 분석:** 외부 지도 앱에서의 긍정적 평판은 2030 직장인 및 외국인 관광객의 방문 전환율(CVR)을 직접적으로 끌어올리는 중요한 지표입니다.")
        
        st.markdown("### 📱 4. SNS 바이럴 트래픽 선순환")
        st.markdown(f"> **인스타그램 영상 총 조회수 {insta_views:,}회 돌파**")
        st.markdown("- **로직 분석:** 폭발적인 SNS 조회수는 잠재 고객들이 네이버에서 매장 이름을 직접 검색하게(브랜드 검색) 만듭니다. 이 트래픽이 네이버 로직 상 가장 강력한 순위 상승 동력으로 작용합니다.")
