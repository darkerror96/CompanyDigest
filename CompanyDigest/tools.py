import os

import requests
import yfinance as yf


# google news API tool
def get_google_news_about_company(company_name):
    url = f"https://gnews.io/api/v4/search?q={company_name}&lang=en&max=5&apikey={os.getenv("NEWS_API_KEY")}"

    response = requests.get(url)
    data = response.json()

    news_data = f"Latest News about {company_name}: -\n\n"

    articles = data["articles"]
    for i in range(len(articles)):
        news_data += str(i) + ". " + articles[i]["description"] + "\n"

    return news_data


# yahoo finance API tool
def get_yahoo_finance_data_about_company(ticker_symbol):
    data = yf.Ticker(ticker_symbol)

    finance_data = f"Latest Finance Info about {ticker_symbol}: -\n\n"
    finance_data += (
        "Live Market Price: " + str(data.analyst_price_targets["current"]) + "\n"
    )
    finance_data += "History Metadata: " + str(data.history_metadata) + "\n"
    finance_data += (
        "Quarterly Income Statement: " + str(data.quarterly_income_stmt) + "\n"
    )
    finance_data += "Earnings History: " + str(data.earnings_history) + "\n"

    return finance_data
