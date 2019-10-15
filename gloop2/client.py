
import asyncio

import aiohttp


async def run_client():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://0.0.0.0:8080') as ws:
        while True:
            msg = await ws.receive_str()
            print(msg)

            """
            msg = input()
            if msg != '':
                print(f'sending "{msg}"')
                await ws.send_json(msg)
            """

if __name__ == '__main__':
    asyncio.run(run_client())
