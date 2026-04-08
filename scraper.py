import requests, json, re, time

def analyze_trust(title, link):
    # Detects official retailers to protect users from marketplace scams
    official = ["amazon.com", "walmart.com", "apple.com", "bestbuy.com", "target.com"]
    return "OFFICIAL" if any(site in link.lower() for site in official) else "MARKETPLACE"

def get_category(title):
    t = title.lower()
    if any(x in t for x in ["ssd", "cpu", "gpu", "laptop", "ram", "motherboard"]): return "PC Hardware"
    if any(x in t for x in ["nike", "adidas", "watch", "shoes", "fashion"]): return "Lifestyle"
    return "General"

def scrape():
    # RSS to JSON via proxy to bypass basic bot-detection
    source = "https://api.rss2json.com/v1/api.json?rss_url=https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1"
    try:
        response = requests.get(source, timeout=15)
        data = response.json()
        raw_items = data.get('items', [])
        
        deals = []
        for item in raw_items:
            title = item['title']
            # Safeguard: Detection for Price Errors, 70%+ off, or Freebies
            is_extreme = any(k in title.lower() for k in ["error", "glitch", "free"]) or re.search(r'(7[0-9]|8[0-9]|9[0-9])%', title)
            
            deals.append({
                "id": str(hash(title + item['link'])),
                "title": title,
                "link": item['link'],
                "usd": 100.0, # Note: Price parsing logic can be expanded here
                "cat": get_category(title),
                "trust": analyze_trust(title, item['link']),
                "is_glitch": is_extreme,
                "timestamp": time.time()
            })
        
        if deals:
            with open('deals.json', 'w') as f:
                json.dump(deals, f, indent=2)
            print(f"Successfully automated {len(deals)} deals.")
            
    except Exception as e:
        print(f"Scraper Safeguard: {e}")

if __name__ == "__main__":
    scrape()
