import sys
import asyncio
import aiohttp


async def run_client():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://0.0.0.0:8080') as ws:

        async def input_loop():
            msg = 0
            while msg is not None:
                msg = input()
                if msg != '':
                    await ws.send_str(msg)
                    await asyncio.sleep(1)

        async def output_loop():
            msg = 0
            while msg is not None:
                msg = await ws.receive()
                msg = str(msg.data)
                print(msg)
                if msg is None:
                    return 1
                await asyncio.sleep(1)

        if len(sys.argv) > 1:
            await input_loop()
        else:
            await output_loop()

if __name__ == '__main__':
    asyncio.run(run_client())
