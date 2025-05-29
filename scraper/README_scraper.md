# Nestlé Scraper Module

This module extracts structured data from the Made With Nestlé Canada website using Playwright + BeautifulSoup.

## How to Run

Make sure you have Python 3.10.13 and dependencies installed:

```bash
cd backend
pip install -r requirements.txt
```

Then run the full scraping pipeline:

```bash
cd ..
python -m scraper.scrape_main.py
```

## How It Works

The main script first extracts all URLs from the sitemap, then sequentially crawls:

1. **Products**
2. **Recipes**
3. **Articles**

All raw data is saved to the `scraper/raw_data/` directory.
Each file contains structured product/article/recipe data for downstream RAG usage.

## TODO

The following product pages could not be successfully scraped due to access issues or structural differences. These cases are excluded from the current dataset and may require custom handling in the future.

### 1. Product List Pages (Not individual products)

These URLs point to product listing pages rather than individual product pages:

- https://www.madewithnestle.ca/mackintosh-toffee
- https://www.madewithnestle.ca/quality-street

### 2. Access Restricted Pages (403 Forbidden / Unauthorized)

These pages return an "You are not authorized to access this page" error:

- https://www.madewithnestle.ca/nescaf%C3%A9/nescaf%C3%A9-gold-dark-roast-capsules-12-cups
- https://www.madewithnestle.ca/nescaf%C3%A9/nescaf%C3%A9-gold-original-capsules-12-cups

> For more information, see `/scripts/graph/` and `/scripts/vector/` for cleaning and database upload steps.
