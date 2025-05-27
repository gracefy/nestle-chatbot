import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

import traceback

# Load environment variables
load_dotenv()

# Load Azure OpenAI and Azure Search configuration from environment variables
EMBEDDING_ENDPOINT = os.environ.get("AZURE_OPENAI_EMBEDDING_ENDPOINT")
EMBEDDING_KEY = os.environ.get("AZURE_OPENAI_EMBEDDING_API_KEY")
EMBEDDING_MODEL = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL")
EMBEDDING_API_VERSION = os.environ.get("AZURE_OPENAI_EMBEDDING_API_VERSION")


CHAT_ENDPOINT = os.environ.get("AZURE_OPENAI_CHAT_ENDPOINT")
CHAT_KEY = os.environ.get("AZURE_OPENAI_CHAT_API_KEY")
CHAT_MODEL = os.environ.get("AZURE_OPENAI_CHAT_MODEL")
CHAT_API_VERSION = os.environ.get("AZURE_OPENAI_CHAT_API_VERSION")
CHAT_TEMPERATURE = float(os.environ.get("AZURE_OPENAI_CHAT_TEMPERATURE", 0.3))
CHAT_MAX_TOKENS = int(os.environ.get("AZURE_OPENAI_CHAT_MAX_TOKENS", 500))

SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.environ.get("AZURE_SEARCH_API_KEY")
SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")


# Init Azure AI Search client
search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=SEARCH_INDEX,
    credential=AzureKeyCredential(SEARCH_KEY),
)

# Init Azure OpenAI client for embeddings
openai_embedding_client = AzureOpenAI(
    azure_endpoint=EMBEDDING_ENDPOINT,
    api_key=EMBEDDING_KEY,
    api_version=EMBEDDING_API_VERSION,
)

# Init Azure OpenAI client for chat completions
openai_chat_client = AzureOpenAI(
    azure_endpoint=CHAT_ENDPOINT,
    api_key=CHAT_KEY,
    api_version=CHAT_API_VERSION,
)


# Generate embeddings for a list of texts using Azure OpenAI
def generate_embeddings(texts):
    try:
        response = openai_embedding_client.embeddings.create(
            model=EMBEDDING_MODEL, input=texts
        )
        return [r.embedding for r in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []


# Get chat completion from Azure OpenAI given a list of messages
def get_chat_completion(messages, top_p=1.0):
    try:
        response = openai_chat_client.chat.completions.create(
            messages=messages,
            temperature=CHAT_TEMPERATURE,
            max_tokens=CHAT_MAX_TOKENS,
            top_p=top_p,
            model=CHAT_MODEL,
        )

        # Return the generated message content
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n\nUsing model:", CHAT_MODEL)

        print(f"Error getting chat completion: {e}")
        traceback.print_exc()
        return ""
