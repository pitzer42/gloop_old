from unittest import TestCase

from examples.mtg.entities.game_steps.setup import setup

from tests.mtg.scripted_player import (
    MtgBot,
    chose
)

from tests.utils import sync


class TestSetup(TestCase):

    @sync
    async def test_setup_step(self):
        player = MtgBot(
            chose()
        )
        await setup(player)
        self.assertIsNotNone(player.deck)
