import numpy as np
import pandas as pd

def calc_cagr(series):
    if len(series)<2: return 0
    return (series.iloc[0]/series.iloc[-1])**(1/len(series))-1 if series.iloc[-1]>0 else 0

def normalized_earnings(df_income, shares_now, ticker):
    # df_income: 5y Net Income
    net = df_income.loc['Net Income'].dropna() if 'Net Income' in df_income.index else pd.Series()
    if net.empty: return None
    mean5 = net.tail(5).mean()
    mean3 = net.tail(3).mean()
    ttm = net.iloc[0] if len(net)>0 else mean3
    # 周期性检测
    if ticker in ['MU','SNDK','NVDA','INTC','AMD'] and net.std()/abs(net.mean())>0.6:
        norm = net.median()  # 用中位数防止顶部
    else:
        norm = mean5*0.5 + mean3*0.3 + ttm*0.2
    return {
        "norm_net_income": norm,
        "norm_eps": norm / shares_now if shares_now else 0,
        "rev_cagr_5y": 0.12, # 示例，实际从revenue计算
        "eps_cagr_5y": 0.15,
        "roic": 0.18,
        "fcf_yield": 0.05
    }