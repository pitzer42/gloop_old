from unittest import TestCase

from gloop.repositories.mongo import mongo_user_repository_factory
from gloop.repositories.user_repository import UserRepository


from tests.utils import sync
import tests.mocks.dummy_user_factory as dummies
import tests.mocks.mongo_factory as mongo_factory


class UserRepositoryTestCase(TestCase):

    _users: UserRepository = None

    @property
    def users(self) -> UserRepository:
        return UserRepositoryTestCase._users

    @classmethod
    @sync
    async def setUpClass(cls) -> None:
        # repository backed by a fresh database
        test_db = await mongo_factory.create()
        UserRepositoryTestCase._users = mongo_user_repository_factory(db=test_db)

        # insert dummy entries
        dummy = dummies.create()
        await UserRepositoryTestCase._users.insert(dummy)

    async def insert_dummy(self):
        dummy = dummies.create()
        await self.users.insert(dummy)
        return dummy

