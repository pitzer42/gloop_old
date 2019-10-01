from gloop.entities.remote_party import RemoteParty
from gloop.entities.remote_player import RemotePlayer

from examples.mtg.entities.match import Match
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer

from examples.mtg.entities.phases.setup import setup
from examples.mtg.entities.phases.beginning import beginning
from examples.mtg.entities.phases.game_over import game_over
from examples.mtg.entities.phases.main import main
from examples.mtg.entities.phases.combat import combat
from examples.mtg.entities.phases.ending import ending


async def mtg_game_loop(main_player: RemotePlayer, party: RemoteParty):

    first = main_player == party[0]
    mtg_party = RemoteParty()
    for player in party:
        mtg_player = MtgRemotePlayer(player)
        mtg_party.append(mtg_player)
        if player == main_player:
            main_player = mtg_player
    party = mtg_party
    match = Match(party)

    await setup(main_player)
    if len(main_player.hand) == 0:
        await game_over(party, loser=main_player)

    assert main_player.deck is not None

    turn_owner = 0
    if first:
        while True:
            try:
                await beginning(main_player)
            except IndexError:
                await game_over(party, loser=main_player)
            await main(main_player, match)
            await combat(main_player, match)
            await main(main_player, match)
            await ending(main_player, match)

            turn_owner += 1
            turn_owner = turn_owner % len(party)
            main_player = party[turn_owner]
    else:
        import asyncio
        await asyncio.Event().wait()
