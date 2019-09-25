from unittest import TestCase

from gloop.entities.remote_party import RemoteParty

from examples.mtg.entities.loop import mtg_game_loop

from tests.mtg.scripted_player import (
    ScriptedPlayer,
    chose
)
from tests.utils import sync


class TestEndToEnd(TestCase):

    @sync
    async def test_end_to_end(self):
        player_1 = ScriptedPlayer(
            chose()
        )

        player_2 = ScriptedPlayer(
            chose()
        )

        party = RemoteParty()
        party.append(player_1)
        party.append(player_2)

        await mtg_game_loop(player_1, party)
