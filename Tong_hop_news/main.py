from datetime import datetime
from scrapers.vnexpress_scraper import get_articles as vne
from scrapers.haituh_scraper import get_articles as haitu
from scrapers.tuoitre_scraper import get_articles as tt
from db import save_article

def collect():
    print(f"\n {datetime.now()}")
    for src, func in [("VNExpress", vne), ("24h", haitu), ("Tuổi Trẻ", tt)]:
        print(f" {src}")
        
        for art in func():
            
            save_article(art["title"], art["link"], art["content"], art["source"],art["published_date"])

collect()

