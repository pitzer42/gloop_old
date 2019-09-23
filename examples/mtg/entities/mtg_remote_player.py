from gloop.models.remote_player import RemotePlayer
from gloop.web.ws_player import WebSocketPlayer


class Deck(list):

    def draw(self, n=1):
        drawn = list()
        for i in range(n):
            card = self.pop()
            drawn.append(card)
        if n == 1:
            return drawn[0]
        return drawn


class Field(list):

    def untap(self):
        for card in self:
            card.untap()


class MtgRemotePlayer(WebSocketPlayer):

    def __init__(self, player: RemotePlayer):
        self.socket = player.socket
        self._player = player
        self.deck = Deck()
        self.hand = list()
        self.field = Field()
        self.graveyard = list()