import streamlit as st
import random
from datetime import datetime

# -----------------------------------------------------------------
# 1. 다이내믹 텍스트 생성 함수 (키워드별 개별 평가용)
# -----------------------------------------------------------------
def get_keyword_evaluation(keyword, rank):
    if rank <= 5:
        texts = [
            f"'{keyword}' 검색 시 **최상위권({rank}위)** 노출을 확고히 점유하고 있습니다. 이 '골든 존'은 잠재 고객의 유입이 가장 집중되는 곳으로, 막대한 트래픽이 실질적인 예약과 방문으로 직결되는 완벽한 매출 견인차 역할을 하고 있습니다.",
            f"현재 '{keyword}' 검색 결과에서 **{rank}위**에 랭크되어 압도적인 브랜드 인지도를 확보했습니다. 광고비 지출 없이도 자연 검색을 통해 매일 엄청난 수의 지역 타겟 고객들에게 1순위 선택지로 노출 중입니다."
        ]
    elif rank <= 15:
        texts = [
            f"'{keyword}' 키워드 검색 시 **상위권({rank}위)**에 안정적으로 노출되고 있습니다. 치열한 지역 상권 경쟁 속에서도 훌륭한 방어율을 보이며, 최상위권 진입을 위한 탄탄한 유효 트래픽을 모으고 있습니다.",
            f"현재 '{keyword}'에서 **{rank}위** 노출을 유지 중입니다. 지속적인 트래픽 관리와 체류 시간 최적화 작업이 알고리즘에 긍정적으로 작용하여, 매장을 찾는 고객들에게 높은 신뢰감을 주는 위치를 선점했습니다."
        ]
    else:
        texts = [
            f"'{keyword}' 키워드에서 **{rank}위**를 기록하며 의미 있는 순위 상승 궤도에 안착했습니다. 네이버 알고리즘에 맞춘 꾸준한 트래픽 파이프라인 구축이 성과를 내기 시작했으며, 지속적인 관리로 상위권 노출을 이끌어내겠습니다.",
            f"현재 최적화 작업을 통해 '{keyword}' 순위가 **{rank}위**로 가시권에 진입했습니다. 블로그와 SNS 바이럴 시너지를 더욱 집중시켜 네이버 플레이스 지수를 다음 단계로 끌어올리겠습니다."
        ]
    return random.choice(texts)

def get_dynamic_evaluations():
    evals = {}
    blog_texts = [
        "네이버 C-Rank 알고리즘에 부합하는 양질의 리뷰노트들이 성공적으로 발행되었습니다. 이 문서들은 매장의 시각적 매력을 돋보이게 하는 '온라인 팸플릿' 역할을 완벽히 수행하며, 방문을 망설이는 고객의 최종 선택을 이끌어내고 있습니다.",
        "이번 달 배포된 리뷰들은 모바일 스마트블록 영역에 최적화되어 노출되고 있습니다. 텍스트와 사진이 조화롭게 어우러진 생생한 후기들이 정보 탐색 후 매장으로 넘어오는 '징검다리 트래픽(전환율)'을 톡톡히 견인 중입니다."
    ]
    evals['blog'] = random.choice(blog_texts)

    comm_texts = [
        "꼼꼼한 리뷰 답글 관리는 신규 고객에게 '청결하고 친절한 매장'이라는 긍정적 시그널을 주어 온라인 방문 이탈률을 획기적으로 방어합니다. 아울러 구글·카카오맵 평판 누적으로 즉시 방문 고객의 발길을 돌리는 데 성공했습니다.",
        "정성스러운 리뷰 답글은 알고리즘 상 '소통이 활발한 우수 매장'으로 분류되어 SEO 가점을 받습니다. 더불어 외국인과 직장인들이 애용하는 구글·카카오맵 평점 상승은 타겟 고객층 다변화에 큰 기여를 하고 있습니다."
    ]
    evals['comm'] = random.choice(comm_texts)

    insta_texts = [
        "숏폼 영상의 폭발적인 조회수는 잠재 고객에게 매장의 존재를 시각적으로 강렬하게 각인시켰음을 의미합니다. 호기심을 느낀 유저들이 네이버에 매장 이름을 직접 검색해 찾아오는 '선순환 브랜드 검색'이 활발히 발생하고 있습니다.",
        "인스타그램을 통한 시각적 바이럴이 성공적으로 확산되었습니다. 이는 매장을 '반드시 가봐야 할 핫플레이스'로 포지셔닝하며, 직접 검색을 유발해 네이버 순위 상승에도 결정적인 가점을 주고 있습니다."
    ]
    evals['insta'] = random.choice(insta_texts)
    
    return evals

