import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import google.generativeai as genai
from app_database import get_session, init_db
from fastapi import Depends, FastAPI
from sqlmodel import Session

# Configure Gemini SDK
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: Initialize the database and pgvector extension
    init_db()
    yield
    # Shutdown logic goes here if needed

app = FastAPI(
    title="AlbumBot API",
    description="A RAG-powered semantic discovery assistant for music albums.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the AlbumBot API"}

@app.post("/search")
def search_albums(
    query: str, session: Session = Depends(get_session)
) -> dict[str, object]:
    # Placeholder for Phase 3: Vectorization & Storage
    # 1. Vectorize the text 'query' using an embedding model
    # 2. Query PostgreSQL pgvector via SQLModel using cosine distance (<=>)
    return {"query": query, "matches": ["Album A", "Album B", "Album C"]}

@app.post("/chat")
def chat_recommendation(
    query: str, session: Session = Depends(get_session)
) -> dict[str, str]:
    # Placeholder for Phase 4: RAG Implementation
    # 1. Call internal album search logic to get matches based on the query
    # 2. Construct System Prompt with query + matches
    # 3. Call Gemini API to generate the conversational response
    return {
        "query": query,
        "recommendation": (
            "Based on your search, you should listen to Album A because..."
        ),
    }
