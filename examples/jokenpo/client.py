import asyncio

import aiohttp


async def run_client():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://0.0.0.0:8080/play') as ws:
        msg = await ws.receive_json()
        print(msg['message'])
        while True:
            msg = await ws.receive_json()
            print(msg['message'])
            await ws.send_json(dict(
                data=input()
            ))
            msg = await ws.receive_json()
            print(msg['message'])

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_client())
    loop.close()

