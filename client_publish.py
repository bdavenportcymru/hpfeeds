import asyncio
from hpfeeds.asyncio import ClientSession


async def main():
    async with ClientSession('157.245.114.100', 10000, 'HONEYPOT', 'H0N3YP0T4U') as client:
        client.publish('mychan', b'{"data": "Hello World"}')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())