import streamlit as st
import requests
import re
import random
from datetime import datetime

# -----------------------------------------------------------------
# 1. API 통신 및 다이내믹 텍스트 생성 함수
# -----------------------------------------------------------------
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).replace('&amp;', '&')

def get_current_place_rank(keyword, store_name, client_id, client_secret):
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    local_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=100"
    current_rank = 0 
    try:
        res = requests.get(local_url, headers=headers, timeout=5)
        if res.status_code == 200:
            items = res.json().get('items', [])
            target_name = store_name.replace(" ", "").lower()
            for index, item in enumerate(items):
                title = clean_html(item.get('title', '')).replace(" ", "").lower()
                if target_name in title:
                    current_rank = index + 1
                    break
    except Exception:
        pass # 에러 발생 시 0 반환 (100위 밖 처리)
    return current_rank

# [핵심] 매월 바뀌는 다이내믹 평가 멘트 풀(Pool)
def get_dynamic_evaluations(promo_keyword, diff):
    evals = {}
    
    # 1. 순위 평가 (상승/하락/유지에 따라 멘트 완벽 분리)
    if diff > 0:
        rank_texts = [
            f"지역 핵심 타겟 키워드인 '{promo_keyword}'에서 성공적으로 상위 노출을 점유함에 따라, 잠재 고객들의 실질적인 유입 트래픽이 집중되고 있습니다. 이러한 노출도 상승은 즉각적인 매장 방문 및 예약 전환으로 이어지는 가장 확실한 매출 견인차 역할을 하고 있습니다.",
            f"이번 달 '{promo_keyword}' 검색 결과에서 가파른 순위 상승을 이뤄냈습니다. 이는 그동안 누적된 트래픽과 체류 시간 데이터가 네이버 알고리즘에 긍정적으로 작용했음을 의미하며, 광고비 절감과 동시에 자연스러운 신규 고객 창출을 이끌어내고 있습니다.",
            f"'{promo_keyword}' 키워드에서의 노출 순위가 눈에 띄게 도약했습니다. 검색 최상단 점유는 우리 매장의 브랜드 인지도를 지역 내 1티어로 끌어올리는 핵심 지표이며, 이번 달 방문객 증가에 가장 큰 기여를 한 것으로 분석됩니다."
        ]
    elif diff < 0:
        rank_texts = [
            f"현재 '{promo_keyword}' 키워드의 지역 내 경쟁이 매우 치열해지며 일시적인 순위 변동이 있었습니다. 하지만 당사의 최적화 로직을 통해 유효 트래픽을 지속적으로 공급하여, 빠른 시일 내에 상위 노출을 탈환하고 안정화할 수 있도록 관리 중입니다.",
            f"네이버 알고리즘 로직 업데이트 및 경쟁 매장들의 방어로 인해 '{promo_keyword}' 순위가 소폭 하락했습니다. 다음 달에는 블로그와 영수증 리뷰 배포를 더욱 타겟팅하여 알고리즘 가점을 회복하는 데 총력을 다하겠습니다.",
            f"'{promo_keyword}' 검색 결과에서 아쉬운 순위 하락이 있었으나, 내부적인 체류 시간 지표는 긍정적입니다. 일시적인 현상으로 분석되며, 외부 유입(SNS, 블로그)을 강화하여 플레이스 지수(Place Index)를 다시 강하게 끌어올리겠습니다."
        ]
    else:
        rank_texts = [
            f"치열한 지역 상권 경쟁 속에서도 '{promo_keyword}' 키워드 상위 노출을 굳건히 방어해 냈습니다. 이처럼 안정적인 순위 유지는 매일 꾸준한 잠재 고객의 검색 유입을 보장하며, 매장의 기초 체력을 튼튼하게 유지하는 비결입니다.",
            f"'{promo_keyword}' 검색 결과에서 변동 없이 탄탄하게 순위를 유지 중입니다. 이미 상위권에 안착한 만큼, 이제는 유입된 고객이 실제 방문으로 이어지도록 리뷰 콘텐츠의 질을 높이는 데 더욱 집중하겠습니다.",
            f"네이버 검색 로직이 요동치는 가운데서도 '{promo_keyword}' 노출 순위를 성공적으로 방어했습니다. 안정적인 트래픽 파이프라인이 구축되었음을 의미하며, 지속적인 우상향 매출을 기대할 수 있는 훌륭한 지표입니다."
        ]
    evals['rank'] = random.choice(rank_texts)

    # 2. 블로그 평가
    blog_texts = [
        "단순 정보 나열이 아닌 네이버 C-Rank 알고리즘에 부합하는 양질의 리뷰노트들이 성공적으로 발행되었습니다. 이 문서들은 매장의 시각적 매력을 돋보이게 하는 '온라인 팸플릿' 역할을 완벽히 수행하며, 방문을 망설이는 고객의 최종 선택을 이끌어내고 있습니다.",
        f"이번 달 배포된 블로그 리뷰들은 '{promo_keyword}' 관련 모바일 스마트블록 영역에 최적화되어 노출되고 있습니다. 텍스트와 사진이 조화롭게 어우러진 생생한 후기들이 정보 탐색 후 매장으로 넘어오는 '징검다리 트래픽(전환율)'을 톡톡히 견인 중입니다.",
        "진정성 있는 스토리텔링이 담긴 고품질 블로그 후기들이 누적되었습니다. 이는 단순히 검색 노출을 넘어, 우리 매장을 방문하고자 하는 고객들에게 강한 신뢰감을 심어주어 오프라인 방문 확정률을 크게 끌어올리는 효과를 냅니다."
    ]
    evals['blog'] = random.choice(blog_texts)

    # 3. 소통 및 다매체 평가
    comm_texts = [
        "꼼꼼한 리뷰 답글 관리는 신규 고객에게 '청결하고 친절하게 관리되는 매장'이라는 긍정적 시그널을 주어 온라인상의 방문 이탈률을 획기적으로 방어합니다. 아울러 구글·카카오맵 평판 누적으로 즉시 방문 고객의 발길을 돌리는 데 성공했습니다.",
        "사장님의 정성스러운 리뷰 답글은 네이버 플레이스 알고리즘 상 '소통이 활발한 우수 매장'으로 분류되어 SEO 가점을 부여받습니다. 더불어 외국인과 직장인들이 애용하는 구글·카카오맵 리뷰 평점 상승은 타겟 고객층 다변화에 큰 기여를 하고 있습니다.",
        "리뷰에 대한 즉각적인 피드백(답글)은 기존 고객의 재방문율을 높이는 가장 훌륭한 CRM(고객 관리) 전략입니다. 외부 지도 플랫폼(구글/카카오)에서의 긍정적 평판 확산과 맞물려, 전방위적인 로컬 평판이 최상급으로 유지되고 있습니다."
    ]
    evals['comm'] = random.choice(comm_texts)

    # 4. 인스타 평가
    insta_texts = [
        "숏폼 영상의 폭발적인 조회수는 잠재 고객에게 매장의 존재를 시각적으로 강렬하게 각인시켰음을 의미합니다. 호기심을 느낀 유저들이 네이버에 매장 이름을 직접 검색해 찾아오는 '선순환 브랜드 검색'이 활발히 발생하고 있습니다.",
        "인스타그램을 통한 시각적 바이럴이 성공적으로 확산되었습니다. 이는 매장을 단순한 음식점이 아닌 '반드시 가봐야 할 핫플레이스'로 포지셔닝하며, 외부 링크가 아닌 직접 검색을 유발해 네이버 순위 상승에도 결정적인 가점을 주고 있습니다.",
        "이번 달 인스타 릴스 노출은 지역 내 2030 타겟층에게 브랜드를 확실하게 눈도장 찍는 계기가 되었습니다. 영상을 공유하고 저장하는 행동이 늘어날수록 바이럴 계수가 기하급수적으로 상승하여, 멈추지 않는 마케팅 플라이휠(Flywheel) 구조가 완성됩니다."
    ]
    evals['insta'] = random.choice(insta_texts)

    return evals

