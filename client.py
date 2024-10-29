import aiohttp
import asyncio
from datetime import datetime
from typing import Dict
from database import database, prices
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://www.deribit.com/api/v2/public/get_index_price"


class DeribitClient:
    def __init__(self):
        self.tickers = ["btc_usd", "eth_usd"]

    async def fetch_price(self, ticker: str) -> Dict[str, float]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{API_URL}?index_name={ticker}") as response:
                    data = await response.json()
                    price = data.get('result', {}).get('index_price')
                    if price is not None:
                        logger.info(f"Price recieved: {ticker}: {price}")
                        return {
                            "ticker": ticker,
                            "price": price,
                            "timestamp": int(datetime.now().timestamp())
                        }
                    else:
                        logger.error(f"Error getting price for: {ticker}")
            except Exception as e:
                logger.error(f"Error getting data for: {ticker}: {e}")
        return {}

    async def save_price(self, data: Dict[str, float]):
        if data:
            query = prices.insert().values(
                ticker=data['ticker'],
                price=data['price'],
                timestamp=data['timestamp']
            )
            await database.execute(query)
            logger.info(f"Saved to db: {data}")

    async def fetch_and_save(self):
        tasks = [self.fetch_price(ticker) for ticker in self.tickers]
        results = await asyncio.gather(*tasks)
        for result in results:
            await self.save_price(result)

    async def start(self):
        await database.connect()
        try:
            while True:
                await self.fetch_and_save()
                await asyncio.sleep(60)
        finally:
            await database.disconnect()


if __name__ == "__main__":
    client = DeribitClient()
    asyncio.run(client.start())
