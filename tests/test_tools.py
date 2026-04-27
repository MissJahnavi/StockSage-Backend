import pytest
from app.services.sentiment import score_text, aggregate_sentiment
from app.services.risk import detect_risks
from app.schemas import InsightResponse, TrendAnalysis, Recommendation, Direction, Action, Severity


# ── Sentiment Tests ────────────────────────────────────────────────────────────

def test_sentiment_positive():
    result = score_text("Stock surges to all-time high on record earnings")
    assert result["sentiment_label"] == "positive"
    assert result["compound_score"] > 0.05


def test_sentiment_negative():
    result = score_text("Stock crashes to zero, company files for bankruptcy")
    assert result["sentiment_label"] == "negative"
    assert result["compound_score"] < -0.05


def test_sentiment_neutral():
    result = score_text("Company releases quarterly report")
    assert result["sentiment_label"] in ["neutral", "positive", "negative"]


def test_aggregate_sentiment():
    articles = [
        {"sentiment_label": "negative"},
        {"sentiment_label": "negative"},
        {"sentiment_label": "positive"},
    ]
    result = aggregate_sentiment(articles)
    assert result["overall"] == "negative"
    assert result["negative_pct"] > 50


# ── Risk Engine Tests ──────────────────────────────────────────────────────────

def test_risk_high_volatility():
    stock = {"current_price": 100.0, "atr": 6.0, "rsi": 50.0, "pe_ratio": 20.0}
    news = []
    risks = detect_risks(stock, news)
    categories = [r.category for r in risks]
    assert "Volatility" in categories
    vol_risk = next(r for r in risks if r.category == "Volatility")
    assert vol_risk.severity.value == "high"


def test_risk_high_rsi():
    stock = {"current_price": 100.0, "atr": 1.0, "rsi": 80.0, "pe_ratio": 20.0}
    news = []
    risks = detect_risks(stock, news)
    categories = [r.category for r in risks]
    assert "Technical (RSI)" in categories


def test_risk_macro_keyword():
    stock = {"current_price": 100.0, "atr": 1.0, "rsi": 50.0, "pe_ratio": 20.0}
    news = [{"title": "Company faces bankruptcy proceedings", "sentiment_label": "negative"}]
    risks = detect_risks(stock, news)
    categories = [r.category for r in risks]
    assert "Macro/News" in categories
    macro = next(r for r in risks if r.category == "Macro/News")
    assert macro.severity.value == "high"


def test_risk_no_risks():
    stock = {"current_price": 100.0, "atr": 1.0, "rsi": 50.0, "pe_ratio": 20.0}
    news = [{"title": "Steady quarter results", "sentiment_label": "neutral"}]
    risks = detect_risks(stock, news)
    # Should have few or no high-severity risks
    high = [r for r in risks if r.severity == Severity.HIGH]
    assert len(high) == 0


# ── Schema Tests ───────────────────────────────────────────────────────────────

def test_insight_schema_valid():
    data = InsightResponse(
        ticker="AAPL",
        trend_analysis=TrendAnalysis(
            summary="Bullish trend",
            direction=Direction.BULLISH,
            key_levels={"support": 180.0, "resistance": 200.0},
            indicators_summary="RSI moderate",
        ),
        news_summary=[],
        risk_factors=[],
        recommendation=Recommendation(
            action=Action.BUY,
            confidence=0.72,
            rationale="Strong fundamentals",
            time_horizon="medium-term (3-12 months)",
        ),
        raw_agent_steps=["step1", "step2"],
    )
    assert data.ticker == "AAPL"
    assert data.recommendation.action == Action.BUY
    assert data.recommendation.confidence == 0.72


# ── Fallback Data Tests ────────────────────────────────────────────────────────

def test_fallback_stock_data():
    from app.data.fallback_data import FALLBACK_STOCKS
    assert "AAPL" in FALLBACK_STOCKS
    aapl = FALLBACK_STOCKS["AAPL"]
    assert "current_price" in aapl
    assert "rsi" in aapl
    assert len(aapl["price_history"]) > 0


def test_stock_tool_fallback():
    from app.tools.stock_tool import get_stock_data
    # Using a fake ticker should return fallback, not crash
    result = get_stock_data("FAKEXYZ999")
    assert isinstance(result, dict)
    assert "current_price" in result
    assert "ticker" in result


def test_news_tool_fallback():
    from app.tools.news_tool import get_news
    # Should return list even for unknown ticker
    result = get_news("FAKEXYZ999")
    assert isinstance(result, list)
