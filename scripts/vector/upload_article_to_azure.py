from scripts.vector.indexed_document import IndexedDocument
from common.constants import PROCESSED_ARTICLES_PATH
from common.azure_clients import search_client, generate_embeddings
from common.utils import load_json


# Load the articles data from JSON file
processed_articles = load_json(PROCESSED_ARTICLES_PATH)

# Prepare the documents with embeddings
documents = []
for article in processed_articles:
    try:
        article_content = article.get("content", "")
        embedding = generate_embeddings([article_content])[0]

        document = IndexedDocument(
            id=article["id"],
            type=article["type"],
            title=article["title"],
            brand=None,
            content=article_content,
            image=article.get("image", None),
            created_at=article.get("created_at", None),
            sourcepage=article.get("sourcepage", None),
            embedding=embedding,
            recipe_tags=[],
            product_category=None,
            product_label=None,
            product_line=None,
            article_theme=article.get("article_theme", None),
            published_at=article.get("published_at", None),
        )
        documents.append(document)
        # print(f"Processed: {article['title']}")
    except Exception as e:
        print(f"Error processing article {article['title']}: {e}")

# Upload documents with embeddings to Azure Cognitive Search
if documents:
    try:
        search_client.upload_documents(documents=documents)
        print(
            f"Successfully uploaded {len(documents)} documents to Azure Cognitive Search!"
        )
    except Exception as e:
        print(f"Error uploading documents to Azure Search: {e}")
