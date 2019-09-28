from gloop.entities.remote_party import RemoteParty
from gloop.entities.remote_player import RemotePlayer

from examples.mtg.entities.match import Match
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

from examples.mtg.entities.phases.setup import setup
from examples.mtg.entities.phases.beginning import beginning
from examples.mtg.entities.phases.game_over import game_over
from examples.mtg.entities.phases.main import main
from examples.mtg.entities.phases.combat import combat


async def mtg_game_loop(main_player: RemotePlayer, party: RemoteParty):
    match = Match(party)
    main_player = MtgRemotePlayer(main_player)
    first = main_player == party[0]

    await setup(main_player)
    if len(main_player.hand) == 0:
        await game_over(party, loser=main_player)

    if first:
        try:
            await beginning(main_player)
        except IndexError:
            await game_over(party, loser=main_player)
        await main(main_player, match)
        await combat(main_player, match)
        await main(main_player, match)
    else:
        import asyncio
        await asyncio.Event().wait()
