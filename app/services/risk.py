from app.schemas import RiskFactor, Severity

MACRO_HIGH = ["bankruptcy", "fraud", "crash", "scandal", "default", "collapse"]
MACRO_MEDIUM = ["inflation", "downgrade", "recession", "layoffs", "investigation"]


def detect_risks(stock_data: dict, news_articles: list[dict]) -> list[RiskFactor]:
    """Run 5-detector risk engine and return list of RiskFactor objects."""
    risks = []

    # 1. Volatility risk (ATR / Price)
    price = stock_data.get("current_price", 0)
    atr = stock_data.get("atr", 0)
    if price and atr:
        atr_pct = (atr / price) * 100
        if atr_pct > 5:
            risks.append(RiskFactor(category="Volatility", severity=Severity.HIGH,
                description=f"ATR is {atr_pct:.1f}% of price — extremely high daily volatility."))
        elif atr_pct > 2.5:
            risks.append(RiskFactor(category="Volatility", severity=Severity.MEDIUM,
                description=f"ATR is {atr_pct:.1f}% of price — elevated volatility."))

    # 2. Technical risk (RSI)
    rsi = stock_data.get("rsi", 50)
    if rsi > 75:
        risks.append(RiskFactor(category="Technical (RSI)", severity=Severity.HIGH,
            description=f"RSI at {rsi:.1f} — severely overbought. High reversal risk."))
    elif rsi > 65:
        risks.append(RiskFactor(category="Technical (RSI)", severity=Severity.MEDIUM,
            description=f"RSI at {rsi:.1f} — approaching overbought territory."))
    elif rsi < 25:
        risks.append(RiskFactor(category="Technical (RSI)", severity=Severity.HIGH,
            description=f"RSI at {rsi:.1f} — severely oversold. Trend may continue downward."))

    # 3. Fundamental risk (P/E)
    pe = stock_data.get("pe_ratio", 0)
    if pe and (pe > 100 or pe < 0):
        risks.append(RiskFactor(category="Fundamental (P/E)", severity=Severity.HIGH,
            description=f"P/E ratio of {pe:.1f} — extreme valuation. High speculative risk."))
    elif pe and pe > 40:
        risks.append(RiskFactor(category="Fundamental (P/E)", severity=Severity.MEDIUM,
            description=f"P/E ratio of {pe:.1f} — elevated valuation relative to market average."))

    # 4. Macro keyword risk (news text)
    all_text = " ".join([a.get("title", "") for a in news_articles]).lower()
    for kw in MACRO_HIGH:
        if kw in all_text:
            risks.append(RiskFactor(category="Macro/News", severity=Severity.HIGH,
                description=f"High-risk keyword '{kw}' detected in recent news headlines."))
            break
    else:
        for kw in MACRO_MEDIUM:
            if kw in all_text:
                risks.append(RiskFactor(category="Macro/News", severity=Severity.MEDIUM,
                    description=f"Moderate-risk keyword '{kw}' detected in recent news."))
                break

    # 5. Sentiment risk
    if news_articles:
        neg_count = sum(1 for a in news_articles if a.get("sentiment_label") == "negative")
        neg_pct = neg_count / len(news_articles) * 100
        if neg_pct > 65:
            risks.append(RiskFactor(category="Sentiment", severity=Severity.HIGH,
                description=f"{neg_pct:.0f}% of recent news articles are negative."))
        elif neg_count > len(news_articles) / 2:
            risks.append(RiskFactor(category="Sentiment", severity=Severity.MEDIUM,
                description=f"Majority of news sentiment is negative ({neg_pct:.0f}%)."))

    return risks
