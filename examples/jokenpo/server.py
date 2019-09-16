from asyncio import Event

from gloop.models.remote_player import RemotePlayer
from gloop.models.remote_party import RemoteParty

from gloop.web.server import (
    create_game_app,
    start_game_server
)


class JoKenPo:

    rules = {
        'paper': 'rock',
        'rock': 'scissors',
        'scissors': 'paper'
    }

    def __init__(self):
        self.moves: list = None
        self.ready: Event = None
        self.clean_up()

    def clean_up(self):
        self.moves = [None] * 2
        self.ready = Event()

    def make_move(self, index, move):
        self.moves[index] = move
        if None not in self.moves:
            self.ready.set()

    def judge(self):
        m0, m1 = self.moves
        result = -1
        if JoKenPo.rules[m0] == m1:
            result = 0
        elif JoKenPo.rules[m1] == m0:
            result = 1
        return result

    async def __call__(self, player: RemotePlayer, party: RemoteParty):

        while True:
            index = party.index(player)

            await player.send(dict(message='(paper/rock/scissors)'))
            move = await player.receive()
            move = move['data']

            self.make_move(index, move)
            await self.ready.wait()
            if index == 0:
                result = self.judge()
                if result == -1:
                    await party.broadcast(dict(message='draw'))
                else:
                    winner = party[result]
                    await winner.send(dict(message='winner'))
                    await party.multicast(winner, dict(message='loser'))
                self.clean_up()


if __name__ == '__main__':
    game = create_game_app(game_loop=JoKenPo())
    start_game_server(game)
