import aiohttp_cors

from aiohttp import web

from gloop.web import app_schema

from gloop2.relay.view import RelayView
from gloop2.channels.channel import create_channel


def _create_cors(app: web.Application):
    wildcard = '*'
    options = aiohttp_cors.ResourceOptions(
        expose_headers=wildcard,
        allow_headers=wildcard
    )
    defaults = {wildcard: options}
    return aiohttp_cors.setup(app, defaults=defaults)


def create_relay_server():

    app = web.Application()
    app[app_schema.channel_factory] = create_channel

    view_register = [
        RelayView
    ]

    cors = _create_cors(app)

    for view in view_register:
        resource = app.router.add_view(view.__route__, view)
        cors.add(resource)

    return app


run_relay_server = web.run_app


if __name__ == '__main__':
    relay = create_relay_server()
    run_relay_server(relay)
