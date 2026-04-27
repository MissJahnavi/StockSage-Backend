from fastapi import APIRouter
from app.tools.news_tool import get_news

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/{ticker}")
def get_ticker_news(ticker: str):
    articles = get_news(ticker.upper())
    return {"ticker": ticker.upper(), "articles": articles, "count": len(articles)}