# -----------------------------------------------------------------
# 2. 메인 UI 및 입력 폼
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 홍보 효과 보고서")
st.markdown("매월 다이내믹하게 변하는 분석 멘트를 통해 클라이언트에게 신선함과 신뢰를 제공합니다.")

try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 네이버 API 키가 없습니다. 먼저 세팅해 주세요.")
    st.stop()

with st.form("report_form"):
    st.subheader("📌 1. 타겟 매장 및 순위 데이터")
    col1, col2, col3 = st.columns(3)
    with col1:
        store_name = st.text_input("매장명 (정확히 입력)", placeholder="예: 동경생고기")
    with col2:
        promo_keyword = st.text_input("메인 홍보 키워드", placeholder="예: 대구 달서구 맛집")
    with col3:
        prev_rank = st.number_input("지난달 순위 (API 하락/상승 분석용)", min_value=1, value=15)

    st.divider()

    st.subheader("🔗 2. 이번 달 핵심 블로그 리뷰 링크 (최대 10개)")
    links = []
    link_cols = st.columns(2)
    for i in range(10):
        with link_cols[i % 2]:
            link = st.text_input(f"블로그 링크 {i+1}")
            links.append(link)
    
    st.divider()

    st.subheader("💬 3. 고객 관리 및 바이럴 홍보 지표")
    col4, col5 = st.columns(2)
    with col4:
        place_replies = st.number_input("네이버 방문자 리뷰 사장님 답글 수", min_value=0, value=45)
        kakao_google_reviews = st.number_input("카카오맵/구글 신규 리뷰 확보 수", min_value=0, value=5)
    with col5:
        insta_views = st.number_input("인스타 홍보 영상 총 조회수", min_value=0, value=15000)

    submit_button = st.form_submit_button("다이내믹 홍보 효과 평가 생성")

