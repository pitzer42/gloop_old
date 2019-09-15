from typing import NoReturn

from gloop.models.remote_party import RemoteParty
from gloop.models.remote_player import RemotePlayer


async def default_game_loop(player: RemotePlayer, party: RemoteParty) -> NoReturn:
    raise NotImplemented()


async def empty_game_loop(player: RemotePlayer, party: RemoteParty) -> NoReturn:
    pass
