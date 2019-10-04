from unittest import TestCase
from unittest.mock import Mock

from gloop.use_cases.start_game import (
    StartGame,
    ACK_MESSAGE
)

from tests.utils import (
    sync,
    make_async_mock
)


class TestRemoteParty(TestCase):

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.game_loop = None
        self.use_case = None
        self.remote_party_factory = None

    def setUp(self):
        self.game_loop = Mock()
        self.remote_party_factory = Mock()
        self.use_case = StartGame(
            self.game_loop,
            self.remote_party_factory
        )

        make_async_mock(self.game_loop)
        make_async_mock(self.remote_party_factory.gather)

    @sync
    async def test_holds_a_game_loop_and_a_remote_party_factory(self):
        self.assertIsNotNone(self.game_loop)
        self.assertIsNotNone(self.remote_party_factory)

    @sync
    async def test_player_receives_ack_message_after_connection(self):
        player = Mock()
        make_async_mock(player.send)
        await self.use_case.start_game(player)
        player.send.assert_called_once_with(ACK_MESSAGE)