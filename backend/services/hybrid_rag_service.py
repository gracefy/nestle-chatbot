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
        # Step 1: vector search
        vector_docs = self.vector_rag.search_documents(question)
        vector_context = self.vector_rag.build_context(vector_docs)
        sources = self.vector_rag.prepare_sources(vector_docs)

        # Step 2: extract brand or fallback name
        brand = self.extract_brand_from_docs(vector_docs)
        name = self.extract_top_name_from_docs(vector_docs)

        # Step 3: graph search
        if brand:
            graph_products = get_products_by_brand(brand)
        elif name:
            graph_product = get_product_by_name(name)
            graph_products = [graph_product] if graph_product else []
        else:
            graph_products = []

        # Step 4: skip graph if nothing found
        if graph_products:
            graph_products = self._filter_and_rerank_products(question, graph_products)
            graph_context = self.build_graph_context(graph_products)
        else:
            graph_context = ""

        # Step 5: Merge vector and graph contexts
        context = self.merge_contexts(vector_context, graph_context)

        # Step 6: Generate answer using the LLM
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

    def _filter_and_rerank_products(
        self, question: str, products: List[dict]
    ) -> List[dict]:
        """
        Filter out unrelated products and rerank based on simple keyword overlap with the question.
        This reduces noise in graph-based context and improves answer relevance.
        """
        if not products:
            return []

        question_lower = question.lower()

        def relevance_score(p: dict) -> int:
            """Simple score: count of matching keywords from question in product fields"""
            fields = " ".join(
                [
                    str(p.get("name", "")),
                    str(p.get("description", "")),
                    str(p.get("label", "")),
                ]
            ).lower()
            return sum(1 for word in question_lower.split() if word in fields)

        # Filter out products with no keyword match
        filtered = [p for p in products if relevance_score(p) > 0]

        # Rerank by descending relevance score
        return sorted(filtered, key=relevance_score, reverse=True)
