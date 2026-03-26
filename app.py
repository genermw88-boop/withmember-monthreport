import streamlit as st
import time
import datetime

# -----------------------------------------------------------------
# 1. 데이터 추출 가짜(Mock) 함수 
# (실제 서비스 시에는 스크래핑 및 네이버/OpenAI API로 대체)
# -----------------------------------------------------------------
def get_naver_place_rank(keyword, store_name):
    time.sleep(1)
    return {"current_rank": 3, "prev_rank": 8, "diff": 5}

def get_naver_reviews(place_id):
    time.sleep(1)
    return {"total_new": 120, "replied": 115, "photo_reviews": 85}

def get_naver_blog_reviews(keyword):
    time.sleep(1)
    return {"total_blogs": 15, "smart_block_exposure": 12}

# -----------------------------------------------------------------
# 2. UI 및 메인 앱 로직
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 프리미엄 보고서 생성기", page_icon="📈", layout="wide")

st.title("📈 WithMember 월간 마케팅 분석 보고서 생성기")
st.markdown("단순 수치 나열을 넘어, 네이버 로직 기반의 심층 분석 리포트를 자동으로 생성합니다.")

with st.form("report_form"):
    st.subheader("📌 매장 및 타겟 정보")
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("매장명", placeholder="예: 맛집상회 강남점")
    with col2:
        keyword = st.text_input("메인 타겟 키워드", placeholder="예: 강남역 맛집")
    with col3:
        place_id = st.text_input("네이버 플레이스 ID", placeholder="예: 12345678")

    st.divider()

    st.subheader("📊 외부 트래픽 및 바이럴 데이터 (직접 입력)")
    st.caption("외부 매체의 트래픽은 네이버 플레이스 지수(Place Index) 상승의 핵심 요인입니다.")
    col4, col5 = st.columns(2)
    with col4:
        blog_keyword = st.text_input("블로그 리뷰노트 키워드", placeholder="예: 매장명 + 리뷰노트")
        google_review_cnt = st.number_input("이번 달 구글/카카오 리뷰 증가 수", min_value=0, value=15)
    with col5:
        insta_views = st.number_input("이번 달 인스타 영상 총 조회수", min_value=0, value=45000)
        insta_saves = st.number_input("인스타 저장/공유 수 (추정치)", min_value=0, value=350)

    submit_button = st.form_submit_button("전문가용 월간 보고서 생성하기")

