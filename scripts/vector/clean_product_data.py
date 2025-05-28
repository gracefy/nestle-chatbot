import os
from common.constants import PRODUCTS_PATH, PROCESSED_PRODUCTS_PATH
from scripts.vector.indexed_document import IndexedDocument
from common.utils import (
    save_json,
    load_json,
    generate_id,
    safe_strip,
    safe_dict,
    safe_first,
)


def main():
    """
    Processes raw product data from JSON file, extracting relevant fields
    and generating a structured IndexedDocument for each product.
    Saves the processed documents to a new JSON file for later use.
    """
    if not os.path.exists(PRODUCTS_PATH):
        raise FileNotFoundError(f"Raw product file not found: {PRODUCTS_PATH}")

    # Load products
    products = load_json(PRODUCTS_PATH)

    processed = []
    for product in products:
        try:
            _id = generate_id(product["brand"], product["title"])
            content = build_content(product)

            doc = IndexedDocument(
                id=_id,
                type="product",
                title=product["title"],
                brand=product["brand"],
                content=content,
                image=safe_first(product.get("images")),
                created_at=product.get("created_at"),
                published_at=None,
                sourcepage=product.get("url"),
                article_theme=None,
                embedding=None,
                recipe_tags=[],
                product_category=safe_strip(product.get("category")),
                product_label=safe_first(product.get("labels")),
                product_line=product.get("product_line", None),
            )

            processed.append(doc.model_dump())
        except Exception as e:
            print(f"Failed to process product: {product.get('name')} → {e}")

    save_json(processed, PROCESSED_PRODUCTS_PATH)
    print(f"Processed {len(processed)} products → {PROCESSED_PRODUCTS_PATH}")


def build_content(product: dict) -> str:
    """
    Constructs a semantically rich content string from a product dictionary
    for embedding in vector databases. Includes title, brand, description,
    features, nutrition, and other key attributes.
    """
    parts = []

    # Basic product metadata
    title = safe_strip(product.get("title"))
    brand = safe_strip(product.get("brand"))
    category = safe_strip(product.get("category"))

    if title:
        parts.append(f"**{title}**")
    if brand:
        parts.append(f"*Brand: {brand}*")
    if category:
        parts.append(f"*Category: {category}*")

    # Descriptive text
    desc = safe_strip(product.get("description"))
    size = safe_strip(product.get("product_size"))
    line = safe_strip(product.get("product_line"))
    label = safe_first(product.get("labels"))

    if desc:
        parts.append(f"Description: {desc}")
    if size:
        parts.append(f"Product Size: {size}")
    if line:
        parts.append(f"Product Line: {line}")
    if label:
        parts.append(f"Product Label: {label}")

    # Structured content
    contents = safe_dict(product.get("contents"))

    if contents:
        # Features
        features = contents.get("features", [])
        if isinstance(features, list):
            feature_lines = [f"- {safe_strip(f)}" for f in features if safe_strip(f)]
            if feature_lines:
                parts.append("Features:\n" + "\n".join(feature_lines))

        # Ingredients
        ingredients = safe_strip(contents.get("ingredients"))
        if ingredients:
            parts.append(f"Ingredients: {ingredients}")

        # Nutrition dict
        nutrition_dict = safe_dict(contents.get("nutrition"))
        serving_size = safe_strip(nutrition_dict.get("serving_size"))
        items = nutrition_dict.get("items", [])
        nutrition_lines = []

        if items:

            for item in items:
                item = safe_dict(item)
                name = safe_strip(item.get("name"))
                amount = safe_strip(item.get("amount"))
                dv = safe_strip(item.get("dv"))

                if not name:
                    continue

                line = f"- {name}"
                if amount:
                    line += f": {amount}"
                if dv:
                    line += f" ({dv}% DV)"
                nutrition_lines.append(line)

                # Handle sub-items if present
                sub_items = item.get("sub_items", [])

                if sub_items:
                    for sub in sub_items:
                        sub = safe_dict(sub)
                        sub_name = safe_strip(sub.get("name"))
                        sub_amount = safe_strip(sub.get("amount"))
                        sub_dv = safe_strip(sub.get("dv"))

                        if not sub_name:
                            continue

                        sub_line = f"  - {sub_name}"
                        if sub_amount:
                            sub_line += f": {sub_amount}"
                        if sub_dv:
                            sub_line += f" ({sub_dv}% DV)"
                        nutrition_lines.append(sub_line)

        if nutrition_lines:
            parts.append(
                f"Nutrition{f' ({serving_size})' if serving_size else ''}:\n"
                + "\n".join(nutrition_lines)
            )

    if not parts:
        print(f"Warning: No content for product {product.get('title', 'Unknown')}")
        return "No content available for this product."

    return "\n\n".join(parts).strip()


if __name__ == "__main__":
    main()
