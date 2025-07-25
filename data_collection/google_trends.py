import json
from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq()

SEED_TERMS = ["ring", "necklace", "earrings", "diamond", "gold"]

# Top 5 Search Surges
def get_search_surges():
    surges = []
    for term in SEED_TERMS:
        pytrends.build_payload([term], timeframe='now 1-d')
        data = pytrends.related_queries()[term]['rising']
        if data is not None:
            top = data.head(1)
            for _, row in top.iterrows():
                surges.append({"term": row['query'], "increase": row['value']})
    surges.sort(key=lambda x: x['increase'], reverse=True)
    with open("data/search_surges.json", "w") as f:
        json.dump(surges[:5], f)

# Regional Heatmap Data
def get_heatmap_data():
    pytrends.build_payload(SEED_TERMS, timeframe='now 7-d')
    df = pytrends.interest_by_region()
    df = df.reset_index().sort_values(SEED_TERMS[0], ascending=False)
    df.to_json("data/heatmap_data.json", orient='records')

# Trend Battle
def get_trend_battle():
    pytrends.build_payload(["lab grown diamond", "moissanite"], timeframe='now 7-d')
    df = pytrends.interest_over_time().drop(columns='isPartial')
    df.to_json("data/trend_battle.json")

# Breakout Style
def get_breakout():
    styles = []
    for term in SEED_TERMS:
        pytrends.build_payload([term], timeframe='now 1-d')
        data = pytrends.related_queries()[term]['rising']
        if data is not None:
            for _, row in data.iterrows():
                if row['value'] == 'Breakout':
                    styles.append(row['query'])
    style = styles[0] if styles else "No breakout found"
    with open("data/breakout_style.json", "w") as f:
        json.dump({"style": style}, f)

get_search_surges()
get_heatmap_data()
get_trend_battle()
get_breakout()
