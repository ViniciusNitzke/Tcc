import unittest
from unittest.mock import patch, MagicMock, Mock
import pytest

from app.domains.addresses.actions import get, get_by_id, update, create
from app.domains.addresses.models import *


class TestAddressesActions(unittest.TestCase):

    @patch('app.domains.addresses.actions.save')
    def test_action_create_should_be_created_new_address(self, save_mock):
        # Arrange
        model_id = str(uuid4())
        addresses_mock = Mock()
        addresses_mock.id = model_id
        addresses_mock.active = True
        addresses_mock.street = 'Rua dos Testes'
        addresses_mock.number = '123'
        addresses_mock.complement = 'Testando'
        addresses_mock.zip_code = '00000000'
        addresses_mock.city = 'Blumenau'
        addresses_mock.state = 'Santa Catarina'
        addresses_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        addresses_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        addresses_mock.query = query
        addresses_mock.query.filter.return_value.first.return_value = []

        # Actions
        create({'street': 'Rua dos Testes', 'number': '123', 'complement': 'Testando',
                'zip_code': '00000000', 'city': 'Blumenau', 'state': 'Santa Catarina'})

        calls = save_mock.call_args
        args = calls[0]
        address = args[0]

        # Assertions
        self.assertTrue(save_mock.called)
        self.assertIsInstance(address, Address)
        self.assertEqual(addresses_mock.id, model_id)
        self.assertEqual(addresses_mock.active, True)
        self.assertEqual(address.street, 'Rua dos Testes')
        self.assertEqual(address.number, '123')
        self.assertEqual(address.complement, 'Testando')
        self.assertEqual(address.zip_code, '00000000')
        self.assertEqual(address.city, 'Blumenau')
        self.assertEqual(address.state, 'Santa Catarina')
        self.assertEqual(addresses_mock.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(addresses_mock.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.addresses.actions.Address')
    def test_action_get_by_id_should_be_return_address(self, address_mock):
        # Arrange
        address_saved = Mock()
        address_saved.street = 'Rua dos Testes'
        address_saved.number = '123'
        address_saved.complement = 'Testando'
        address_saved.zip_code = '00000000'
        address_saved.city = 'Blumenau'
        address_saved.state = 'Santa Catarina'
        address_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        address_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = Mock()
        query.get = MagicMock(return_value=address_saved)
        address_mock.query = query

        # Action
        address = get_by_id(address_mock.id)

        # Assertions
        address_mock.query.get.assert_called_once_with(address_mock.id)
        self.assertEqual(address_saved, address)

    @patch('app.domains.addresses.actions.Address')
    def test_actions_get_by_id_should_raise_a_id_exception(self, address_mock):
        # Arrange
        address_mock.query.get.return_value = None
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id(address_mock.id)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.addresses.actions.Address')
    def test_action_get_should_be_return_addresses(self, address_mock):
        # Arrange
        address_saved = Mock()
        address_saved.street = 'Rua dos Testes'
        address_saved.number = '123'
        address_saved.complement = 'Testando'
        address_saved.zip_code = '00000000'
        address_saved.city = 'Blumenau'
        address_saved.state = 'Santa Catarina'
        address_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        address_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = Mock()
        query.all = MagicMock(return_value=[address_saved])
        address_mock.query = query

        # Action
        addresses = get()

        # Assertions
        self.assertTrue(address_mock.query.all.called)
        self.assertEqual(len(addresses), 1)

    @patch('app.domains.addresses.actions.get_by_id')
    @patch('app.domains.addresses.actions.commit')
    def test_action_update_should_be_updated_address(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())

        address_saved = Mock()
        address_saved.street = 'Rua dos Testes'
        address_saved.number = '123'
        address_saved.complement = 'Testando'
        address_saved.zip_code = '00000000'
        address_saved.city = 'Blumenau'
        address_saved.state = 'Santa Catarina'
        address_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        address_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        get_by_id_mock.return_value = address_saved
        address_saved.serialize.return_value = {}

        # Action
        address = update(id,
                         {'active': False, 'street': 'R Testes', 'number': '000', 'complement': 'Teste',
                          'zip_code': '00000123', 'city': 'Blu', 'state': 'SC'})

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertTrue(commit_mock.called)
        self.assertEqual(address.active, False)
        self.assertEqual(address.street, 'R Testes')
        self.assertEqual(address.number, '000')
        self.assertEqual(address.complement, 'Teste')
        self.assertEqual(address.zip_code, '00000123')
        self.assertEqual(address.city, 'Blu')
        self.assertEqual(address.state, 'SC')
        self.assertEqual(address.on_create, address_saved.on_create)
        self.assertEqual(address.on_update, address.on_update)

    @patch('app.domains.addresses.actions.get_by_id')
    @patch('app.domains.addresses.actions.commit')
    def test_action_update_must_raise_an_id_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        with pytest.raises(IdNotExistError) as exc:

            # Action
            get_by_id_mock.return_value = None
            update('1', {})

        # Assertions
        get_by_id_mock.assert_called_once_with('1')
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.addresses.actions.get_by_id')
    @patch('app.domains.addresses.actions.commit')
    def test_action_update_must_raise_a_json_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        with pytest.raises(JsonError) as exc:

            # Action
            update(id, [])

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): street, number, zip_code, city, state',
                         exc.value.description)
