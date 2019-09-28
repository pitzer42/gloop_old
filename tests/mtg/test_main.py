from unittest import TestCase

from examples.mtg.entities.phases.setup import setup
from examples.mtg.entities.phases.beginning import beginning
from examples.mtg.entities.phases.main import main

from examples.mtg.entities.match import Match
from gloop.entities.remote_party import RemoteParty

from tests.mtg.scripted_player import (
    MtgBot,
    chose,
    chose_card
)

from tests.utils import sync


class TestMain(TestCase):

    @sync
    async def test_smoke(self):

        player_two_was_prompted = [False]

        def register_prompt_and(chose_func):
            def wrapper(message):
                player_two_was_prompted[0] = True
                return chose_func(message)
            return wrapper

        player_one = MtgBot(
            chose(),
            chose(i=1),
            chose(0),
            chose_card('Plains'),
            chose(2)
        )

        player_two = MtgBot(
            chose(),
            chose(i=1),
            register_prompt_and(chose(i=2))
        )

        party = RemoteParty()
        party.append(player_one)
        party.append(player_two)

        match = Match(party)

        await setup(player_one)
        await setup(player_two)
        await beginning(player_one)
        await beginning(player_two)

        await main(player_one, match)

        self.assertTrue(player_two_was_prompted[0])
