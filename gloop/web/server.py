import aiohttp_cors
from aiohttp import web

from gloop.entities.game_loop import empty_game_loop
from gloop.entities.remote_party import RemotePartyFactory

from gloop.web import app_schema

from gloop.web.views.game_view import GameView


def _create_cors(app: web.Application):
    wildcard = '*'
    options = aiohttp_cors.ResourceOptions(
        expose_headers=wildcard,
        allow_headers=wildcard
    )
    defaults = {wildcard: options}
    return aiohttp_cors.setup(app, defaults=defaults)


def create_game_app(
        party_size=2,
        game_loop=empty_game_loop):

    app = web.Application()
    app[app_schema.party_factory] = RemotePartyFactory(party_size)
    app[app_schema.game_loop] = game_loop

    view_register = [
        GameView
    ]

    cors = _create_cors(app)

    for view in view_register:
        resource = app.router.add_view(view.__route__, view)
        cors.add(resource)

    return app


def start_game_app(game_app):
    web.run_app(game_app)
