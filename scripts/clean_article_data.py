import os
from common.utils import generate_id, save_json, load_json
from models.indexed_document import IndexedDocument
from common.constants import ARTICLES_PATH, PROCESSED_ARTICLES_PATH


# Build embedding text from article content
def build_content(text: str) -> str:
    return text.strip()


# Process articles from raw JSON file
def main():
    if not os.path.exists(ARTICLES_PATH):
        raise FileNotFoundError(f"Raw article file not found: {ARTICLES_PATH}")

    # Load articles
    articles = load_json(ARTICLES_PATH)

    processed = []
    for article in articles:
        try:
            if not article.get("content"):
                continue

            _id = generate_id("article", article["title"])
            content = build_content(article["content"])

            doc = IndexedDocument(
                id=_id,
                type="article",
                title=article["title"],
                brand=None,
                content=content,
                image=None,
                created_at=article.get("created_at"),
                published_at=article.get("published_at"),
                sourcepage=article.get("url"),
                article_category=article.get("category"),
                embedding=None,
                recipe_tags=[],
                product_category=None,
                pruduct_label=None,
                product_line=None,
            )

            processed.append(doc.model_dump())
        except Exception as e:
            print(f"Failed to process article: {article.get('title')} → {e}")

    save_json(processed, PROCESSED_ARTICLES_PATH)
    print(f"Processed {len(processed)} articles → {PROCESSED_ARTICLES_PATH}")


if __name__ == "__main__":
    main()
