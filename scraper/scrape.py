from bs4 import BeautifulSoup
import requests
from scraper.utils import save_data
from loguru import logger

class BBCScraper:
    def __init__(self, url):
        self.url = url
        logger.add("logs/scraper.log", rotation="1 MB", level="INFO")  # Save logs to a file

    def scrape(self):
        try:
            logger.info(f"Starting scrape for {self.url}")
            # Make an HTTP GET request to the URL
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error if the response status code is not 200

            # Use BeautifulSoup to parse the HTML content
            logger.info("Parsing HTML content with BeautifulSoup")
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the <article> element
            article = soup.find("article")
            if not article:
                logger.error("No <article> tag found on the page.")
                return None

            # Target data extraction
            data = {}

            # 1. Headline
            headline_tag = article.find("h1")
            data["headline"] = headline_tag.text.strip() if headline_tag else "N/A"

            # 2. Article link
            data["article_link"] = self.url

            # 3. Published date-time
            time_tag = article.find("time")
            data["published_datetime"] = time_tag["datetime"].strip() if time_tag and "datetime" in time_tag.attrs else "N/A"

            # 4. All images (src and alt)
            images = article.find_all("img")
            data["images"] = [
                {"src": img.get("src", "N/A"), "alt": img.get("alt", "N/A")} for img in images
            ]

            # 5. Author name and place
            byline_div = article.find("div", {"data-testid": "byline-new-contributors"})
            if byline_div:
                spans = byline_div.find_all("span")
                data["author_name"] = spans[0].text.strip() if len(spans) > 0 else "N/A"
                data["author_place"] = spans[1].text.strip() if len(spans) > 1 else "N/A"
            else:
                data["author_name"] = "N/A"
                data["author_place"] = "N/A"

            # 6. Tags
            tags_div = article.find("div", {"data-component": "tags"})
            if tags_div:
                tags = tags_div.find_all("a")
                data["tags"] = [tag.text.strip() for tag in tags]
            else:
                data["tags"] = []

            # 7. Text content
            text_blocks = article.find_all("div", {"data-component": "text-block"})
            data["text"] = "\n".join(
                [p.text.strip() for div in text_blocks for p in div.find_all("p")]
            )

            logger.info("Scraping completed successfully.")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"An HTTP error occurred: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            return None