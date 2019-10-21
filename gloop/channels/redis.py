import aioredis

from gloop.channels import Channel

DEFAULT_REDIS_ADDRESS = 'redis://localhost:6379'
MESSAGE_KEY = b'message'


class RedisChannel(Channel):

    def __init__(
            self,
            name: str,
            address: str = DEFAULT_REDIS_ADDRESS):
        self._name = name
        self._address = address
        self._redis = None

    async def open(self):
        self._redis = await aioredis.create_redis(self._address)

    async def receive(self):
        streams = [self._name]
        record = await self._redis.xread(streams)
        binary_message = record[0][2][MESSAGE_KEY]
        return binary_message.decode()

    async def send(self, message):
        record = {
            MESSAGE_KEY: message
        }
        return await self._redis.xadd(
            self._name,
            record
        )

    async def close(self):
        self._redis.close()
        await self._redis.wait_closed()
