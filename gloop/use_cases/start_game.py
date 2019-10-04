from gloop.entities.remote_player import RemotePlayer
from gloop.entities.remote_party import RemotePartyFactory

ACK_MESSAGE = dict(
    message='waiting for other players to join the party.'
)


class StartGame:

    def __init__(self, game_loop, remote_party_factory: RemotePartyFactory):
        self.game_loop = game_loop
        self.remote_party_factory = remote_party_factory

    async def start_game(self, player: RemotePlayer):
        await player.send(ACK_MESSAGE)
        party = await self.remote_party_factory.gather(player)
        await self.game_loop(player, party)
