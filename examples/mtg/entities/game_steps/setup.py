import random

from gloop.entities.remote_player import RemotePlayer

from examples.mtg.entities.deck import Deck
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

MESSAGE = 'which deck do you want to use?'
DECK_1='deck_one'
ANSWER_OPTIONS = (DECK_1, )


def create_message():
    return dict(
        msg=MESSAGE,
        options=ANSWER_OPTIONS
    )


class Card:

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


def deck_1():
    deck = Deck()
    for i in range(4):
        deck.append(Card('Serra Angel', 5))
        deck.append(Card('Plains', 0))
    random.shuffle(deck)
    return deck


async def setup(player: MtgRemotePlayer):

    msg = create_message()
    deck_option = None

    while deck_option not in ANSWER_OPTIONS:
        await player.send(msg)
        deck_option = await player.receive()

    deck_factory = {
        DECK_1: deck_1
    }.get(deck_option)

    player.deck = deck_factory()
