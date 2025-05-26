import asyncio
from scraper.crawlers.product_crawler import ProductCrawler
from scraper.crawlers.sitemap_crawler import SitemapCrawler
from scraper.crawlers.recipe_crawler import RecipeCrawler
from scraper.crawlers.article_crawler import ArticleCrawler


# Main entry point for running all crawlers
async def run_all():

    # Step 1: Extract sitemap links
    print("Starting SitemapCrawler to extract sitemap links...")
    await SitemapCrawler().run()

    # Step 2.1: Crawl products
    print("Starting ProductCrawler...")
    await ProductCrawler().run()

    # Step 2.2: Crawl recipes
    print("Starting RecipeCrawler...")
    await RecipeCrawler().run()

    # Step 2.3: Crawl articles
    print("Starting ArticleCrawler...")
    await ArticleCrawler().run()


if __name__ == "__main__":
    asyncio.run(run_all())
