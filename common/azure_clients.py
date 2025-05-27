import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


# Load environment variables
load_dotenv()

# Init Azure Search client
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name="main_index",
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY")),
)

# Init Azure OpenAI client
openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


# Function to generate embeddings using Azure OpenAI
def generate_embeddings(texts):
    try:
        response = openai_client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"), input=texts
        )
        return [r.embedding for r in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []
