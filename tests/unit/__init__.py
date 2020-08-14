import unittest

from app import create_app, db
from app.domains.users.models import User
from app.domains.suppliers.models import Supplier
from app.domains.addresses.models import Address
from app.domains.categories.models import Category


class AbstractViewUnitTest(unittest.TestCase):

    def setUp(self) -> None:
        self._app = create_app()
        db.create_all(app=self._app)
        self._client = self._app.test_client()

    def tearDown(self) -> None:
        db.drop_all(app=self._app)
