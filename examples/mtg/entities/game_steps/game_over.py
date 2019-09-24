from gloop.entities.remote_party import RemoteParty


async def game_over(party: RemoteParty, loser=None, winner=None):
    if loser is not None:
        msg = dict(
            msg='you have lost'
        )
        await loser.send(msg)

    if winner is not None:
        msg = dict(
            msg=f'{winner} have won'
        )
        await party.send(msg)
