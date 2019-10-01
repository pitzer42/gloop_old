from examples.mtg.entities.phases import create_indexed_list

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

MAIN_PHASE_MESSAGE = dict(
    msg=INQUIRE_MESSAGE,
    options=ANSWER_OPTIONS
)


async def main(player: MtgRemotePlayer, match):
    await player.send(MAIN_PHASE_MESSAGE)
    move_msg = await player.receive()

    while move_msg != NOTHING and move_msg in ANSWER_OPTIONS:
        move = move_map.get(move_msg)
        await move(player, match)

        other = match.others(player)[0]
        await other.send(MAIN_PHASE_MESSAGE)
        move_msg = await other.receive()

        if move_msg != NOTHING and move_msg in ANSWER_OPTIONS:
            move = move_map.get(move_msg)
            await move(other, match)
            move_msg = await player.send(MAIN_PHASE_MESSAGE)

    match.stack.solve()


async def play_from_hand(player: MtgRemotePlayer, match):
    not_enought_resources_message = dict(
        msg='you do not have enough resources to play this'
    )

    def create_hand_options_message():

        return dict(
            msg='which card do you want to play?',
            options=create_indexed_list(player.hand)
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

    def create_field_options_message():
        counter = 0
        options = list()
        for card in player.field:
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
        msg = create_field_options_message()
        await player.send(msg)
        try:
            index = await player.receive()
            index = int(index)
            while 0 <= index < len(player.field):
                card = player.field[index]
                match.stack.append(card)
        except ValueError:
            index = None

move_map = {
    PLAY_FROM_HAND: play_from_hand,
    PLAYER_FROM_FIELD: play_from_field
}




