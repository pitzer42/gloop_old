from aiohttp import web

from gloop2.channels import web_socket

from gloop2.channels.redis import RedisChannel
from gloop2.channels import redis


waiting_list: RedisChannel = None
new_match: RedisChannel = None
clients = list()


def generate_client_id(request):
    global clients
    return str(len(clients))


async def index(request):
    global waiting_list
    global new_match

    if waiting_list is None:
        waiting_list = await redis.create_write_only_channel('waiting_list')

    if new_match is None:
        new_match = await redis.create_read_only_channel('new_match')

    name = generate_client_id(request)
    ws = await web_socket.create_channel(name, request)
    clients.append(ws)
    await waiting_list.send(name)
    match = await new_match.receive()
    await ws.send(match)
    print(f'sending {match} to {name}')
    return ws._ws

if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', index)
    web.run_app(app)



