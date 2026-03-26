import streamlit as st
import requests
import re
from datetime import datetime

# -----------------------------------------------------------------
# 1. API 통신 및 데이터 처리 함수 (현재 순위 전용)
# -----------------------------------------------------------------
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).replace('&amp;', '&')

def get_current_place_rank(keyword, store_name, client_id, client_secret):
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    # 지역 검색 API (현재 순위 추출)
    local_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=100"
    current_rank = 0 
    
    try:
        res = requests.get(local_url, headers=headers)
        if res.status_code == 200:
            items = res.json().get('items', [])
            for index, item in enumerate(items):
                title = clean_html(item.get('title', ''))
                # 띄어쓰기 무시하고 매장명 매칭
                if store_name.replace(" ", "") in title.replace(" ", ""):
                    current_rank = index + 1
                    break
        else:
            st.warning("순위 API 호출 실패. API 키를 확인하세요.")
    except Exception as e:
        st.error(f"순위 검색 중 오류 발생: {e}")
        
    return current_rank

# -----------------------------------------------------------------
# 2. 메인 UI 및 입력 폼
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 홍보 효과 보고서")
st.markdown("자동 API 추출과 수기 데이터를 결합하여 가장 정확한 실질적 홍보 효과를 분석합니다.")

try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 네이버 API 키가 없습니다.")
    st.stop()

with st.form("report_form"):
    st.subheader("📌 1. 타겟 키워드 및 순위 데이터")
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("매장명 (정확히 입력)", placeholder="예: 동경생고기")
    with col2:
        promo_keyword = st.text_input("메인 홍보 키워드", placeholder="예: 대구 달서구 맛집")
    with col3:
        prev_rank = st.number_input("지난달 순위 (직접 입력)", min_value=1, value=15)

    st.divider()

    st.subheader("📝 2. 블로그 홍보 성과 입력")
    st.caption("발행된 블로그의 링크와 누적된 총 반응(좋아요/댓글)을 입력해 주세요.")
    
    blog_link = st.text_input("이번 달 대표 우수 블로그 링크")
    col4, col5 = st.columns(2)
    with col4:
        blog_likes = st.number_input("위 블로그들의 총 좋아요(공감) 수", min_value=0, value=0)
    with col5:
        blog_comments = st.number_input("위 블로그들의 총 댓글 수", min_value=0, value=0)

    st.divider()

    st.subheader("💬 3. 고객 관리 및 바이럴 홍보 지표")
    col6, col7 = st.columns(2)
    with col6:
        place_replies = st.number_input("네이버 방문자 리뷰 사장님 답글 수", min_value=0, value=0)
        kakao_google_reviews = st.number_input("카카오맵/구글 신규 우수 리뷰 수", min_value=0, value=0)
    with col7:
        insta_views = st.number_input("인스타 홍보 영상 총 조회수", min_value=0, value=0)

    submit_button = st.form_submit_button("마케팅 홍보 효과 평가 생성")

# -----------------------------------------------------------------
# 3. 데이터 분석 및 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not promo_keyword:
        st.warning("매장명과 홍보 키워드를 모두 입력해 주세요.")
    else:
        with st.spinner('API로 현재 순위를 추출하고 홍보 효과를 분석 중입니다...'):
            
            # API 순위 추출 실행
            current_rank = get_current_place_rank(promo_keyword, store_name, naver_client_id, naver_client_secret)
            
            # 순위 증감 로직
            rank_text = ""
            if current_rank == 0:
                rank_text = f"현재 100위 밖 (API 검색 범위 외)"
            else:
                diff = prev_rank - current_rank
                if diff > 0:
                    rank_text = f"**{current_rank}위** (전월 {prev_rank}위 대비 🔺{diff}계단 상승)"
                elif diff < 0:
                    rank_text = f"**{current_rank}위** (전월 {prev_rank}위 대비 🔻{abs(diff)}계단 하락)"
                else:
                    rank_text = f"**{current_rank}위** (전월 순위 유지)"

            current_month = datetime.now().month

            st.success("✅ 평가 보고서 생성이 완료되었습니다!")
            
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 홍보 효과 보고서")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 순위 평가
            st.markdown(f"### 🥇 1. '{promo_keyword}' 검색 노출 및 유입 효과")
            st.markdown(f"> **현재 검색 노출 순위: {rank_text}**")
            if current_rank > 0 and current_rank <= prev_rank:
                st.markdown(f"- **홍보 효과 평가:** 지역 핵심 타겟 키워드인 '{promo_keyword}'에서 상위 노출을 점유하여, 식사를 고민하는 잠재 고객들의 실질적인 유입 트래픽이 집중되고 있습니다. 이러한 상위권 유지는 전단지 수만 장을 뿌리는 것 이상의 강력한 인지도 상승효과를 가져오며, 즉각적인 방문 전환으로 이어지고 있습니다.")
            else:
                st.markdown(f"- **홍보 효과 평가:** 현재 순위 변동을 모니터링 중이며, 더욱 최적화된 유효 트래픽 유입과 체류 시간 증가 작업을 통해 최상단 노출을 위한 기반을 다지고 있습니다.")
            
            # 2. 블로그 리뷰 평가 (좋아요/댓글 기반)
            st.markdown(f"### 📝 2. 블로그 리뷰노트 반응도 및 입소문 효과")
            if blog_link:
                st.markdown(f"> **우수 블로그 링크:** {blog_link}")
            st.markdown(f"> **고객 반응도: 좋아요 {blog_likes}개 / 댓글 {blog_comments}개 확보**")
            st.markdown(f"- **홍보 효과 평가:** 단순한 리뷰 발행을 넘어, 실제 유저들의 '좋아요'와 '댓글' 등 활발한 인게이지먼트(참여)가 발생했습니다. 이는 해당 리뷰가 네이버 알고리즘상 '신뢰도 높은 정보'로 분류되게 만들며, 글을 읽은 잠재 고객들에게 매장에 대한 긍정적인 입소문(Word of Mouth) 효과를 강력하게 증폭시키는 역할을 합니다.")
            
            # 3. 방문자 답글 & 다매체 평가
            st.markdown("### 💬 3. 고객 소통 지수 및 로컬 지도 평판 효과")
            st.markdown(f"> **네이버 리뷰 사장님 답글 {place_replies}건 완료 / 구글·카카오맵 신규 우수 리뷰 {kakao_google_reviews}건 확보**")
            st.markdown("- **홍보 효과 평가:** 꼼꼼한 리뷰 답글 관리는 신규 고객에게 '관리받는 매장'이라는 긍정적 시그널을 주어 방문 이탈률을 방어합니다. 또한 구글과 카카오맵의 평판이 누적되면서, 길 찾기 앱을 켜고 바로 이동하는 '즉시 방문 고객'과 '외국인 관광객'의 발길을 우리 매장으로 확실하게 돌리는 집객 효과를 내고 있습니다.")
            
            # 4. 인스타 트래픽 평가
            if insta_views > 0:
                st.markdown("### 📱 4. SNS 숏폼 영상 바이럴 및 브랜드 확산 효과")
                st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
                st.markdown(f"- **홍보 효과 평가:** 조회수 {insta_views:,}회는 수만 명의 머릿속에 매장의 매력을 시각적으로 각인시켰음을 의미합니다. 이 중 호기심을 느낀 유저들이 네이버에 매장 이름을 직접 검색하여 찾아오는 '선순환 트래픽'이 발생하고 있으며, 이는 장기적으로 지역 내 독보적인 핫플레이스로 자리매김하는 막대한 브랜드 가치를 창출합니다.")
