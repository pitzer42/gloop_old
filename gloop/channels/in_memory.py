import asyncio
from gloop.channels import Channel

__CHANNELS__ = dict()


class InMemoryChannel(Channel):

    def __init__(self, name):
        self._index = -1
        self._name = name
        self._channel = None

    async def open(self):
        if self._name not in __CHANNELS__:
            __CHANNELS__[self._name] = list()
        self._channel = __CHANNELS__[self._name]

    async def receive(self):
        self._index += 1
        while len(self._channel) <= self._index:
            await asyncio.sleep(1)
        return self._channel[self._index]

    async def send(self, message):
        return self._channel.append(message)

    async def close(self):
        del self
