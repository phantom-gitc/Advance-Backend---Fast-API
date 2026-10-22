from fastapi import FastAPI
from app.routes.query import router as query_router

app = FastAPI(
    title="RAG API with Qdrant",
    description="RAG API for querying documents using Qdrant",
    version="1.0.0"
)

app.include_router(query_router)

