from fastapi import APIRouter, HTTPException
from app.tools.stock_tool import get_stock_data

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.get("/{ticker}")
def get_stock(ticker: str, period: str = "6mo"):
    data = get_stock_data(ticker.upper(), period)
    if data.get("error") and "No live data" not in data.get("error", ""):
        raise HTTPException(status_code=404, detail=data["error"])
    return data
