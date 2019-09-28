from gloop.entities.remote_player import RemotePlayer


class Field(list):

    def untap(self):
        for card in self:
            card.untap()


class MtgRemotePlayer(RemotePlayer):

    def __init__(self, player: RemotePlayer):
        self._player = player
        self.deck = None
        self.hand = list()
        self.field = Field()
        self.graveyard = list()
        self.resources = 0

    async def send(self, message: str):
        return await self._player.send(message)

    async def receive(self) -> str:
        return await self._player.receive()
