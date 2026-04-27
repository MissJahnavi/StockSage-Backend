"""
Fallback data used in two situations:
  1. STOCK / NEWS APIs unavailable  →  FALLBACK_STOCKS, FALLBACK_NEWS (existing use)
  2. Gemini API limit exceeded       →  FALLBACK_INSIGHTS (new)

FALLBACK_INSIGHTS mirrors the exact shape of InsightResponse so the frontend
renders identically to a live Gemini response — charts, sentiment badges,
risk cards, recommendation pill and all.
"""

# ── Stock price + indicator fallbacks (used by stock_tool.py) ─────────────────

FALLBACK_STOCKS = {
    "AAPL": {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "current_price": 189.30,
        "change_percent": 1.24,
        "volume": 52_431_000,
        "market_cap": 2_940_000_000_000,
        "pe_ratio": 29.4,
        "week_52_high": 199.62,
        "week_52_low": 164.08,
        "rsi": 58.2,
        "macd": 1.34,
        "macd_signal": 0.98,
        "macd_histogram": 0.36,
        "bollinger_upper": 194.5,
        "bollinger_lower": 181.2,
        "bollinger_mid": 187.85,
        "atr": 3.2,
        "sma_20": 187.5,
        "sma_50": 182.3,
        "price_history": [
            {"date": "2024-10-01", "close": 226.51},
            {"date": "2024-10-15", "close": 233.40},
            {"date": "2024-11-01", "close": 222.91},
            {"date": "2024-11-15", "close": 228.52},
            {"date": "2024-12-01", "close": 243.04},
            {"date": "2024-12-15", "close": 251.10},
            {"date": "2025-01-01", "close": 243.85},
            {"date": "2025-01-15", "close": 237.33},
            {"date": "2025-02-01", "close": 227.63},
            {"date": "2025-02-15", "close": 214.00},
            {"date": "2025-03-01", "close": 213.49},
            {"date": "2025-03-15", "close": 202.52},
            {"date": "2025-04-01", "close": 189.30},
            {"date": "2025-04-15", "close": 192.80},
            {"date": "2025-04-23", "close": 191.50},
        ],
    },
    "TSLA": {
        "ticker": "TSLA",
        "company_name": "Tesla Inc.",
        "current_price": 241.37,
        "change_percent": -2.14,
        "volume": 98_254_000,
        "market_cap": 772_000_000_000,
        "pe_ratio": 65.8,
        "week_52_high": 488.54,
        "week_52_low": 138.80,
        "rsi": 42.7,
        "macd": -3.21,
        "macd_signal": -1.85,
        "macd_histogram": -1.36,
        "bollinger_upper": 268.4,
        "bollinger_lower": 218.9,
        "bollinger_mid": 243.65,
        "atr": 12.8,
        "sma_20": 248.1,
        "sma_50": 281.4,
        "price_history": [
            {"date": "2024-10-01", "close": 249.98},
            {"date": "2024-10-15", "close": 220.11},
            {"date": "2024-11-01", "close": 352.56},
            {"date": "2024-11-15", "close": 338.23},
            {"date": "2024-12-01", "close": 403.84},
            {"date": "2024-12-15", "close": 479.86},
            {"date": "2025-01-01", "close": 403.20},
            {"date": "2025-01-15", "close": 388.57},
            {"date": "2025-02-01", "close": 328.50},
            {"date": "2025-02-15", "close": 320.10},
            {"date": "2025-03-01", "close": 272.41},
            {"date": "2025-03-15", "close": 255.39},
            {"date": "2025-04-01", "close": 241.37},
            {"date": "2025-04-15", "close": 237.01},
            {"date": "2025-04-23", "close": 236.00},
        ],
    },
    "NVDA": {
        "ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "current_price": 875.40,
        "change_percent": 3.45,
        "volume": 41_230_000,
        "market_cap": 2_150_000_000_000,
        "pe_ratio": 68.2,
        "week_52_high": 974.00,
        "week_52_low": 462.19,
        "rsi": 63.5,
        "macd": 12.4,
        "macd_signal": 9.8,
        "macd_histogram": 2.6,
        "bollinger_upper": 920.0,
        "bollinger_lower": 831.0,
        "bollinger_mid": 875.5,
        "atr": 22.3,
        "sma_20": 862.0,
        "sma_50": 820.5,
        "price_history": [
            {"date": "2024-10-01", "close": 121.35},
            {"date": "2024-10-15", "close": 139.56},
            {"date": "2024-11-01", "close": 138.85},
            {"date": "2024-11-15", "close": 141.95},
            {"date": "2024-12-01", "close": 134.25},
            {"date": "2024-12-15", "close": 128.30},
            {"date": "2025-01-01", "close": 124.92},
            {"date": "2025-01-15", "close": 131.38},
            {"date": "2025-02-01", "close": 127.25},
            {"date": "2025-02-15", "close": 135.28},
            {"date": "2025-03-01", "close": 112.27},
            {"date": "2025-03-15", "close": 107.29},
            {"date": "2025-04-01", "close": 875.40},
            {"date": "2025-04-15", "close": 858.00},
            {"date": "2025-04-23", "close": 875.40},
        ],
    },
    "MSFT": {
        "ticker": "MSFT",
        "company_name": "Microsoft Corporation",
        "current_price": 415.50,
        "change_percent": 0.87,
        "volume": 18_450_000,
        "market_cap": 3_090_000_000_000,
        "pe_ratio": 34.1,
        "week_52_high": 468.35,
        "week_52_low": 385.58,
        "rsi": 55.8,
        "macd": 2.1,
        "macd_signal": 1.5,
        "macd_histogram": 0.6,
        "bollinger_upper": 432.0,
        "bollinger_lower": 398.0,
        "bollinger_mid": 415.0,
        "atr": 8.5,
        "sma_20": 412.0,
        "sma_50": 405.3,
        "price_history": [
            {"date": "2024-10-01", "close": 430.32},
            {"date": "2024-10-15", "close": 444.65},
            {"date": "2024-11-01", "close": 422.93},
            {"date": "2024-11-15", "close": 431.48},
            {"date": "2024-12-01", "close": 444.92},
            {"date": "2024-12-15", "close": 449.73},
            {"date": "2025-01-01", "close": 453.30},
            {"date": "2025-01-15", "close": 438.62},
            {"date": "2025-02-01", "close": 408.19},
            {"date": "2025-02-15", "close": 399.42},
            {"date": "2025-03-01", "close": 388.49},
            {"date": "2025-03-15", "close": 395.74},
            {"date": "2025-04-01", "close": 415.50},
            {"date": "2025-04-15", "close": 411.22},
            {"date": "2025-04-23", "close": 415.50},
        ],
    },
}


