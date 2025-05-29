# Environment Setup Guide

This document explains how to prepare your Azure and Neo4j services, set environment variables, and upload data before running the chatbot.

---

## 1. Set Up Vector Database (Azure AI Search)

### 🔧 Required:

- Azure OpenAI embedding model: `text-embedding-ada-002`  
  Version: `2023-05-15`

- Azure AI Search (formerly Azure Cognitive Search):

  - Create a Search service
  - Create a Search Index
    You can find a sample schema at:

    👉 [`scripts/vector/nestle_index_schema.json`](scripts/vector/nestle_index_schema.json)

### Set in `.env`:

```env
AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_API_KEY=<your-search-key>
AZURE_SEARCH_INDEX=<your-index-name>

AZURE_OPENAI_EMBEDDING_ENDPOINT=https://<your-aoai-endpoint>.openai.azure.com/
AZURE_OPENAI_EMBEDDING_API_KEY==<your-openai-key>
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
AZURE_OPENAI_EMBEDDING_API_VERSION=2023-05-15
```

### Upload data:

```bash
python -m scripts.vector.upload_article_to_azure
python -m scripts.vector.upload_product_to_azure
python -m scripts.vector.upload_recipe_to_azure
```

---

## 2. Set Up Graph Database (Neo4j)

### 🔧 Required:

- Register a [Neo4j Aura](https://neo4j.com/cloud/aura/) instance
- Set a password for your database (no schema setup needed — handled by script)

### Set in `.env`:

```env
NEO4J_URI=neo4j+s://<your-neo4j-uri>
NEO4J_USERNAME=<your-neo4j-username>
NEO4J_PASSWORD=<your-password>
AURA_INSTANCEID=<your-aura-instance-id>
AURA_INSTANCENAME=<your-aura-instance-name>
```

### 🚀 Upload graph data:

```bash
python -m scripts.vector.upload_graph_data
```

---

## 3. Set Up Azure OpenAI for Chat

### 🔧 Required:

- Deploy Azure OpenAI chat model in Azure Portal
- Use a chat model like `gpt-35-turbo` or `gpt-4`

### Set in `.env`:

```env
AZURE_OPENAI_CHAT_ENDPOINT=https://<your-aoai-endpoint>.openai.azure.com/
AZURE_OPENAI_CHAT_API_KEY=<your-openai-key>
AZURE_OPENAI_CHAT_MODEL=<your-chat-model>(e.g., gpt-35-turbo)
AZURE_OPENAI_CHAT_API_VERSION=<your-api-version>(e.g., 2024-12-01-preview)
AZURE_OPENAI_CHAT_TEMPERATURE=0.3
AZURE_OPENAI_CHAT_MAX_TOKENS=1000
```

---

## Summary

Make sure the following scripts have been run to populate both vector and graph databases:

```bash
# Vector database
python -m scripts.vector.upload_article_to_azure
python -m scripts.vector.upload_product_to_azure
python -m scripts.vector.upload_recipe_to_azure

# Graph database
python -m scripts.vector.upload_graph_data
```

Then you're ready to launch the chatbot locally or deploy to production
