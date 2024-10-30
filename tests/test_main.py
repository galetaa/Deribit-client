import pytest
from aiohttp import ClientSession

BASE_URL = "http://fastapi:8000"


@pytest.mark.asyncio
async def test_get_all_prices():
    async with ClientSession() as session:
        async with session.get(f"{BASE_URL}/prices", params={"ticker": "btc_usd"}) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_latest_price():
    async with ClientSession() as session:
        async with session.get(f"{BASE_URL}/prices/latest", params={"ticker": "btc_usd"}) as response:
            assert response.status == 200
            data = await response.json()
            assert "price" in data
            assert "timestamp" in data


@pytest.mark.asyncio
async def test_non_existent_endpoint():
    async with ClientSession() as session:
        async with session.get(f"{BASE_URL}/nonexistent") as response:
            assert response.status == 404


@pytest.mark.asyncio
async def test_missing_ticker_parameter():
    async with ClientSession() as session:
        async with session.get(f"{BASE_URL}/prices") as response:
            assert response.status == 422


@pytest.mark.asyncio
async def test_invalid_ticker_parameter():
    async with ClientSession() as session:
        async with session.get(f"{BASE_URL}/prices", params={"ticker": "invalid_ticker"}) as response:
            assert response.status == 404
            data = await response.json()
            assert "detail" in data


@pytest.mark.asyncio
async def test_filter_with_no_results():
    start_date = 1234567890
    end_date = 1234567891
    async with ClientSession() as session:
        async with session.get(
                f"{BASE_URL}/prices/filter",
                params={"ticker": "btc_usd", "start_date": start_date, "end_date": end_date}
        ) as response:
            assert response.status == 404


@pytest.mark.asyncio
async def test_invalid_date_format():
    async with ClientSession() as session:
        async with session.get(
                f"{BASE_URL}/prices/filter",
                params={"ticker": "btc_usd", "start_date": "not_a_timestamp", "end_date": "also_not_a_timestamp"}
        ) as response:
            assert response.status == 422


@pytest.mark.asyncio
async def test_unsupported_method():
    async with ClientSession() as session:
        async with session.post(f"{BASE_URL}/prices", params={"ticker": "btc_usd"}) as response:
            assert response.status == 405


@pytest.mark.asyncio
async def test_price_data_structure():
    async with ClientSession() as session:
        async with session.get(f"{BASE_URL}/prices/latest", params={"ticker": "btc_usd"}) as response:
            assert response.status == 200
            data = await response.json()
            assert isinstance(data["price"], (float, int))
            assert isinstance(data["timestamp"], int)
