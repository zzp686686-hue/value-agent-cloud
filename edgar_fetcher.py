# 以SEC filing为准，yfinance兜底
import yfinance as yf
from datetime import datetime

CYCLICAL = {'NVDA','MU','SNDK','INTC','AMD','STX','WDC','XOM','CVX','F','GM'}

def fetch_market(ticker):
    t = yf.Ticker(ticker)
    info = t.info
    hist = t.history(period="5y")
    return {
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "shares": info.get("sharesOutstanding"),
        "ev": info.get("enterpriseValue"),
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "ps": info.get("priceToSalesTrailing12Months"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "date": datetime.now().isoformat()
    }

def fetch_financials_5y(ticker):
    t = yf.Ticker(ticker)
    # 这里生产环境换成 sec-edgar-api 解析 10-K / 10-Q
    inc = t.financials
    cf = t.cashflow
    bs = t.balance_sheet
    return {"income": inc, "cashflow": cf, "balance": bs}