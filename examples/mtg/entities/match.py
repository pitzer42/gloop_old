from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer
from gloop.entities.remote_party import RemoteParty


class Match:

    def __init__(self, party: RemoteParty):
        self.party = [MtgRemotePlayer(remote) for remote in party]
        self.stack = list()

    def others(self, some_player):
        i = 0
        for remote in self.party:
            if remote.socket == some_player.socket:
                break
            i += 1
        return self.party[:i] + self.party[i+1:]
