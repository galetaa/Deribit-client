from httpx import AsyncClient
from main import app
import pytest
import asyncio
from main import database


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_database():
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_all_prices(async_client):
    response = await async_client.get("/prices", params={"ticker": "btc_usd"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_latest_price(async_client):
    response = await async_client.get("/prices/latest", params={"ticker": "btc_usd"})
    assert response.status_code == 200
    data = response.json()
    assert "price" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_get_prices_with_filter(async_client):
    start_date = 1633046400
    end_date = 1633132800
    response = await async_client.get(
        "/prices/filter",
        params={"ticker": "btc_usd", "start_date": start_date, "end_date": end_date}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
