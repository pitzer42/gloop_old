from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer


async def upkeep(player: MtgRemotePlayer):
    player.field.untap()
    card = player.deck.draw()
    player.hand.append(card)
