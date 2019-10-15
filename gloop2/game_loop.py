import asyncio

from random import randint

from gloop.web import app_schema
from gloop2.channels.redis import create_channel

clients = list()
match_channel = None
new_match_channel = None


async def loop():
    for i in range(0, 10):
        await match_channel.send(i)


async def listen_to_channel(name=None):
    global match_channel
    global new_match_channel

    match_channel_name = str(randint(1000, 9999)) if name is None else name

    match_channel = await create_channel(match_channel_name)

    await loop()

if __name__ == '__main__':
    asyncio.run(listen_to_channel())


