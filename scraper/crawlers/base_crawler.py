from urllib.parse import urlparse
from playwright.async_api import async_playwright


class BaseCrawler:
    """
    Base class for Playwright-based crawlers.
    Handles browser initialization and context setup.
    """

    def __init__(self, headless=True):
        self.headless = headless  # Run browser in headless mode by default
        self.browser = None
        self.context = None

    # Launch a new browser context with default viewport and user settings
    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="America/Toronto",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        )

    # Load the page content using Playwright
    async def load_page_content(self, url: str, click_more=False) -> str:
        if not self.browser:
            raise RuntimeError("Browser not initialized. Call init_browser() first.")
        try:
            page = await self.context.new_page()
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # Accept cookie banner
            try:
                await page.click('text="Accept All Cookies"', timeout=3000)
                # print("Cookie banner accepted.")
            except:
                pass

            # Recursively click "More" pagination button until no more pages are available
            if click_more:
                while True:
                    try:
                        more_btn = await page.wait_for_selector(
                            'a[rel="next"]', timeout=3000
                        )
                        await more_btn.click()
                        await page.wait_for_timeout(1000)
                        # print("Clicked 'More' button.")
                    except:
                        break

            await page.wait_for_timeout(1000)
            content = await page.content()
            await page.close()
            return content
        except Exception as e:
            print(f"❌ Error loading {url}: {e}")
            return ""

    # Check if the URL is internal to the madewithnestle.ca domain
    def is_internal_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.netloc.endswith("madewithnestle.ca")

    # Check if the URL is redirecting to an external site
    async def is_redirect_to_external(self, url: str) -> bool:
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=10000)
            final_url = page.url
            await page.close()

            return not urlparse(final_url).netloc.endswith("madewithnestle.ca")
        except Exception:
            return False

    # Check if the URL is a broken link (returns 404 or other error status)
    async def is_broken_link(self, url: str) -> bool:
        try:
            page = await self.context.new_page()
            response = await page.goto(url, timeout=10000)
            await page.close()
            return response is None or response.status >= 400
        except Exception:
            return True

    # Clean up browser resources after crawling is complete
    async def close_browser(self):
        if self.browser:
            await self.browser.close()

    # Extract stripped text
    def _text(self, soup, selector: str) -> str:
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else None
