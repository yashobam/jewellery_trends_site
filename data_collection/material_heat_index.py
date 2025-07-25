import json
from pytrends.request import TrendReq

pytrends = TrendReq()
MATERIALS = ["gold", "silver", "moissanite", "resin", "opal"]

def material_index():
    pytrends.build_payload(MATERIALS, timeframe='now 7-d')
    df = pytrends.interest_over_time().drop(columns='isPartial')
    latest = df.iloc[-1].to_dict()
    ranked = sorted([{"material": k, "score": v} for k, v in latest.items()], key=lambda x: -x['score'])
    with open("data/materials.json", "w") as f:
        json.dump(ranked, f)

material_index()
