import streamlit as st
from datetime import datetime

# -----------------------------------------------------------------
# 1. 메인 UI 및 입력 폼 (API 완전 제거 / 100% 수기 입력 최적화)
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 홍보 효과 보고서")
st.markdown("정확한 성과 데이터를 바탕으로 에러 없이 1초 만에 완벽한 평가 보고서를 생성합니다.")

with st.form("report_form"):
    st.subheader("📌 1. 타겟 매장 및 순위 성과")
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 동경생고기")
        promo_keyword = st.text_input("메인 홍보 키워드", placeholder="예: 대구 달서구 맛집")
    with col2:
        current_rank = st.number_input("현재 플레이스 순위", min_value=1, value=3)
        rank_increase = st.number_input("이번 달 순위 상승폭 (유지 시 0)", min_value=0, value=5)

    st.divider()

    st.subheader("🔗 2. 이번 달 핵심 블로그 리뷰 링크 (최대 10개)")
    st.caption("보고서에 노출할 홍보 블로그 링크를 입력해 주세요. (빈칸은 자동으로 제외됩니다)")
    
    links = []
    link_cols = st.columns(2)
    for i in range(10):
        with link_cols[i % 2]:
            link = st.text_input(f"블로그 링크 {i+1}")
            links.append(link)
    
    st.divider()

    st.subheader("💬 3. 고객 관리 및 바이럴 홍보 지표")
    col3, col4 = st.columns(2)
    with col3:
        place_replies = st.number_input("방문자 리뷰 사장님 답글 수", min_value=0, value=45)
        kakao_google_reviews = st.number_input("카카오맵/구글 신규 리뷰 확보 수", min_value=0, value=5)
    with col4:
        insta_views = st.number_input("인스타 홍보 영상 총 조회수", min_value=0, value=15000)

    submit_button = st.form_submit_button("마케팅 홍보 효과 평가 생성")

# -----------------------------------------------------------------
# 2. 데이터 분석 및 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not promo_keyword:
        st.warning("매장명과 홍보 키워드를 모두 입력해 주세요.")
    else:
        # API 로딩이 없으므로 즉시 결과 출력
        current_month = datetime.now().month
        
        # 순위 증감 텍스트 생성
        if rank_increase > 0:
            rank_text = f"**{current_rank}위** (전월 대비 🔺{rank_increase}계단 상승)"
        else:
            rank_text = f"**{current_rank}위** (전월 순위 안정적 유지)"

        st.success("✅ 평가 보고서 생성이 완료되었습니다!")
        
        st.markdown("---")
        st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 홍보 효과 보고서")
        st.markdown(f"**수신:** {store_name} 대표님")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. 순위 평가
        st.markdown(f"### 🥇 1. '{promo_keyword}' 검색 노출 및 유입 효과")
        st.markdown(f"> **현재 검색 노출 순위: {rank_text}**")
        st.markdown(f"- **홍보 효과 평가:** 지역 핵심 타겟 키워드인 '{promo_keyword}'에서 성공적으로 상위 노출을 점유함에 따라, 해당 지역에서 식사를 고민하는 잠재 고객들의 실질적인 클릭 및 유입 트래픽이 집중되고 있습니다. 이러한 노출도 상승은 단순 인지도 확대를 넘어 즉각적인 매장 방문 및 예약 전환으로 이어지는 가장 확실한 매출 견인차 역할을 하고 있습니다.")
        
        # 2. 블로그 리뷰 평가 (10개 링크 리스트업)
        st.markdown(f"### 📝 2. 우수 블로그 리뷰(리뷰노트) 배포 및 설득 효과")
        
        valid_links = [l for l in links if l.strip()]
        if valid_links:
            st.markdown("**[이번 달 주요 홍보 블로그 링크]**")
            for idx, valid_link in enumerate(valid_links):
                st.markdown(f"{idx+1}. {valid_link}")
        else:
            st.markdown("> 이번 달 신규 등록된 핵심 링크 없음")
                
        st.markdown("- **홍보 효과 평가:** 단순 정보 나열이 아닌 네이버 알고리즘에 부합하는 양질의 리뷰노트들이 성공적으로 발행되었습니다. 이 문서들은 매장의 시각적 매력과 생생한 후기를 전달하는 '온라인 팸플릿' 역할을 완벽히 수행하며, 검색 후 방문을 망설이는 고객의 최종 선택을 이끌어내는 결정적인 설득 창구가 되고 있습니다.")
        
        # 3. 방문자 답글 & 다매체 평가
        st.markdown("### 💬 3. 고객 소통 관리 및 로컬 지도 평판 효과")
        st.markdown(f"> **방문자 리뷰 사장님 답글 {place_replies}건 완료 / 구글·카카오맵 신규 리뷰 {kakao_google_reviews}건 확보**")
        st.markdown("- **홍보 효과 평가:** 꼼꼼한 리뷰 답글 관리는 신규 고객에게 '청결하고 친절하게 관리되는 매장'이라는 긍정적 시그널을 주어 온라인상의 방문 이탈률을 획기적으로 방어합니다. 또한 구글과 카카오맵의 평판이 지속적으로 누적되면서, 길 찾기 앱을 켜고 바로 이동하는 '즉시 방문 고객'과 '외국인 관광객'의 발길을 우리 매장으로 확실하게 돌리는 집객 효과를 내고 있습니다.")
        
        # 4. 인스타 트래픽 평가
        if insta_views > 0:
            st.markdown("### 📱 4. SNS 숏폼 영상 바이럴 및 브랜드 확산 효과")
            st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
            st.markdown(f"- **홍보 효과 평가:** 영상 조회수 {insta_views:,}회는 수만 명의 잠재 고객에게 매장의 존재를 시각적으로 강렬하게 각인시켰음을 의미합니다. 호기심을 느낀 유저들이 네이버에 매장 이름을 직접 검색하여 찾아오는 '선순환 브랜드 검색 트래픽'이 활발히 발생하고 있으며, 이는 장기적으로 지역 내 독보적인 핫플레이스로 자리매김하는 막대한 브랜드 홍보 가치를 창출합니다.")
