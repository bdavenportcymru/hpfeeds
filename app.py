import asyncio
from hpfeeds.asyncio import ClientSession


async def main():
    async with ClientSession('localhost', 10000, 'james', 'secret') as client:
        client.subscribe('mychan')

        async for ident, channel, payload in client:
            print(channel)
            print(ident)
            print(payload)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())