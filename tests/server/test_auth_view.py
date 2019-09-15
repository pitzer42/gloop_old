from tests.server.game_server_test_case import GameServerTestCase

from engine.web.views.auth_view import AuthView
from engine.web.views.user_view import UserView

from tests.utils import sync

import tests.mocks.dummy_user_factory as dummies


class TestAuthView(GameServerTestCase):

    @sync
    async def test_post_credentials_to_get_auth_token(self):
        dummy_data = dummies.create().__dict__

        await self.client.put(
            UserView.__route__,
            json=dummy_data
        )

        response = await self.client.post(
            AuthView.__route__,
            json=dummy_data
        )

        json_response = await response.json()
        self.assertEqual(response.status, 200)
        self.assertIsNotNone(json_response)
        self.assertIn('token', json_response)

    #TODO: Test access protected view
