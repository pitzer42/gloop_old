import asyncio
from aiohttp.web import (
    View,
    WebSocketResponse
)


from aiohttp_cors import CorsViewMixin

from gloop.use_cases.start_game import StartGame

from gloop.web import app_schema


class RelayView(View, CorsViewMixin):

    __route__ = '/play'

    def __init__(self, *args, **kwargs):
        View.__init__(self, *args, **kwargs)
        self.clients = dict()
        self.new_client_channel = None
        self.new_match_channel = None

    @property
    def channel_factory(self) -> StartGame:
        return self.request.app[app_schema.channel_factory]

    async def get(self):
        if self.new_client_channel is None:
            self.new_client_channel = await self.channel_factory(app_schema.new_client_channel)
        if self.new_match_channel is None:
            self.new_match_channel = await self.channel_factory(app_schema.new_match_channel)

        client = WebSocketResponse()
        await client.prepare(self.request)
        client_id = self.create_client_id(client)
        self.clients[client_id] = client

        match_name = None

        async def set_match_name(name):
            global match_name
            match_name = name

        new_match = await self.new_match_channel.subscribe(set_match_name)
        await self.new_client_channel.publish(client_id)
        await client.send_json(client_id)

        await new_match
        await client.send_json(match_name)
        match_channel = self.channel_factory(new_match)
        match_end = await match_channel.subscribe(client.send_str)
        await match_end

        return client

    def create_client_id(self, connection):
        return f"{id(self)}:{id(connection)}"
