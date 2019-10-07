from aiohttp.web import (
    Request,
    WebSocketResponse
)

from gloop2.channels import Channel


class WebSocketChannel(Channel):

    def __init__(self,
                 name: str,
                 ws: WebSocketResponse):
        super(WebSocketChannel, self).__init__(name)
        self._ws = ws

    async def receive(self):
        return await self._ws.receive()

    async def send(self, message):
        message = str(message)
        return await self._ws.send_str(message)


async def create_channel(
            name: str,
            request: Request) -> WebSocketChannel:
    ws = WebSocketResponse()
    await ws.prepare(request)
    return WebSocketChannel(name, ws)

create_read_only_channel = create_channel

create_write_only_channel = create_channel
