import streamlit as st
from datetime import datetime

# -----------------------------------------------------------------
# 1. 메인 UI 및 입력 폼 (API 없이 100% 정확한 수기 입력)
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 성과 보고서 생성기")
st.markdown("입력된 정확한 데이터를 바탕으로 실질적인 '홍보 효과'를 분석하는 전문가용 리포트를 추출합니다.")

with st.form("report_form"):
    st.subheader("📌 1. 매장 및 타겟 키워드")
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 동경생고기")
    with col2:
        promo_keyword = st.text_input("메인 홍보 키워드", placeholder="예: 대구 달서구 맛집")

    st.divider()

    st.subheader("📊 2. 이번 달 마케팅 성과 입력")
    st.caption("클라이언트에게 보고할 정확한 수치들을 입력해 주세요.")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown("**[플레이스 순위 지표]**")
        prev_rank = st.number_input("지난달 노출 순위", min_value=1, value=15)
        current_rank = st.number_input("이번 달 노출 순위", min_value=1, value=3)
    with col4:
        st.markdown("**[리뷰 및 소통 지표]**")
        blog_count = st.number_input("이번 달 발행된 블로그 리뷰 수", min_value=0, value=10)
        place_replies = st.number_input("이번 달 방문자 리뷰 답글 수", min_value=0, value=45)
    with col5:
        st.markdown("**[다매체 및 SNS 지표]**")
        kakao_google_reviews = st.number_input("카카오맵/구글 신규 리뷰 수", min_value=0, value=5)
        insta_views = st.number_input("인스타 영상 총 조회수", min_value=0, value=15000)

    st.divider()

    st.subheader("🔗 3. 이번 달 핵심 블로그 리뷰 링크 (선택사항)")
    st.caption("보고서에 첨부할 우수 리뷰노트 링크를 입력해 주세요. (빈칸은 출력되지 않습니다)")
    
    links = []
    link_cols = st.columns(2)
    for i in range(10):
        with link_cols[i % 2]:
            link = st.text_input(f"블로그 링크 {i+1}", key=f"link_{i}")
            links.append(link)

    submit_button = st.form_submit_button("마케팅 홍보 효과 보고서 추출")

