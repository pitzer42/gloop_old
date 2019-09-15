from aiohttp import web

from aiohttp_cors import CorsViewMixin

from engine.use_cases.start_game import StartGame

from engine.web import app_schema
from engine.web.ws_player import WebSocketPlayer


class GameView(web.View, CorsViewMixin):

    __route__ = '/play'

    @property
    def use_case(self) -> StartGame:
        game_loop = self.request.app[app_schema.game_loop]
        party_factory = self.request.app[app_schema.party_factory]
        return StartGame(game_loop, party_factory)

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        player = WebSocketPlayer(ws)
        await self.use_case.start_game(player)
