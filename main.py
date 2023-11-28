import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key = "PXNPY1YZLCSVVHJS"
news_api = "c18ba0c8ddbc4988a675a0bfabcb17a4"
yesterday = str(date.today() - timedelta(days=1))
day_before = str(date.today() - timedelta(days=2))
account_sid = "AC8606bad5d03332b5b8ebc3f9d2330a45"
auth_token = "d35033bb83d6588a0a414ff0e47d83d1"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key,
}
response = requests.get(url="https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
yesterday_close = float(data[yesterday]["4. close"])
day_before_close = float(data[day_before]["4. close"])
percent_change = round(((yesterday_close - day_before_close) / day_before_close) * 100, 2)
up_down = None
if percent_change > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
if abs(percent_change) > 0.5:
    news_parameters = {
        "apiKey": "c18ba0c8ddbc4988a675a0bfabcb17a4",
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    news_response.raise_for_status()
    news = news_response.json()["articles"][:3]
    client = Client(account_sid, auth_token)


    for article in news:
        headline = article["title"]
        brief = article["description"]
        message = client.messages \
            .create(
            body=f"{STOCK}: {up_down}{percent_change}  \n Headline : {headline}, \n Brief : {brief} ",
            from_="+16628073835",
            to='+919830430161'
        )