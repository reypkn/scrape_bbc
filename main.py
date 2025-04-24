import asyncio
from scraper.scrape_section_urls_playwright import SectionURLScraperPlaywright

async def main():
    # Base URL for the Israel-Gaza War section
    section_url = "https://www.bbc.com/news/topics/c2vdnvdg6xxt"

    # Initialize the Playwright scraper
    scraper = SectionURLScraperPlaywright(section_url)

    # Await the scraper's async method
    article_urls = await scraper.scrape_section()

    # Print the scraped URLs
    if article_urls:
        print("Scraped Article URLs:")
        for url in article_urls:
            print(url)
    else:
        print("Failed to scrape article URLs.")

if __name__ == "__main__":
    asyncio.run(main())