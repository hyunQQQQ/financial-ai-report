import requests
from fastapi import FastAPI

app = FastAPI()

def get_bitcoin_price():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
    ###print(data)
    return {
        "price": data[0]["trade_price"],
        "high": data[0]["high_price"],
        "low": data[0]["low_price"],
        "change_rate": data[0]["signed_change_rate"]
    }

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/price")
def price():
    return get_bitcoin_price()
