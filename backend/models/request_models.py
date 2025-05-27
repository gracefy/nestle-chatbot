from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    Contains the user's question to be answered by the RAG service.
    """

    question: str
