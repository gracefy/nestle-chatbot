from typing import Dict
from abc import ABC, abstractmethod
from common.azure_clients import get_chat_completion


class BaseRAGService(ABC):
    """
    Abstract base class for all RAG service types.
    Defines the core interface and shared logic such as get_answer.
    """

    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    @abstractmethod
    def answer_question(self, question: str) -> Dict:
        pass

    def get_answer(self, question: str, context: str) -> str:
        """
        Calls the LLM to generate an answer, using the provided context.
        The system prompt instructs the model to only use the context and reference numbers.
        """
        system_message = (
            "You are Nestlé's official AI assistant. Only answer questions related to Nestlé. "
            "Answer customer questions using only the provided content from semantic and graph-based retrieval. "
            "Cite reference numbers like [1], [2] **only if** those numbers correspond to the provided sources. "
            "Do not invent references or refer to content not included. "
        )

        user_message = f"{question}\n\nContext:\n{context}"

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        answer = get_chat_completion(messages)

        return answer.strip()
