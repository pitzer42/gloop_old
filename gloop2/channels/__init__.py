from abc import (
    ABCMeta,
    abstractmethod
)


class Channel(metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    async def receive(self):
        raise NotImplemented()

    @abstractmethod
    async def send(self, message):
        raise NotImplemented()


async def create_channel(name):
    raise NotImplemented()


async def create_read_only_channel(name):
    raise NotImplemented()


async def create_write_only_channel(name):
    raise NotImplemented()


async def transform(
        func,
        channel_in: Channel,
        channel_out: Channel):

    message = await channel_in.receive()
    message = await func(message)
    if message is not None:
        await channel_out.send(message)


async def run_transformer(
        func,
        channel_in: Channel,
        channel_out: Channel):

    while True:
        await transform(func, channel_in, channel_out)
