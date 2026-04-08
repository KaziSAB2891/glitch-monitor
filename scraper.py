import requests
import json
import re
import time

def analyze_trust(title):
    official_terms = ["Amazon.com", "Walmart.com", "Sold by Brand", "Verified Seller"]
    if any(term.lower() in title.lower() for term in official_terms):
        return "OFFICIAL"
    return "MARKETPLACE"

def get_category(title):
    t = title.lower()
    if any(x in t for x in ["ssd", "cpu", "gpu", "laptop", "ram"]): return "Electronics"
    if any(x in t for x in ["nike", "adidas", "shirt", "shoes"]): return "Fashion"
    return "General"

def scrape():
    # RSS to JSON proxy to avoid bot-detection
    source = "https://api.rss2json.com/v1/api.json?rss_url=https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1"
    try:
        data = requests.get(source).json()
        raw_items = data.get('items', [])
        
        deals = []
        for item in raw_items:
            title = item['title']
            # Glitch detection: 70%+ off or keyword 'error'
            if re.search(r'(7[0-9]|8[0-9]|9[0-9])%', title) or "error" in title.lower():
                deals.append({
                    "id": str(hash(title)),
                    "title": title,
                    "link": item['link'],
                    "usd": 100.0, # Placeholder: logic to extract price can be added
                    "cat": get_category(title),
                    "trust": analyze_trust(title),
                    "is_glitch": "90%" in title or "error" in title.lower(),
                    "time": time.time()
                })
        
        with open('deals.json', 'w') as f:
            json.dump(deals, f)
            
    except Exception as e:
        print(f"Scrape failed: {e}")

if __name__ == "__main__":
    scrape()
