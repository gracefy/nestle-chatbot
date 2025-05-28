import os
from typing import List
from common.constants import RECIPES_PATH, PROCESSED_RECIPES_PATH
from scripts.vector.indexed_document import IndexedDocument
from common.utils import save_json, generate_id, load_json, safe_strip


def main():
    """
    Processes raw recipe data from JSON file, extracting relevant fields
    and generating a structured IndexedDocument for each recipe.
    Saves the processed documents to a new JSON file for later use.
    """
    if not os.path.exists(RECIPES_PATH):
        raise FileNotFoundError(f"Raw recipe file not found: {RECIPES_PATH}")

    # Load recipes
    recipes = load_json(RECIPES_PATH)

    processed = []
    for recipe in recipes:
        try:
            _id = generate_id(recipe["brand"], recipe["title"])
            content = build_content(recipe)

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


def build_content(recipe: dict) -> str:
    """
    Constructs a semantically rich content string from a recipe dictionary
    for embedding in vector databases. Includes title, brand, description,
    ingredients, instructions, tags, and stats.
    """

    title = safe_strip(recipe.get("title", ""))
    brand = safe_strip(recipe.get("brand", ""))
    description = safe_strip(recipe.get("description", ""))
    ingredients = recipe.get("ingredients", [])
    instructions = recipe.get("instructions", [])
    tags: List[str] = [safe_strip(tag) for tag in recipe.get("tags", [])]
    stats = recipe.get("stats", {})

    parts = [f"Recipe: {title}"]
    if brand:
        parts.append(f"Brand: {brand}")
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


if __name__ == "__main__":
    main()
