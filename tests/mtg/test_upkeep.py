from unittest import TestCase

from examples.mtg.entities.game_steps.upkeep import upkeep
from examples.mtg.entities.game_steps.setup import setup

from tests.mtg.scripted_player import (
    MtgBot,
    chose
)

from tests.utils import sync


class TestUpkeep(TestCase):

    @sync
    async def test_upkeep_step(self):
        player = MtgBot(
            chose()
        )
        await setup(player)
        hand_size = len(player.hand)
        deck_size = len(player.deck)

        await upkeep(player)
        new_hand_size = len(player.hand)
        new_deck_size = len(player.deck)

        self.assertEqual(hand_size + 1, new_hand_size)
        self.assertEqual(deck_size - 1, new_deck_size)
        for card in player.field:
            self.assertFalse(card.is_tapped())
