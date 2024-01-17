import requests
import os
from twilio.rest import Client

# create environment variable=  export api_key=id
stock_api_key = "S5HOIOQ8GDDGCKIJ"
news_api_key = os.environ.get("news")
account_sid = os.environ.get('account')
auth_token = os.environ.get('token')

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
}

news_api_params = {
    "qInTitle": COMPANY_NAME,
    "apiKey": news_api_key,
}

response = requests.get(STOCK_ENDPOINT, stock_api_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
# print(data["Time Series (Daily)"]["2024-01-16"]["4. close"])
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_close = day_before_yesterday_data["4. close"]

difference = float(yesterday_close) - float(day_before_yesterday_close)
up_down = None
if difference > 0:
    up_down = "🔼"
else:
    up_down = "🔻"

difference_percent = round((difference / float(yesterday_close)) * 100)

# alert for > 2% change in stock
if abs(difference_percent) > 2:
    response = requests.get(NEWS_ENDPOINT, news_api_params)
    response.raise_for_status()
    data = response.json()["articles"]

    first_three_articles = data[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{difference_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in first_three_articles]

    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from="+15132453456",
            to="+15132234576",
        )

## STEP 2: https://newsapi.org/


#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

