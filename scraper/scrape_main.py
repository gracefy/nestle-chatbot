import asyncio
from scraper.crawlers.product_crawler import ProductCrawler
from scraper.crawlers.sitemap_crawler import SitemapCrawler
from scraper.crawlers.recipe_crawler import RecipeCrawler
from scraper.crawlers.article_crawler import ArticleCrawler


async def run_all():

    # print("Starting SitemapCrawler...")
    # await SitemapCrawler().run()

    print("Starting ProductCrawler...")
    await ProductCrawler().run()

    # print("Starting RecipeCrawler...")
    # await RecipeCrawler().run()

    # print("Starting ArticleCrawler...")
    # await ArticleCrawler().run()


if __name__ == "__main__":
    asyncio.run(run_all())