# ── News fallbacks (used by news_tool.py) ─────────────────────────────────────

FALLBACK_NEWS = {
    "AAPL": [
        {"title": "Apple's AI Integration Drives Strong iPhone 16 Demand", "url": "https://example.com/apple-ai", "source": "TechCrunch", "published_at": "2025-04-20", "sentiment_label": "positive", "compound_score": 0.72},
        {"title": "Apple Expands India Manufacturing to Reduce China Dependency", "url": "https://example.com/apple-india", "source": "Reuters", "published_at": "2025-04-18", "sentiment_label": "positive", "compound_score": 0.54},
        {"title": "Apple Faces EU Regulatory Scrutiny Over App Store Fees", "url": "https://example.com/apple-eu", "source": "Bloomberg", "published_at": "2025-04-15", "sentiment_label": "negative", "compound_score": -0.38},
        {"title": "Apple Vision Pro Sales Miss Analyst Expectations in Q1", "url": "https://example.com/apple-vp", "source": "WSJ", "published_at": "2025-04-12", "sentiment_label": "negative", "compound_score": -0.29},
        {"title": "Apple Services Revenue Hits Record High Driven by App Store", "url": "https://example.com/apple-svc", "source": "CNBC", "published_at": "2025-04-10", "sentiment_label": "positive", "compound_score": 0.65},
    ],
    "TSLA": [
        {"title": "Tesla Q1 Deliveries Miss Estimates Amid Brand Controversy", "url": "https://example.com/tsla-q1", "source": "CNBC", "published_at": "2025-04-21", "sentiment_label": "negative", "compound_score": -0.61},
        {"title": "Tesla Cybertruck Production Ramp Progresses Ahead of Schedule", "url": "https://example.com/tsla-cybertruck", "source": "Electrek", "published_at": "2025-04-19", "sentiment_label": "positive", "compound_score": 0.48},
        {"title": "Elon Musk DOGE Role Creates Tesla Shareholder Concerns", "url": "https://example.com/tsla-musk", "source": "WSJ", "published_at": "2025-04-16", "sentiment_label": "negative", "compound_score": -0.44},
        {"title": "Tesla Full Self-Driving Version 13 Receives Positive Early Reviews", "url": "https://example.com/tsla-fsd", "source": "The Verge", "published_at": "2025-04-14", "sentiment_label": "positive", "compound_score": 0.55},
        {"title": "Tesla Price Cuts in China Squeeze Margins Further", "url": "https://example.com/tsla-china", "source": "FT", "published_at": "2025-04-11", "sentiment_label": "negative", "compound_score": -0.50},
    ],
    "NVDA": [
        {"title": "NVIDIA Blackwell GPU Demand Exceeds All Supply Forecasts", "url": "https://example.com/nvda-blackwell", "source": "The Verge", "published_at": "2025-04-22", "sentiment_label": "positive", "compound_score": 0.85},
        {"title": "NVIDIA H20 Chip Export Restrictions Impacting China Revenue", "url": "https://example.com/nvda-china", "source": "FT", "published_at": "2025-04-18", "sentiment_label": "negative", "compound_score": -0.52},
        {"title": "NVIDIA Announces New AI Data Center Partnerships with AWS", "url": "https://example.com/nvda-aws", "source": "TechCrunch", "published_at": "2025-04-15", "sentiment_label": "positive", "compound_score": 0.67},
        {"title": "NVIDIA CEO Jensen Huang Previews Next Generation Rubin Architecture", "url": "https://example.com/nvda-rubin", "source": "Wired", "published_at": "2025-04-13", "sentiment_label": "positive", "compound_score": 0.74},
        {"title": "NVIDIA Faces Antitrust Questions Over AI Chip Market Dominance", "url": "https://example.com/nvda-antitrust", "source": "Reuters", "published_at": "2025-04-10", "sentiment_label": "negative", "compound_score": -0.40},
    ],
    "MSFT": [
        {"title": "Microsoft Azure AI Revenue Surges 35% Year-Over-Year", "url": "https://example.com/msft-azure", "source": "Bloomberg", "published_at": "2025-04-20", "sentiment_label": "positive", "compound_score": 0.78},
        {"title": "Microsoft Copilot Integration Boosts Office 365 Subscriptions", "url": "https://example.com/msft-copilot", "source": "Reuters", "published_at": "2025-04-17", "sentiment_label": "positive", "compound_score": 0.62},
        {"title": "Microsoft Gaming Segment Faces Headwinds After Activision Deal", "url": "https://example.com/msft-gaming", "source": "IGN", "published_at": "2025-04-14", "sentiment_label": "neutral", "compound_score": -0.08},
        {"title": "Microsoft Bing AI Search Share Grows as Google Faces Pressure", "url": "https://example.com/msft-bing", "source": "TechCrunch", "published_at": "2025-04-12", "sentiment_label": "positive", "compound_score": 0.55},
        {"title": "Microsoft Faces EU Data Residency Compliance Challenges", "url": "https://example.com/msft-eu", "source": "Politico", "published_at": "2025-04-09", "sentiment_label": "negative", "compound_score": -0.33},
    ],
}


