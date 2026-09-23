from src.universe import get_universe
from src.edgar_fetcher import fetch_market, fetch_financials_5y
from src.financials import normalized_earnings
from src.valuation import fair_value_engine
from src.report_generator import generate_report
import os

WATCHLIST = ["GOOGL","NVDA","INTC","AAPL","TSLA","MU","SNDK","LULU","COST","ADBE","CRM","ORCL","PYPL","CSCO"]

def run():
    tickers = get_universe()
    print(f"Scanning {len(tickers)} tickers")
    results=[]
    alerts=[]
    for ticker in tickers[:600]: # 生产全量
        try:
            mkt = fetch_market(ticker)
            fin = fetch_financials_5y(ticker)
            if not mkt['price']: continue
            norm = normalized_earnings(fin['income'], mkt['shares'], ticker)
            if not norm: continue
            val = fair_value_engine(norm['norm_eps'], 'Strong', norm['roic'], norm['eps_cagr_5y'], True)
            price = mkt['price']
            bear_mos = (val['bear_fair']-price)/val['bear_fair'] if val['bear_fair'] else -1
            base_mos = (val['base_fair']-price)/val['base_fair'] if val['base_fair'] else -1
            # 第一层筛选
            if norm['roic']<0.1 or bear_mos < -0.5: continue
            results.append({
                "ticker": ticker, "price": price, "market_cap": mkt['market_cap'],
                "ttm_eps": mkt.get('pe') and price/mkt['pe'],
                "norm_eps": norm['norm_eps'], "pe": mkt['pe'],
                "bear_fair": val['bear_fair'], "base_fair": val['base_fair'],
                "bear_mos": bear_mos, "base_mos": base_mos,
                "fcf_yield": norm['fcf_yield'], "roic": norm['roic'],
                "debt": mkt['ev'], "moat": "Strong"
            })
            if ticker in WATCHLIST:
                # 检测异动: 简化
                if abs(base_mos)>0.3:
                    alerts.append({"ticker":ticker,"reason":"估值进入新区间","mos":base_mos})
        except Exception as e:
            print(ticker, e)
            continue
    os.makedirs("docs", exist_ok=True)
    generate_report(results, alerts)
    print("Done. docs/data.json generated")

if __name__ == "__main__":
    run()