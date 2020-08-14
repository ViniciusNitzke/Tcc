import pytest
from unittest.mock import patch, MagicMock, Mock
from uuid import uuid4

from app.exceptions.exceptions import JsonError
from app.domains.products.views import validating_if_json_is_correct
from tests.unit import AbstractViewUnitTest


class TestCategoriesViews(AbstractViewUnitTest):

    @patch('app.domains.addresses.views.create_address')
    def test_post_address_should_be_created(self, create_address_mock):
        # Arrange
        id = str(uuid4())
        payload = {'street': 'Rua dos Testes', 'number': '123', 'complement': 'Testando', 'zip_code': '00000-000',
                   'city': 'Blumenau', 'state': 'Santa Catarina'}
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': id, 'active': True, 'street': 'Rua dos Testes',
                                                     'number': '123', 'complement': 'Testando', 'zip_code': '00000-000',
                                                     'city': 'Blumenau', 'state': 'Santa Catarina'})
        create_address_mock.return_value = obj_view

        # Action
        response = self._client.post('/addresses', json=payload)

        # Assertions
        self.assertEqual(response.status_code, 201)
        create_address_mock.assert_called_once_with({'street': 'Rua dos Testes', 'number': '123',
                                                     'complement': 'Testando', 'zip_code': '00000-000',
                                                     'city': 'Blumenau', 'state': 'Santa Catarina'})

    @patch('app.domains.addresses.views.create_address')
    def test_post_address_should_raise_a_exception(self, create_address_mock):
        # Arrange
        with pytest.raises(JsonError) as exc:

            # Action
            self._client.post('/addresses', json={})
            validating_if_json_is_correct(['street', 'number', 'zip_code', 'city', 'state'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): street, number, zip_code, city, state',
                         exc.value.description)

    @patch('app.domains.addresses.views.update_address')
    def test_put_address_should_be_updated(self, update_address_mock):
        # Arrange
        id = str(uuid4())
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': id, 'active': True, 'street': 'Rua dos Testes',
                                                     'number': '123', 'complement': 'Testando', 'zip_code': '00000-000',
                                                     'city': 'Blumenau', 'state': 'Santa Catarina'})
        update_address_mock.return_value = obj_view

        # Action
        response = self._client.put('/addresses/{}'.format(id), json={'active': False, 'street': 'Rua dos Testes',
                                                                      'number': '123', 'complement': 'Testando',
                                                                      'zip_code': '00000-000', 'city': 'Blumenau',
                                                                      'state': 'Santa Catarina'})

        # Assertions
        self.assertEqual(response.status_code, 200)
        update_address_mock.assert_called_once_with(id, {'active': False, 'street': 'Rua dos Testes',
                                                         'number': '123', 'complement': 'Testando',
                                                         'zip_code': '00000-000', 'city': 'Blumenau',
                                                         'state': 'Santa Catarina'})

    @patch('app.domains.addresses.views.get_addresses')
    def test_get_addresses_should_be_called_once(self, get_address_mock):
        # Arrange
        id = str(uuid4())
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': id, 'active': True, 'street': 'Rua dos Testes',
                                                     'number': '123', 'complement': 'Testando', 'zip_code': '00000-000',
                                                     'city': 'Blumenau', 'state': 'Santa Catarina'})
        get_address_mock.return_value = [obj_view]

        # Action
        response = self._client.get('/addresses')
        data = response.get_json()

        # Assertions
        self.assertEqual(1, len(data))
        get_address_mock.assert_called_once()

    @patch('app.domains.addresses.views.get_address_by_id')
    def test_get_address_by_id_should_be_called_once_with_id(self, get_address_by_id_mock):
        # Arrange
        id = str(uuid4())
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': id, 'active': True, 'street': 'Rua dos Testes',
                                                     'number': '123', 'complement': 'Testando', 'zip_code': '00000-000',
                                                     'city': 'Blumenau', 'state': 'Santa Catarina'})
        get_address_by_id_mock.return_value = obj_view

        # Action
        response = self._client.get('/addresses/{}'.format(id))

        # Assertions
        self.assertEqual(response.status_code, 200)
        get_address_by_id_mock.assert_called_once_with(id)
