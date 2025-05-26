import asyncio
import os
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scraper.crawlers.base_crawler import BaseCrawler
from utils import save_json
from constants import (
    BASE_URL,
    SITEMAP_URL,
    SITEMAP_LINKS_PATH,
)


class SitemapCrawler(BaseCrawler):
    def __init__(self, headless=True):
        super().__init__(headless)

    async def run(self):

        await self.init_browser()

        sitemap = {
            "brands": [],
            "recipes": [],
            "articles": [],
            "about": [],
        }

        # Load main sitemap
        html = await self.load_page_content(SITEMAP_URL)
        soup = BeautifulSoup(html, "html.parser")

        # Extract brand links
        brand_section = soup.select_one(".sitemap-section.brands-section")
        if brand_section:
            for category_block in brand_section.select("ul.sitemap-list > li"):
                category = category_block.select_one("strong")
                category_name = (
                    category.get_text(strip=True) if category else "Uncategorized"
                )
                for a in category_block.select("li.sitemap-sublist-item > a"):
                    url = a.get("href")
                    title = a.get_text(strip=True)
                    sitemap["brands"].append(
                        {"title": title, "url": url, "category": category_name}
                    )
        print(f"Extracted {len(sitemap['brands'])} brands.")

        # Extract recipe links from "All Recipes" page
        recipe_html = await self.load_page_content(
            "https://www.madewithnestle.ca/recipes"
        )
        recipe_soup = BeautifulSoup(recipe_html, "html.parser")

        facet_section = recipe_soup.select_one(
            "ul[data-drupal-facet-alias='recipe_brand_reference']"
        )
        if facet_section:
            for li in facet_section.select("li.facet-item"):
                a_tag = li.select_one("a[href]")
                if not a_tag:
                    continue
                brand_url = urljoin(BASE_URL, a_tag["href"])
                brand_name = a_tag.get_text(strip=True).rsplit("(", 1)[0].strip()
                sitemap["recipes"].append({"brand": brand_name, "url": brand_url})

        print(f"Extracted {len(sitemap['recipes'])} recipe brands.")

        # Extract articles and about pages
        seen_about_urls = set()

        feeds_section = soup.select_one(".sitemap-list.feeds-section")
        if feeds_section:
            for a in feeds_section.select("a[href]"):
                href = a.get("href")
                title = a.get_text(strip=True)
                full_url = urljoin(BASE_URL, href) if href.startswith("/") else href
                if href.startswith("/articles?field_category_target_id="):
                    sitemap["articles"].append({"title": title, "url": full_url})
                elif (
                    not href.startswith("/articles") and full_url not in seen_about_urls
                ):
                    sitemap["about"].append({"title": title, "url": full_url})
                    seen_about_urls.add(full_url)

        print(f"Extracted {len(sitemap['articles'])} articles.")

        # Legal and policy pages
        for section in soup.select(".sitemap-section"):
            for a in section.select("a[href]"):
                href = a.get("href")
                title = a.get_text(strip=True)
                full_url = urljoin(BASE_URL, href) if href.startswith("/") else href
                if any(
                    key in href
                    for key in [
                        "terms",
                        "privacy",
                        "cookie",
                        "contact",
                        "policy",
                        "contest",
                    ]
                ):
                    if full_url not in seen_about_urls:
                        sitemap["about"].append({"title": title, "url": full_url})
                        seen_about_urls.add(full_url)

        print(f"Extracted {len(sitemap['about'])} about/legal pages.")

        save_json(sitemap, SITEMAP_LINKS_PATH)
        print(f"Saved full sitemap to {SITEMAP_LINKS_PATH}")
        return sitemap
