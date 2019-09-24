from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

INQUIRE_MESSAGE = 'what do you want to do?'
PLAY_FROM_HAND = 'play_from_hand'
PLAYER_FROM_FIELD = 'play_from_field'
NOTHING = 'nothing'
ANSWER_OPTIONS = (
    PLAY_FROM_HAND,
    PLAYER_FROM_FIELD,
    NOTHING
)


async def play_from_hand(player: MtgRemotePlayer, match):
    options = list()
    indexer = 0
    for card in player.hand:
        options.append(
            f'{indexer}-{card}'
        )
        indexer += 1
    index = None
    while index is None:
        msg = dict(
            msg='which card do you want to play?',
            options=options
        )
        await player.send(msg)
        try:
            index = await player.receive()
            index = int(index)
            while 0 <= index < len(player.hand):
                card = player.hand[index]
                if player.resources >= card.cost:
                    player.resources -= card.cost
                    match.stack.append(card)
                    return
                else:
                    msg = dict(
                        msg='you do not have enough resources to play this'
                    )
                    await player.send(msg)
                    raise ValueError(msg)
        except ValueError:
            index = None


async def play_from_field(player: MtgRemotePlayer, match):
    pass

move_switch = {
    PLAY_FROM_HAND: play_from_hand,
    PLAYER_FROM_FIELD: play_from_field
}


def create_message():
    return dict(
        msg=INQUIRE_MESSAGE,
        options=ANSWER_OPTIONS
    )


async def main_phase(player: MtgRemotePlayer, match):
    msg = create_message()
    await player.send(msg)
    move_msg = await player.receive()
    while move_msg != NOTHING and move_msg in ANSWER_OPTIONS:
        move = move_switch.get(move_msg)
        await move(player, match)
        msg = create_message()
        move_msg = await player.send(msg)

    others = match.others(player)
    other = others[0]
    await main_phase(other, match)

    print(match.stack)
    # resolve stack




