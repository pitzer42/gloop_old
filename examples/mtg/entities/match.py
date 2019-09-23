from gloop.models.remote_party import RemoteParty


class Match:

    def __init__(self, party: RemoteParty):
        self.party = party
        self.stack = list()
