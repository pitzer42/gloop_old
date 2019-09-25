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
    not_enought_resources_message = dict(
        msg='you do not have enough resources to play this'
    )

    def create_hand_options_message():
        counter = 0
        options = list()
        for card in player.hand:
            options.append(
                f'{counter}-{card}'
            )
            counter += 1
        return dict(
            msg='which card do you want to play?',
            options=options
        )

    index = None
    while index is None:
        msg = create_hand_options_message()
        await player.send(msg)
        try:
            index = await player.receive()
            index = int(index)
            while 0 <= index < len(player.hand):
                card = player.hand[index]
                if player.resources >= card.cost:
                    player.resources -= card.cost
                    player.hand.pop(index)
                    match.stack.append(card)
                    return
                else:
                    await player.send(not_enought_resources_message)
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


async def main(player: MtgRemotePlayer, match):
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
    await main(other, match)

    print(match.stack)
    # resolve stack




