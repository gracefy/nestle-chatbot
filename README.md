# Nestlé Canada AI Chatbot

An AI-powered chatbot using RAG (Retrieval-Augmented Generation), deployed on Google Cloud, combining vector-based and graph-based retrieval.

---

## Demo

🔗 Google Cloud Deployment: [Live Demo](https://nestle-chatbot-1056934369723.us-central1.run.app/)  
🔗 GitHub Repo: [github.com/gracefy/nestle-chatbot](https://github.com/gracefy/nestle-chatbot)

---

## Tech Stack

| Layer       | Tech                        |
| ----------- | --------------------------- |
| Frontend    | React + Tailwind            |
| Backend     | FastAPI (Python)            |
| Web Crawler | Playwright + BeautifulSoup  |
| Vector DB   | Azure AI Search             |
| Graph DB    | Neo4j Aura                  |
| LLM         | Azure OpenAI (GPT-35-turbo) |
| Deployment  | Google Cloud Run (Docker)   |

---

## Features

- **Web Crawling**: Structured scraping of Nestlé website content (products, recipes, articles)
- **Vector-based RAG**: Uses Azure OpenAI embeddings + Azure AI Search for semantic retrieval
- **Graph-based RAG (GraphRAG)**: Models brand-product relationships in Neo4j for structured context
- **Hybrid RAG**: Combines semantic and structured knowledge for deeper context understanding
- **LLM via Azure OpenAI**: Deployed `gpt-35-turbo` for chat completion generation
- **Chat API**: Single `/chat` endpoint using HybridRAG; optional `/vector-chat` also available
- **Deployment**: Fully deployable on Google Cloud Run using Docker with environment configuration

## Additional Features

- **Graph Editing API**: Add/update brand & product nodes and relationships via `/graph` endpoints.  
  👉 See [Graph Editing Usage Guide](./README_graph_edit.md) for API details and testing instructions.
- **Interactive API Docs**: Explore all endpoints via [Swagger UI `/docs`](https://nestle-chatbot-1056934369723.us-central1.run.app/docs)
- **UI Enhancements**: Optional `expanded` mode for a larger chat window to improve user experience.

---

## Setup Locally

To run the chatbot locally, follow these steps:

### Prerequisites

- Python 3.10.13
- Azure account (for Cognitive Search and OpenAI)
- Neo4j Aura account (for graph database)

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/nestle-chatbot
cd nestle-chatbot
```

### 2. Backend Setup

**Python Environment**:

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

### 3. Environment Configuration

Before creating .env files, you must configure:

- Azure OpenAI (for embeddings and chat)
- Azure Cognitive Search (for vector database)
- Neo4j Aura (for graph database)

📄 See [`README_setup_env.md`](README_setup_env.md) for detailed instructions.

Also see: [`frontend/.env.example`](frontend/.env.example) for frontend variables.

To set up environment variables:

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

### 5. Start the Application

**Frontend**:

```bash
cd frontend
npm run dev
```

**Backend**:

Please make sure you are in the **project root directory**

```bash
uvicorn backend.main:app --reload
```

### 6.Access the App

**Default Ports**

| Service     | Port |
| ----------- | ---- |
| Frontend    | 5173 |
| Backend API | 8000 |

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Web Crawling Details

For details on how the web scraper works and how to run it locally, please refer to:

👉 [`scraper/README_scraper.md`](scraper/README_scraper.md)

## Potential Enhancements

- **Expand crawling coverage**: Include additional content types like FAQs and About pages to enrich semantic context.
- **Smarter reranking**: Apply keyword-based or model-assisted reranking to vector results for more accurate answer grounding.
- **Extend graph schema**: Add entities such as ingredients, categories, or article references to enhance structured reasoning.
- **Improve prompt & model tuning**: Use GPT-4 and refine system prompts to improve accuracy and grounding of answers.
