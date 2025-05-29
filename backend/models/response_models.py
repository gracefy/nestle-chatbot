from pydantic import BaseModel
from typing import List, Optional


class Source(BaseModel):
    """
    Represents a single source document referenced in the chat response.
    """

    title: str
    url: Optional[str] = None
    image: Optional[str] = None
    content: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint, including the answer and its sources.
    """

    answer: str
    sources: List[Source]


class GraphStats(BaseModel):
    """
    Statistics about the graph operations
    """

    nodes_created: int = 0
    properties_set: int = 0
    relationships_created: Optional[int] = None


class GraphAddResponse(BaseModel):
    """
    Response model for graph editing
    """

    status: str
    stats: Optional[GraphStats] = None
