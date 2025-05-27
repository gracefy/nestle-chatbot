from typing import List
from common.azure_clients import search_client, get_chat_completion
from backend.models.response_models import Source


class RAGService:
    def __init__(self, top_k: int = 5):
        self.top_k = top_k  # Number of documents to retrieve

    def answer_question(self, question: str) -> dict:
        """
        Main entry point for answering a user question using RAG.
        1. Retrieve relevant documents.
        2. Build the context string with reference numbers.
        3. Generate an answer using the LLM.
        4. Prepare the sources for the frontend.
        """
        docs = self.search_documents(question)
        context = self.build_context(docs)
        answer = self.get_answer(question, context)
        sources = self.prepare_sources(docs)

        return {
            "answer": answer,
            "sources": sources,
        }

    def get_answer(self, question: str, context: str) -> str:
        """
        Calls the LLM to generate an answer, using the provided context.
        The system prompt instructs the model to only use the context and reference numbers.
        """
        system_message = (
            "You are a helpful assistant. Use only the information provided in the context. "
            "Use the reference numbers like [1], [2], exactly as shown in the context. "
        )

        user_message = f"{question}\n\nContext:\n{context}"

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        response = get_chat_completion(messages)

        return response

    def search_documents(self, question: str) -> List[dict]:
        """
        Uses the search client to retrieve top_k relevant documents for the question.
        """
        results = search_client.search(search_text=question, top=self.top_k)
        return [doc for doc in results]

    def build_context(self, docs: List[dict]) -> str:
        """
        Builds the context string for the LLM, numbering each document as [1], [2], etc.
        """
        return f"\n\n".join(
            f"[{i+1}] {doc['content']}"
            for i, doc in enumerate(docs)
            if doc.get("content")
        )

    def prepare_sources(self, docs: List[dict]) -> List[dict]:
        """
        Prepares the source metadata for the frontend, including title, url, image, and content.
        """
        return [
            {
                "title": doc["title"],
                "url": doc["sourcepage"],
                "image": doc["image"],
                "content": doc["content"],
            }
            for doc in docs
        ]
