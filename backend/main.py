from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api.chat import router as chat_router
from backend.api.graph_editing import router as graph_editing_router

app = FastAPI()
app.include_router(chat_router, tags=["Chat"])
app.include_router(graph_editing_router, prefix="/graph", tags=["Graph Editing"])

# Allow cross-origin requests from any origin (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")
