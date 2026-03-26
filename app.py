import streamlit as st
import time

# -----------------------------------------------------------------
# 1. 데이터 추출 가짜(Mock) 함수 
# (실제 서비스 시에는 BeautifulSoup, Selenium, 네이버 API 코드로 대체합니다)
# -----------------------------------------------------------------
def get_naver_place_rank(keyword, store_name):
    # 실제 크롤링 로직이 들어갈 자리
    time.sleep(1) # 로딩 효과
    return {"current_rank": 3, "up_down": "🔺5계단 상승"}

def get_naver_reviews(place_id):
    # 실제 리뷰 스크래핑 로직이 들어갈 자리
    time.sleep(1)
    return {"total_new": 120, "replied": 115, "reply_rate": 95.8}

def get_naver_blog_reviews(keyword):
    # 실제 네이버 검색 API 로직이 들어갈 자리
    time.sleep(1)
    return {"total_blogs": 15}

# -----------------------------------------------------------------
# 2. UI 및 메인 앱 로직
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 보고서 생성기", page_icon="📊", layout="centered")

st.title("📊 WithMember 월간 마케팅 보고서 생성기")
st.markdown("매장 대표님들께 보낼 월간 성과 보고서를 자동으로 추출하고 생성합니다.")

with st.form("report_form"):
    st.subheader("1. 네이버 로직 자동 추출 (검색/플레이스/블로그)")
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("메인 타겟 키워드 (예: 강남역 맛집)")
        store_name = st.text_input("매장명")
    with col2:
        place_id = st.text_input("네이버 플레이스 ID (숫자)")
        blog_keyword = st.text_input("블로그 검색 키워드 (예: 매장명 + 리뷰노트)")

    st.divider()

    st.subheader("2. 다매체 및 SNS 성과 (직접 입력)")
    col3, col4 = st.columns(2)
    with col3:
        google_review_cnt = st.number_input("이번 달 구글/카카오 리뷰 증가 수", min_value=0, value=0)
    with col4:
        insta_views = st.number_input("이번 달 인스타 영상 총 조회수", min_value=0, value=0)

    submit_button = st.form_submit_button("월간 보고서 생성하기")

# -----------------------------------------------------------------
# 3. 보고서 생성 결과 화면
# -----------------------------------------------------------------
if submit_button:
    if not keyword or not store_name:
        st.warning("타겟 키워드와 매장명을 입력해주세요!")
    else:
        with st.spinner('네이버 데이터를 추출하고 보고서를 생성 중입니다...'):
            # 데이터 추출 함수 호출
            rank_data = get_naver_place_rank(keyword, store_name)
            review_data = get_naver_reviews(place_id)
            blog_data = get_naver_blog_reviews(blog_keyword)
            
            st.success("보고서 생성이 완료되었습니다!")
            
            st.markdown("---")
            st.markdown(f"### 📋 [WithMember] 2026년 3월 마케팅 성과 보고서 - {store_name} 대표님")
            
            st.markdown("#### 📈 네이버 플레이스 핵심 지표 (자동 추출)")
            st.markdown(f"- **현재 검색 순위:** '{keyword}' 검색 시 **{rank_data['current_rank']}위** ({rank_data['up_down']})")
            st.markdown(f"- **고객 소통 지수:** 신규 방문자 리뷰 {review_data['total_new']}건 중 **{review_data['replied']}건 답글 완료** (작성률 {review_data['reply_rate']}%)")
            st.markdown(f"- **블로그 리뷰(리뷰노트):** '{blog_keyword}' 관련 **총 {blog_data['total_blogs']}건**의 고품질 리뷰 발행 완료")
            
            st.markdown("#### 🌐 다매체 확장 및 바이럴 성과 분석")
            
            # 구글/카카오 리뷰 텍스트 자동 생성 로직
            if google_review_cnt > 0:
                st.markdown(f"- **글로벌/직장인 타겟 리뷰 (구글/카카오맵):** 이번 달 **총 {google_review_cnt}건의 신규 리뷰**가 확보되었습니다. 이는 네이버 외 매체를 이용하는 고관여 고객층의 신뢰도(Trust Score)가 상승했음을 의미하며, 길 찾기 후 직접 방문하는 전환율 개선이 기대됩니다.")
            else:
                st.markdown("- **글로벌/직장인 타겟 리뷰 (구글/카카오맵):** 이번 달 신규 리뷰 변동 사항 없음.")
                
            # 인스타 조회수 텍스트 자동 생성 로직
            if insta_views > 0:
                st.markdown(f"- **SNS 바이럴 파급력 (인스타그램):** 이번 달 영상 콘텐츠가 **총 {insta_views:,}회의 조회수**를 기록했습니다. 잠재 고객들에게 시각적 매력이 강력하게 노출되었으며, 이 트래픽이 네이버 플레이스로 유입되어 전반적인 검색 순위 상승에 기여하고 있습니다.")
            else:
                st.markdown("- **SNS 바이럴 파급력 (인스타그램):** 이번 달 집계된 영상 트래픽 없음.")