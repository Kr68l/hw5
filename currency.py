import aiohttp
import asyncio
import json
import sys
from datetime import datetime, timedelta

class ExchangeRateFetcher:
    PRIVATBANK_API_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    def __init__(self):
        self.dates_to_fetch = 10

    async def fetch_exchange_rate(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.PRIVATBANK_API_URL, params={'json': '', 'date': date.strftime('%d.%m.%Y')}) as response:
                data = await response.json()
                return data['exchangeRate']

    async def fetch_exchange_rates(self):
        today = datetime.now()
        exchange_rates = []

        for i in range(self.dates_to_fetch):
            current_date = today - timedelta(days=i)
            rates = await self.fetch_exchange_rate(current_date)
            exchange_rates.append({current_date.strftime('%d.%m.%Y'): {'EUR': rates[0]['saleRateNB'], 'USD': rates[1]['saleRateNB']}})

        return exchange_rates

async def main():
    days_to_fetch = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    if days_to_fetch <= 0 or days_to_fetch > 10:
        print("Error: Invalid number of days. Please choose a number between 1 and 10.")
        return

    exchange_rate_fetcher = ExchangeRateFetcher()
    exchange_rate_fetcher.dates_to_fetch = days_to_fetch

    exchange_rates = await exchange_rate_fetcher.fetch_exchange_rates()

    print(json.dumps(exchange_rates, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
