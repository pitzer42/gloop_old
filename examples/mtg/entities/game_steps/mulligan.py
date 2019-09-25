import random

from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

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
    hand_size = len(player.hand)
    while hand_size > 0:
        msg = create_message(player.hand)
        await player.send(msg)
        msg = await player.receive()
        if msg == POSITIVE:
            for card in player.hand:
                player.deck.append(card)
            random.shuffle(player.deck)
            hand_size -= 1
            player.hand = player.deck.draw(n=hand_size)
        else:
            break
