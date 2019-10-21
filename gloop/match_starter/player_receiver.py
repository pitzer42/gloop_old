import asyncio
from aiohttp import web
from gloop.channels import Channel
from gloop.match_starter import config


def receive_player(
        waiting_list_channel: Channel,
        new_matches_channel: Channel,
        channel_factory,
        client_channel_factory,
        game_loop):

    async def _receive_player(request):
        ws = client_channel_factory(request)
        ws_id = str(id(ws))
        await ws.open()
        await waiting_list_channel.send(ws_id)

        new_match = str()
        while ws_id not in new_match:
            new_match = await new_matches_channel.receive()

        await ws.send(new_match)

        match_params = new_match.split(' ')
        match_channel_name = match_params[0]
        player_ids = match_params[1:]

        match = channel_factory(match_channel_name)
        await match.open()

        await game_loop(
            ws,
            match,
            *player_ids
        )

        return ws.close()

    return _receive_player


if __name__ == '__main__':

    _waiting_list_channel = config.channel_factory(config.WAITING_LIST_CHANNEL_NAME)
    _new_matches_channel = config.channel_factory(config.NEW_MATCHES_CHANNEL_NAME)

    asyncio.run(
        asyncio.gather(
            _waiting_list_channel.open(),
            _new_matches_channel.open()
        )
    )

    app = web.Application()
    app.router.add_get(
        '/',
        receive_player(
            _waiting_list_channel,
            _new_matches_channel,
            config.channel_factory,
            config.client_channel_factory,
            config.game_loop
        )
    )
    web.run_app(app)
