from urllib.parse import urljoin

BASE_URL = "https://www.madewithnestle.ca"
SITEMAP_URL = urljoin(BASE_URL, "/sitemap")

# Raw data directory and file paths
DATA_DIR = "scraper/raw_data"
PRODUCTS_PATH = f"{DATA_DIR}/products.json"
RECIPES_PATH = f"{DATA_DIR}/recipes.json"
ARTICLES_PATH = f"{DATA_DIR}/articles.json"
ABOUT_PATH = f"{DATA_DIR}/about.json"

SITEMAP_LINKS_PATH = f"{DATA_DIR}/links/sitemap_links.json"
EXTERNAL_LINKS_PATH = f"{DATA_DIR}/links/external_links.json"
BROKEN_LINKS_PATH = f"{DATA_DIR}/links/broken_links.json"

# Processed data directory and file paths
PROCESSED_DIR = "processed_data"
PROCESSED_PRODUCTS_PATH = f"{PROCESSED_DIR}/products_for_search.json"
PROCESSED_RECIPES_PATH = f"{PROCESSED_DIR}/recipes_for_search.json"
PROCESSED_ARTICLES_PATH = f"{PROCESSED_DIR}/articles_for_search.json"
