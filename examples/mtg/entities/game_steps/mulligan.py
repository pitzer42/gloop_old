import random

from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

INITIAL_HAND_SIZE = 7
INQUIRE_MESSAGE = 'mulligan?'
POSITIVE = 'y'
NEGATIVE = 'n'
ANSWER_OPTIONS = (POSITIVE, NEGATIVE)


def create_message(hand):
    return dict(
        msg='mulligan?',
        data=[repr(card) for card in hand],
        options=('y', 'n')
    )


async def mulligan(player: MtgRemotePlayer):
    required_mulligan = True
    hand_size = INITIAL_HAND_SIZE
    while required_mulligan and hand_size > 0:
        player.hand = player.deck.draw(n=hand_size)
        msg = create_message(player.hand)
        await player.send(msg)
        msg = await player.receive()
        required_mulligan = msg == POSITIVE
        if required_mulligan:
            for card in player.hand:
                player.deck.append(card)
            random.shuffle(player.deck)
            hand_size -= 1
