import streamlit as st
import json
import pandas as pd

st.title("Daily Jewellery Trends Dashboard")

st.header("🔍 Top 5 Search Surges")
with open("data/search_surges.json") as f:
    st.json(json.load(f))

st.header("🚀 Breakout Style of the Day")
with open("data/breakout_style.json") as f:
    st.success(json.load(f)['style'])

st.header("🗺️ Regional Heatmap")
df = pd.read_json("data/heatmap_data.json")
st.map(df.rename(columns={"geoName": "location", "ring": "value"}))

st.header("⚔️ Trend Battle: Lab-Grown vs Moissanite")
battle_df = pd.read_json("data/trend_battle.json")
st.line_chart(battle_df)

st.header("🎨 Moodboard of the Day")
with open("data/moodboard.json") as f:
    mood = json.load(f)
    st.subheader(f"Query: {mood['query']}")
    st.image(mood["images"])

st.header("💎 Materials Heat Index")
with open("data/materials.json") as f:
    st.bar_chart(pd.DataFrame(json.load(f)).set_index("material"))
