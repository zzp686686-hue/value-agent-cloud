import requests, pandas as pd
def get_sp500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = pd.read_html(url)[0]
    return df['Symbol'].str.replace('.', '-').tolist()
def get_nasdaq100():
    # Nasdaq-100 from Nasdaq API fallback to wiki
    try:
        r = requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100", headers={"User-Agent":"Mozilla"}).json()
        return [x['symbol'] for x in r['data']['data']['rows']]
    except:
        df = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[0]
        return df['Ticker'].tolist()
def get_universe():
    sp = get_sp500()
    ndx = get_nasdaq100()
    return sorted(list(set(sp+ndx)))
