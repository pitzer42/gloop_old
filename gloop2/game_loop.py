import asyncio

from random import randint

from gloop.web import app_schema
from gloop2.channels.channel import create_channel

clients = list()
match_channel = None
new_match_channel = None


async def loop(message):
    for i in range(0, 10):
        await match_channel.publish(i)


async def listen_to_channel():
    global match_channel
    global new_match_channel

    match_channel_name = str(randint(1000, 9999))

    match_channel = await create_channel(match_channel_name)
    new_match_channel = await create_channel(app_schema.new_match_channel)

    await new_match_channel.publish(match_channel_name)

    task = await match_channel.subscribe(loop)
    await task

if __name__ == '__main__':
    asyncio.run(listen_to_channel())


