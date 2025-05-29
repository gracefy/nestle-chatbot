# Nestlé Canada AI Chatbot

An AI-powered chatbot using RAG (Retrieval-Augmented Generation), deployed on Azure, combining semantic and graph-based retrieval.

---

## Demo

🔗 Azure Deployment: [Live Demo](https://nestle-chatbot-1056934369723.us-central1.run.app/)  
🔗 GitHub Repo: [github.com/gracefy/nestle-chatbot](https://github.com/gracefy/nestle-chatbot)

---

## Tech Stack

| Layer      | Tech                       |
| ---------- | -------------------------- |
| Frontend   | React + Tailwind           |
| Backend    | FastAPI (Python)           |
| Vector DB  | Azure Cognitive Search     |
| Graph DB   | Neo4j Aura                 |
| LLM        | Azure OpenAI (GPT-4-turbo) |
| Deployment | Azure App Service (Docker) |

---

## Features

- **Web Crawling**: Structured scraping of Nestlé website content (products, recipes, articles)
- **Vector-based RAG**: Uses Azure OpenAI embeddings + Azure Cognitive Search for semantic retrieval
- **Graph-based RAG (GraphRAG)**: Models brand-product relationships in Neo4j for structured context
- **Hybrid RAG**: Combines semantic and structured knowledge for deeper context understanding
- **LLM via Azure OpenAI**: Deployed `gpt-35-turbo` for chat completion generation
- **Chat API**: Single `/chat` endpoint using HybridRAG; optional `/vector-chat` also available
- **Azure Deployment**: Fully deployable on Azure App Service with environment configuration

---

## Setup Locally

To run the chatbot locally, follow these steps:

### Prerequisites

- Python 3.10.13
- Azure account (for Cognitive Search and OpenAI)
- Neo4j Aura account (for graph database)

### Steps

```bash
git clone https://github.com/yourname/nestle-chatbot
cd nestle-chatbot
```

# 1. Backend Setup

```bash
pyenv install 3.10.13
pyenv local 3.10.13
```

**macOS/Linux**:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## **创建 `.env` 文件**:

## Environment Configuration

Before setting up `.env` files, you must configure the following services:

- Azure OpenAI (for embeddings and chat)
- Azure Cognitive Search (for vector database)
- Neo4j Aura (for graph database)

📄 Please refer to [`SETUP_ENV.md`](SETUP_ENV.md) for detailed instructions on:

- Setting up embedding models and indexes
- Initializing vector and graph databases
- Required environment variable structure
- Uploading preprocessed data with Python scripts

---

## Frontend Environment

The frontend reads `VITE_API_BASE_URL` from `.env.local` or `.env.production`.

👉 Refer to [`frontend/.env.example`](frontend/.env.example) for variable format.

```bash
cp .env.example .env
```

And fill in the required environment variables for Azure Cognitive Search, Neo4j, and OpenAI.

# 2. Frontend Setup

```bash
cd frontend
npm install
```

# 3. Start the Application

**Frontend**:

```bash
cd frontend
npm run dev
```

**Backend**:

```bash
cd backend
uvicorn main:app --reload
```

### Access the App

## Default Ports

| Service     | Port |
| ----------- | ---- |
| Frontend    | 5173 |
| Backend API | 8000 |

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000](http://localhost:8000)

### Access the API Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Web Crawling Details

For details on how the web scraper works and how to run it locally, please refer to:

👉 [`scraper/README_scraper.md`](scraper/README_scraper.md)
