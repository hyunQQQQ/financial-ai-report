import requests  # HTTP 요청 보내는 라이브러리
from fastapi import FastAPI  # FastAPI 서버
from bs4 import BeautifulSoup  # HTML 파싱용
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# FastAPI 앱 객체 생성
app = FastAPI()

# 기본 루트 엔드포인트 (테스트용)
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}  # 확인용 메시지 반환

# /price 엔드포인트 → 비트코인 가격 반환
@app.get("/price")
def price():
    return get_bitcoin_price()  # 비트코인 가격 데이터 함수 호출 결과 반환

# /news 엔드포인트 → 뉴스 리스트 반환
@app.get("/news")
def news():
    return {"news": get_naver_news_api()} 

# /report 엔드포인트 → 가격 + 뉴스 통합 반환
@app.get("/report")
def report():
    price_data = get_bitcoin_price()  # 비트코인 가격 데이터
    news_data = get_naver_news_api()  
    return {
        "price": price_data,  # 가격 정보 포함
        "news": news_data  # 뉴스 정보 포함
    }

# 비트코인 가격 가져오는 함수
def get_bitcoin_price():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"  # 업비트 비트코인 API URL
    response = requests.get(url)  # GET 요청 보내기
    data = response.json()  # 응답 JSON으로 변환
    return {
        "price": data[0]["trade_price"],  # 현재가
        "high": data[0]["high_price"],  # 고가
        "low": data[0]["low_price"],  # 저가
        "change_rate": data[0]["signed_change_rate"]  # 변동률
    }

# 네이버 뉴스 API 호출 함수
def get_naver_news_api():
    query = "비트코인"
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10"

    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        news_list = []
        for item in data['items']:
            news_list.append({
                "title": item['title'],
                "url": item['link']
            })
        return news_list
    else:
        print(f"API 요청 실패: {response.status_code}")
        return []
