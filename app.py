import streamlit as st
from datetime import datetime

# -----------------------------------------------------------------
# UI 및 보고서 생성 로직 (100% 수동 입력 기반으로 안정성 극대화)
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📊", layout="wide")

st.title("📊 WithMember 월간 마케팅 분석 보고서 생성기")
st.markdown("정확한 수기 데이터를 바탕으로 네이버 로직 기반의 전문적인 분석 멘트를 자동 생성합니다.")

with st.form("report_form"):
    st.subheader("📌 매장 및 타겟 정보")
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 동경생고기")
    with col2:
        main_keyword = st.text_input("메인 타겟 키워드", placeholder="예: 대구 달서구 맛집")

    st.divider()

    st.subheader("📊 이번 달 성과 데이터 입력 (정확한 수치 입력)")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown("**[네이버 플레이스 지표]**")
        place_total_reviews = st.number_input("이번 달 신규 방문자 리뷰 수", min_value=0, value=50)
        place_replies = st.number_input("이번 달 사장님 답글 수", min_value=0, value=48)
    with col4:
        st.markdown("**[네이버 블로그 지표]**")
        blog_total_reviews = st.number_input("플레이스 누적 블로그 리뷰 수", min_value=0, value=143) # 대표님이 원하시던 부분!
        blog_new_reviews = st.number_input("이번 달 신규 블로그(리뷰노트) 발행 수", min_value=0, value=10)
    with col5:
        st.markdown("**[외부 다매체 지표]**")
        google_review_cnt = st.number_input("구글/카카오맵 신규 리뷰 수", min_value=0, value=5)
        insta_views = st.number_input("인스타 영상 총 조회수", min_value=0, value=15000)

    submit_button = st.form_submit_button("전문가용 마케팅 보고서 추출")

# -----------------------------------------------------------------
# 결과 출력
# -----------------------------------------------------------------
if submit_button:
    with st.spinner('입력된 데이터를 바탕으로 전문 분석 리포트를 작성 중입니다...'):
        
        # 소통율 계산
        if place_total_reviews > 0:
            reply_rate = round((place_replies / place_total_reviews) * 100, 1)
        else:
            reply_rate = 0
            
        current_month = datetime.now().month

        st.success("✅ 보고서 생성이 완료되었습니다! 복사해서 대표님들께 전달하세요.")
        
        # 리포트 텍스트 출력
        st.markdown("---")
        st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 성과 분석 리포트")
        st.markdown(f"**수신:** {store_name} 대표님")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. 소통 지수
        st.markdown("### 💬 1. 플레이스 고객 소통 및 활성도 지수")
        st.markdown(f"> **이번 달 신규 방문자 리뷰 {place_total_reviews}건 중, 사장님 답글 {place_replies}건 완료 (소통율 {reply_rate}%)**")
        st.markdown("- **로직 분석:** 네이버 알고리즘은 관리자와 고객 간의 활발한 소통이 일어나는 매장에 플레이스 지수(Place Index) 가점을 크게 부여합니다. 현재 훌륭한 답글률을 유지하고 계시며, 이는 검색 순위 최적화(SEO)의 가장 탄탄한 기반이 됩니다.")
        
        # 2. 블로그 리뷰 (정확한 수치 반영)
        st.markdown("### 📝 2. 블로그 리뷰(리뷰노트) 누적 및 스마트블록 점유율")
        st.markdown(f"> **플레이스 연동 블로그 리뷰 총 {blog_total_reviews}건 누적 (이번 달 신규 발행 {blog_new_reviews}건)**")
        st.markdown(f"- **로직 분석:** '{main_keyword}' 관련하여 양질의 C-Rank 포스팅이 지속적으로 누적되고 있습니다. 특히 이번 달 발행된 {blog_new_reviews}건의 고품질 리뷰가 모바일 스마트블록 점유율을 높여, 정보 탐색 후 매장으로 넘어오는 '징검다리 트래픽(전환율)'을 톡톡히 견인하고 있습니다.")
        
        # 3. 외부 로컬 SEO
        st.markdown("### 🗺️ 3. 로컬 SEO 및 외부 지도 플랫폼 확장성")
        st.markdown(f"> **구글맵스 및 카카오맵 신규 우수 리뷰 총 {google_review_cnt}건 확보**")
        st.markdown("- **로직 분석:** 네이버는 타 플랫폼에서의 브랜드 인지도를 간접 평가에 반영합니다. 외부 지도 앱에서의 긍정적 평판은 길 찾기 후 바로 방문하는 '고관여 고객'과 '외국인 관광객'의 방문 전환을 직접적으로 끌어올리는 중요한 지표입니다.")
        
        # 4. SNS 트래픽
        st.markdown("### 📱 4. SNS 바이럴 트래픽 및 마케팅 선순환(Flywheel)")
        st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
        st.markdown("- **로직 분석:** 폭발적인 인스타그램 조회수는 잠재 고객들이 네이버에서 매장 이름을 직접 검색하게 만드는 '브랜드 검색'을 유발합니다. 외부 링크가 아닌 직접 검색을 통한 트래픽 유입은 네이버 로직 상 가장 강력한 순위 상승 동력으로 작용하고 있습니다.")
