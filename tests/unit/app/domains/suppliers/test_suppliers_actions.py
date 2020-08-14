import unittest
from unittest.mock import patch, MagicMock, Mock
import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.domains.suppliers.models import *
from app.domains.suppliers.actions import get_by_id, update, create, get


class TestSuppliersActions(unittest.TestCase):
    @patch('app.domains.suppliers.actions.save')
    def test_if_suppliers_actions_creates_a_new_supplier(self, save_mock):
        # Arrange
        model_id = str(uuid4())
        address_id = str(uuid4())
        category_id = str(uuid4())
        suppliers_mock = Mock()
        suppliers_mock.id = model_id
        suppliers_mock.active = True
        suppliers_mock.company_name = 'Company Tester SA'
        suppliers_mock.cnpj = '73808025000190'
        suppliers_mock.trading_name = 'Trading Name'
        suppliers_mock.phone = '04732342021'
        suppliers_mock.email = 'empresa@business.com'
        suppliers_mock.address_id = address_id
        suppliers_mock.category_id = category_id
        suppliers_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        suppliers_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        suppliers_mock.query = query
        suppliers_mock.query.filter.return_value.first.return_value = []

        # Action
        create({
            'active': suppliers_mock.active,
            'company_name': suppliers_mock.company_name,
            'cnpj': suppliers_mock.cnpj,
            'trading_name': suppliers_mock.trading_name,
            'phone': suppliers_mock.phone,
            'email': suppliers_mock.email,
            'address_id': suppliers_mock.address_id,
            'category_id': suppliers_mock.category_id})

        # Assertions
        self.assertTrue(save_mock.called)
        self.assertEqual(suppliers_mock.active, True)
        self.assertEqual(suppliers_mock.company_name, 'Company Tester SA')
        self.assertEqual(suppliers_mock.cnpj, '73808025000190')
        self.assertEqual(suppliers_mock.trading_name, 'Trading Name')
        self.assertEqual(suppliers_mock.phone, '04732342021')
        self.assertEqual(suppliers_mock.email, 'empresa@business.com')
        self.assertEqual(suppliers_mock.address_id, address_id)
        self.assertEqual(suppliers_mock.category_id, category_id)
        self.assertEqual(suppliers_mock.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(suppliers_mock.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.suppliers.actions.save')
    def test_create_must_raise_a_sql_alchemy_error(self, save_mock):
        # Arrange
        id = str(uuid4())
        save_mock.side_effect = SQLAlchemyError
        with pytest.raises(InvalidValueError) as exc:
            # Action
            create({'active': True, 'company_name': 'Company Tester', 'cnpj': '73808025000190',
                    'trading_name': 'Trading name', 'phone': '04732342022', 'email': 'empresa@business.com',
                    'address_id': id, 'category_id': id})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be '
                         'unique: cnpj', exc.value.description)

    @patch('app.domains.suppliers.actions.Supplier')
    def test_if_get_by_id_returns_a_supplier(self, supplier_mock):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        supplier_saved = Mock()
        supplier_saved.active = True
        supplier_saved.company_name = 'Company Tester SA'
        supplier_saved.cnpj = '73808025000190'
        supplier_saved.trading_name = 'Trading name'
        supplier_saved.phone = '04732342021'
        supplier_saved.email = 'empresa@business.com'
        supplier_saved.address_id = address_id
        supplier_saved.category_id = category_id
        supplier_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        supplier_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = Mock()
        query.get = MagicMock(return_value=supplier_saved)
        supplier_mock.query = query

        # Action
        supplier = get_by_id(supplier_saved.id)

        # Assertions
        supplier_mock.query.get.assert_called_once_with(supplier_saved.id)
        self.assertEqual(supplier_saved, supplier)

    @patch('app.domains.suppliers.actions.Supplier')
    def test_actions_get_by_id_should_raise_a_id_exception(self, supplier_mock):
        # Arrange
        supplier_mock.query.get.return_value = None
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id(supplier_mock.id)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.suppliers.actions.Supplier')
    def test_if_get_returns_suppliers(self, supplier_mock):
        # Arrange
        address_id = str(uuid4())
        category_id = str(uuid4())
        supplier_mock.active = True
        supplier_mock.company_name = 'Company Tester SA'
        supplier_mock.cnpj = '73808025000190'
        supplier_mock.trading_name = 'Trading name'
        supplier_mock.phone = '04732342021'
        supplier_mock.email = 'empresa@business.com'
        supplier_mock.address_id = address_id
        supplier_mock.category_id = category_id
        supplier_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        supplier_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = Mock()
        query.all = MagicMock(return_value=[supplier_mock])
        supplier_mock.query = query

        # Action
        suppliers = get()

        # Assertions
        self.assertTrue(supplier_mock.query.all.called)
        self.assertEqual(len(suppliers), 1)

    @patch('app.domains.suppliers.actions.get_by_id')
    @patch('app.domains.suppliers.actions.commit')
    def test_action_update_should_be_updated_user(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        address_id = str(uuid4())
        category_id = str(uuid4())
        supplier_saved = Mock()
        supplier_saved.active = True
        supplier_saved.company_name = 'Company Tester SA'
        supplier_saved.cnpj = '73808025000190'
        supplier_saved.trading_name = 'Trading name'
        supplier_saved.phone = '04732342021'
        supplier_saved.email = 'empresa@business.com'
        supplier_saved.address_id = address_id
        supplier_saved.category_id = category_id
        supplier_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        supplier_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        get_by_id_mock.return_value = supplier_saved
        supplier_saved.serialize.return_value = {}

        # Action
        supplier = update(id,
                          {'active': True,
                           'company_name': 'Company Tester',
                           'cnpj': '73808025000190',
                           'trading_name': 'Trading name',
                           'phone': '04732342022',
                           'email': 'empresa@business.com',
                           'address_id': address_id,
                           'category_id': category_id})

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertTrue(commit_mock.called)
        self.assertEqual(supplier.active, True)
        self.assertEqual(supplier.company_name, 'Company Tester')
        self.assertEqual(supplier.cnpj, '73808025000190')
        self.assertEqual(supplier.trading_name, 'Trading name')
        self.assertEqual(supplier.phone, '04732342022')
        self.assertEqual(supplier.email, 'empresa@business.com')
        self.assertEqual(supplier.address_id, address_id)
        self.assertEqual(supplier.category_id, category_id)
        self.assertEqual(supplier.on_create, supplier_saved.on_create)
        self.assertEqual(supplier.on_update, supplier.on_update)

    @patch('app.domains.suppliers.actions.get_by_id')
    @patch('app.domains.suppliers.actions.commit')
    def test_action_update_must_raise_a_json_exception(self, commit_mock, get_by_id_mock):
        # Arrange

        with pytest.raises(JsonError) as exc:
            # Action
            update(id, [])

        # Assertions
        get_by_id_mock.assert_called_with(id)
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): company_name, cnpj, trading_name, phone, '
                         'email, address_id, category_id', exc.value.description)

    @patch('app.domains.suppliers.actions.get_by_id')
    @patch('app.domains.suppliers.actions.commit')
    def test_supplier_must_raise_an_id_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id_mock.return_value = None
            update('1', {})

        # Assertions
        get_by_id_mock.assert_called_once()
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.suppliers.actions.get_by_id')
    @patch('app.domains.suppliers.actions.commit')
    def test_action_update_must_raise_a_sql_alchemy_error(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        commit_mock.side_effect = SQLAlchemyError
        with pytest.raises(InvalidValueError) as exc:
            # Action
            update(id, {'active': True, 'company_name': 'Company Tester', 'cnpj': '73808025000190',
                        'trading_name': 'Trading name', 'phone': '04732342022', 'email': 'empresa@business.com',
                        'address_id': id, 'category_id': id})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be unique:'
                         ' cnpj', exc.value.description)
