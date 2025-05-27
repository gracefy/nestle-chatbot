import os
from typing import List
from common.constants import RECIPES_PATH, PROCESSED_RECIPES_PATH
from scripts.vector.indexed_document import IndexedDocument
from common.utils import save_json, generate_id, load_json


# Build embedding text from key fields
def build_content(
    title: str,
    description: str,
    ingredients: List[str],
    instructions: List[str],
    tags: List[str],
    stats: dict,
) -> str:
    parts = [f"Recipe: {title}"]
    if description:
        parts.append(f"Description: {description}")
    if ingredients:
        parts.append("Ingredients: " + ", ".join(ingredients))
    if instructions:
        parts.append("Instructions: " + " ".join(instructions))
    if tags:
        parts.append("Tags: " + ", ".join(tags))
    if stats:
        stats_str = f"Prep time: {stats.get('prep_time', '')}, Cook time: {stats.get('cook_time', '')}, Total time: {stats.get('total_time', '')}, Servings: {stats.get('servings', '')}"
        parts.append(f"Stats: {stats_str}")
    return "\n".join(parts)


# Process recipes from raw JSON file
def main():
    if not os.path.exists(RECIPES_PATH):
        raise FileNotFoundError(f"Raw recipe file not found: {RECIPES_PATH}")

    # Load recipes
    recipes = load_json(RECIPES_PATH)

    processed = []
    for recipe in recipes:
        try:
            _id = generate_id(recipe["brand"], recipe["title"])
            content = build_content(
                recipe["title"],
                recipe.get("description", ""),
                recipe.get("ingredients", []),
                recipe.get("instructions", []),
                recipe.get("tags", []),
                recipe.get("stats", {}),
            )

            doc = IndexedDocument(
                id=_id,
                type="recipe",
                title=recipe["title"],
                brand=recipe["brand"],
                content=content,
                image=recipe["images"][0] if recipe.get("images") else None,
                created_at=recipe.get("created_at"),
                sourcepage=recipe["url"],
                embedding=None,
                recipe_tags=recipe.get("tags", []),
                product_category=None,
                pruduct_label=None,
                product_line=None,
                article_theme=None,
                published_at=None,
            )
            processed.append(doc.model_dump())
        except Exception as e:
            print(f"Failed to process recipe: {recipe.get('title')} — {e}")

    save_json(processed, PROCESSED_RECIPES_PATH)

    print(f"Processed {len(processed)} recipes → {PROCESSED_RECIPES_PATH}")


if __name__ == "__main__":
    main()
