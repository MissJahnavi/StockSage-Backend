import pandas as pd
from datetime import date, timedelta
from loguru import logger
from massive import RESTClient  # pip install massive  (Polygon.io rebranded SDK)
from app.core.config import settings
from app.data.fallback_data import FALLBACK_STOCKS, DEFAULT_STOCK

# ── Massive (Polygon.io) free-tier endpoints used ─────────────────────────────
#
#  get_snapshot_all / get_snapshot_ticker  → current price, change%, volume
#  list_aggs                               → OHLCV bars (up to 100 days)
#  get_ticker_details                      → company name, market cap, etc.
#
#  Get a free key at: https://massive.com  (same key works on polygon.io too)
# ─────────────────────────────────────────────────────────────────────────────


def _get_client() -> RESTClient:
    """Return an authenticated Massive/Polygon REST client."""
    if not settings.POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY not set in .env")
    return RESTClient(api_key=settings.POLYGON_API_KEY)


# ── Technical indicators (unchanged — works on any OHLCV DataFrame) ───────────

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


# ── Massive / Polygon.io fetch ─────────────────────────────────────────────────

def _fetch_from_massive(ticker: str) -> dict:
    """
    Fetch live stock data via the Massive (Polygon.io) Python client.

      Call 1 — get_snapshot_ticker  : current price, change %, volume, OHLC
      Call 2 — list_aggs            : last ~100 days of OHLCV bars
      Call 3 — get_ticker_details   : company name, market cap, description

    Returns a dict with the same shape as the previous Alpha Vantage version so
    nothing downstream (agent, schemas, routers, frontend) needs to change.
    """
    client = _get_client()

    # ── Call 1: Current snapshot ──────────────────────────────────────────────
    snapshot = client.get_snapshot_ticker("stocks", ticker)
    day       = snapshot.day        # today's OHLCV
    prev_day  = snapshot.prev_day   # previous day's close

    current_price = float(snapshot.last_trade.price if snapshot.last_trade else day.close or 0)
    day_open      = float(day.open  or current_price)
    day_high      = float(day.high  or current_price)
    day_low       = float(day.low   or current_price)
    volume        = int(day.volume  or 0)
    prev_close    = float(prev_day.close if prev_day else current_price)
    change_pct    = float(snapshot.todays_change_perc or 0)

    # ── Call 2: ~100 trading-day aggregate bars ───────────────────────────────
    from_date = (date.today() - timedelta(days=140)).isoformat()  # buffer for weekends/holidays
    to_date   = date.today().isoformat()

    aggs = list(client.list_aggs(
        ticker=ticker,
        multiplier=1,
        timespan="day",
        from_=from_date,
        to=to_date,
        adjusted=True,
        sort="asc",
        limit=120,
    ))

    if not aggs:
        raise ValueError(f"Massive returned no aggregate bars for '{ticker}'")

    rows = [
        {
            "Date":   pd.to_datetime(a.timestamp, unit="ms"),
            "Open":   float(a.open),
            "High":   float(a.high),
            "Low":    float(a.low),
            "Close":  float(a.close),
            "Volume": float(a.volume),
        }
        for a in aggs
    ]
    df = pd.DataFrame(rows).set_index("Date")

    # Last 90 points for the price-history chart
    price_history = [
        {"date": str(idx.date()), "close": round(float(row["Close"]), 2)}
        for idx, row in df.tail(90).iterrows()
    ]

    indicators = _compute_indicators(df)

    # ── Call 3: Ticker details (company info) ─────────────────────────────────
    company_name = ticker
    market_cap   = 0
    pe_ratio     = 0.0
    week_52_high = day_high
    week_52_low  = day_low

    try:
        details      = client.get_ticker_details(ticker)
        company_name = details.name or ticker
        market_cap   = int(details.market_cap or 0)
        # P/E ratio is not in ticker details; keep 0 (available via financials endpoint on paid plans)
        week_52_high = float(snapshot.last_quote.high if hasattr(snapshot, "last_quote") and snapshot.last_quote else df["High"].max())
        week_52_low  = float(snapshot.last_quote.low  if hasattr(snapshot, "last_quote") and snapshot.last_quote else df["Low"].min())
    except Exception as e:
        logger.warning(f"Massive ticker details failed for {ticker}: {e}. Using defaults.")
        week_52_high = float(df["High"].max())
        week_52_low  = float(df["Low"].min())

    return {
        "ticker":         ticker.upper(),
        "company_name":   company_name,
        "current_price":  round(current_price, 2),
        "change_percent": round(change_pct, 2),
        "volume":         volume,
        "market_cap":     market_cap,
        "pe_ratio":       round(pe_ratio, 2),
        "week_52_high":   round(week_52_high, 2),
        "week_52_low":    round(week_52_low, 2),
        "price_history":  price_history,
        **indicators,
    }


# ── Public interface (unchanged signature) ────────────────────────────────────

def get_stock_data(ticker: str, period: str = "6mo") -> dict:
    """
    Fetch stock data via the Massive (Polygon.io) Python client.
    Falls back to hardcoded data if Massive fails (no key, rate limit, etc.).
    Always returns a safe dict — never raises.

    NOTE: `period` param is accepted for API compatibility but ignored —
    list_aggs always fetches the last ~100 trading days, which covers the
    default 6mo period well enough.
    """
    ticker = ticker.upper().strip()
    try:
        data = _fetch_from_massive(ticker)
        logger.info(f"Fetched live data from Massive for {ticker}")
        return data
    except Exception as e:
        logger.warning(f"Massive failed for {ticker}: {e}. Using fallback data.")
        if ticker in FALLBACK_STOCKS:
            return FALLBACK_STOCKS[ticker]
        fallback = dict(DEFAULT_STOCK)
        fallback["ticker"] = ticker
        fallback["error"]  = f"No live data available. Using placeholder. ({e})"
        return fallback
