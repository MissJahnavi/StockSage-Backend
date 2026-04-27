from fastapi import APIRouter
from app.schemas import QueryRequest, InsightResponse
from app.agents.financial_agent import run_analysis
from loguru import logger
import re

router = APIRouter(prefix="/query", tags=["Query"])

# Words that look like tickers (short ALL-CAPS) but are not
_SKIP_WORDS = {
    # Common English words that appear in queries
    "I", "A", "AN", "AS", "AT", "BE", "BY", "DO", "GO", "IF", "IN", "IS",
    "IT", "ME", "MY", "NO", "OF", "OK", "ON", "OR", "SO", "TO", "UP", "US",
    "WE", "AM", "HE", "HI",
    # Finance verbs / nouns that appear uppercased
    "BUY", "SELL", "HOLD", "SHORT", "LONG", "CALL", "PUT", "ETF", "IPO",
    "EPS", "PE", "ROE", "FCF", "YOY", "QOQ", "ATH", "ATL", "SMA", "EMA",
    "RSI", "MACD", "ADX", "GDP", "CPI", "FED", "SEC", "NYSE", "NASDAQ",
    # Common query words
    "THE", "AND", "FOR", "ARE", "WAS", "HAS", "HAD", "NOT", "BUT", "ALL",
    "CAN", "MAY", "NOW", "HOW", "WHY", "WHO", "GET", "SET", "NEW", "OLD",
    "TOP", "LOW", "HIGH", "OUT", "OFF", "ITS", "THIS", "THAT", "WITH",
    "WILL", "WHAT", "GIVE", "SHOW", "TELL", "LOOK", "FIND", "HELP",
    # Query action words
    "ANALYZE", "ANALYSIS", "STOCK", "SHARE", "PRICE", "MARKET", "TRADE",
    "INVEST", "OUTLOOK", "FUTURE", "GOOD", "BAD", "BEST", "WORTH", "ABOUT",
}

# Common company name → ticker mapping so "Analyze NVIDIA stock" works
_NAME_TO_TICKER = {
    "NVIDIA": "NVDA", "APPLE": "AAPL", "MICROSOFT": "MSFT", "GOOGLE": "GOOGL",
    "ALPHABET": "GOOGL", "AMAZON": "AMZN", "TESLA": "TSLA", "META": "META",
    "FACEBOOK": "META", "NETFLIX": "NFLX", "AMD": "AMD", "INTEL": "INTC",
    "QUALCOMM": "QCOM", "BROADCOM": "AVGO", "ORACLE": "ORCL", "SAP": "SAP",
    "IBM": "IBM", "SALESFORCE": "CRM", "ADOBE": "ADBE", "PAYPAL": "PYPL",
    "UBER": "UBER", "LYFT": "LYFT", "AIRBNB": "ABNB", "SPOTIFY": "SPOT",
    "TWITTER": "X", "SNAP": "SNAP", "PINTEREST": "PINS", "ZOOM": "ZM",
    "SHOPIFY": "SHOP", "PALANTIR": "PLTR", "COINBASE": "COIN",
    "JPMORGAN": "JPM", "GOLDMAN": "GS", "MORGAN": "MS", "BOFA": "BAC",
    "VISA": "V", "MASTERCARD": "MA", "AMEX": "AXP",
    "JOHNSON": "JNJ", "PFIZER": "PFE", "MODERNA": "MRNA",
    "WALMART": "WMT", "TARGET": "TGT", "COSTCO": "COST",
    "EXXON": "XOM", "CHEVRON": "CVX",
    "BERKSHIRE": "BRK", "WARREN": "BRK",
    "BOEING": "BA", "FORD": "F", "GM": "GM", "FERRARI": "RACE",
}


def _extract_ticker(query: str) -> str:
    """
    Extract a stock ticker from a natural language query.

    Priority order:
      1. Explicit $TICKER format  e.g. "$AAPL"
      2. Company name → known ticker map  e.g. "NVIDIA" → "NVDA"
      3. Short ALL-CAPS word not in skip list  e.g. "TSLA"
      4. Default to "AAPL"
    """
    upper = query.upper()
    words = re.findall(r"[A-Z]+", upper)  # all letter-only tokens

    # 1. $TICKER pattern (most explicit signal)
    dollar = re.search(r"\$([A-Z]{1,5})\b", upper)
    if dollar:
        return dollar.group(1)

    # 2. Known company name → canonical ticker
    for word in words:
        if word in _NAME_TO_TICKER:
            return _NAME_TO_TICKER[word]

    # 3. First short ALL-CAPS word that looks like a ticker
    for word in words:
        if 1 <= len(word) <= 5 and word not in _SKIP_WORDS:
            return word

    return "AAPL"


@router.post("/", response_model=InsightResponse)
def query(req: QueryRequest):
    ticker = req.ticker if req.ticker and req.ticker.strip() else _extract_ticker(req.query)
    ticker = ticker.upper().strip()
    logger.info(f"Query received: '{req.query}' | Ticker: {ticker}")
    return run_analysis(req.query, ticker, req.period)
