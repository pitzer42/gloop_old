from random import shuffle
from examples.mtg.entities.card import Card
from examples.mtg.entities.deck import Deck

DECK_ONE = 'deck_one'


def create_deck_one():
    deck = Deck()
    for i in range(4):
        deck.append(Card('Serra Angel', 5))
        deck.append(Card('Plains', 0))
    shuffle(deck)
    return deck


FACTORY_MAP = {
    DECK_ONE: create_deck_one
}


def get_by_name(deck_name):
    factory = FACTORY_MAP.get(deck_name)
    return factory()