from typing import Dict, List, Optional
from backend.services.vector_rag_service import VectorRAGService
from backend.services.base_rag_service import BaseRAGService
from backend.services.graph_query import get_product_by_name, get_products_by_brand


class HybridRAGService(BaseRAGService):
    def __init__(self):
        self.vector_rag = VectorRAGService()

    def answer_question(self, question: str) -> Dict:
        """
        Combines vector-based and graph-based context for a better answer.
        1. Retrieve vector documents.
        2. Extract brand from top documents.
        3. Query Neo4j for related graph context.
        4. Merge both into a unified context for the LLM.
        """
        # Vector search to get relevant documents
        vector_docs = self.vector_rag.search_documents(question)

        # build vector context and sources
        vector_context = self.vector_rag.build_context(vector_docs)
        sources = self.vector_rag.prepare_sources(vector_docs)

        # Extract brand from vector documents
        brand = self.extract_brand_from_docs(vector_docs)
        name = self.extract_top_name_from_docs(vector_docs)

        if brand:
            graph_products = get_products_by_brand(brand)
        elif name:
            graph_product = get_product_by_name(name)
            graph_products = [graph_product] if graph_product else []
        else:
            graph_products = []

        # Build graph context from graph products
        graph_context = self.build_graph_context(graph_products)

        # Merge vector and graph contexts
        context = self.merge_contexts(vector_context, graph_context)

        answer = self.get_answer(question, context)

        return {"answer": answer, "sources": sources}

    def extract_brand_from_docs(self, docs: List[dict]) -> Optional[str]:
        """Extracts the most common non-empty brand from top documents."""
        brands = [doc.get("brand") for doc in docs if doc.get("brand")]
        return max(set(brands), key=brands.count) if brands else None

    def extract_top_name_from_docs(self, docs: List[dict]) -> Optional[str]:
        """Extracts the most common non-empty name from top documents."""
        names = [doc.get("name") for doc in docs if doc.get("name")]
        return max(set(names), key=names.count) if names else None

    def build_graph_context(self, graph_products: List[dict]) -> str:
        """Builds a context string from graph-based knowledge."""
        if not graph_products:
            return ""

        parts = []
        for p in graph_products:
            lines = [
                f"Product: {p.get('name', '')}",
                f"Label: {p.get('label', '')}",
                f"Size: {p.get('product_size', '')}",
                f"Product Line: {p.get('product_line', '')}",
                f"Description: {p.get('description', '')}",
                f"URL: {p.get('url', '')}",
            ]
            parts.append("\n".join(lines).strip())

        return "\n\n".join(parts).strip()

    def merge_contexts(self, vector_context: str, graph_context: str) -> str:
        """Merges vector and graph contexts into a single string."""
        if not graph_context:
            return vector_context
        if not vector_context:
            return graph_context
        return f"{vector_context}\n\n[Graph Knowledge from Neo4j]\n{graph_context}"
