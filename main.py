from fastapi import FastAPI, HTTPException, status
from database import database
from sqlalchemy import select
from pydantic import BaseModel
from database import prices
from prometheus_client import Counter, generate_latest
from starlette.responses import Response

app = FastAPI()
REQUEST_COUNT = Counter('request_count', 'API Request Count', ['method', 'endpoint'])


class PriceData(BaseModel):
    ticker: str
    price: float
    timestamp: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/prices", response_model=list[PriceData])
async def get_all_prices(ticker: str):
    query = select(prices).where(prices.c.ticker == ticker)
    rows = await database.fetch_all(query)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return rows


@app.get("/prices/latest", response_model=PriceData)
async def get_latest_price(ticker: str):
    query = (
        select(prices)
        .where(prices.c.ticker == ticker)
        .order_by(prices.c.timestamp.desc())
        .limit(1)
    )
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    return row


@app.get("/prices/filter", response_model=list[PriceData])
async def get_prices_with_filter(ticker: str, start_date: int, end_date: int):
    query = (
        select(prices)
        .where(prices.c.ticker == ticker)
        .where(prices.c.timestamp >= start_date)
        .where(prices.c.timestamp <= end_date)
    )
    rows = await database.fetch_all(query)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for specified date range")
    return rows


@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    return response


@app.get("/metrics")
async def get_metrics():
    return Response(generate_latest(), media_type="text/plain")
