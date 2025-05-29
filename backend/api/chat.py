from fastapi import APIRouter, HTTPException, status, Request
from backend.models.request_models import ChatRequest
from backend.models.response_models import ChatResponse
from backend.services.vector_rag_service import VectorRAGService
from backend.services.hybrid_rag_service import HybridRAGService

# Create a FastAPI router
router = APIRouter()

# Instantiate the RAG service
rag_service = VectorRAGService()
hybrid_service = HybridRAGService()


# Endpoint for hybrid RAG chat
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that receives a user question, calls the RAG service to get an answer,
    and returns the answer along with the referenced sources.
    """
    # Validate the request
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Question cannot be empty"
        )

    try:
        result = hybrid_service.answer_question(question)
        # print(f"RAG result: {result}")

        answer = result.get("answer", "").strip()
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No answer generated for the given question.",
            )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG failed: {str(e)}",
        )


# Endpoint for vector-based chat
# Can be used for comparison with hybrid RAG service
@router.post("/vector-chat", response_model=ChatResponse)
def vector_chat_endpoint(request: ChatRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Question cannot be empty"
        )
    try:
        result = rag_service.answer_question(question)

        answer = result.get("answer", "").strip()
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No answer generated for the given question.",
            )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG failed: {str(e)}",
        )
