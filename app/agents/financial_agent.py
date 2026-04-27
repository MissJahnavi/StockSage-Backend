import json
import re
from loguru import logger
from app.core.llm import get_llm
from app.core.config import settings
from app.tools.stock_tool import get_stock_data
from app.tools.news_tool import get_news
from app.rag.vector_store import search as rag_search
from app.services.risk import detect_risks
from app.data.fallback_data import get_fallback_insight
from app.schemas import (
    InsightResponse, TrendAnalysis, NewsItem, RiskFactor, Recommendation, Direction, Action
)


SYSTEM_PROMPT = """You are an expert AI financial analyst. Analyse the provided stock data and return ONLY a valid JSON object — no markdown, no code fences, no explanation, no text before or after the JSON.

The JSON must have exactly these fields:

{
  "ticker": "string — the ticker symbol",
  "trend_analysis": {
    "summary": "string — 2-3 sentences describing the current price trend",
    "direction": "string — must be one of: bullish, bearish, sideways",
    "key_levels": {"support": 0.0, "resistance": 0.0},
    "indicators_summary": "string — brief RSI, MACD and Bollinger interpretation"
  },
  "news_summary": [],
  "risk_factors": [],
  "recommendation": {
    "action": "string — must be one of: buy, hold, avoid",
    "confidence": 0.75,
    "rationale": "string — 2-3 sentence investment rationale",
    "time_horizon": "string — e.g. medium-term (3-12 months)"
  },
  "raw_agent_steps": ["step description"]
}

Critical rules:
- direction value must be exactly the word: bullish OR bearish OR sideways
- action value must be exactly the word: buy OR hold OR avoid
- confidence must be a number between 0.0 and 1.0
- Output ONLY the JSON object. The very first character of your response must be {
"""