# -----------------------------------------------------------------
# 3. 데이터 분석 및 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not promo_keyword:
        st.warning("매장명과 홍보 키워드를 모두 입력해 주세요.")
    else:
        with st.spinner('API 순위 추출 및 이번 달 맞춤형 분석 멘트를 작성 중입니다...'):
            
            # API 추출
            current_rank = get_current_place_rank(promo_keyword, store_name, naver_client_id, naver_client_secret)
            
            # 순위 증감 로직 계산
            diff = prev_rank - current_rank if current_rank > 0 else 0
            
            # 텍스트 생성
            rank_text = ""
            if current_rank == 0:
                rank_text = f"현재 100위 밖 (신규 진입 및 트래픽 최적화 작업 중)"
                diff = -1 # 100위 밖이면 하락/방어 멘트가 나오도록 처리
            else:
                if diff > 0:
                    rank_text = f"**{current_rank}위** (전월 {prev_rank}위 대비 🔺{diff}계단 상승)"
                elif diff < 0:
                    rank_text = f"**{current_rank}위** (전월 {prev_rank}위 대비 🔻{abs(diff)}계단 하락)"
                else:
                    rank_text = f"**{current_rank}위** (전월 순위 굳건히 유지)"

            # 다이내믹 멘트 가져오기
            eval_texts = get_dynamic_evaluations(promo_keyword, diff)
            current_month = datetime.now().month

            st.success("✅ 매월 새로워지는 맞춤형 평가 보고서가 생성되었습니다!")
            
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 홍보 효과 보고서")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 순위 평가
            st.markdown(f"### 🥇 1. '{promo_keyword}' 검색 노출 및 유입 효과")
            st.markdown(f"> **현재 검색 노출 순위: {rank_text}**")
            st.markdown(f"- **홍보 효과 평가:** {eval_texts['rank']}")
            
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
