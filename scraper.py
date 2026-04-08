import requests
import json
import re
import time

def analyze_trust(title, link):
    # Detects if the deal is from an official platform or a 3rd party
    official_sources = ["amazon.com", "walmart.com", "bestbuy.com", "apple.com"]
    if any(site in link.lower() for site in official_sources):
        return "OFFICIAL"
    return "MARKETPLACE"

def get_category(title):
    t = title.lower()
    if any(x in t for x in ["ssd", "cpu", "gpu", "laptop", "ram", "motherboard"]): return "PC Hardware"
    if any(x in t for x in ["nike", "adidas", "watch", "shoes"]): return "Lifestyle"
    return "General"

def scrape():
    # RSS Source - can be expanded to include other global feeds
    source = "https://api.rss2json.com/v1/api.json?rss_url=https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1"
    try:
        data = requests.get(source, timeout=10).json()
        raw_items = data.get('items', [])
        
        deals = []
        for item in raw_items:
            title = item['title']
            # Safeguard: Ensure we capture both extreme glitches and regular high-value deals
            is_extreme = "90%" in title or "error" in title.lower() or "free" in title.lower()
            
            deals.append({
                "id": str(hash(title + item['link'])),
                "title": title,
                "link": item['link'],
                "usd": 100.0, # Logic can be added to parse price from title strings
                "cat": get_category(title),
                "trust": analyze_trust(title, item['link']),
                "is_glitch": is_extreme,
                "timestamp": time.time()
            })
        
        # Self-Healing: Only save if we actually found data
        if deals:
            with open('deals.json', 'w') as f:
                json.dump(deals, f, indent=2)
            print(f"Successfully synced {len(deals)} deals.")
            
    except Exception as e:
        print(f"Automation Safeguard Triggered: {e}")

if __name__ == "__main__":
    scrape()
