import asyncio

from random import randint

from gloop2.channels import run_transformer
from gloop2.channels.redis import create_channel
from gloop2.channels.redis import create_write_only_channel
from gloop2.channels.redis import create_read_only_channel
from gloop2.channels.redis import RedisChannel

MATCH_SIZE = 2
clients = list()
waiting_list: RedisChannel = None
new_match: RedisChannel = None


async def init_channels():
    global waiting_list
    global new_match

    waiting_list = await create_read_only_channel('waiting_list')
    new_match = await create_write_only_channel('new_match')


async def launch_match(message):
    global clients
    clients.append(message)
    if len(clients) == MATCH_SIZE:
        match_name = str(randint(1000, 9999))
        # match = await create_channel(match_name)
        clients.clear()
        return match_name


async def main():
    await init_channels()
    await run_transformer(
        launch_match,
        waiting_list,
        new_match
    )


if __name__ == '__main__':
    asyncio.run(main())
