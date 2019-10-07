import asyncio

import abc

import aioredis


class Channel(metaclass=abc.ABCMeta):

    def __init__(self, name):
        self.name = name

    async def receive(self):
        raise NotImplemented()

    async def send(self, message):
        raise NotImplemented()


async def create_channel(name):
    raise NotImplemented()


async def create_read_only_channel(name):
    raise NotImplemented()


async def create_write_only_channel(name):
    raise NotImplemented()


class RedisChannel(Channel):

    def __init__(self,
                 name: str,
                 pub: aioredis.Redis,
                 sub: aioredis.Channel):

        super(RedisChannel, self).__init__(name)
        self.pub = pub
        self.sub = sub

    async def receive(self):
        return await self.sub.get()

    async def send(self, message):
        await self.pub.publish(
            self.name,
            message
        )


async def redis_channel_factory(
            name,
            pub: aioredis.Redis = None,
            sub: aioredis.Redis = None) -> RedisChannel:

    if sub is None:
        sub = await aioredis.create_redis('redis://localhost')

    if pub is None:
        pub = await aioredis.create_redis('redis://localhost')

    sub = await sub.subscribe(name)
    sub = sub[0]
    return RedisChannel(name, pub, sub)


async def transform(
        func,
        channel_in: Channel,
        channel_out: Channel):

    message = await channel_in.receive()
    message = func(message)
    await channel_out.send(message)


async def run_transformer(
        func,
        channel_in: Channel,
        channel_out: Channel):

    while True:
        await transform(func, channel_in, channel_out)


if __name__ == '__main__':

    async def main():
        channel_1 = await redis_channel_factory('in')
        channel_2 = await redis_channel_factory('out')

        def increment(message):
            return int(message) + 1

        await run_transformer(increment, channel_1, channel_2)

    asyncio.run(main())