# ── Generic stock placeholder (used when ticker not in FALLBACK_STOCKS) ───────

DEFAULT_STOCK = {
    "ticker": "UNKNOWN",
    "company_name": "Unknown Company",
    "current_price": 100.0,
    "change_percent": 0.0,
    "volume": 1_000_000,
    "market_cap": 1_000_000_000,
    "pe_ratio": 20.0,
    "week_52_high": 120.0,
    "week_52_low": 80.0,
    "rsi": 50.0,
    "macd": 0.0,
    "macd_signal": 0.0,
    "macd_histogram": 0.0,
    "bollinger_upper": 105.0,
    "bollinger_lower": 95.0,
    "bollinger_mid": 100.0,
    "atr": 2.0,
    "sma_20": 100.0,
    "sma_50": 100.0,
    "price_history": [
        {"date": "2025-01-01", "close": 100.0},
        {"date": "2025-02-01", "close": 102.0},
        {"date": "2025-03-01", "close": 98.0},
        {"date": "2025-04-01", "close": 100.0},
    ],
}


# ── Full InsightResponse fallbacks (used when Gemini API fails) ───────────────
#
# Shape must match InsightResponse exactly:
#   ticker, trend_analysis, news_summary, risk_factors, recommendation,
#   raw_agent_steps, error
#
# trend_analysis keys: summary, direction, key_levels, indicators_summary
# recommendation keys: action, confidence, rationale, time_horizon
# risk_factors keys:   category, severity, description
# news_summary:        pulled from FALLBACK_NEWS above at runtime

