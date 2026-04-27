from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import settings
from app.services.sentiment import score_text
from app.data.fallback_data import FALLBACK_NEWS


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=2, max=8),
    retry=retry_if_exception_type(Exception),
    reraise=False,
)
def _fetch_from_newsapi(ticker: str) -> list[dict]:
    from newsapi import NewsApiClient
    if not settings.NEWSAPI_KEY:
        raise ValueError("NEWSAPI_KEY not configured")

    client = NewsApiClient(api_key=settings.NEWSAPI_KEY)
    result = client.get_everything(q=ticker, language="en", sort_by="publishedAt", page_size=10)
    articles = result.get("articles", [])

    output = []
    for article in articles[:10]:
        text = f"{article.get('title', '')} {article.get('description', '')}"
        sentiment = score_text(text)
        output.append({
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "source": article.get("source", {}).get("name", ""),
            "published_at": str(article.get("publishedAt", ""))[:10],
            **sentiment,
        })
    return output


def get_news(ticker: str) -> list[dict]:
    """
    Fetch news with sentiment. Falls back to hardcoded news if NewsAPI fails.
    Always returns a safe list — never raises.
    """
    ticker = ticker.upper().strip()
    try:
        articles = _fetch_from_newsapi(ticker)
        logger.info(f"Fetched {len(articles)} live news articles for {ticker}")
        return articles
    except Exception as e:
        logger.warning(f"NewsAPI failed for {ticker}: {e}. Using fallback news.")
        if ticker in FALLBACK_NEWS:
            return FALLBACK_NEWS[ticker]
        return [
            {
                "title": f"No live news available for {ticker}",
                "url": "",
                "source": "Fallback",
                "published_at": "2025-04-23",
                "sentiment_label": "neutral",
                "compound_score": 0.0,
            }
        ]
