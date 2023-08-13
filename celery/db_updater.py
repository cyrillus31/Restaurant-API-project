import asyncio
import aiohttp

from .xlsx_parser import parser



async def call_url(session, url):
    async with session.post(url) as response:
        return await response.text()

async def main():
    urls = ["https://example.com", "https://example.org", "https://example.net"]
    async with aiohttp.ClientSession() as session:
        tasks = [call_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)

asyncio.run(main())