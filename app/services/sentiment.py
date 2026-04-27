from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def score_text(text: str) -> dict:
    """Score a text string with VADER. Returns label + compound score."""
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {"sentiment_label": label, "compound_score": round(compound, 4)}


def aggregate_sentiment(articles: list[dict]) -> dict:
    """Aggregate sentiment across a list of articles."""
    if not articles:
        return {"overall": "neutral", "positive_pct": 0, "negative_pct": 0, "neutral_pct": 0}
    labels = [a.get("sentiment_label", "neutral") for a in articles]
    total = len(labels)
    pos = labels.count("positive") / total * 100
    neg = labels.count("negative") / total * 100
    neu = labels.count("neutral") / total * 100
    overall = "positive" if pos > neg and pos > neu else ("negative" if neg > pos else "neutral")
    return {
        "overall": overall,
        "positive_pct": round(pos, 1),
        "negative_pct": round(neg, 1),
        "neutral_pct": round(neu, 1),
    }
