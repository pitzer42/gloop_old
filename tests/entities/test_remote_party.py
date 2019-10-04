from unittest import TestCase
from unittest.mock import Mock

from gloop.entities.remote_party import RemoteParty

from tests.utils import (
    sync,
    make_async_mock
)


PARTY_SIZE = 4


def create_party() -> RemoteParty:
    party = RemoteParty()
    for i in range(PARTY_SIZE):
        player = Mock()
        make_async_mock(player.send)
        party.append(player)
    return party


class TestRemoteParty(TestCase):

    def test_is_a_list(self):
        party = RemoteParty()
        self.assertIsInstance(party, list)

    @sync
    async def test_broadcasts_message(self):
        party = create_party()
        message = 'test_message'
        await party.broadcast(message)
        for player in party:
            player.send.assert_called_once_with(message)

    @sync
    async def test_multicast_message(self):
        party = create_party()
        message = 'test_message'
        first_player = party[0]

        await party.multicast(first_player, message)

        first_player.send.assert_not_called()
        for player in party[1:]:
            player.send.assert_called_once_with(message)
