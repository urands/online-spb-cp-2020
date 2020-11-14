import asyncio
import os
from aiohttp import ClientSession, ClientResponseError
# from aiohttp_retry import RetryClient, RetryOptions

async def fetch(url, body, session):
    async with session.post(url,json=body) as response:
        if response.status not in (200, 429,):
            raise ClientResponseError()
        print(response.status)
        print(response)
        return await response.json()


async def bound_fetch(sem, url, body, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, body, session)

async def fetch_address(address_list):
    url = os.getenv('POCHTA_URL', "https://address.pochta.ru/validate/api/v7_1")
    headers = {
        "AuthCode": os.getenv('POCHTA_TOKEN', "53fb9daa-7f06-481f-aad6-c6a7a58ec0bb"),
    }
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(int(os.getenv('POCHTA_DDOS_LIMIT', 1000)))

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession(headers=headers) as session:
        for val in address_list:
            body = {
                "addr": [{"val": val}],
                "version": "demo",
                "reqId": "12204cb4-37fb-4059-91e6-c6e17e946d77"
            }

            task = asyncio.ensure_future(
                bound_fetch(sem, url, body, session)
            )
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        return await responses





