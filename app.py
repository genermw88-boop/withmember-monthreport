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
        pass 
    return current_rank

# [수정됨] 과거 대비 상승폭이 아닌, '현재 달성한 순위 구간'을 기준으로 다이내믹 멘트 생성
def get_dynamic_evaluations(promo_keyword, current_rank):
    evals = {}
    
    # 1. 순위 평가 (최상위권 / 상위권 / 순위권 진입 등으로 분리)
    if 1 <= current_rank <= 5: # 1~5위 최상위권
        rank_texts = [
            f"지역 핵심 키워드인 '{promo_keyword}'에서 최상위 노출(Top 5)을 확고히 점유하고 있습니다. 이 구간은 잠재 고객의 클릭과 유입이 가장 집중되는 '골든 존'으로, 막대한 트래픽이 실질적인 예약과 매장 방문으로 직결되는 완벽한 매출 견인차 역할을 하고 있습니다.",
            f"현재 '{promo_keyword}' 검색 결과에서 최상위권에 랭크되어 압도적인 브랜드 인지도를 확보했습니다. 광고비 지출 없이도 자연 검색을 통해 매일 엄청난 수의 지역 타겟 고객들에게 우리 매장이 1순위 선택지로 노출되고 있습니다."
        ]
    elif 6 <= current_rank <= 15: # 6~15위 상위권
        rank_texts = [
            f"'{promo_keyword}' 키워드 검색 시 모바일 첫 화면 및 상위권에 안정적으로 노출되고 있습니다. 치열한 지역 상권 경쟁 속에서도 훌륭한 방어율을 보이고 있으며, 꾸준한 유효 트래픽 유입을 통해 최상위권 진입을 위한 탄탄한 도약대를 마련했습니다.",
            f"현재 '{promo_keyword}'에서 상위권 노출을 안정적으로 유지 중입니다. 지속적인 트래픽 관리와 체류 시간 최적화 작업이 알고리즘에 긍정적으로 작용하고 있으며, 매장을 찾는 고객들에게 높은 신뢰감을 주는 위치를 선점했습니다."
        ]
    elif current_rank > 15: # 16위 이하 꾸준한 상승 구간
        rank_texts = [
            f"'{promo_keyword}' 키워드에서 의미 있는 노출 순위를 기록하며 순위 상승 궤도에 안착했습니다. 네이버 알고리즘에 맞춘 꾸준한 트래픽 파이프라인 구축이 성과를 내기 시작했으며, 지속적인 관리를 통해 상위권 노출을 목표로 페이스를 끌어올리겠습니다.",
            f"현재 검색 알고리즘 최적화 작업을 통해 '{promo_keyword}' 순위가 가시권에 진입했습니다. 블로그와 SNS 등 외부 채널의 바이럴 시너지를 더욱 집중시켜, 네이버 플레이스 지수(Place Index)를 다음 단계로 끌어올리겠습니다."
        ]
    else: # 100위 밖 (0)
        rank_texts = [
            f"현재 '{promo_keyword}' 키워드에 대한 맞춤형 순위 최적화(SEO) 기초 작업을 진행 중입니다. 알고리즘이 매장의 데이터를 수집하고 평가하는 단계이며, 조만간 검색 결과에 안정적으로 안착할 수 있도록 다방면의 트래픽을 유도하고 있습니다."
        ]
    evals['rank'] = random.choice(rank_texts)

    # 2. 블로그 평가
    blog_texts = [
        "단순 정보 나열이 아닌 네이버 C-Rank 알고리즘에 부합하는 양질의 리뷰노트들이 성공적으로 발행되었습니다. 이 문서들은 매장의 시각적 매력을 돋보이게 하는 '온라인 팸플릿' 역할을 완벽히 수행하며, 방문을 망설이는 고객의 최종 선택을 이끌어내고 있습니다.",
        f"이번 달 배포된 블로그 리뷰들은 '{promo_keyword}' 관련 모바일 스마트블록 영역에 최적화되어 노출되고 있습니다. 텍스트와 사진이 조화롭게 어우러진 생생한 후기들이 정보 탐색 후 매장으로 넘어오는 '징검다리 트래픽(전환율)'을 톡톡히 견인 중입니다."
    ]
    evals['blog'] = random.choice(blog_texts)

    # 3. 소통 및 다매체 평가
    comm_texts = [
        "꼼꼼한 리뷰 답글 관리는 신규 고객에게 '청결하고 친절하게 관리되는 매장'이라는 긍정적 시그널을 주어 온라인상의 방문 이탈률을 획기적으로 방어합니다. 아울러 구글·카카오맵 평판 누적으로 즉시 방문 고객의 발길을 돌리는 데 성공했습니다.",
        "사장님의 정성스러운 리뷰 답글은 네이버 플레이스 알고리즘 상 '소통이 활발한 우수 매장'으로 분류되어 SEO 가점을 부여받습니다. 더불어 외국인과 직장인들이 애용하는 구글·카카오맵 리뷰 평점 상승은 타겟 고객층 다변화에 큰 기여를 하고 있습니다."
    ]
    evals['comm'] = random.choice(comm_texts)

    # 4. 인스타 평가
    insta_texts = [
        "숏폼 영상의 폭발적인 조회수는 잠재 고객에게 매장의 존재를 시각적으로 강렬하게 각인시켰음을 의미합니다. 호기심을 느낀 유저들이 네이버에 매장 이름을 직접 검색해 찾아오는 '선순환 브랜드 검색'이 활발히 발생하고 있습니다.",
        "인스타그램을 통한 시각적 바이럴이 성공적으로 확산되었습니다. 이는 매장을 단순한 음식점이 아닌 '반드시 가봐야 할 핫플레이스'로 포지셔닝하며, 외부 링크가 아닌 직접 검색을 유발해 네이버 순위 상승에도 결정적인 가점을 주고 있습니다."
    ]
    evals['insta'] = random.choice(insta_texts)

    return evals

