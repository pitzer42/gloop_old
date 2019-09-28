from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer
from gloop.entities.remote_party import RemoteParty


class Stack(list):

    def solve(self):
        for effect in self:
            effect.apply()
        self.clear()


class Match:

    def __init__(self, party: RemoteParty):
        self.party = party
        self.stack = Stack()

    def others(self, some_player):
        i = self.party.index(some_player)
        return self.party[:i] + self.party[i+1:]
