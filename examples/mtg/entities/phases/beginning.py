from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer


async def _untap(player: MtgRemotePlayer):
    player.field.untap()


async def _upkeep(player: MtgRemotePlayer):
    pass


async def _draw(player: MtgRemotePlayer):
    card = player.deck.draw()
    player.hand.extend(card)


async def beginning(player: MtgRemotePlayer):
    await _untap(player)
    await _upkeep(player)
    await _draw(player)
