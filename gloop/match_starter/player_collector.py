import random
import asyncio

from gloop.channels import Channel
from gloop.channels import transform_loop

from gloop.match_starter import (
    channel_factory,
    WAITING_LIST_CHANNEL_NAME,
    NEW_MATCHES_CHANNEL_NAME,
    MATCH_SIZE
)


async def collect_players_loop(
        waiting_list_channel: Channel,
        new_match_channel: Channel,
        match_size: int):

    buffer = list()

    await waiting_list_channel.open()
    await new_match_channel.open()

    await transform_loop(
        collect_players(buffer, match_size),
        waiting_list_channel,
        new_match_channel
    )


def collect_players(buffer, match_size):

    async def _collect(player):
        buffer.append(player)
        if len(buffer) == match_size:
            match_id = generate_match_id()
            new_match_message = match_id + ' '
            new_match_message += ' '.join(buffer)
            buffer.clear()
            print(new_match_message)
            return new_match_message

    return _collect


def generate_match_id():
    return str(random.randint(100000, 999999))


if __name__ == '__main__':
    asyncio.run(
        collect_players_loop(
            channel_factory(WAITING_LIST_CHANNEL_NAME),
            channel_factory(NEW_MATCHES_CHANNEL_NAME),
            MATCH_SIZE
        )
    )


