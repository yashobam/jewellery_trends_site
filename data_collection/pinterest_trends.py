import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from pytrends.request import TrendReq

# Step 1: Get top breakout jewellery-related queries from Google Trends
pytrends = TrendReq()
SEED_TERMS = ["ring", "necklace", "earrings", "diamond", "gold"]
breakout_keywords = []

for term in SEED_TERMS:
    pytrends.build_payload([term], timeframe='now 1-d')
    data = pytrends.related_queries()[term]['rising']
    if data is not None:
        for _, row in data.iterrows():
            if row['value'] == 'Breakout':
                breakout_keywords.append(row['query'])

# Step 2: Search Pinterest using the top breakout keyword
QUERY = breakout_keywords[0] if breakout_keywords else "jewelry"
URL = f"https://www.pinterest.com/search/pins/?q={QUERY.replace(' ', '%20')}"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.get(URL)
time.sleep(5)  # Allow content to load
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Extract Pinterest images
images = browser.find_elements(By.TAG_NAME, "img")
urls = []
for img in images:
    src = img.get_attribute("src")
    if src and "pinimg.com" in src:
        urls.append(src)

browser.quit()

# Save final moodboard
unique_imgs = list(dict.fromkeys(urls))[:6]
with open("data/moodboard.json", "w") as f:
    json.dump({"query": QUERY, "images": unique_imgs}, f)