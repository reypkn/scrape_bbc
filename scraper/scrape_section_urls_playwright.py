from playwright.async_api import async_playwright
from loguru import logger

class SectionURLScraperPlaywright:
    def __init__(self, base_url, max_retries=10):
        self.base_url = base_url
        self.article_urls = []
        self.max_retries = max_retries
        logger.add("logs/playwright_section_url_scraper.log", rotation="1 MB", level="INFO")  # Save logs to a file

    async def scrape_section(self):
        async with async_playwright() as p:
            # Set headless=False to see the browser window
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(self.base_url)

            try:
                # Handle the "I agree" pop-up
                try:
                    logger.info("Checking for the 'I agree' pop-up.")
                    await page.wait_for_selector("button[title='I agree']", timeout=5000)  # Wait for the button to appear
                    await page.click("button[title='I agree']")  # Click the button
                    logger.info("Clicked the 'I agree' button.")
                except Exception as e:
                    logger.warning(f"'I agree' button not found or could not be clicked: {e}")

                # Start scraping
                while True:
                    logger.info(f"Scraping page: {page.url}")

                    # Wait for the article grid to load
                    await page.wait_for_selector("div[data-testid='alaska-grid']")

                    # Extract article URLs
                    cards = await page.query_selector_all("div[data-testid='liverpool-card'] div[data-testid='anchor-inner-wrapper'] a")
                    current_urls = []
                    for card in cards:
                        url = await card.get_attribute("href")
                        if url and url not in self.article_urls:
                            if not url.startswith("http"):
                                url = f"https://www.bbc.com{url}"  # Convert relative URLs to absolute
                            self.article_urls.append(url)
                            current_urls.append(url)

                    logger.info(f"Found {len(current_urls)} new article URLs on this load. Total: {len(self.article_urls)}")

                    # Check for "Next Page" button
                    next_button = await page.query_selector("button[data-testid='pagination-next-button']")
                    if not next_button:
                        logger.info("Next Page button not found. No more content to load.")
                        break

                    # Scroll to the button to ensure it's visible
                    await next_button.scroll_into_view_if_needed()
                    logger.info("Scrolled to Next Page button.")

                    # Click the "Next Page" button
                    logger.info("Clicking Next Page button to load more content.")
                    try:
                        await next_button.click(timeout=5000, force=True)
                        await page.wait_for_timeout(2000)  # Wait for initial loading
                    except Exception as e:
                        logger.error(f"Failed to click Next Page button: {e}. Stopping pagination.")
                        break

                    # Simulate user interaction to trigger content loading
                    for _ in range(3):
                        await page.evaluate("window.scrollBy(0, window.innerHeight)")
                        await page.wait_for_timeout(2000)
                        await page.evaluate("window.scrollBy(0, -window.innerHeight)")
                        await page.wait_for_timeout(2000)

                    # Scroll through the entire page
                    for _ in range(5):
                        await page.evaluate("window.scrollBy(0, 500)")
                        await page.wait_for_timeout(1000)

                    # Log the page's HTML for debugging
                    html_content = await page.content()
                    logger.debug(f"Page HTML after clicking 'Next Page': {html_content}")

                    # Check if new content is loaded
                    retries = 0
                    while retries < self.max_retries:
                        await page.wait_for_timeout(5000)  # Increase timeout to wait for content
                        new_cards = await page.query_selector_all("div[data-testid='liverpool-card'] div[data-testid='anchor-inner-wrapper'] a")
                        if len(new_cards) > len(cards):
                            logger.info("New content detected.")
                            break
                        retries += 1

                    if retries == self.max_retries:
                        logger.warning("No new content detected after clicking 'Next Page'. Ending pagination.")
                        break

                # Save all collected article URLs to a file
                with open("data/section_article_urls_playwright.txt", "w") as file:
                    file.write("\n".join(self.article_urls))
                logger.info(f"Scraped {len(self.article_urls)} article URLs across all loads.")

            except Exception as e:
                logger.exception(f"An error occurred: {e}")
            finally:
                await browser.close()

        return self.article_urls