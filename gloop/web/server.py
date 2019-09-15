import aiohttp_cors
from aiohttp import web

from gloop.models.game_loop import empty_game_loop
from gloop.models.remote_party import RemotePartyFactory

from gloop.repositories.mongo import mongo_user_repository_factory

from gloop.web import app_schema

from gloop.web.views.user_view import UserView
from gloop.web.views.game_view import GameView
from gloop.web.views.auth_view import AuthView


def _create_cors(app: web.Application):
    wildcard = '*'
    options = aiohttp_cors.ResourceOptions(
        expose_headers=wildcard,
        allow_headers=wildcard
    )
    defaults = {wildcard: options}
    return aiohttp_cors.setup(app, defaults=defaults)


def create_game_app(
        user_repo_factory=mongo_user_repository_factory,
        game_loop=empty_game_loop,
        party_size=2):

    app = web.Application()
    app[app_schema.user_repo] = user_repo_factory()
    app[app_schema.party_factory] = RemotePartyFactory(party_size)
    app[app_schema.game_loop] = game_loop

    view_register = [
        UserView,
        GameView,
        AuthView
    ]

    cors = _create_cors(app)

    for view in view_register:
        resource = app.router.add_view(view.__route__, view)
        cors.add(resource)

    return app


def start_game_server(game_app):
    web.run_app(game_app)
