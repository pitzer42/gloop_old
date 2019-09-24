from gloop.entities.remote_player import RemotePlayer
from gloop.web.ws_player import WebSocketPlayer


class Field(list):

    def untap(self):
        for card in self:
            card.untap()


class MtgRemotePlayer(WebSocketPlayer):

    def __init__(self, player: RemotePlayer):
        self.socket = player.socket
        self._player = player
        self.deck = None
        self.hand = list()
        self.field = Field()
        self.graveyard = list()
        self.resources = 0
