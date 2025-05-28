import os
from common.utils import generate_id, save_json, load_json, safe_strip
from scripts.vector.indexed_document import IndexedDocument
from common.constants import ARTICLES_PATH, PROCESSED_ARTICLES_PATH


def main():
    """
    Processes raw article data from JSON file, extracting relevant fields
    and generating a structured IndexedDocument for each article.
    Saves the processed documents to a new JSON file for later use.
    """
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
            content = build_content(article)

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
                article_theme=article.get("theme"),
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


def build_content(article: dict) -> str:
    """
    Constructs a semantically rich content string from an article dictionary
    for embedding in vector databases. Includes title, theme, and body content.
    """
    parts = []

    title = safe_strip(article.get("title"))
    theme = safe_strip(article.get("theme"))
    body = safe_strip(article.get("content"))

    if title:
        parts.append(f"**{title}**")
    if theme:
        parts.append(f"Theme: {theme}")
    if body:
        parts.append(body)

    return "\n\n".join(parts).strip()


if __name__ == "__main__":
    main()
