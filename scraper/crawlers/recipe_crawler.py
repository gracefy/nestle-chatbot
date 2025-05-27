import json
import asyncio
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from scraper.crawlers.base_crawler import BaseCrawler
from common.constants import RECIPES_PATH, SITEMAP_LINKS_PATH
from scraper.models import Recipe, RecipeStats
from common.utils import save_json, clean_text


class RecipeCrawler(BaseCrawler):
    """
    RecipeCrawler handles scraping of recipe pages from the Nestlé Canada website.
    It loads each brand's recipe list page, paginates if needed, and scrapes structured
    recipe data from individual recipe detail pages.
    """

    def __init__(self, headless=True, max_concurrent=5):
        super().__init__(headless)
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def run(self):
        await self.init_browser()
        try:
            with open(SITEMAP_LINKS_PATH, "r", encoding="utf-8") as f:
                sitemap = json.load(f)

            recipes = sitemap.get("recipes", [])

            all_recipes: List[dict] = []

            for recipe in recipes:
                brand_name = recipe["brand"]
                recipe_url = recipe["url"]

                print(f"\nCrawling recipes for brand: {brand_name} ...")

                html = await self.load_page_content(recipe_url, click_more=True)
                soup = BeautifulSoup(html, "html.parser")

                recipe_cards = soup.select(
                    ".recipe-search-results .recipe-search-card-wrapper"
                )

                print(f"Found {len(recipe_cards)} recipes for {brand_name}")

                tasks = [
                    self.parse_recipe_page(card, brand_name) for card in recipe_cards
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                recipes = [r.dict() for r in results if isinstance(r, Recipe)]
                all_recipes.extend(recipes)

                print(f"{brand_name}: {len(recipes)} recipes scraped.")

            if all_recipes:
                save_json(all_recipes, RECIPES_PATH)
                print(f"\nSaved {len(all_recipes)} recipes to {RECIPES_PATH}")

        finally:
            await self.close_browser()

    async def parse_recipe_page(self, card, brand: str) -> Recipe:
        async with self.semaphore:
            try:
                a_tag = card.select_one("a[href]")
                recipe_url = urljoin("https://www.madewithnestle.ca", a_tag["href"])

                html = await self.load_page_content(recipe_url)
                soup = BeautifulSoup(html, "html.parser")

                name = soup.select_one("h1")
                title = name.get_text(strip=True) if name else "Untitled"

                description_tag = soup.select_one(".display-info p.coh-paragraph")
                description = (
                    description_tag.get_text(strip=True) if description_tag else None
                )

                stats = RecipeStats(
                    prep_time=clean_text(self._text(soup, ".stat.prep-time")),
                    cook_time=clean_text(self._text(soup, ".stat.cook-time")),
                    total_time=clean_text(self._text(soup, ".stat.total-time")),
                    servings=clean_text(self._text(soup, ".stat.serving")),
                    skill=clean_text(self._text(soup, ".stat.skill-level")),
                )

                image_set = set()
                for img in soup.select(".swiper-slide img.coh-image"):
                    src = img.get("data-src") or img.get("src")
                    if src and src not in image_set:
                        image_set.add(src)

                images = list(image_set)

                ingredients = [
                    i.get_text(strip=True)
                    for i in soup.select(
                        ".what-you-need-content .ingredient-description"
                    )
                ]

                instructions = [
                    i.get_text(strip=True)
                    for i in soup.select("h3:-soup-contains('Instructions') ~ div p")
                ]
                if not instructions:
                    instructions = [
                        i.get_text(strip=True)
                        for i in soup.select(
                            "article .coh-row-inner .coh-column p.coh-paragraph"
                        )
                    ]

                tags = [
                    tag.get_text(strip=True)
                    for tag in soup.select(
                        ".coh-container.coh-style-recipe-tags-button:first-child"
                    )
                ]

                now = datetime.now(timezone.utc).isoformat()

                return Recipe(
                    brand=brand,
                    title=title,
                    url=recipe_url,
                    images=images,
                    description=description,
                    stats=stats,
                    ingredients=ingredients,
                    instructions=instructions,
                    tags=tags,
                    created_at=now,
                )
            except Exception as e:
                print(f"Failed to parse recipe at {recipe_url}: {e}")
                return None
