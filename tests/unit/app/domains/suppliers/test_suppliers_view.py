from unittest.mock import patch, MagicMock, Mock
import pytest

from tests.unit import AbstractViewUnitTest
from app.exceptions.exceptions import JsonError
from app.domains.suppliers.views import validating_if_json_is_correct


class TestSuppliersView(AbstractViewUnitTest):

    @patch('app.domains.suppliers.views.get_suppliers')
    def test_get_suppliers_should_be_1(self, get_supplier_mock):
        # Arrange
        obj = Mock()
        obj.serialize_summed_version = MagicMock(return_value={})
        get_supplier_mock.return_value = [obj]

        # Action
        response = self._client.get('/suppliers')
        data = response.get_json()

        # Assertions
        self.assertEqual(len(data), 1)
        get_supplier_mock.assert_called_once()

    @patch('app.domains.suppliers.views.get_supplier_by_id')
    def test_get_user_by_id_should_be_1(self, get_supplier_by_id_mock):
        # Arrange
        obj = Mock()
        obj.serialize = MagicMock(return_value={})
        get_supplier_by_id_mock.return_value = obj
        _id = '013e4324-5a92-428d-9fb0-d826cb3e8a72'

        # Action
        response = self._client.get('/suppliers/{}'.format(_id))

        # Assertions
        self.assertEqual(response.status_code, 200)
        get_supplier_by_id_mock.assert_called_once_with(_id)

    @patch('app.domains.suppliers.views.create_supplier')
    def test_post_supplier_should_be_created(self, create_supplier_mock):
        # Arrange
        payload = \
            {'active': True,
             'company_name': 'Company Tester',
             'cnpj': '73808025000190',
             'trading_name': 'Trading name',
             'phone': '04732342022',
             'email': 'empresa@business.com',
             'address_id': '013e4324-5a92-428d-9fb0-d826cb3e8a72',
             'category_id': '013e4324-5a92-428d-9fb0-d826cb3e8a72'}
        obj = Mock()
        obj.serialize = MagicMock(return_value={})
        create_supplier_mock.return_value = obj

        # Action
        response = self._client.post('/suppliers', json=payload)
        validating_if_json_is_correct(['cnpj'], **{'company_name': 'Company Tester',
                                                   'cnpj': '73808025000190',
                                                   'trading_name': 'Trading name',
                                                   'phone': '04732342022',
                                                   'email': 'empresa@business.com',
                                                   'address_id': '013e4324-5a92-428d-9fb0-d826cb3e8a72',
                                                   'category_id': '013e4324-5a92-428d-9fb0-d826cb3e8a72'})

        # Assertions
        self.assertEqual(response.status_code, 201)
        create_supplier_mock.assert_called_once_with({'active': True,
                                                      'company_name': 'Company Tester',
                                                      'cnpj': '73808025000190',
                                                      'trading_name': 'Trading name',
                                                      'phone': '04732342022',
                                                      'email': 'empresa@business.com',
                                                      'address_id': '013e4324-5a92-428d-9fb0-d826cb3e8a72',
                                                      'category_id': '013e4324-5a92-428d-9fb0-d826cb3e8a72'})

    @patch('app.domains.suppliers.views.create_supplier')
    def test_post_suppliers_should_raise_a_exception(self, create_supplier_mock):
        # Arrange
        with pytest.raises(JsonError) as exc:

            # Action
            self._client.post('/suppliers', json={})
            validating_if_json_is_correct(['cnpj'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): cnpj', exc.value.description)

    @patch('app.domains.suppliers.views.update_supplier')
    def test_put_supplier_should_be_updated(self, update_supplier_mock):
        # Arrange
        _id = '013e4324-5a92-428d-9fb0-d826cb3e8a72'
        obj = Mock()
        obj.serialize = MagicMock(return_value={'company_name': 'pasd'})
        update_supplier_mock.return_value = obj

        # Action
        response = self._client.put('/suppliers/{}'.format(_id), json={'company_name': 'new_name'})

        # Assertions
        self.assertEqual(response.status_code, 200)
        update_supplier_mock.assert_called_once_with('013e4324-5a92-428d-9fb0-d826cb3e8a72',
                                                     {'company_name': 'new_name'})