# -----------------------------------------------------------------
# 2. 메인 UI 및 입력 폼
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 홍보 효과 보고서")
st.markdown("정확한 성과 데이터를 기반으로 클라이언트의 신뢰를 높이는 평가 보고서를 생성합니다.")

with st.form("report_form"):
    st.subheader("📌 1. 타겟 매장 및 핵심 홍보 키워드 (최대 5개)")
    store_name = st.text_input("매장명 (정확히 입력)", placeholder="예: 동경생고기")
    
    st.caption("이번 달 집중 관리한 키워드와 현재 플레이스 순위를 입력해 주세요. (입력한 곳까지만 출력됩니다)")
    
    keywords = []
    ranks = []
    
    # 5개의 키워드와 순위를 2개의 열로 나란히 입력받음
    for i in range(5):
        col_k, col_r = st.columns([3, 1])
        with col_k:
            k = st.text_input(f"홍보 키워드 {i+1}", key=f"kw_{i}")
        with col_r:
            r = st.number_input(f"순위", min_value=1, value=1, key=f"rank_{i}")
        if k.strip():
            keywords.append(k)
            ranks.append(r)

    st.divider()

    st.subheader("🔗 2. 이번 달 우수 블로그 리뷰 링크 (최대 10개)")
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
        place_replies = st.number_input("네이버 방문자 리뷰 사장님 답글 수", min_value=0, value=45)
        kakao_google_reviews = st.number_input("카카오맵/구글 신규 리뷰 확보 수", min_value=0, value=5)
    with col4:
        insta_views = st.number_input("인스타 홍보 영상 총 조회수", min_value=0, value=15000)

    submit_button = st.form_submit_button("마케팅 홍보 효과 평가 생성")

# -----------------------------------------------------------------
# 3. 데이터 분석 및 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not keywords:
        st.warning("매장명과 최소 1개 이상의 홍보 키워드를 입력해 주세요.")
    else:
        with st.spinner('다이내믹 분석 멘트를 적용하여 보고서를 작성 중입니다...'):
            
            eval_texts = get_dynamic_evaluations()
            current_month = datetime.now().month

            st.success("✅ 에러 없이 깔끔한 맞춤형 평가 보고서가 생성되었습니다!")
            
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 홍보 효과 보고서")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 키워드별 순위 평가 (입력한 키워드 개수만큼 반복해서 출력)
            st.markdown(f"### 🥇 1. 핵심 타겟 키워드 검색 노출 및 유입 효과")
            for i in range(len(keywords)):
                st.markdown(f"> **[{keywords[i]}]**")
                st.markdown(f"- **홍보 효과 평가:** {get_keyword_evaluation(keywords[i], ranks[i])}")
                st.markdown("") # 줄바꿈
            
            # 2. 블로그 리뷰 평가
            st.markdown(f"### 📝 2. 우수 블로그 리뷰(리뷰노트) 배포 및 설득 효과")
            valid_links = [l for l in links if l.strip()]
            if valid_links:
                st.markdown("**[이번 달 주요 홍보 블로그 링크]**")
                for idx, valid_link in enumerate(valid_links):
                    st.markdown(f"{idx+1}. {valid_link}")
            else:
                st.markdown("> 이번 달 신규 등록된 핵심 링크 없음")
            st.markdown(f"- **홍보 효과 평가:** {eval_texts['blog']}")
            
            # 3. 방문자 답글 & 다매체 평가
            st.markdown("### 💬 3. 고객 소통 관리 및 로컬 지도 평판 효과")
            st.markdown(f"> **방문자 리뷰 사장님 답글 {place_replies}건 완료 / 구글·카카오맵 신규 리뷰 {kakao_google_reviews}건 확보**")
            st.markdown(f"- **홍보 효과 평가:** {eval_texts['comm']}")
            
            # 4. 인스타 트래픽 평가
            if insta_views > 0:
                st.markdown("### 📱 4. SNS 숏폼 영상 바이럴 및 브랜드 확산 효과")
                st.markdown(f"> **이번 달 인스타그램 영상 콘텐츠 총 조회수 {insta_views:,}회 돌파**")
                st.markdown(f"- **홍보 효과 평가:** {eval_texts['insta']}")
