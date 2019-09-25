from unittest import TestCase

from examples.mtg.entities.phases.setup import setup
from examples.mtg.entities.phases.beginning import _untap as untap
from examples.mtg.entities.phases.beginning import _upkeep as _upkeep
from examples.mtg.entities.phases.beginning import _draw as draw


from tests.mtg.scripted_player import (
    MtgBot,
    chose
)

from tests.utils import sync


class TestUpkeep(TestCase):

    @sync
    async def test_untap_step(self):
        player = MtgBot(
            chose(),
            chose()
        )
        await setup(player)

        card = player.hand.pop()
        card.tap()
        player.field.append(card)

        await untap(player)

        self.assertFalse(card.is_tapped)

    @sync
    async def test_upkeep_step(self):
        pass

    @sync
    async def test_draw_step(self):
        player = MtgBot(
            chose(),
            chose()
        )
        await setup(player)
        hand_size = len(player.hand)
        deck_size = len(player.deck)

        await draw(player)
        new_hand_size = len(player.hand)
        new_deck_size = len(player.deck)

        self.assertEqual(hand_size + 1, new_hand_size)
        self.assertEqual(deck_size - 1, new_deck_size)