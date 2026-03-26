# -----------------------------------------------------------------
# 2. 스마트플레이스 크롤링 로직 (Selenium 강화 버전)
# -----------------------------------------------------------------
def scrape_place_reviews(place_id):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    # 네이버 봇 차단 우회를 위해 브라우저 창 크기와 user-agent 명시
    options.add_argument('window-size=1920x1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    url = f"https://m.place.naver.com/restaurant/{place_id}/review/visitor"
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # 네이버 플레이스 동적 로딩을 위해 기존 4초 -> 6초로 대기 시간 증가
        time.sleep(6) 
        
        # 스크롤을 천천히 내려서 숨겨진 리뷰까지 로딩 유도
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 1. 사장님 답글 개수 파악 (텍스트 기반 검색)
        replies = driver.find_elements(By.XPATH, "//*[contains(text(), '사장님 답글')]")
        reply_count = len(replies)
        
        # 2. 실제 화면에 로딩된 방문자 리뷰 박스 개수 파악 (가짜 숫자 50 제거)
        # 네이버 리뷰 리스트의 공통 속성인 role="presentation"을 가진 항목을 찾습니다.
        review_boxes = driver.find_elements(By.XPATH, "//li[@role='presentation' or contains(@class, 'owAeM')]")
        actual_reviews = len(review_boxes)
        
        driver.quit()
        
        return {
            "total_new": actual_reviews, 
            "replied": reply_count
        }
        
    except Exception as e:
        st.error(f"크롤링 중 에러 발생: {e}")
        return {"total_new": 0, "replied": 0}
