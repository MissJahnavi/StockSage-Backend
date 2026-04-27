from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.routers import stock, news, rag, query
import os

setup_logging()
os.makedirs("logs", exist_ok=True)
os.makedirs(settings.FAISS_INDEX_PATH, exist_ok=True)

app = FastAPI(
    title="AI Financial Agent",
    description="AI-powered financial research agent using Google Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock.router)
app.include_router(news.router)
app.include_router(rag.router)
app.include_router(query.router)


@app.get("/health", tags=["System"])
def health():
    return {
        "status": "ok",
        "model": settings.GEMINI_MODEL,
        "google_api_key_set": bool(settings.GOOGLE_API_KEY),
        "newsapi_key_set": bool(settings.NEWSAPI_KEY),
    }
