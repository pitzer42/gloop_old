import asyncio

from typing import NoReturn

from gloop.models.remote_player import RemotePlayer


class RemoteParty(list):

    async def broadcast(self, message: str) -> NoReturn:
        player: RemotePlayer
        for player in self:
            await player.send(message)

    async def multicast(self, emitter: RemotePlayer, message: str) -> NoReturn:
        player: RemotePlayer
        for player in self:
            if player is not emitter:
                await player.send(message)


class RemotePartyFactory:

    def __init__(self, limit: int):
        self._limit = limit
        self._buffer = list()
        self._signals = list()
        self._party: RemoteParty = None

    async def gather(self, player: RemotePlayer) -> RemoteParty:
        self._party = None
        signal = asyncio.Event()
        self._buffer.append(player)
        self._signals.append(signal)
        if self._is_full():
            self._party = self._create_party()
        else:
            await signal.wait()
        return self._party

    def _is_full(self):
        return len(self._buffer) >= self._limit

    def _create_party(self):
        # TODO: test with a single loop
        party = RemoteParty()
        for player in self._buffer:
            party.append(player)
        self._buffer.clear()
        for signal in self._signals:
            signal.set()
        self._signals.clear()
        return party
