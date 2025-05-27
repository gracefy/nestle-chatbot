from pydantic import BaseModel
from typing import Optional, List


class IndexedDocument(BaseModel):
    # Base Fields (common to all types)
    id: str
    type: str  # 'recipe', 'article', or 'product'
    title: str
    brand: Optional[str] = None  # Optional for articles
    content: str  # General content field (depends on type)
    image: Optional[str] = None  # Optional for articles
    created_at: Optional[str] = None
    sourcepage: Optional[str] = None
    # sourcename: Optional[str] = None
    embedding: Optional[List[float]] = None  # Embedding vector for search

    # Recipe-specific fields
    recipe_tags: Optional[List[str]] = None

    # Product-specific fields
    product_category: Optional[str] = None
    product_label: Optional[str] = None
    product_line: Optional[str] = None

    # Article-specific fields
    article_theme: Optional[str] = None
    published_at: Optional[str] = None
