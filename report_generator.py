import json, datetime
def generate_report(results, watchlist_alerts):
    # results: list of dict with all metrics
    # 按 Base MoS 排序取Top10
    top10 = sorted(results, key=lambda x: x['base_mos'], reverse=True)[:10]
    report = {
        "date": datetime.date.today().isoformat(),
        "top10": top10,
        "watchlist": watchlist_alerts
    }
    with open("docs/data.json","w") as f:
        json.dump(report,f,indent=2)
    return report