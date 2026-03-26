import streamlit as st
import requests
import re
from datetime import datetime

# -----------------------------------------------------------------
# 1. API 통신 및 데이터 처리 함수
# -----------------------------------------------------------------
def clean_html(raw_html):
    # 네이버 API 결과의 <b> 태그 등 불필요한 HTML을 제거하는 함수
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).replace('&amp;', '&')

def get_naver_api_data(keyword, store_name, client_id, client_secret):
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    # 1. 지역 검색 API (플레이스 순위 추출)
    local_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=100"
    current_rank = 0 # 기본값 (100위 밖)
    
    try:
        res_local = requests.get(local_url, headers=headers)
        if res_local.status_code == 200:
            items = res_local.json().get('items', [])
            for index, item in enumerate(items):
                title = clean_html(item.get('title', ''))
                # API 검색 결과에서 매장명이 포함되어 있으면 해당 순위 기록
                if store_name.replace(" ", "") in title.replace(" ", ""):
                    current_rank = index + 1
                    break
    except Exception as e:
        st.error(f"순위 검색 API 에러: {e}")

    # 2. 블로그 검색 API (홍보 키워드 누적 리뷰 수 추출)
    blog_url = f"https://openapi.naver.com/v1/search/blog.json?query={keyword}&display=10"
    total_blogs = 0
    
    try:
        res_blog = requests.get(blog_url, headers=headers)
        if res_blog.status_code == 200:
            total_blogs = res_blog.json().get('total', 0)
    except Exception as e:
        st.error(f"블로그 검색 API 에러: {e}")
        
    return current_rank, total_blogs

# -----------------------------------------------------------------
# 2. 메인 UI 및 입력 폼
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 보고서 생성기")
st.markdown("정확한 수기 데이터와 네이버 API를 결합하여 고객사 맞춤형 평가 보고서를 생성합니다.")

# Secrets에서 API 키 로드
try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 네이버 API 키가 없습니다. 먼저 세팅해 주세요.")
    st.stop()

with st.form("report_form"):
    st.subheader("📌 1. 매장 및 타겟 정보")
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("매장명 (정확히 입력)", placeholder="예: 동경생고기")
    with col2:
        promo_keyword = st.text_input("메인 홍보 키워드", placeholder="예: 대구 달서구 맛집")
    with col3:
        prev_rank = st.number_input("지난달 순위 (상승폭 계산용)", min_value=1, value=15)

    st.divider()

    st.subheader("📊 2. 성과 데이터 입력")
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("**[내부 소통 및 리뷰 지표]**")
        place_replies = st.number_input("이번 달 방문자 리뷰 답글 수", min_value=0, value=0)
    with col5:
        st.markdown("**[외부 다매체 지표]**")
        kakao_google_reviews = st.number_input("이번 달 카카오맵/구글 신규 리뷰 수", min_value=0, value=0)
        insta_views = st.number_input("이번 달 인스타 총 조회수", min_value=0, value=0)

    st.divider()

    st.subheader("🔗 3. 이번 달 핵심 블로그 리뷰 링크 (최대 10개)")
    st.caption("보고서에 첨부할 우수 리뷰노트 링크를 입력해 주세요. (빈칸은 출력되지 않습니다)")
    
    links = []
    # 2열로 깔끔하게 10개 입력칸 배치
    link_cols = st.columns(2)
    for i in range(10):
        with link_cols[i % 2]:
            link = st.text_input(f"블로그 링크 {i+1}")
            links.append(link)

    submit_button = st.form_submit_button("전문가용 보고서 추출하기")

