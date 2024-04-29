from scraper_machine import scrape_and_save_offers
from src.hosts import url1, url2

def main():
    urls = [url1, url2]
    for url in urls:
        scrape_and_save_offers(url)

if __name__ == "__main__":
    main()