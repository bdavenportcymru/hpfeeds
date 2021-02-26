import asyncio
from hpfeeds.asyncio import ClientSession


async def main():
    async with ClientSession('x.x.x.x', 10000, 'IDENT', 'secret_password') as client:
        client.publish('channel_name', b'{"data": "Hello World"}')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())