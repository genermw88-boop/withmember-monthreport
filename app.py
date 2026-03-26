# -----------------------------------------------------------------
# 3. 메인 UI 및 보고서 생성 로직 (Secrets 자동 연동 적용)
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📊", layout="wide")

st.title("📊 WithMember 월간 마케팅 분석 보고서 생성기")
st.markdown("네이버 검색 API와 브라우저 자동화(Selenium)를 통해 실제 데이터를 추출합니다.")

# 서버의 Secrets에서 API 키를 자동으로 불러옵니다.
try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 네이버 API 키가 설정되지 않았습니다. Settings > Secrets를 확인해 주세요.")
    st.stop() # 키가 없으면 아래 코드를 실행하지 않고 멈춤

with st.form("report_form"):
    st.subheader("📌 매장 및 타겟 정보")
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("매장명")
    with col2:
        keyword = st.text_input("메인 검색 키워드 (순위용)")
    with col3:
        place_id = st.text_input("네이버 플레이스 ID (숫자)")
        
    blog_keyword = st.text_input("블로그 API 검색 키워드", placeholder="예: 매장명 + 리뷰노트")

    st.divider()

    st.subheader("📊 외부 트래픽 데이터 (직접 입력)")
    col4, col5 = st.columns(2)
    with col4:
        google_review_cnt = st.number_input("이번 달 구글/카카오 리뷰 증가 수", min_value=0, value=0)
    with col5:
        insta_views = st.number_input("이번 달 인스타 영상 총 조회수", min_value=0, value=0)

    submit_button = st.form_submit_button("실제 데이터 추출 및 보고서 생성")

# -----------------------------------------------------------------
# 4. 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not place_id:
        st.warning("플레이스 ID를 입력해야 크롤링이 가능합니다.")
    else:
        with st.spinner('실시간으로 네이버 데이터를 스크래핑하고 API를 호출하고 있습니다. (약 10초 소요)...'):
            
            # 자동으로 불러온 API 키를 바로 함수에 집어넣습니다.
            real_blog_count = get_real_blog_reviews(blog_keyword, naver_client_id, naver_client_secret)
            review_data = scrape_place_reviews(place_id)
            
            # (이하 기존 출력부 코드와 동일)
            # 방어 코드 (분모가 0이 되는 것 방지)
            if review_data['total_new'] > 0:
                reply_rate = round((review_data['replied'] / review_data['total_new']) * 100, 1)
            else:
                reply_rate = 0
                
            # ... 하단 리포트 출력 마크다운 코드 유지 ...
