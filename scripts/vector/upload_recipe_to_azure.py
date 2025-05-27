from scripts.vector.indexed_document import IndexedDocument
from common.constants import PROCESSED_RECIPES_PATH
from common.azure_clients import search_client, generate_embeddings
from common.utils import load_json

# Load the recipes data from JSON file
processed_recipes = load_json(PROCESSED_RECIPES_PATH)

# Prepare the documents with embeddings
documents = []
for recipe in processed_recipes:
    try:
        recipe_content = recipe.get("content", "")
        embedding = generate_embeddings([recipe_content])[0]

        document = IndexedDocument(
            id=recipe["id"],
            type=recipe["type"],
            title=recipe["title"],
            brand=recipe["brand"],
            content=recipe_content,
            image=recipe.get("image", None),
            created_at=recipe.get("created_at", None),
            sourcepage=recipe.get("sourcepage", None),
            embedding=embedding,
            recipe_tags=recipe.get("recipe_tags", []),
            product_category=None,
            product_label=None,
            product_line=None,
            article_theme=None,
            published_at=None,
        )
        documents.append(document)
        # print(f"Processed: {recipe['title']}")
    except Exception as e:
        print(f"Error processing recipe {recipe['title']}: {e}")

# Upload documents with embeddings to Azure Cognitive Search
if documents:
    try:
        search_client.upload_documents(documents=documents)
        print(
            f"Successfully uploaded {len(documents)} documents to Azure Cognitive Search!"
        )
    except Exception as e:
        print(f"Error uploading documents to Azure Search: {e}")
