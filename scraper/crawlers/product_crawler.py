import json
import asyncio
import traceback
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from scraper.crawlers.base_crawler import BaseCrawler
from constants import (
    PRODUCTS_PATH,
    SITEMAP_LINKS_PATH,
    EXTERNAL_LINKS_PATH,
    BROKEN_LINKS_PATH,
)
from scraper.models import Product, Nutrition, NutritionItem, ProductContent
from scraper.utils import save_json


class ProductCrawler(BaseCrawler):
    """
    ProductCrawler handles the end-to-end scraping of product data from brand pages
    on the Nestlé Canada website. It loads each brand's product listing page, paginates
    if needed, visits each product's detail page, extracts structured data, and saves
    the results to JSON file.
    """

    SPECIAL_BRAND_URLS = {
        "Coffee Mate": [
            "https://www.madewithnestle.ca/coffee-mate-liquid",
            "https://www.madewithnestle.ca/coffee-mate-powder",
        ],
        "NESCAFÉ": ["https://www.madewithnestle.ca/nescafe/coffee"],
        "Drumstick": [
            "https://www.madewithnestle.ca/drumstick/tubs",
            "https://www.madewithnestle.ca/drumstick/classics",
            "https://www.madewithnestle.ca/drumstick/minis",
            "https://www.madewithnestle.ca/drumstick/featured-cones",
            "https://www.madewithnestle.ca/drumstick/plant-based",
        ],
        "Boost": ["https://www.madewithnestle.ca/boost/products"],
    }

    def __init__(self, headless=True, max_concurrent=5):
        super().__init__(headless)
        self.semaphore = asyncio.Semaphore(max_concurrent)  # Limit concurrent requests
        self.external_links = []
        self.broken_links = []

    # Main entry point to start the crawling process
    async def run(self):
        await self.init_browser()
        try:
            # Load brand data from JSON file
            with open(SITEMAP_LINKS_PATH, "r", encoding="utf-8") as f:
                sitemap = json.load(f)

            brands = sitemap.get("brands", [])

            all_products: List[dict] = []

            # Iterate through each brand and scrape products
            for brand in brands:
                brand_name = brand["title"]
                category = brand["category"]
                print(f"\nCrawling brand: {brand_name}...")

                brand_urls = await self.classify_brand(brand)
                if not brand_urls:
                    continue

                # Loop through brand URLs and scrape product cards
                for brand_url in brand_urls:
                    html = await self.load_page_content(brand_url, click_more=True)
                    soup = BeautifulSoup(html, "html.parser")
                    product_cards = soup.select(
                        ".coh-column.product-column, .coh-column.nescafe-product, .coh-column.product-card, .coh-column.product-drumstick"
                    )

                    if not product_cards:
                        print(f"No products found for brand: {brand_name}")
                        continue

                    # Parse each product concurrently
                    tasks = [
                        self.parse_product_page(card, brand_name, category)
                        for card in product_cards
                    ]

                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    brand_products = [
                        p.dict() for p in results if isinstance(p, Product)
                    ]
                    all_products.extend(brand_products)
                    print(f"{brand_name}: {len(brand_products)} products scraped.")

            # Save successfully parsed products
            if all_products:
                save_json(all_products, PRODUCTS_PATH)
                print(f"\nSaved {len(all_products)} products to {PRODUCTS_PATH}")

            # Save skipped external brand links for reference
            if self.external_links:
                save_json(self.external_links, EXTERNAL_LINKS_PATH)
                print(
                    f"Saved {len(self.external_links)} external brands to {EXTERNAL_LINKS_PATH}"
                )

            # Save broken links for reference
            if self.broken_links:
                save_json(self.broken_links, BROKEN_LINKS_PATH)
                print(
                    f"Saved {len(self.broken_links)} broken links to {BROKEN_LINKS_PATH}"
                )
        finally:
            await self.close_browser()

    # Parse individual product card to extract structured data
    async def parse_product_page(self, card, brand_name, category) -> Product:
        async with self.semaphore:
            try:
                # Extract product detail link
                a_tag = card.select_one("a[href]")
                detail_url = a_tag["href"]
                if not detail_url.startswith(("http", "https")):
                    detail_url = "https://www.madewithnestle.ca" + detail_url

                # Extract product name from the card
                title = a_tag.get_text(strip=True)

                # Load and parse detail page
                detail_html = await self.load_page_content(detail_url)
                detail_soup = BeautifulSoup(detail_html, "html.parser")

                # Extract product name, description, size
                name_tag = detail_soup.select_one("h1")
                name = name_tag.get_text(strip=True) if name_tag else title

                desc_tag = detail_soup.select_one(
                    ".product-description p"
                ) or detail_soup.select_one(".coh-inline-element + p")
                description = desc_tag.get_text(strip=True) if desc_tag else None

                product_size_tag = detail_soup.select_one(".product-size")
                product_size = (
                    product_size_tag.get_text(strip=True) if product_size_tag else None
                )

                # Extract all image URLs from product carousel
                images = []
                for img in detail_soup.select(
                    ".product-media-carousel .swiper-slide img"
                ):
                    src = img.get("src")
                    if not src:
                        continue
                    full_url = urljoin("https://www.madewithnestle.ca", src)
                    if full_url not in images:
                        images.append(full_url)

                # Extract subtitle from list page, detail page, or fallback to url
                subtitle_from_list = card.select_one(".product-subtitle")
                sub_brand = (
                    subtitle_from_list.get_text(strip=True)
                    if subtitle_from_list
                    else None
                )

                subtitle_from_detail = detail_soup.select_one(".product-subtitle")
                product_line = (
                    subtitle_from_detail.get_text(strip=True)
                    if subtitle_from_detail
                    else sub_brand
                )

                if not product_line:
                    lowered_url = detail_url.lower()
                    for keyword in [
                        "liquid",
                        "powder",
                        "plant-based",
                        "classics",
                        "layers",
                        "extraaz",
                        "tubs",
                        "minis",
                        "featured-cones",
                    ]:
                        if keyword in lowered_url:
                            product_line = keyword
                            break

                # Extract labels from list page and detail page
                labels = [
                    lbl.get_text(strip=True)
                    for lbl in card.select(".product-highlight-label")
                ]

                label_tags = detail_soup.select(".product-highlight")
                detail_labels = [tag.get_text(strip=True) for tag in label_tags]
                if detail_labels:
                    for label in detail_labels:
                        if label not in labels:
                            labels.append(label)

                # Extract product content details: features, nutrition, ingredients, recyclability
                features = [
                    li.get_text(strip=True)
                    for li in detail_soup.select(
                        ".coh-accordion-tabs-content ul.coh-list-container.coh-unordered-list li"
                    )
                ]

                # Extract nutrition information to build NutritionItem objects
                nutrition_items = []
                serving_tag = detail_soup.select_one(".coh-container.serving-size")
                serving_size = serving_tag.get_text(strip=True) if serving_tag else None
                parent = None
                for row in detail_soup.select(
                    ".coh-row-inner.row-depth-0, .coh-row-inner.row-depth-1"
                ):
                    label = row.select_one(".label-column")
                    amount = row.select_one(".first-column .amount-value")
                    dv = row.select_one(".second-column .nutrient-value")
                    if not label:
                        continue
                    if "row-depth-0" in row.get("class", []):
                        item = NutritionItem(
                            name=label.get_text(strip=True),
                            amount=amount.get_text(strip=True) if amount else None,
                            dv=dv.get_text(strip=True) if dv else None,
                            sub_items=[],
                        )
                        nutrition_items.append(item)
                        parent = item
                    elif parent:
                        item = NutritionItem(
                            name=label.get_text(strip=True),
                            amount=amount.get_text(strip=True) if amount else None,
                            dv=dv.get_text(strip=True) if dv else None,
                        )
                        parent.sub_items.append(item)

                nutrition = Nutrition(serving_size=serving_size, items=nutrition_items)

                ingredients = None
                ingredient_section = detail_soup.select_one(".sub-ingredients")
                if ingredient_section:
                    p = ingredient_section.find("p")
                    if p:
                        ingredients = p.get_text(strip=True)

                recyclability_tag = detail_soup.select_one(
                    ".coh-accordion-tabs-content .field--name-field-optional-recyclability"
                )
                recyclability = (
                    recyclability_tag.get_text(strip=True)
                    if recyclability_tag
                    else None
                )

                # Set product content
                contents = ProductContent(
                    features=features,
                    nutrition=nutrition if nutrition.items else None,
                    ingredients=ingredients,
                    recyclability=recyclability,
                )

                now = datetime.now(timezone.utc).isoformat()

                return Product(
                    name=name,
                    url=detail_url,
                    brand=brand_name,
                    category=category,
                    images=images,
                    product_size=product_size,
                    product_line=product_line,
                    description=description,
                    labels=labels,
                    contents=contents,
                    created_at=now,
                )

            except Exception as e:
                print(f"Failed to parse product card under brand {brand_name}: {e}")
                traceback.print_exc()
                return None

    # Classify brand URLs to determine if they are internal, external, broken, or special cases
    async def classify_brand(self, brand: dict) -> Optional[list]:
        name = brand["title"]
        url = brand["url"].strip()
        category = brand["category"]

        if not self.is_internal_url(url):
            print(f"External brand: {name} → {url}")
            self.external_links.append(
                {"title": name, "url": url, "category": category}
            )
            return None

        if await self.is_redirect_to_external(url):
            print(f"Redirects to external: {name} → {url}")
            self.external_links.append(
                {"title": name, "url": url, "category": category}
            )
            return None

        if await self.is_broken_link(url):
            print(f"Broken link: {name} → {url}")
            self.broken_links.append({"title": name, "url": url, "category": category})
            return None

        if name in self.SPECIAL_BRAND_URLS:
            return self.SPECIAL_BRAND_URLS[name]

        return [url]