# -----------------------------------------------------------------
# 3. 보고서 생성 결과 화면 (네이버 로직 기반 분석 텍스트 적용)
# -----------------------------------------------------------------
if submit_button:
    if not keyword or not store_name:
        st.warning("매장명과 타겟 키워드를 입력해주세요.")
    else:
        with st.spinner('네이버 알고리즘 지표를 분석하여 보고서를 작성 중입니다...'):
            # 데이터 추출
            rank_data = get_naver_place_rank(keyword, store_name)
            review_data = get_naver_reviews(place_id)
            blog_data = get_naver_blog_reviews(blog_keyword)
            current_month = datetime.datetime.now().month
            
            # 비율 계산
            reply_rate = round((review_data['replied'] / review_data['total_new']) * 100, 1) if review_data['total_new'] > 0 else 0
            photo_rate = round((review_data['photo_reviews'] / review_data['total_new']) * 100, 1) if review_data['total_new'] > 0 else 0

            st.success("✅ 보고서 생성이 완료되었습니다. 아래 내용을 복사하여 대표님께 전달하세요.")
            
            # --- 보고서 출력부 ---
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 성과 분석 리포트")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 플레이스 순위 로직 분석
            st.markdown("### 🥇 1. 네이버 스마트플레이스 검색 노출 최적화(SEO) 지표")
            st.markdown(f"> **현재 '{keyword}' 검색 시 {rank_data['current_rank']}위 노출 중 (전월 대비 🔺{rank_data['diff']}계단 상승)**")
            st.markdown(f"""
            - **로직 분석:** 네이버 플레이스 순위는 단순 클릭수가 아닌 **'유효 트래픽'과 '체류 시간'**을 복합적으로 평가합니다. 이번 달 순위 상승은 매장 방문객들의 지속적인 트래픽 유입과 리뷰 탐색으로 인한 체류 시간 증가가 알고리즘에 긍정적인 신호(Positive Signal)로 작용한 결과입니다.
            - **기대 효과:** 최상단 노출을 통해 지역 내 잠재 고객의 자연 유입(Organic Traffic)이 극대화되고 있으며, 이는 광고비 지출 없이도 예약 및 방문 전환율을 높이는 핵심 동력입니다.
            """)
            
            # 2. 리뷰 및 소통 지수 분석
            st.markdown("### 💬 2. 플레이스 활성도 및 고객 소통 지수(Engagement)")
            st.markdown(f"> **신규 방문자 리뷰 {review_data['total_new']}건 중 {review_data['replied']}건 답글 완료 (소통율 {reply_rate}%)**")
            st.markdown(f"""
            - **로직 분석:** 네이버 알고리즘은 **'관리자가 적극적으로 관리하는 매장'**에 높은 점수를 부여합니다. {reply_rate}%에 달하는 압도적인 답글률은 플레이스 지수(Place Index) 상승의 강력한 가점 요인입니다. 또한 전체 리뷰 중 사진 리뷰 비율이 {photo_rate}%에 달해, 신규 고객이 메뉴를 탐색하며 머무는 '체류 시간'을 획기적으로 늘리고 있습니다.
            - **기대 효과:** 고객의 신뢰도(Trust Score) 상승은 물론, 알고리즘 상 '우수 관리 매장'으로 분류되어 노출 안정성이 한층 강화되었습니다.
            """)
            
            # 3. 블로그 콘텐츠 및 C-Rank 분석
            st.markdown("### 📝 3. 블로그 리뷰노트 및 스마트블록 점유율")
            st.markdown(f"> **핵심 타겟 키워드 기반 고품질 리뷰 총 {blog_data['total_blogs']}건 발행 완료**")
            st.markdown(f"""
            - **로직 분석:** 단순 수량 늘리기가 아닌, 네이버의 **C-Rank(크리에이터 신뢰도) 및 DIA+(문서 품질) 로직**에 부합하는 양질의 블로거들을 섭외하여 진행했습니다. 현재 발행된 글 중 다수가 모바일 검색 시 최상단 '스마트블록' 영역에 안정적으로 노출되고 있습니다.
            - **기대 효과:** 정보 탐색 목적의 고객들에게 생생한 UGC(사용자 생성 콘텐츠)를 제공함으로써, 블로그에서 플레이스로 넘어오는 '검색 전환율(CVR)'이 크게 향상되었습니다.
            """)
            
            # 4. 다매체 (구글/카카오) 로직 분석
            st.markdown("### 🗺️ 4. 로컬 SEO 및 외부 지도 플랫폼 확장성")
            st.markdown(f"> **구글 맵스 및 카카오맵 신규 우수 리뷰 총 {google_review_cnt}건 확보**")
            st.markdown(f"""
            - **로직 분석:** 네이버는 타 플랫폼에서의 브랜드 인지도를 간접적으로 평가에 반영합니다(외부 백링크 효과). 구글과 카카오맵에서의 리뷰 축적은 길 찾기 기능을 사용하는 **'고관여/방문 직전 고객'**과 **'외국인 관광객'** 트래픽을 네이버 플레이스로 연결하는 탄탄한 브릿지 역할을 합니다.
            - **기대 효과:** 플랫폼 다각화를 통해 특정 검색 포털에 의존하는 리스크를 줄이고, 다방면에서 '찐 맛집'이라는 브랜드 평판(Brand Reputation)을 확립하고 있습니다.
            """)
            
            # 5. SNS 바이럴 트래픽 분석
            st.markdown("### 📱 5. SNS(인스타그램) 바이럴 및 선순환(Flywheel) 트래픽")
            st.markdown(f"> **이번 달 인스타그램 영상 총 조회수 {insta_views:,}회 / 저장 및 공유 {insta_saves:,}건**")
            st.markdown(f"""
            - **로직 분석:** SNS 조회수 {insta_views:,}회는 네이버 지도에서 **'매장명 직접 검색(브랜드 검색)'**을 유발하는 가장 강력한 트리거입니다. 네이버 알고리즘은 외부 링크를 통하지 않고 사용자가 직접 매장 이름을 검색해서 들어오는 트래픽에 가장 높은 SEO 점수를 부여합니다.
            - **기대 효과:** 인스타그램 영상으로 시각적 후킹 -> 네이버 브랜드 검색 -> 플레이스 방문 및 저장이라는 **'마케팅 선순환(Flywheel) 구조'**가 성공적으로 안착하여 전체적인 마케팅 ROI(투자 대비 수익률)가 극대화되고 있습니다.
            """)
            
            st.markdown("---")
            st.markdown("💡 **WithMember 인사이트:** 이번 달은 특히 인스타그램 바이럴 트래픽이 네이버 플레이스의 브랜드 검색량 증가로 직결되며 순위 상승을 견인했습니다. 다음 달에는 상승된 순위를 유지하기 위해 **'저장하기' 유도 프로모션**을 매장 내에 추가로 배치하는 것을 제안 드립니다.")
