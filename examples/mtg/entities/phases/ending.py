from examples.mtg.entities.phases import create_indexed_list

from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

MAX_HAND_SIZE = 7
SEPARATOR = ','


def create_discard_message(hand_size):
    return f'You have more than {MAX_HAND_SIZE} cards in you hand. Chose {hand_size - MAX_HAND_SIZE} ' \
           f'cards to be discarded.'


def create_discard_n_cards_message(hand: list) -> dict:
    return dict(
        message=create_discard_message(len(hand)),
        options=create_indexed_list(hand)
    )


async def _cleanup(player: MtgRemotePlayer):
    pass


async def _end(player: MtgRemotePlayer):
    async def ensure_right_sized_hand():
        while len(player.hand) > MAX_HAND_SIZE:
            msg = create_discard_n_cards_message(player.hand)
            await player.send(msg)
            cards_to_discard = await player.receive()
            try:
                cards_to_discard = cards_to_discard.split(SEPARATOR)
                cards_to_discard = [int(i) for i in cards_to_discard]
            except ValueError:
                continue
            over_sized_hand = list(player.hand)

            for card_index in cards_to_discard:
                if card_index < 0 or card_index >= len(over_sized_hand):
                    continue

            for card_index in cards_to_discard:
                card = over_sized_hand[card_index]
                player.hand.remove(card)
                player.graveyard.append(card)

    await ensure_right_sized_hand()
    player.resources = 0


async def ending(player: MtgRemotePlayer, match):
    await _cleanup(player)
    await _end(player)