# -----------------------------------------------------------------
# 3. 데이터 분석 및 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not promo_keyword:
        st.warning("매장명과 홍보 키워드를 입력해 주세요.")
    else:
        with st.spinner('API 데이터를 분석하고 리포트를 작성 중입니다...'):
            
            # API 추출
            current_rank, total_blogs = get_naver_api_data(promo_keyword, store_name, naver_client_id, naver_client_secret)
            
            # 순위 증감 계산 로직
            rank_text = ""
            if current_rank == 0:
                rank_text = f"현재 100위 밖 (순위 진입을 위한 트래픽 작업 진행 중)"
            else:
                diff = prev_rank - current_rank
                if diff > 0:
                    rank_text = f"**{current_rank}위** (전월 대비 🔺{diff}계단 상승)"
                elif diff < 0:
                    rank_text = f"**{current_rank}위** (전월 대비 🔻{abs(diff)}계단 하락 - 추가 관리 요망)"
                else:
                    rank_text = f"**{current_rank}위** (전월 순위 유지)"

            current_month = datetime.now().month

            st.success("✅ 평가 보고서 생성이 완료되었습니다!")
            
            # -------------------------------------------------------------
            # [보고서 출력부]
            # -------------------------------------------------------------
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 성과 평가 보고서")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 순위 평가
            st.markdown("### 🥇 1. 네이버 스마트플레이스 순위 최적화 평가")
            st.markdown(f"> **'{promo_keyword}' 검색 시 현재 노출 순위: {rank_text}**")
            st.markdown("- **평가 보고:** 네이버 지역 검색 API를 통해 실시간으로 확인된 데이터입니다. 꾸준한 유효 트래픽 유입과 체류 시간 증가가 알고리즘 상 긍정적인 신호(Positive Signal)로 작용하여 검색 최상단으로 이동하고 있습니다. 이는 광고비 지출 없이도 예약 및 방문 전환율을 획기적으로 높이는 핵심 동력입니다.")
            
            # 2. 블로그 리뷰 평가
            st.markdown(f"### 📝 2. '{promo_keyword}' 타겟 블로그 마케팅 평가")
            st.markdown(f"> **네이버 전체 검색 노출 문서: 총 {total_blogs:,}건 확보**")
            st.markdown("- **평가 보고:** 단순 배포가 아닌 네이버 C-Rank(크리에이터 신뢰도) 알고리즘에 부합하는 양질의 리뷰노트들이 성공적으로 안착했습니다. 이 문서들이 모바일 스마트블록 영역에 노출되면서, 맛집을 탐색하는 고객들의 '징검다리 트래픽' 역할을 완벽하게 수행하고 있습니다.")
            
            # 입력된 블로그 링크 리스트업
            valid_links = [l for l in links if l.strip()]
            if valid_links:
                st.markdown("**[이번 달 우수 리뷰 링크 모음]**")
                for idx, valid_link in enumerate(valid_links):
                    st.markdown(f"{idx+1}. {valid_link}")
            
            # 3. 방문자 답글 & 다매체 평가
            st.markdown("### 💬 3. 플레이스 소통 지수 및 로컬 다매체 확장 평가")
            st.markdown(f"> **방문자 리뷰 사장님 답글 {place_replies}건 완료 / 구글·카카오맵 신규 리뷰 {kakao_google_reviews}건 확보**")
            st.markdown("- **평가 보고:** 네이버 알고리즘은 '관리자가 적극적으로 소통하는 매장'에 강력한 SEO 가점을 부여합니다. 꼼꼼한 답글 관리가 플레이스 지수를 탄탄하게 받쳐주고 있습니다. 또한, 구글/카카오맵의 평판 상승은 길 찾기 후 바로 방문하는 2030 직장인 및 외국인 관광객 등 고관여 고객층의 신뢰도(Trust Score)를 상승시켜 직접 방문율을 크게 끌어올리고 있습니다.")
            
            # 4. 인스타 트래픽 평가
            st.markdown("### 📱 4. SNS 바이럴 파급력 및 마케팅 선순환 평가")
            st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
            st.markdown("- **평가 보고:** 숏폼 영상을 통한 폭발적인 조회수는 인스타그램 내에서 끝나지 않습니다. 영상을 본 수만 명의 잠재 고객이 네이버에서 우리 매장 이름을 '직접 검색(Brand Search)'하게 만들며, 이 자연 유입 트래픽이 네이버 로직 상 매장 인기도를 증명하는 가장 강력한 순위 상승 무기로 작용하고 있습니다.")
            
            st.markdown("---")
            st.markdown("💡 **WithMember 인사이트:** 모든 채널(플레이스, 블로그, SNS, 다매체)의 마케팅이 유기적으로 맞물려 훌륭한 선순환(Flywheel) 구조를 완성했습니다. 다음 달에도 현재의 긍정적인 상승 기류를 유지하기 위해 최선을 다하겠습니다.")
