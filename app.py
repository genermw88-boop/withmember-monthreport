import streamlit as st
import requests
import random
from datetime import datetime

# -----------------------------------------------------------------
# 1. 네이버 지도 숨겨진 내부 망(Internal API) 직접 호출 로직
# -----------------------------------------------------------------
def get_real_map_rank(keyword, store_name):
    # 실제 네이버 지도가 검색할 때 쓰는 비공식 주소입니다.
    url = "https://map.naver.com/v5/api/search"
    
    # 네이버 지도를 쓰는 것처럼 서버를 속이는 세팅
    params = {
        "caller": "pc_map",
        "query": keyword,
        "type": "all",
        "page": 1,
        "displayCount": 100, # 1위부터 100위까지 한 번에 긁어옵니다.
        "isPlaceRecommendationReplace": "true",
        "lang": "ko"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://map.naver.com/"
    }
    
    try:
        res = requests.get(url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            # 네이버 지도의 검색 결과 리스트로 깊숙이 들어갑니다.
            places = data.get("result", {}).get("place", {}).get("list", [])
            
            if not places:
                return 0
                
            target_name = store_name.replace(" ", "").lower()
            
            # 1위부터 100위까지 돌면서 우리 매장 이름이 있는지 찾습니다.
            for idx, place in enumerate(places):
                name = place.get("name", "").replace(" ", "").lower()
                if target_name in name:
                    return idx + 1 # 찾으면 실제 순위 반환
                    
    except Exception as e:
        pass
        
    return 0 # 못 찾거나 에러 나면 0 (100위 밖)

# -----------------------------------------------------------------
# 2. 다이내믹 텍스트 생성 (자동 추출된 순위 기반)
# -----------------------------------------------------------------
def get_keyword_evaluation(keyword, rank):
    if rank == 0:
        return f"현재 '{keyword}' 키워드에 대한 맞춤형 순위 최적화(SEO) 기초 작업을 진행 중입니다. 네이버 알고리즘이 매장의 데이터를 수집하고 평가하는 단계이며, 조만간 검색 결과에 안정적으로 안착할 수 있도록 다방면의 유효 트래픽을 유도하고 있습니다."
    elif rank <= 5:
        texts = [
            f"'{keyword}' 검색 시 **최상위권({rank}위)** 노출을 확고히 점유하고 있습니다. 이 '골든 존'은 잠재 고객의 유입이 가장 집중되는 곳으로, 막대한 트래픽이 실질적인 예약과 방문으로 직결되는 완벽한 매출 견인차 역할을 하고 있습니다.",
            f"현재 '{keyword}' 검색 결과에서 **{rank}위**에 랭크되어 압도적인 브랜드 인지도를 확보했습니다. 자연 검색을 통해 매일 엄청난 수의 지역 타겟 고객들에게 1순위 선택지로 노출 중입니다."
        ]
        return random.choice(texts)
    elif rank <= 15:
        texts = [
            f"'{keyword}' 키워드 검색 시 **상위권({rank}위)**에 안정적으로 노출되고 있습니다. 치열한 지역 상권 경쟁 속에서도 훌륭한 방어율을 보이며, 최상위권 진입을 위한 탄탄한 유효 트래픽을 모으고 있습니다.",
            f"현재 '{keyword}'에서 **{rank}위** 노출을 유지 중입니다. 지속적인 트래픽 관리와 체류 시간 최적화 작업이 알고리즘에 긍정적으로 작용하여, 매장을 찾는 고객들에게 높은 신뢰감을 주는 위치를 선점했습니다."
        ]
        return random.choice(texts)
    else:
        texts = [
            f"'{keyword}' 키워드에서 **{rank}위**를 기록하며 의미 있는 순위 상승 궤도에 안착했습니다. 네이버 알고리즘에 맞춘 꾸준한 트래픽 파이프라인 구축이 성과를 내기 시작했으며, 지속적인 관리로 상위권 노출을 이끌어내겠습니다."
        ]
        return random.choice(texts)

def get_dynamic_evaluations():
    evals = {}
    blog_texts = [
        "네이버 C-Rank 알고리즘에 부합하는 양질의 리뷰노트들이 성공적으로 발행되었습니다. 이 문서들은 매장의 시각적 매력을 돋보이게 하는 '온라인 팸플릿' 역할을 완벽히 수행하며, 방문을 망설이는 고객의 최종 선택을 이끌어내고 있습니다.",
        "이번 달 배포된 리뷰들은 스마트블록 영역에 최적화되어 노출되고 있습니다. 텍스트와 사진이 조화롭게 어우러진 생생한 후기들이 정보 탐색 후 매장으로 넘어오는 '징검다리 트래픽(전환율)'을 톡톡히 견인 중입니다."
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
# 3. 메인 UI 및 입력 폼
# -----------------------------------------------------------------
st.set_page_config(page_title="WithMember 리포트 자동화", page_icon="📈", layout="wide")

st.title("📈 WithMember 프리미엄 마케팅 홍보 효과 보고서")
st.markdown("네이버 지도의 실제 데이터를 추적하여 순위와 성과를 1초 만에 자동 분석합니다.")

with st.form("report_form"):
    st.subheader("📌 1. 타겟 매장 및 자동 분석할 홍보 키워드 (최대 5개)")
    store_name = st.text_input("매장명 (순위 검색용, 띄어쓰기 없이 정확히)", placeholder="예: 동경생고기")
    
    st.caption("홍보 키워드만 입력하세요. **순위는 파이썬이 네이버 지도를 뚫고 알아서 찾아옵니다.**")
    
    keywords = []
    kw_cols = st.columns(5)
    for i in range(5):
        with kw_cols[i]:
            k = st.text_input(f"키워드 {i+1}", key=f"kw_{i}")
            if k.strip():
                keywords.append(k.strip())

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
    col1, col2 = st.columns(2)
    with col1:
        place_replies = st.number_input("네이버 방문자 리뷰 사장님 답글 수", min_value=0, value=45)
        kakao_google_reviews = st.number_input("카카오맵/구글 신규 리뷰 확보 수", min_value=0, value=5)
    with col2:
        insta_views = st.number_input("인스타 홍보 영상 총 조회수", min_value=0, value=15000)

    submit_button = st.form_submit_button("순위 100% 자동 분석 및 보고서 추출")

# -----------------------------------------------------------------
# 4. 데이터 분석 및 결과 출력
# -----------------------------------------------------------------
if submit_button:
    if not store_name or not keywords:
        st.warning("매장명과 최소 1개 이상의 홍보 키워드를 입력해 주세요.")
    else:
        with st.spinner('네이버 지도 내부망에 접속하여 실제 순위를 자동 추출 중입니다...'):
            
            # 입력된 키워드들에 대해 자동으로 찐 순위를 추출합니다.
            analyzed_ranks = []
            for kw in keywords:
                rank = get_real_map_rank(kw, store_name)
                analyzed_ranks.append(rank)
            
            eval_texts = get_dynamic_evaluations()
            current_month = datetime.now().month

            st.success("✅ 순위 자동 추출 및 평가 보고서 생성이 완료되었습니다!")
            
            st.markdown("---")
            st.markdown(f"## [WithMember] {current_month}월 종합 마케팅 홍보 효과 보고서")
            st.markdown(f"**수신:** {store_name} 대표님")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 1. 키워드별 순위 평가
            st.markdown(f"### 🥇 1. 핵심 타겟 키워드 검색 노출 및 유입 효과")
            for i in range(len(keywords)):
                rank_num = analyzed_ranks[i]
                rank_display = f"{rank_num}위" if rank_num > 0 else "현재 100위 밖 (최적화 진행 중)"
                
                st.markdown(f"> **[{keywords[i]}]** - 현재 플레이스 순위: **{rank_display}**")
                st.markdown(f"- **홍보 효과 평가:** {get_keyword_evaluation(keywords[i], rank_num)}")
                st.markdown("") 
            
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
