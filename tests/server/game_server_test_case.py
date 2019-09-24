from aiohttp.test_utils import AioHTTPTestCase

from gloop.web.server import create_game_app

from gloop.entities.remote_party import RemoteParty
from gloop.entities.remote_player import RemotePlayer


async def test_game_loop(player: RemotePlayer, party: RemoteParty):
    if player == party[0]:
        await party.broadcast(dict(
            message='game on'
        ))


class GameServerTestCase(AioHTTPTestCase):

    async def get_application(self):
        return create_game_app(
            game_loop=test_game_loop
        )
