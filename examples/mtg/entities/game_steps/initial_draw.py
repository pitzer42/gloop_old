from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer


INITIAL_HAND_SIZE = 7


async def initial_draw(player: MtgRemotePlayer):
    player.hand = player.deck.draw(n=INITIAL_HAND_SIZE)