# -----------------------------------------------------------------
# 2. 메인 UI 및 입력 폼
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 홍보 효과 보고서")
st.markdown("매월 다이내믹하게 변하는 분석 멘트를 통해 클라이언트에게 신뢰를 제공합니다.")

try:
    naver_client_id = st.secrets["NAVER_CLIENT_ID"]
    naver_client_secret = st.secrets["NAVER_CLIENT_SECRET"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 네이버 API 키가 없습니다. 먼저 세팅해 주세요.")
    st.stop()

with st.form("report_form"):
    # 지난달 순위 입력칸 완전 삭제됨
    st.subheader("📌 1. 타겟 매장 및 키워드 데이터")
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("매장명 (정확히 입력)", placeholder="예: 동경생고기")
    with col2:
        promo_keyword = st.text_input("메인 홍보 키워드", placeholder="예: 대구 달서구 맛집")

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
    if not store_name or not promo_keyword:
        st.warning("매장명과 홍보 키워드를 모두 입력해 주세요.")
    else:
        with st.spinner('API 실시간 순위 추출 및 맞춤형 분석 멘트를 작성 중입니다...'):
            
            # API 단일 추출 (현재 순위만)
            current_rank = get_current_place_rank(promo_keyword, store_name, naver_client_id, naver_client_secret)
            
            # 절대 순위 텍스트 생성
            if current_rank == 0:
                rank_text = f"현재 100위 밖 (신규 진입 및 트래픽 최적화 작업 중)"
            elif 1 <= current_rank <= 5:
                rank_text = f"**{current_rank}위** (최상위권 노출 점유 중 🏆)"
            elif 6 <= current_rank <= 15:
                rank_text = f"**{current_rank}위** (상위권 안정적 노출 중 ⭐)"
            else:
                rank_text = f"**{current_rank}위** (꾸준한 순위 상승 궤도 진입 📈)"

            # 다이내믹 멘트 가져오기
            eval_texts = get_dynamic_evaluations(promo_keyword, current_rank)
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
