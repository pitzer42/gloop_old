from aiohttp.web import (
    Request,
    WebSocketResponse
)

from gloop.channels import Channel


class WebSocketChannel(Channel):

    def __init__(
            self,
            request: Request):
        self._request = request
        self._ws = None

    async def open(self):
        if self._ws is None:
            self._ws = WebSocketResponse()
            await self._ws.prepare(self._request)

    async def receive(self):
        ws_record = await self._ws.receive()
        return ws_record.data

    async def send(self, message):
        message = str(message)
        return await self._ws.send_str(message)

    async def close(self):
        await self._ws.close()
        return self._request
