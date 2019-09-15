from aiohttp import web

from aiohttp_cors import CorsViewMixin

import gloop.web.app_schema as app_schema

from gloop.web.views.data_ports import (
    json_to_credentials,
    token_to_authentication_json
)

from gloop.use_cases.authentication import Authentication


class AuthView(web.View, CorsViewMixin):

    __route__ = '/users/login'

    @property
    def use_case(self) -> Authentication:
        users = self.request.app[app_schema.user_repo]
        return Authentication(users)

    async def post(self):
        json_request = await self.request.json()
        name, password = json_to_credentials(json_request)
        token = await self.use_case.login(name, password)
        json_token = token_to_authentication_json(token)
        return web.json_response(json_token)
