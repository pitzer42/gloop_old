from gloop.channels.redis import RedisChannel
from gloop.channels.web_socket import WebSocketChannel

WAITING_LIST_CHANNEL_NAME = 'waiting_list'
NEW_MATCHES_CHANNEL_NAME = 'new_matches'

MATCH_SIZE = 2

channel_factory = RedisChannel
client_channel_factory = WebSocketChannel


async def game_loop(main_player, match_channel, *players):
    pass