# -----------------------------------------------------------------
# 2. 데이터 분석 및 결과 출력 (홍보 효과 중심의 워딩)
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not promo_keyword:
        st.warning("매장명과 홍보 키워드를 입력해 주세요.")
    else:
        with st.spinner('입력된 수치를 바탕으로 홍보 효과를 분석 중입니다...'):
            
            # 1. 순위 증감 텍스트
            diff = prev_rank - current_rank
            if diff > 0:
                rank_text = f"**{current_rank}위** (전월 {prev_rank}위 대비 🔺{diff}계단 상승)"
            elif diff < 0:
                rank_text = f"**{current_rank}위** (전월 {prev_rank}위 대비 🔻{abs(diff)}계단 하락)"
            else:
                rank_text = f"**{current_rank}위** (전월 순위 안정적 유지)"

            # 2. 블로그 노출 기대효과 계산 (가상 수치)
            # 블로그 1개당 최소 150~300명의 지역 타겟 고객에게 노출된다고 가정
            expected_exposure = blog_count * 200 

            current_month = datetime.now().month

            st.success("✅ 홍보 효과 평가 보고서 생성이 완료되었습니다!")
            
            # -------------------------------------------------------------
            # [보고서 출력부]
            # -------------------------------------------------------------
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 홍보 효과 보고서")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 순위 평가 (트래픽 및 유입 효과)
            st.markdown(f"### 🥇 1. '{promo_keyword}' 검색 노출 및 유입 효과")
            st.markdown(f"> **현재 검색 노출 순위: {rank_text}**")
            st.markdown(f"- **홍보 효과 평가:** 메인 타겟 키워드인 '{promo_keyword}'에서 상위 노출을 점유함에 따라, 해당 지역에서 식사를 고민하는 잠재 고객들의 클릭(유입) 트래픽이 집중되고 있습니다. 상위권 유지는 전단지 수만 장을 뿌리는 것 이상의 강력한 인지도 상승효과를 가져오며, 광고비 지출 없이도 자연스러운 예약 및 방문 전환으로 이어지는 가장 확실한 매출 견인차 역할을 하고 있습니다.")
            
            # 2. 블로그 리뷰 평가 (디지털 전단지 및 설득 효과)
            st.markdown(f"### 📝 2. 블로그 리뷰(리뷰노트) 배포 및 설득 효과")
            st.markdown(f"> **이번 달 고품질 블로그 리뷰 총 {blog_count}건 발행 완료**")
            st.markdown(f"- **홍보 효과 평가:** 이번 달 발행된 {blog_count}건의 블로그는 네이버 검색 결과 곳곳에 배치되어, 우리 매장을 검색한 고객에게 매장의 분위기와 맛을 시각적으로 어필하는 '온라인 팸플릿' 역할을 완벽히 수행하고 있습니다. 보수적으로 잡아도 약 **{expected_exposure:,}명 이상의 지역 잠재 고객에게 브랜드가 노출된 것과 같은 홍보 가치**를 지니며, 방문을 망설이는 고객의 최종 선택을 이끌어내는 결정적인 후기로 작용하고 있습니다.")
            
            # 입력된 블로그 링크 리스트업
            valid_links = [l for l in links if l.strip()]
            if valid_links:
                st.markdown("**[이번 달 주요 홍보 블로그 링크]**")
                for idx, valid_link in enumerate(valid_links):
                    st.markdown(f"{idx+1}. {valid_link}")
            
            # 3. 방문자 답글 & 다매체 평가 (신뢰도 및 전환율 효과)
            st.markdown("### 💬 3. 고객 소통(답글) 및 로컬 지도 평판 효과")
            st.markdown(f"> **네이버 리뷰 사장님 답글 {place_replies}건 완료 / 구글·카카오맵 신규 우수 리뷰 {kakao_google_reviews}건 확보**")
            st.markdown("- **홍보 효과 평가:** 꼼꼼한 리뷰 답글 관리는 신규 고객에게 '청결하고 친절하게 관리되는 매장'이라는 강한 신뢰감을 심어주어 방문 이탈률을 크게 낮춥니다. 또한 구글과 카카오맵의 평판이 긍정적으로 누적되면서, 네이버를 쓰지 않는 2030 직장인 그룹과 길 찾기 앱을 켜고 바로 이동하는 '즉시 방문 고객(외국인 포함)'들의 발길을 우리 매장으로 돌리는 탁월한 집객 효과를 내고 있습니다.")
            
            # 4. 인스타 트래픽 평가 (바이럴 및 인지도 확산 효과)
            if insta_views > 0:
                st.markdown("### 📱 4. SNS 숏폼 영상 바이럴 및 브랜드 확산 효과")
                st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
                st.markdown(f"- **홍보 효과 평가:** 영상 조회수 {insta_views:,}회는 단순히 영상을 본 것을 넘어, 수만 명의 머릿속에 매장의 매력을 각인시켰음을 의미합니다. 이 중 호기심을 느낀 유저들이 네이버에 매장 이름을 직접 검색하여 찾아오는 '선순환 트래픽'이 발생하고 있으며, 이는 장기적으로 지역 내 독보적인 '핫플레이스'로 자리매김하는 막대한 브랜드 홍보 가치를 지닙니다.")
            
            st.markdown("---")
            st.markdown("💡 **WithMember 종합 분석:** 검색 상위 노출로 시선을 끌고, 블로그로 설득하며, SNS로 확산시키고, 꼼꼼한 리뷰 관리로 방문을 확정 짓는 '빈틈없는 마케팅 파이프라인'이 성공적으로 작동하고 있습니다. 다음 달에도 매장의 매출 증대를 위해 트래픽과 평판 관리에 만전을 기하겠습니다.")
