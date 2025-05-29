from urllib.parse import urljoin

# URLs
BASE_URL = "https://www.madewithnestle.ca"
SITEMAP_URL = urljoin(BASE_URL, "/sitemap")

# Raw data paths
RAW_DIR = "scraper/raw_data"
PRODUCTS_PATH = f"{RAW_DIR}/products.json"
RECIPES_PATH = f"{RAW_DIR}/recipes.json"
ARTICLES_PATH = f"{RAW_DIR}/articles.json"
ABOUT_PATH = f"{RAW_DIR}/about.json"

SITEMAP_LINKS_PATH = f"{RAW_DIR}/links/sitemap_links.json"
EXTERNAL_LINKS_PATH = f"{RAW_DIR}/links/external_links.json"
BROKEN_LINKS_PATH = f"{RAW_DIR}/links/broken_links.json"

# Processed data for Vector DB
PROCESSED_DIR = "processed_data"
GRAPH_PROCESSED_DIR = f"{PROCESSED_DIR}/vector"
PROCESSED_PRODUCTS_PATH = f"{PROCESSED_DIR}/products_vector.json"
PROCESSED_RECIPES_PATH = f"{PROCESSED_DIR}/recipes_vector.json"
PROCESSED_ARTICLES_PATH = f"{PROCESSED_DIR}/articles_vector.json"


# Processed data for graph DB
GRAPH_PROCESSED_DIR = f"{PROCESSED_DIR}/graph"
GRAPH_PRODUCTS_PATH = f"{GRAPH_PROCESSED_DIR}/products_graph.json"
GRAPH_BRANDS_PATH = f"{GRAPH_PROCESSED_DIR}/brands_graph.json"
GRAPH_EDGES_PATH = f"{GRAPH_PROCESSED_DIR}/edges_graph.json"
