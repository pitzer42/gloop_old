import asyncio
import aioredis

from gloop2.channels import Channel, run_transformer


class RedisChannel(Channel):

    def __init__(self,
                 name: str,
                 pub: aioredis.Redis,
                 sub: aioredis.Channel):

        super(RedisChannel, self).__init__(name)
        self.pub = pub
        self.sub = sub

    async def receive(self):
        if not self.sub:
            raise Exception(f'{self.name} is a write-only channel')
        return await self.sub.get()

    async def send(self, message):
        if not self.pub:
            raise Exception(f'{self.name} is a read-only channel')
        await self.pub.publish(
            self.name,
            message
        )


async def create_channel(
            name: str,
            pub: aioredis.Redis = None,
            sub: aioredis.Redis = None) -> RedisChannel:

    if sub is None:
        sub = await aioredis.create_redis('redis://localhost')

    if pub is None:
        pub = await aioredis.create_redis('redis://localhost')

    sub = await sub.subscribe(name)
    sub = sub[0]
    return RedisChannel(name, pub, sub)


async def create_read_only_channel(
            name: str,
            sub: aioredis.Redis = None) -> RedisChannel:

    if sub is None:
        sub = await aioredis.create_redis('redis://localhost')

    sub = await sub.subscribe(name)
    sub = sub[0]
    return RedisChannel(name, False, sub)


async def create_write_only_channel(
            name: str,
            pub: aioredis.Redis = None) -> RedisChannel:

    if pub is None:
        pub = await aioredis.create_redis('redis://localhost')

    return RedisChannel(name, pub, False)

if __name__ == '__main__':

    async def main():
        channel_1 = await create_read_only_channel('in')
        channel_2 = await create_write_only_channel('out')

        def increment(message):
            return int(message) + 1

        await run_transformer(increment, channel_1, channel_2)

    asyncio.run(main())
