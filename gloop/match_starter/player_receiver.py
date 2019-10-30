from aiohttp import web

from gloop import match_starter


def receive_player(
        waiting_list_channel_name: str,
        new_matches_channel_name: str,
        channel_factory,
        client_channel_factory,
        game_loop):

    async def _receive_player(request):

        ws = client_channel_factory(request)
        waiting_list_channel = channel_factory(waiting_list_channel_name)
        new_matches_channel = channel_factory(new_matches_channel_name)

        await ws.open()
        await waiting_list_channel.open()
        await new_matches_channel.open()

        ws_id = str(id(ws))
        await waiting_list_channel.send(ws_id)
        print(ws_id)

        new_match = str()
        while ws_id not in new_match:
            new_match = await new_matches_channel.receive()

        await ws.send(new_match)
        print(f'{ws_id} <- {new_match}')

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

        return await ws.close()

    return _receive_player


if __name__ == '__main__':

    app = web.Application()
    app.router.add_get(
        '/',
        receive_player(
            match_starter.WAITING_LIST_CHANNEL_NAME,
            match_starter.NEW_MATCHES_CHANNEL_NAME,
            match_starter.channel_factory,
            match_starter.client_channel_factory,
            match_starter.game_loop
        )
    )
    web.run_app(app)