def _repair_json(text: str) -> str:
    """
    Multi-stage repair pipeline for LLM JSON output.

    Handles these real Gemini 2.5 Flash failure modes:
      1. BOM / invisible prefix characters
      2. <think>…</think> or [INST]…[/INST] wrapper blocks
      3. Markdown code fences (```json … ```)
      4. Prose before/after the JSON object
      5. Pipe-literal values: "direction": "bullish" | "bearish"  →  "bullish"
      6. Trailing commas before } or ]
      7. Python-style True/False/None instead of true/false/null
    """
    text = text.strip().lstrip("\ufeff")

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"\[INST\].*?\[/INST\]", "", text, flags=re.DOTALL)
    text = text.strip()

    text = re.sub(r"^```(?:json)?\s*\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text, flags=re.MULTILINE)
    text = text.strip()

    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in LLM response. Raw output: {text[:300]!r}")

    depth = 0
    in_string = False
    escape_next = False
    end = start
    for i, ch in enumerate(text[start:], start=start):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break

    text = text[start:end + 1]

    # 5. Fix pipe-literal values  "direction": "bullish" | "bearish"  →  "direction": "bullish"
    text = re.sub(r'(":\s*"[^"]+")(\s*\|\s*"[^"]+")+', r"\1", text)

    # 6. Fix trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)

    # 7. Fix Python literals
    text = re.sub(r"\bTrue\b", "true", text)
    text = re.sub(r"\bFalse\b", "false", text)
    text = re.sub(r"\bNone\b", "null", text)

    return text


def _fallback_response(ticker: str, stock_data: dict, news: list, risks: list, error: str = "") -> InsightResponse:
    """Create a structured response when the LLM fails."""
    rsi = stock_data.get("rsi", 50)
    change = stock_data.get("change_percent", 0)
    direction = Direction.BULLISH if change > 1 else (Direction.BEARISH if change < -1 else Direction.SIDEWAYS)
    action = Action.HOLD
    if rsi < 35 and change < -2:
        action = Action.AVOID
    elif rsi < 50 and change > 0:
        action = Action.BUY

    return InsightResponse(
        ticker=ticker,
        trend_analysis=TrendAnalysis(
            summary=f"{ticker} is showing {direction.value} momentum. Price is {'up' if change > 0 else 'down'} {abs(change):.1f}%.",
            direction=direction,
            key_levels={"support": stock_data.get("bollinger_lower", 0), "resistance": stock_data.get("bollinger_upper", 0)},
            indicators_summary=f"RSI: {rsi:.1f}, MACD: {stock_data.get('macd', 0):.3f}",
        ),
        news_summary=[NewsItem(**n) for n in news[:5]],
        risk_factors=risks,
        recommendation=Recommendation(
            action=action,
            confidence=0.55,
            rationale="Analysis based on technical indicators. LLM analysis unavailable — using rule-based fallback.",
            time_horizon="medium-term (3-12 months)",
        ),
        raw_agent_steps=["Rule-based fallback triggered", error],
        error=error if error else None,
    )


def run_analysis(query: str, ticker: str, period: str = "6mo") -> InsightResponse:
    """
    Main agent function. Gathers data from all tools, calls Gemini, returns InsightResponse.
    """
    ticker = ticker.upper().strip()
    steps = []

    # Step 1: Fetch stock data
    steps.append(f"Fetching stock data for {ticker}")
    stock_data = get_stock_data(ticker, period)

    # Step 2: Fetch news
    steps.append(f"Fetching news for {ticker}")
    news = get_news(ticker)

    # Step 3: RAG retrieval
    steps.append(f"Searching knowledge base for: {query}")
    rag_results = rag_search(f"{ticker} {query}", k=3)
    rag_context = "\n".join([r["content"] for r in rag_results]) if rag_results else "No stored context found."

    steps.append("Running risk detection engine")
    risks = detect_risks(stock_data, news)

    # Step 5: Call Gemini
    steps.append(f"Calling {settings.GEMINI_MODEL} for analysis")

    price_history_summary = stock_data.get("price_history", [])[-5:]

    prompt = f"""{SYSTEM_PROMPT}

USER QUERY: {query}

STOCK DATA:
Ticker: {ticker}
Company: {stock_data.get('company_name', ticker)}
Price: ${stock_data.get('current_price', 0):.2f} ({stock_data.get('change_percent', 0):+.2f}%)
Market Cap: ${stock_data.get('market_cap', 0):,}
P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
52W High: ${stock_data.get('week_52_high', 0):.2f} | 52W Low: ${stock_data.get('week_52_low', 0):.2f}
RSI: {stock_data.get('rsi', 50):.1f}
MACD: {stock_data.get('macd', 0):.4f} | Signal: {stock_data.get('macd_signal', 0):.4f}
Bollinger Upper: {stock_data.get('bollinger_upper', 0):.2f} | Lower: {stock_data.get('bollinger_lower', 0):.2f}
ATR: {stock_data.get('atr', 0):.4f}
SMA20: {stock_data.get('sma_20', 0):.2f} | SMA50: {stock_data.get('sma_50', 0):.2f}
Recent prices: {price_history_summary}

NEWS (with sentiment):
{json.dumps(news[:5], indent=2)}

STORED CONTEXT:
{rag_context}

DETECTED RISKS:
{json.dumps([r.model_dump() for r in risks], indent=2)}

Now produce the JSON analysis for ticker {ticker}. Remember: ONLY JSON, no code fences."""

    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        raw_text = response.content if hasattr(response, "content") else str(response)
        steps.append("Received LLM response — repairing and parsing JSON")

        repaired = _repair_json(raw_text)
        data = json.loads(repaired)

        # Normalize enums
        data["ticker"] = ticker
        data["raw_agent_steps"] = steps + data.get("raw_agent_steps", [])

        # Force news_summary from our fetched data (more reliable than LLM)
        data["news_summary"] = news[:5]

        # Merge risk factors
        llm_risks = data.get("risk_factors", [])
        engine_risks = [r.model_dump() for r in risks]
        merged_risks = engine_risks
        for lr in llm_risks:
            if isinstance(lr, dict) and not any(lr.get("category") == er.get("category") for er in merged_risks):
                merged_risks.append(lr)
        data["risk_factors"] = merged_risks

        return InsightResponse(**data)

    except Exception as e:
        logger.error(f"LLM analysis failed for {ticker}: {e}")
        try:
            logger.debug(f"Raw LLM output was: {raw_text[:500]!r}")
        except NameError:
            pass  # raw_text not set — LLM call itself failed

        # Priority 1 — use rich pre-computed insight if we have one for this ticker
        precomputed = get_fallback_insight(ticker)
        if precomputed:
            logger.info(f"Serving pre-computed fallback insight for {ticker}")
            try:
                # Swap in live news and risk data if they were successfully fetched
                data = dict(precomputed)
                if news:
                    data["news_summary"] = news[:5]
                if risks:
                    # Merge live risks on top of precomputed ones (deduplicate by category)
                    live_risk_dicts = [r.model_dump() for r in risks]
                    existing_categories = {r["category"] for r in data["risk_factors"]}
                    for r in live_risk_dicts:
                        if r["category"] not in existing_categories:
                            data["risk_factors"].append(r)
                data["error"] = f"Gemini API unavailable. Displaying pre-computed analysis. ({e})"
                return InsightResponse(**data)
            except Exception as parse_err:
                logger.warning(f"Pre-computed insight parse failed: {parse_err}. Falling through to rule-based fallback.")

        # Priority 2 — thin rule-based fallback (always works, even for unknown tickers)
        return _fallback_response(ticker, stock_data, news, risks, error=str(e))
