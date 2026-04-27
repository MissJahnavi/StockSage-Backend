from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class Direction(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Action(str, Enum):
    BUY = "buy"
    HOLD = "hold"
    AVOID = "avoid"


class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language question about a stock")
    ticker: Optional[str] = Field(None, description="Stock ticker symbol e.g. AAPL")
    period: str = Field("6mo", description="Historical data period")


class TrendAnalysis(BaseModel):
    summary: str
    direction: Direction
    key_levels: dict = Field(default_factory=dict)
    indicators_summary: str


class NewsItem(BaseModel):
    title: str
    url: str
    source: str
    published_at: str
    sentiment_label: str
    compound_score: float


class RiskFactor(BaseModel):
    category: str
    severity: Severity
    description: str


class Recommendation(BaseModel):
    action: Action
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    time_horizon: str


class InsightResponse(BaseModel):
    ticker: str
    trend_analysis: TrendAnalysis
    news_summary: List[NewsItem] = Field(default_factory=list)
    risk_factors: List[RiskFactor] = Field(default_factory=list)
    recommendation: Recommendation
    raw_agent_steps: List[str] = Field(default_factory=list)
    error: Optional[str] = None


class RAGIngestRequest(BaseModel):
    text: str
    metadata: dict = Field(default_factory=dict)


class RAGSearchRequest(BaseModel):
    query: str
    k: int = 5
