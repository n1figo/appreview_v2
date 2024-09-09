from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_reviews(url, num_scrolls=5):
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드 실행

    # 웹드라이버 초기화
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # 리뷰 버튼 클릭
    try:
        review_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and contains(., '리뷰')]"))
        )
        review_button.click()
    except Exception as e:
        print(f"리뷰 버튼을 찾을 수 없습니다: {e}")
        driver.quit()
        return []

    # 리뷰 로딩을 위해 스크롤
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # 페이지 소스 가져오기
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # 리뷰 추출
    reviews = []
    review_elements = soup.find_all('div', class_='RHo1pe')
    for element in review_elements:
        author = element.find('span', class_='X43Kjb').text
        rating = len(element.find_all('span', class_='kvMYJc'))
        content = element.find('div', class_='h3YV2d').text
        reviews.append({'author': author, 'rating': rating, 'content': content})

    driver.quit()
    return reviews

# 사용 예시
url = "https://play.google.com/store/apps/details?id=com.kbins.kbinsure&hl=ko-KR"
reviews = get_reviews(url)

# 결과를 DataFrame으로 변환
df = pd.DataFrame(reviews)
print(df)

# CSV 파일로 저장 (선택사항)
# df.to_csv('app_reviews.csv', index=False, encoding='utf-8-sig')
