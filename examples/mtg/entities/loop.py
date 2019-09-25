import random

from gloop.entities.remote_party import RemoteParty
from gloop.entities.remote_player import RemotePlayer

from examples.mtg.entities.match import Match
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

from examples.mtg.entities.game_steps.setup import setup
from examples.mtg.entities.game_steps.mulligan import mulligan
from examples.mtg.entities.game_steps.upkeep import upkeep
from examples.mtg.entities.game_steps.game_over import game_over
from examples.mtg.entities.game_steps.main_phase import main_phase
from examples.mtg.entities.game_steps.initial_draw import initial_draw


async def mtg_game_loop(main_player: RemotePlayer, party: RemoteParty):
    match = Match(party)
    main_player = MtgRemotePlayer(main_player)
    first = main_player == party[0]

    await setup(main_player)
    await initial_draw(main_player)
    await mulligan(main_player)
    if len(main_player.hand) == 0:
        await game_over(party, loser=main_player)

    if first:
        try:
            await upkeep(main_player)
        except IndexError:
            await game_over(party, loser=main_player)

        await main_phase(main_player, match)
    else:
        import asyncio
        await asyncio.Event().wait()
