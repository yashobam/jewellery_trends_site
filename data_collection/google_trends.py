# jewellery_trends_site/

# Project Structure:
# - data_collection/
#     - google_trends.py
#     - pinterest_trends.py
#     - material_heat_index.py
# - dashboard/
#     - app.py
# - data/
#     - search_surges.json
#     - breakout_style.json
#     - heatmap_data.json
#     - trend_battle.json
#     - moodboard.json
#     - materials.json
# - .github/workflows/
#     - daily_update.yml

# -------------------------
# data_collection/google_trends.py
import json
from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq()

SEED_TERMS = ["ring", "necklace", "earrings", "diamond", "gold"]

# Helper: Check if related_queries result is valid

def is_valid_related_query(result, term):
    return (
        isinstance(result, dict)
        and term in result
        and isinstance(result[term], dict)
        and 'rising' in result[term]
        and isinstance(result[term]['rising'], pd.DataFrame)
        and not result[term]['rising'].empty
    )

# Top 5 Search Surges
def get_search_surges():
    surges = []
    for term in SEED_TERMS:
        try:
            print("Nothing built yet")
            pytrends.build_payload([term], timeframe='now 1-d')
            print("PAYLOAD BUILT")
            result = pytrends.related_queries()
            print("RESULT IS", result)
            if is_valid_related_query(result, term):
                data = result[term]['rising']
                top = data.head(1)
                for _, row in top.iterrows():
                    surges.append({"term": row['query'], "increase": row['value']})
        except Exception as e:
            print(f"Error processing {term}: {e}")
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
        try:
            pytrends.build_payload([term], timeframe='now 1-d')
            result = pytrends.related_queries()
            if is_valid_related_query(result, term):
                for _, row in result[term]['rising'].iterrows():
                    if row['value'] == 'Breakout':
                        styles.append(row['query'])
        except Exception as e:
            print(f"Error getting breakout for {term}: {e}")
    style = styles[0] if styles else "No breakout found"
    with open("data/breakout_style.json", "w") as f:
        json.dump({"style": style}, f)

get_search_surges()
get_heatmap_data()
get_trend_battle()
get_breakout()
