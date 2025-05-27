import json
import asyncio
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from scraper.crawlers.base_crawler import BaseCrawler
from common.constants import ARTICLES_PATH, SITEMAP_LINKS_PATH
from scraper.models import Article
from common.utils import save_json, clean_text


class ArticleCrawler(BaseCrawler):
    """
    ArticleCrawler handles scraping of editorial articles from the Nestlé Canada website.
    It loads category-level article listings, paginates if needed, and parses individual article pages
    to extract metadata such as title, date, and content.
    """

    def __init__(self, headless=True, max_concurrent=5):
        super().__init__(headless)
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def run(self):
        """
        Main entry point. Iterates through all article category pages listed in the sitemap,
        extracts article links, fetches individual article pages, and saves the results to JSON.
        """
        await self.init_browser()
        try:
            with open(SITEMAP_LINKS_PATH, "r", encoding="utf-8") as f:
                sitemap = json.load(f)

            articles = sitemap.get("articles", [])

            all_articles: List[dict] = []

            for article in articles:
                category = article["title"]
                article_url = article["url"]

                print(f"\nCrawling articles for category: {category} ...")

                html = await self.load_page_content(article_url, click_more=True)
                soup = BeautifulSoup(html, "html.parser")

                article_cards = soup.select(".masonry-item.views-row")

                print(f"Found {len(article_cards)} articles for {category}")

                # Parse each article card concurrently
                tasks = [
                    self.parse_article_page(card, category) for card in article_cards
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                articles = [r.dict() for r in results if isinstance(r, Article)]
                all_articles.extend(articles)

                print(f"{category}: {len(articles)} articles scraped.")

            if all_articles:
                save_json(all_articles, ARTICLES_PATH)
                print(f"\nSaved {len(all_articles)} articles to {ARTICLES_PATH}")

        finally:
            await self.close_browser()

    # Parse the full content of an individual article from its detail page
    async def parse_article_page(self, card, category: str) -> Article:
        async with self.semaphore:
            try:
                a_tag = card.select_one("a[href]")
                article_url = urljoin("https://www.madewithnestle.ca", a_tag["href"])

                html = await self.load_page_content(article_url)
                soup = BeautifulSoup(html, "html.parser")

                title_tag = soup.select_one("h1")
                title = title_tag.get_text(strip=True) if title_tag else "Untitled"

                date_tag = soup.select_one("h2.coh-style-published-date")
                date = date_tag.get_text(strip=True) if date_tag else None

                # Extract paragraphs from the content div directly under title
                content_div = title_tag.find_parent("div")
                paragraphs = [
                    p.get_text(strip=True)
                    for p in content_div.find_all("p", recursive=False)
                    if p.get_text(strip=True)
                ]
                content = "\n".join(paragraphs)

                now = datetime.now(timezone.utc).isoformat()

                return Article(
                    title=title,
                    url=article_url,
                    category=category,
                    content=clean_text(content),
                    punlished_at=date,
                    created_at=now,
                )
            except Exception as e:
                print(f"Failed to parse article at {article_url}: {e}")
                return None
