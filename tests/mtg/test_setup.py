from unittest import TestCase

from examples.mtg.entities.phases.setup import _deck_selection as deck_selection
from examples.mtg.entities.phases.setup import _initial_draw as initial_draw
from examples.mtg.entities.phases.setup import _mulligan as mulligan
from examples.mtg.entities.phases.setup import INITIAL_HAND_SIZE

from tests.mtg.scripted_player import (
    MtgBot,
    chose
)

from tests.utils import sync


class TestSetup(TestCase):

    @sync
    async def test_deck_selection_step(self):
        player = MtgBot(
            chose()
        )
        await deck_selection(player)
        self.assertIsNotNone(player.deck)

    @sync
    async def test_initial_draw_step(self):
        player = MtgBot(
            chose()
        )
        await deck_selection(player)
        deck_size = len(player.deck)

        await initial_draw(player)
        hand_size = len(player.hand)
        new_deck_size = len(player.deck)

        self.assertEqual(hand_size, INITIAL_HAND_SIZE)
        self.assertEqual(deck_size - INITIAL_HAND_SIZE, new_deck_size)

    @sync
    async def test_do_not_mulligan(self):
        player = MtgBot(
            chose(),
            chose(i=1)
        )
        await deck_selection(player)
        await initial_draw(player)
        await mulligan(player)
        hand_size = len(player.hand)
        self.assertEqual(hand_size, INITIAL_HAND_SIZE)

    @sync
    async def test_mulligan_n_times(self):
        n = 4
        expected_hand_size = INITIAL_HAND_SIZE - n

        player = MtgBot(
            *[chose()]*(n+1)
        )

        await deck_selection(player)
        await initial_draw(player)
        await mulligan(player)
        hand_size = len(player.hand)
        self.assertEqual(hand_size, expected_hand_size)

    @sync
    async def test_mulligan_10_times(self):
        n = 10
        expected_hand_size = 0

        player = MtgBot(
            *[chose()] * (n + 1)
        )

        await deck_selection(player)
        await initial_draw(player)
        await mulligan(player)
        hand_size = len(player.hand)
        self.assertEqual(hand_size, expected_hand_size)



