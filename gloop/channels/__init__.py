from abc import (
    ABCMeta,
    abstractmethod
)


class BreakTransformLoop(Exception):
    pass


class Channel(metaclass=ABCMeta):

    @abstractmethod
    async def open(self):
        raise NotImplemented()

    @abstractmethod
    async def receive(self):
        raise NotImplemented()

    @abstractmethod
    async def send(self, message):
        raise NotImplemented()

    @abstractmethod
    async def close(self):
        raise NotImplemented()


async def transform_step(
        f,
        channel_in: Channel,
        channel_out: Channel):

    x = await channel_in.receive()
    y = await f(x)
    if y is not None:
        await channel_out.send(y)
    return y


async def transform_loop(
        func,
        channel_in: Channel,
        channel_out: Channel):

    try:
        while True:
            await transform_step(
                func,
                channel_in,
                channel_out
            )
    except BreakTransformLoop:
        pass
