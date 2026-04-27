# StockSage — AI Financial Research Agent

Ask a natural language question about any stock. Get back a full analysis — price chart, technical indicators, news sentiment, risk breakdown, and a Gemini-powered buy/hold/avoid recommendation.

---

## Tech Stack

**Backend:** FastAPI · LangChain · Gemini 2.5 Flash · FAISS · polygon-api-client · NewsAPI · VADER · ta · pandas

**Frontend:** React · Vite · Tailwind CSS · Recharts · Axios

---

## Setup

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # fill in your API keys
python run.py                   # starts at http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                     # starts at http://localhost:5173
```

---

## API Keys

| Key | Get it from | Required? |
|-----|------------|-----------|
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | ✅ Yes |
| `POLYGON_API_KEY` | [massive.com](https://massive.com) *(formerly polygon.io)* | Recommended |
| `NEWSAPI_KEY` | [newsapi.org](https://newsapi.org) | Optional |

> **Note:** Polygon.io rebranded as Massive.com (Oct 2025). Same keys, same endpoints, nothing changes.

---

## How It Works

```
Query → Ticker Extraction → Polygon (OHLCV + company info)
     → NewsAPI + VADER sentiment → FAISS RAG → Risk Engine
     → Gemini 2.5 Flash → structured JSON → React dashboard
```

Each analysis makes **3 Polygon calls** (aggs, ticker details, previous close) and is computed against **real 6-month OHLCV history**.

---

## Fallback Behaviour

The app never crashes when APIs are unavailable:

1. **Gemini fails** → pre-written rich analysis served for AAPL, TSLA, NVDA, MSFT
2. **Polygon fails** → hardcoded OHLCV data used for the same 4 tickers
3. **Unknown ticker + all APIs down** → neutral placeholder response

---

## Key Notes

- `faiss-cpu` must be **≥ 1.9.0** if you're on NumPy 2.x — older versions crash
- Polygon free tier: **5 req/min**, delayed data only
- Gemini free tier: rate-limited — fallback insights serve automatically on quota hit
- Embedding model: `models/text-embedding-004` (the deprecated `gemini-embedding-exp-03-07` was removed)

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Status check |
| GET | `/stock/{ticker}` | Price + indicators |
| GET | `/news/{ticker}` | Headlines + sentiment |
| POST | `/query/` | Full AI analysis |
| POST | `/rag/ingest` | Add to knowledge base |
| POST | `/rag/search` | Semantic search |

---

## Tests

```bash
cd backend && pytest tests/ -v
```

---

> ⚠️ For informational purposes only. Not financial advice.
