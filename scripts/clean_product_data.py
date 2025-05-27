import os
from common.constants import PRODUCTS_PATH, PROCESSED_PRODUCTS_PATH
from models.indexed_document import IndexedDocument
from common.utils import save_json, generate_id, safe_strip, safe_dict, load_json


# Build embedding text from key fields
def build_content(product: dict) -> str:
    parts = []

    # Description + Size
    desc = safe_strip(product.get("description"))
    size = safe_strip(product.get("product_size"))

    desc_line = ""

    if desc:
        desc_line += desc

    if size:
        if desc_line:
            desc_line += f" (Size: {size})"
        else:
            desc_line = f"Size: {size}"

    if desc_line:
        parts.append(desc_line)

    # Product contents
    contents = safe_dict(product.get("contents"))

    if isinstance(contents, dict) and contents:
        # Features
        features = contents.get("features", [])
        if isinstance(features, list):
            lines = [
                f"- {safe_strip(f)}"
                for f in features
                if isinstance(f, str) and f.strip()
            ]
            if lines:
                parts.append("Features:\n" + "\n".join(lines))

        # Ingredients
        ingredients = safe_strip(contents.get("ingredients"))
        if ingredients:
            parts.append(f"Ingredients: {ingredients}")

        # Nutrition
        nutrition_dict = safe_dict(contents.get("nutrition"))
        serving_size = safe_strip(nutrition_dict.get("serving_size"))
        items = nutrition_dict.get("items", [])
        nutrition_lines = []

        if isinstance(items, list):
            for item in items:
                item = safe_dict(item)
                if not isinstance(item, dict):
                    continue

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

                sub_items = item.get("sub_items")
                if isinstance(sub_items, list):
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
            header = f"Nutrition{f' ({serving_size})' if serving_size else ''}:"
            parts.append(header + "\n" + "\n".join(nutrition_lines))

    # Fallback: title only if all parts are empty
    if not parts:
        title = safe_strip(product.get("title"))
        brand = safe_strip(product.get("brand"))
        if title:
            fallback = f"#fallback {title} by {brand}" if brand else title
            parts.append(fallback)

    return "\n\n".join(parts).strip()


# Process products from raw JSON file
def main():
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
                image=product["images"][0] if product.get("images") else None,
                created_at=product.get("created_at"),
                published_at=None,
                sourcepage=product.get("url"),
                article_category=None,
                embedding=None,
                recipe_tags=[],
                product_category=product.get("category", None),
                product_label=product["labels"][0] if product.get("labels") else None,
                product_line=product.get("product_line", None),
            )

            processed.append(doc.model_dump())
        except Exception as e:
            print(f"Failed to process product: {product.get('name')} → {e}")

    save_json(processed, PROCESSED_PRODUCTS_PATH)
    print(f"Processed {len(processed)} products → {PROCESSED_PRODUCTS_PATH}")


if __name__ == "__main__":
    main()
