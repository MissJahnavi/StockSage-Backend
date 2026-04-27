import pandas as pd
from datetime import date, timedelta
from loguru import logger
import massive
from app.core.config import settings
from app.data.fallback_data import FALLBACK_STOCKS, DEFAULT_STOCK


# Period string → calendar days to look back
PERIOD_DAYS = {
    "1mo":  40,
    "3mo":  100,
    "6mo":  190,
    "1y":   370,
    "2y":   740,
    "5y":   1830,
}


def _get_client() -> massive.RESTClient:
    """Return an authenticated Massive REST client."""
    if not settings.POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY not set in .env")
    return massive.RESTClient(settings.POLYGON_API_KEY)


# ── Technical indicators ───────────────────────────────────────────────────────

def _compute_indicators(df: pd.DataFrame) -> dict:
    """Compute RSI, MACD, Bollinger Bands, ATR, SMA from OHLCV DataFrame."""
    try:
        import ta
        close = df["Close"]
        high  = df["High"]
        low   = df["Low"]

        rsi         = ta.momentum.RSIIndicator(close, window=14).rsi().iloc[-1]
        macd_obj    = ta.trend.MACD(close)
        macd        = macd_obj.macd().iloc[-1]
        macd_signal = macd_obj.macd_signal().iloc[-1]
        macd_histo  = macd_obj.macd_diff().iloc[-1]
        bb          = ta.volatility.BollingerBands(close, window=20)
        atr         = ta.volatility.AverageTrueRange(high, low, close, window=14).average_true_range().iloc[-1]
        sma_20      = close.rolling(20).mean().iloc[-1]
        sma_50      = close.rolling(50).mean().iloc[-1]

        def _s(v, d=2): return round(float(v), d) if pd.notna(v) else 0.0

        return {
            "rsi":             _s(rsi),
            "macd":            _s(macd, 4),
            "macd_signal":     _s(macd_signal, 4),
            "macd_histogram":  _s(macd_histo, 4),
            "bollinger_upper": _s(bb.bollinger_hband().iloc[-1]),
            "bollinger_lower": _s(bb.bollinger_lband().iloc[-1]),
            "bollinger_mid":   _s(bb.bollinger_mavg().iloc[-1]),
            "atr":             _s(atr, 4),
            "sma_20":          _s(sma_20),
            "sma_50":          _s(sma_50),
        }
    except Exception as e:
        logger.warning(f"Indicator computation failed: {e}")
        return {
            "rsi": 50.0, "macd": 0.0, "macd_signal": 0.0, "macd_histogram": 0.0,
            "bollinger_upper": 0.0, "bollinger_lower": 0.0, "bollinger_mid": 0.0,
            "atr": 0.0, "sma_20": 0.0, "sma_50": 0.0,
        }


# ── Massive fetch (free endpoints only) ───────────────────────────────────────

def _fetch_from_massive(ticker: str, period: str = "6mo") -> dict:
    """
    Fetch stock data using only free-tier Massive (Polygon.io) endpoints.

      get_aggs → OHLCV bars for the requested period  ✅ FREE

    Current price, change%, volume are derived from the latest bar —
    no paid snapshot endpoint needed.
    """
    client = _get_client()

    # ── Date range ────────────────────────────────────────────────────────────
    days_back = PERIOD_DAYS.get(period, 190)
    from_date = (date.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date   = date.today().strftime("%Y-%m-%d")

    # ── Fetch OHLCV bars via get_aggs (same as working test code) ────────────
    aggs      = client.get_aggs(
        ticker=ticker,
        multiplier=1,
        timespan="day",
        from_=from_date,
        to=to_date,
    )
    aggs_list = list(aggs)

    if not aggs_list:
        raise ValueError(f"Massive returned no data for '{ticker}' ({from_date} → {to_date})")

    # ── Build DataFrame ───────────────────────────────────────────────────────
    rows = [
        {
            "Date":   pd.to_datetime(a.timestamp, unit="ms"),
            "Open":   float(a.open),
            "High":   float(a.high),
            "Low":    float(a.low),
            "Close":  float(a.close),
            "Volume": float(a.volume),
        }
        for a in aggs_list
    ]
    df = pd.DataFrame(rows).set_index("Date")

    # ── Derive price stats from bars (no snapshot needed) ─────────────────────
    latest        = df.iloc[-1]
    prev          = df.iloc[-2] if len(df) >= 2 else latest
    current_price = round(float(latest["Close"]), 2)
    prev_close    = round(float(prev["Close"]), 2)
    change_pct    = round(((current_price - prev_close) / prev_close) * 100, 2) if prev_close else 0.0
    volume        = int(latest["Volume"])
    week_52_high  = round(float(df["High"].max()), 2)
    week_52_low   = round(float(df["Low"].min()), 2)

    # ── Price history for chart (last 90 bars) ────────────────────────────────
    price_history = [
        {"date": str(idx.date()), "close": round(float(row["Close"]), 2)}
        for idx, row in df.tail(90).iterrows()
    ]

    indicators = _compute_indicators(df)

    # ── Company name & market cap (free endpoint, best-effort) ───────────────
    company_name = ticker
    market_cap   = 0
    pe_ratio     = 0.0

    try:
        details      = client.get_ticker_details(ticker)
        company_name = details.name or ticker
        market_cap   = int(details.market_cap or 0)
    except Exception as e:
        logger.warning(f"Massive ticker details failed for {ticker}: {e}. Using defaults.")

    return {
        "ticker":         ticker.upper(),
        "company_name":   company_name,
        "current_price":  current_price,
        "change_percent": change_pct,
        "volume":         volume,
        "market_cap":     market_cap,
        "pe_ratio":       pe_ratio,
        "week_52_high":   week_52_high,
        "week_52_low":    week_52_low,
        "price_history":  price_history,
        **indicators,
    }


# ── Public interface ───────────────────────────────────────────────────────────

def get_stock_data(ticker: str, period: str = "6mo") -> dict:
    """
    Fetch stock data via Massive (Polygon.io) free-tier endpoints.
    Falls back to hardcoded data if Massive fails.
    Always returns a safe dict — never raises.
    """
    ticker = ticker.upper().strip()
    try:
        data = _fetch_from_massive(ticker, period)
        logger.info(f"Fetched live data from Massive for {ticker} (period={period})")
        return data
    except Exception as e:
        logger.warning(f"Massive failed for {ticker}: {e}. Using fallback data.")
        if ticker in FALLBACK_STOCKS:
            return FALLBACK_STOCKS[ticker]
        fallback = dict(DEFAULT_STOCK)
        fallback["ticker"] = ticker
        fallback["error"]  = f"No live data available. Using placeholder. ({e})"
        return fallback
