from examples.mtg.repositories import decks
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

INITIAL_HAND_SIZE = 7
DECK_OPTIONS = (decks.DECK_ONE,)
DECK_SELECTION_MESSAGE = dict(
    msg='which deck do you want to use?',
    options=DECK_OPTIONS
)
POSITIVE = 'y'
NEGATIVE = 'n'
BINARY_OPTIONS = (POSITIVE, NEGATIVE)


async def _deck_selection(player: MtgRemotePlayer):
    option = None
    while option not in DECK_OPTIONS:
        await player.send(DECK_SELECTION_MESSAGE)
        option = await player.receive()
    player.deck = decks.get_by_name(option)


async def _initial_draw(player: MtgRemotePlayer):
    player.hand = player.deck.draw(n=INITIAL_HAND_SIZE)


async def _mulligan(player: MtgRemotePlayer):

    def create_mulligan_message(hand):
        return dict(
            msg='mulligan?',
            data=[repr(card) for card in hand],
            options=BINARY_OPTIONS
        )

    hand_size = len(player.hand)
    while hand_size > 0:
        msg = create_mulligan_message(player.hand)
        await player.send(msg)
        msg = await player.receive()
        if msg == POSITIVE:
            for card in player.hand:
                player.deck.append(card)
            player.deck.shuffle()
            hand_size -= 1
            player.hand = player.deck.draw(n=hand_size)
        else:
            break


async def setup(player: MtgRemotePlayer):
    await _deck_selection(player)
    await _initial_draw(player)
    await _mulligan(player)




