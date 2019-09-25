from unittest import TestCase

from examples.mtg.entities.game_steps.mulligan import mulligan
from examples.mtg.entities.game_steps.setup import setup

from tests.mtg.scripted_player import (
    MtgBot,
    chose
)

from tests.utils import sync


class TestMulligan(TestCase):

    @sync
    async def test_mulligan_step(self):
        player = MtgBot(
            chose(),
            chose(i=1)
        )
        await setup(player)
        await mulligan(player)

        hand_size = len(player.hand)
        deck_size = len(player.deck)

        await upkeep(player)
        new_hand_size = len(player.hand)
        new_deck_size = len(player.deck)

        self.assertEqual(hand_size + 1, new_hand_size)
        self.assertEqual(deck_size - 1, new_deck_size)
        for card in player.field:
            self.assertFalse(card.is_tapped())