FALLBACK_INSIGHTS = {
    "AAPL": {
        "ticker": "AAPL",
        "trend_analysis": {
            "summary": (
                "Apple has experienced a gradual pullback from its December 2024 peak near $251, "
                "declining roughly 25% to current levels around $189. The stock is trading below "
                "both its 20-day ($187.50) and 50-day ($182.30) moving averages, suggesting the "
                "downtrend remains intact in the short term, though the SMA50 is beginning to act "
                "as a support floor."
            ),
            "direction": "bearish",
            "key_levels": {"support": 181.20, "resistance": 194.50},
            "indicators_summary": (
                "RSI at 58.2 is neutral — not yet overbought, leaving room to move higher. "
                "MACD histogram of +0.36 signals a nascent bullish crossover forming. "
                "Price is near the Bollinger midband ($187.85), consistent with consolidation. "
                "ATR of 3.2 reflects moderate volatility."
            ),
        },
        "news_summary": FALLBACK_NEWS["AAPL"],
        "risk_factors": [
            {
                "category": "Macro/News",
                "severity": "medium",
                "description": "EU regulatory pressure on App Store fees could impact Services segment margins, which now represent over 25% of revenue.",
            },
            {
                "category": "Fundamental (Valuation)",
                "severity": "medium",
                "description": "P/E of 29.4x is above the S&P 500 average (~21x), leaving limited margin of safety if earnings growth disappoints.",
            },
            {
                "category": "Technical (Trend)",
                "severity": "low",
                "description": "Stock remains in a downtrend from its 52-week high of $199.62. A close above $194 is needed to confirm trend reversal.",
            },
        ],
        "recommendation": {
            "action": "hold",
            "confidence": 0.68,
            "rationale": (
                "Apple's strong Services flywheel, loyal customer base, and India manufacturing diversification "
                "provide long-term resilience. However, the near-term technical picture remains soft with price "
                "below key moving averages. Existing holders should hold through the consolidation; new buyers "
                "may find a better entry on a pullback toward the $181 Bollinger lower band."
            ),
            "time_horizon": "medium-term (3-12 months)",
        },
        "raw_agent_steps": [
            "Fetching stock data for AAPL",
            "Fetching news for AAPL",
            "Searching knowledge base for AAPL analysis",
            "Running risk detection engine",
            "Gemini API unavailable — serving pre-computed fallback insight",
        ],
        "error": "Gemini API limit reached. Displaying pre-computed analysis.",
    },

    "TSLA": {
        "ticker": "TSLA",
        "trend_analysis": {
            "summary": (
                "Tesla has been in a sharp downtrend since its December 2024 high near $480, shedding "
                "nearly 50% of its value to around $241. Price is well below the 50-day SMA ($281.40), "
                "and the 20-day SMA ($248.10) is also acting as overhead resistance. Selling pressure "
                "has been elevated on high volume days following delivery miss announcements."
            ),
            "direction": "bearish",
            "key_levels": {"support": 218.90, "resistance": 268.40},
            "indicators_summary": (
                "RSI at 42.7 is approaching oversold territory but has not yet triggered a reversal signal. "
                "MACD of -3.21 with a signal of -1.85 confirms strong bearish momentum. "
                "Negative MACD histogram of -1.36 shows acceleration in selling. "
                "Price is hugging the lower Bollinger band, indicating oversold conditions on a volatility basis."
            ),
        },
        "news_summary": FALLBACK_NEWS["TSLA"],
        "risk_factors": [
            {
                "category": "Sentiment",
                "severity": "high",
                "description": "Over 60% of recent news is negative, driven by Q1 delivery miss and Elon Musk's political involvement reducing brand appeal.",
            },
            {
                "category": "Fundamental (P/E)",
                "severity": "high",
                "description": "P/E ratio of 65.8x is extremely elevated for a company facing slowing delivery growth and margin compression from China price wars.",
            },
            {
                "category": "Volatility",
                "severity": "high",
                "description": "ATR of 12.8 represents over 5% of the stock price, indicating extreme daily volatility and elevated risk for short-term positions.",
            },
            {
                "category": "Technical (Trend)",
                "severity": "medium",
                "description": "All major moving averages are in a downward slope. No technical base has formed yet at current levels.",
            },
        ],
        "recommendation": {
            "action": "avoid",
            "confidence": 0.74,
            "rationale": (
                "Tesla faces a rare combination of deteriorating fundamentals (delivery miss, margin pressure) "
                "and worsening technicals (below all SMAs, negative MACD momentum). The elevated P/E of 65.8x "
                "leaves no room for earnings disappointment. While FSD v13 progress is a positive catalyst, "
                "it is not sufficient to reverse the near-term headwinds. Risk-averse investors should avoid "
                "until a technical base forms near the $218 support level."
            ),
            "time_horizon": "short-term (1-3 months)",
        },
        "raw_agent_steps": [
            "Fetching stock data for TSLA",
            "Fetching news for TSLA",
            "Searching knowledge base for TSLA analysis",
            "Running risk detection engine",
            "Gemini API unavailable — serving pre-computed fallback insight",
        ],
        "error": "Gemini API limit reached. Displaying pre-computed analysis.",
    },

    "NVDA": {
        "ticker": "NVDA",
        "trend_analysis": {
            "summary": (
                "NVIDIA continues to demonstrate strong bullish momentum, with the stock trading near "
                "$875 and above both its 20-day ($862) and 50-day ($820.50) moving averages. The "
                "Blackwell GPU product cycle is driving unprecedented data center demand, and institutional "
                "buying remains consistently strong on any dips toward the SMA20."
            ),
            "direction": "bullish",
            "key_levels": {"support": 831.00, "resistance": 920.00},
            "indicators_summary": (
                "RSI at 63.5 is healthy — trending upward without entering overbought territory above 70. "
                "MACD of +12.4 above signal of +9.8 confirms bullish trend continuation. "
                "Positive histogram of +2.6 shows momentum is building. "
                "Price is trading above the Bollinger midband, consistent with an uptrend."
            ),
        },
        "news_summary": FALLBACK_NEWS["NVDA"],
        "risk_factors": [
            {
                "category": "Macro/News",
                "severity": "high",
                "description": "US export restrictions on H20 chips to China could remove a significant revenue stream and weigh on forward guidance.",
            },
            {
                "category": "Fundamental (Valuation)",
                "severity": "high",
                "description": "P/E of 68.2x prices in near-perfect execution. Any guidance miss or demand softening could trigger a sharp de-rating.",
            },
            {
                "category": "Volatility",
                "severity": "medium",
                "description": "ATR of 22.3 (~2.5% of price) indicates significant daily swings — position sizing should account for this elevated volatility.",
            },
        ],
        "recommendation": {
            "action": "buy",
            "confidence": 0.76,
            "rationale": (
                "NVIDIA is the primary infrastructure layer for the AI compute buildout, with Blackwell GPU "
                "demand far outpacing supply and AWS/hyperscaler partnerships solidifying its moat. "
                "The technical setup — above both major SMAs with positive MACD momentum — supports continued "
                "upside toward the $920 resistance. Buy on dips toward the $831 Bollinger lower band for "
                "optimal risk/reward, with a stop below $800."
            ),
            "time_horizon": "medium-term (3-12 months)",
        },
        "raw_agent_steps": [
            "Fetching stock data for NVDA",
            "Fetching news for NVDA",
            "Searching knowledge base for NVDA analysis",
            "Running risk detection engine",
            "Gemini API unavailable — serving pre-computed fallback insight",
        ],
        "error": "Gemini API limit reached. Displaying pre-computed analysis.",
    },

    "MSFT": {
        "ticker": "MSFT",
        "trend_analysis": {
            "summary": (
                "Microsoft is showing a moderate bullish recovery after bottoming near $388 in March 2025. "
                "The stock has reclaimed its 20-day SMA ($412) and is approaching the 50-day SMA ($405.30) "
                "from above, which is a constructive sign. Azure AI revenue growth of 35% YoY is the primary "
                "fundamental catalyst supporting the recovery."
            ),
            "direction": "bullish",
            "key_levels": {"support": 398.00, "resistance": 432.00},
            "indicators_summary": (
                "RSI at 55.8 is in neutral-bullish territory with room to run toward 65-70 before becoming "
                "overbought. MACD of +2.1 above signal of +1.5 confirms a fresh bullish crossover. "
                "Price trading above the Bollinger midband ($415) is consistent with mild upward momentum. "
                "ATR of 8.5 reflects normal large-cap volatility."
            ),
        },
        "news_summary": FALLBACK_NEWS["MSFT"],
        "risk_factors": [
            {
                "category": "Macro/News",
                "severity": "medium",
                "description": "EU data residency compliance challenges could increase operational costs and slow Azure growth in the European market.",
            },
            {
                "category": "Fundamental (Valuation)",
                "severity": "medium",
                "description": "P/E of 34.1x is premium to the market but reasonable given ~15% EPS growth expectations driven by AI monetisation.",
            },
            {
                "category": "Sentiment",
                "severity": "low",
                "description": "Majority of recent news is positive (Azure, Copilot), with only gaming segment showing headwinds — limited downside risk from news flow.",
            },
        ],
        "recommendation": {
            "action": "buy",
            "confidence": 0.72,
            "rationale": (
                "Microsoft offers the most balanced AI risk/reward in mega-cap tech. Azure's 35% YoY AI "
                "revenue growth, Copilot monetisation across Office 365, and GitHub Copilot enterprise "
                "adoption provide multiple durable growth vectors. The technical recovery from the March "
                "lows with a fresh MACD bullish crossover supports an entry here, with a target toward "
                "the $432 Bollinger upper band and a stop below the $398 support."
            ),
            "time_horizon": "medium-term (3-12 months)",
        },
        "raw_agent_steps": [
            "Fetching stock data for MSFT",
            "Fetching news for MSFT",
            "Searching knowledge base for MSFT analysis",
            "Running risk detection engine",
            "Gemini API unavailable — serving pre-computed fallback insight",
        ],
        "error": "Gemini API limit reached. Displaying pre-computed analysis.",
    },
}


def get_fallback_insight(ticker: str) -> dict | None:
    """
    Return a pre-computed InsightResponse-shaped dict for the given ticker,
    or None if we don't have one (caller should use _fallback_response instead).
    """
    return FALLBACK_INSIGHTS.get(ticker.upper())

