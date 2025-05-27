from scripts.vector.indexed_document import IndexedDocument
from common.constants import PROCESSED_PRODUCTS_PATH
from common.azure_clients import search_client, generate_embeddings
from common.utils import load_json


# Load the products data from JSON file
processed_products = load_json(PROCESSED_PRODUCTS_PATH)

# Prepare the documents with embeddings
documents = []
for product in processed_products:
    try:
        product_content = product.get("content", "")
        if not product_content.strip():
            # Skip products without content
            print(f"Skipping product {product['title']} due to missing content.")
            continue
        embedding = generate_embeddings([product_content])[0]

        document = IndexedDocument(
            id=product["id"],
            type=product["type"],
            title=product["title"],
            brand=product["brand"],
            content=product_content,
            image=product.get("image", None),
            created_at=product.get("created_at", None),
            sourcepage=product.get("sourcepage", None),
            embedding=embedding,
            recipe_tags=[],
            product_category=product.get("product_category", None),
            product_label=product.get("product_label", None),
            product_line=product.get("product_line", None),
            article_theme=None,
            published_at=None,
        )
        documents.append(document)
        # print(f"Processed: {product['title']}")
    except Exception as e:
        print(f"Error processing product {product['title']}: {e}")

# Upload documents with embeddings to Azure Cognitive Search
if documents:
    try:
        search_client.upload_documents(documents=documents)
        print(
            f"Successfully uploaded {len(documents)} documents to Azure Cognitive Search!"
        )
    except Exception as e:
        print(f"Error uploading documents to Azure Search: {e}")
