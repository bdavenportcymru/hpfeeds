import asyncio
from hpfeeds.asyncio import ClientSession


async def main():
    async with ClientSession('localhost', 10000, 'james', 'secret') as client:
        client.publish('mychan', b'{"data": "Hello World"}')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())