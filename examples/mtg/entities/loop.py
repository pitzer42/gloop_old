import random

from examples.mtg.entities.match import Match
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

from gloop.models.remote_party import RemoteParty
from gloop.models.remote_player import RemotePlayer


async def mtg_game_loop(main_player: RemotePlayer, party: RemoteParty):

    main_player = MtgRemotePlayer(main_player)
    await main_player.send('starting match')

    match = Match(party)
    hand = main_player.hand
    field = main_player.field
    deck = main_player.deck

    for i in range(4):
        deck.append('Serra Angel')
        deck.append('Plains')
    random.shuffle(deck)

    hand_size = 7
    required_mulligan = True

    while required_mulligan and hand_size > 0:
        hand = deck.draw(n=hand_size)
        msg = dict(
            hand=hand
        )
        await main_player.send(msg)
        await main_player.send('mulligan?(y/n)')
        msg = await main_player.receive()
        required_mulligan = msg == 'y'

        # mulligan step
        if required_mulligan:
            for card in hand:
                deck.append(card)
            random.shuffle(deck)
            hand_size -= 1

    # game-over by empty hand
    if hand_size == 0:
        msg = dict(
            msg='you have lost'
        )
        await main_player.send(msg)

        msg = dict(
            msg=f'{main_player.id} have lost'
        )
        await main_player.send(msg)

    random.shuffle(party)

    field.untap()

    card = deck.draw()
    hand.append(card)

    msg = dict(
        hand=hand,
        field=field
    )
    await main_player.send(msg)

    move = await main_player.receive()

    def yield_command(*args, **kwargs):
        pass

    def activate_card_command(*args, **kwargs):
        pass

    def play_from_hand_command(*args, **kwargs):
        pass

    command = {
        'yield': yield_command,
        'activate_card': activate_card_command,
        'play_from_hand': play_from_hand_command,
    }.get(move)

    match.stack.append(command)

    """
    move
        yield
        activate card in field
        play card from hand
    """