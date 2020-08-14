import datetime
import unittest
from unittest.mock import patch, MagicMock, Mock
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
import pytest

from app.exceptions.exceptions_of_import import *
from app.exceptions.exceptions import InvalidValueError, JsonError
from app.domains.products.actions import get as get_products, \
    create as create_products, \
    get_by_id as get_by_id_products, \
    update as update_products, IdNotExistError, \
    inserting_products_from_the_csv_file_in_db as insert_data, \
    validating_if_the_product_sku_already_exists_in_the_db as validate, \
    validating_and_updating_if_the_product_sku_already_exists_in_the_db as validate_by_supplier, \
    get_percentages


class TestProductActions(unittest.TestCase):
    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.save')
    def test_action_create_should_be_created_new_products(self, save_mock, product_mock):
        # Arrange
        products_id = str(uuid4())
        id = str(uuid4())
        product_mock.id = products_id
        product_mock.name = 'Nescau'
        product_mock.cost_values = 10.00
        product_mock.unit_box = 5
        product_mock.weight_unit = 0.500
        product_mock.validity = '2021-12-19'
        product_mock.sku = '09ub124ibbi413'
        product_mock.description = 'Descrição...'
        product_mock.category_line_id = id
        product_mock.supplier_id = id
        product_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        product_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        product_mock.query = query
        product_mock.query.filter.return_value.first.return_value = []

        # Arrange
        create_products({'name': product_mock.name,
                         'cost_values': product_mock.cost_values,
                         'unit_box': product_mock.unit_box,
                         'weight_unit': product_mock.weight_unit,
                         'validity': product_mock.validity,
                         'sku': product_mock.sku,
                         'description': product_mock.description,
                         'category_line_id': product_mock.category_line_id,
                         'supplier_id': product_mock.supplier_id})

        # Assertions
        self.assertTrue(save_mock.called)
        self.assertEqual(product_mock.name, 'Nescau')
        self.assertEqual(product_mock.cost_values, 10)
        self.assertEqual(product_mock.unit_box, 5)
        self.assertEqual(product_mock.weight_unit, 0.500)
        self.assertEqual(product_mock.validity, '2021-12-19')
        self.assertEqual(product_mock.sku, '09ub124ibbi413')
        self.assertEqual(product_mock.description, 'Descrição...')
        self.assertEqual(product_mock.category_line_id, id)
        self.assertEqual(product_mock.supplier_id, id)
        self.assertEqual(product_mock.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(product_mock.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.products.actions.save')
    def test_create_must_raise_a_sql_alchemy_error(self, save_mock):
        # Arrange
        id = str(uuid4())
        save_mock.side_effect = SQLAlchemyError
        with pytest.raises(InvalidValueError) as exc:
            # Action
            create_products({'name': 'Nestle', 'cost_values': 12.00, 'unit_box': 1, 'weight_unit': 0.70,
                             'validity': '2021-12-19', 'sku': '08767gyuvy865', 'description': 'Descrição do produto',
                             'category_line_id': '7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed',
                             'supplier_id': '7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed'})
        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be '
                         'unique: sku', exc.value.description)

    @patch('app.domains.products.actions.Product')
    def test_actions_get_by_id_should_be_return_products(self, product_mock):
        # Arrange
        id = str(uuid4())
        product_saved = Mock()
        product_saved.name = 'Nescau'
        product_saved.cost_values = 10.00
        product_saved.unit_box = 5
        product_saved.weight_unit = 0.500
        product_saved.validity = '2021-12-19'
        product_saved.sku = '09ub124ibbi413'
        product_saved.description = 'Descrição...'
        product_saved.category_line_id = id
        product_saved.supplier_id = id
        product_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        product_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        query.get = MagicMock(return_value=product_mock)
        product_mock.query = query

        # Action
        products = get_by_id_products(product_mock.id)

        # Assertions
        product_mock.query.get.assert_called_once_with(products.id)
        self.assertEqual(product_mock, products)

    @patch('app.domains.products.actions.Product')
    def test_actions_get_by_id_should_raise_a_id_exception(self, product_mock):
        # Arrange
        product_mock.query.get.return_value = None
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id_products(product_mock.id)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.products.actions.Product')
    def test_actions_get_should_be_return_products(self, product_mock):
        # Arrange
        id = str(uuid4())
        product_mock.name = 'Nescau'
        product_mock.cost_values = 10.00
        product_mock.unit_box = 5
        product_mock.weight_unit = 0.500
        product_mock.validity = "2021-12-19"
        product_mock.sku = '09ub124ibbi413'
        product_mock.description = 'Descrição...'
        product_mock.category_line_id = id
        product_mock.supplier_id = id
        product_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        product_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        query.all = MagicMock(return_value=[product_mock])
        product_mock.query = query

        # Action
        products = get_products()

        # Assertions
        self.assertTrue(product_mock.query.all.called)
        self.assertEqual(len(products), 1)

    @patch('app.domains.products.actions.get_by_id')
    @patch('app.domains.products.actions.commit')
    def test_actions_update_should_be_updated_products(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        product_saved = Mock()
        product_saved.name = 'Nescau'
        product_saved.cost_values = 10.00
        product_saved.unit_box = 5
        product_saved.weight_unit = 0.500
        product_saved.validity = '2021-12-21'
        product_saved.sku = '09ub124ibbi413'
        product_saved.description = 'Descrição...'
        product_saved.category_line_id = id
        product_saved.supplier_id = id
        product_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        product_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        get_by_id_mock.return_value = product_saved
        product_saved.serialize.return_value = {}

        # Action
        product = update_products(id,
                                  {'name': 'Nestle',
                                   'cost_values': 12,
                                   'unit_box': 5,
                                   'weight_unit': 0.70,
                                   'validity': '2021-12-19',
                                   'sku': '08767gyuvy865',
                                   'description': 'Descrição do produto',
                                   'category_line_id': id,
                                   'supplier_id': id})

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertTrue(commit_mock.called)
        self.assertEqual(product.name, 'Nestle')
        self.assertEqual(product.cost_values, 12)
        self.assertEqual(product.unit_box, 5)
        self.assertEqual(product.weight_unit, 0.70)
        self.assertEqual(product.validity, '2021-12-19')
        self.assertEqual(product.sku, '08767gyuvy865')
        self.assertEqual(product.description, 'Descrição do produto')
        self.assertEqual(product.category_line_id, id)
        self.assertEqual(product.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(product.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.products.actions.get_by_id')
    @patch('app.domains.products.actions.commit')
    def test_product_must_raise_a_json_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        with pytest.raises(JsonError) as exc:
            # Action
            update_products(id, None)

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): name, cost_values, unit_box, weight_unit, '
                         'validity, sku, category_line_id, supplier_id', exc.value.description)

    @patch('app.domains.products.actions.get_by_id')
    @patch('app.domains.products.actions.commit')
    def test_product_must_raise_an_id_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id_mock.return_value = None
            update_products('1', {})

        # Assertions
        get_by_id_mock.assert_called_once_with('1')
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.products.actions.get_by_id')
    @patch('app.domains.products.actions.commit')
    def test_update_must_raise_a_sql_alchemy_error(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        commit_mock.side_effect = SQLAlchemyError
        with pytest.raises(InvalidValueError) as exc:
            # Action
            update_products(id, {'name': 'Nestle', 'cost_values': 12.00, 'unit_box': 1, 'weight_unit': 0.70,
                                 'validity': '2021-12-19', 'sku': '08767gyuvy865',
                                 'description': 'Descrição do produto',
                                 'category_line_id': '7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed'})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be '
                         'unique: sku', exc.value.description)

    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.save')
    @patch('app.domains.products.actions.import_product_csv_file')
    @patch('app.domains.products.actions.get')
    def test_action_inserting_products_from_the_csv_file_in_db_should_return_a_list_of_saved_products(self,
                                                                                                      get_mock,
                                                                                                      import_csv_mock,
                                                                                                      save_mock,
                                                                                                      product_mock):
        # Arrange
        id = str(uuid4())
        get_mock.return_value = [product_mock]
        import_csv_mock.return_value = [{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                                         'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                                         'category_line_id': id, 'supplier_id': id}]

        # Action
        response = insert_data(['import_csv'], 'sku', validate, [], [], [])

        # Assertions
        self.assertTrue(get_mock.called)
        self.assertTrue(import_csv_mock.called)
        self.assertTrue(save_mock.called)
        self.assertTrue(product_mock.called)
        self.assertEqual([product_mock], get_mock.return_value)
        self.assertEqual([save_mock()], response)
        self.assertEqual([{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                           'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                           'category_line_id': id, 'supplier_id': id}], import_csv_mock.return_value)

    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.save')
    @patch('app.domains.products.actions.import_product_csv_file')
    @patch('app.domains.products.actions.get')
    def test_action_inserting_products_from_the_csv_file_in_db_should_raise_a_invalid_value_error(self,
                                                                                                  get_mock,
                                                                                                  import_csv_mock,
                                                                                                  save_mock,
                                                                                                  product_mock):
        # Arrange
        id = str(uuid4())
        get_mock.return_value = [product_mock]
        save_mock.side_effect = SQLAlchemyError
        import_csv_mock.return_value = [{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                                         'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                                         'category_line_id': '342343', 'supplier_id': id}]
        with pytest.raises(InvalidValueError) as exc:

            # Action
            insert_data(['import_csv'], 'sku', validate, [], [], [])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be '
                         'unique: sku', exc.value.description)

    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.save')
    @patch('app.domains.products.actions.import_product_csv_file')
    @patch('app.domains.products.actions.get')
    def test_action_inserting_products_from_the_csv_file_in_db_should_raise_a_data_already_exists_error(self,
                                                                                                        get_mock,
                                                                                                        import_csv_mock,
                                                                                                        save_mock,
                                                                                                        product_mock):
        # Arrange
        product_mock.side_effect = DataAlreadyExistsError
        with pytest.raises(DataAlreadyExistsError) as exc:
            # Action
            insert_data(['import_csv'], 'sku', validate, [], [], [])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('All the data in the file has already been added', exc.value.description)

    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.save')
    @patch('app.domains.products.actions.import_product_csv_file')
    @patch('app.domains.products.actions.get')
    def test_action_inserting_products_by_supplier_from_the_csv_file_in_db_should_return_a_list_of_saved_products(self,
                                                                                                                  get_mock,
                                                                                                                  import_csv_mock,
                                                                                                                  save_mock,
                                                                                                                  product_mock):
        # Arrange
        id = str(uuid4())
        get_mock.return_value = [product_mock]
        import_csv_mock.return_value = [{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                                         'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                                         'category_line_id': id, 'supplier_id': id}]

        # Action
        response = insert_data(['import_csv'], 'sku', validate_by_supplier, [], [], [])

        # Assertions
        self.assertTrue(get_mock.called)
        self.assertTrue(import_csv_mock.called)
        self.assertTrue(save_mock.called)
        self.assertTrue(product_mock.called)
        self.assertEqual([product_mock], get_mock.return_value)
        self.assertEqual([save_mock()], response)
        self.assertEqual([{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                           'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                           'category_line_id': id, 'supplier_id': id}], import_csv_mock.return_value)

    @patch('app.domains.products.actions.update')
    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.import_product_csv_file')
    @patch('app.domains.products.actions.get')
    def test_action_inserting_products_by_supplier_from_the_csv_file_in_db_should_update_a_list_of_saved_products(self,
                                                                                                                  get_mock,
                                                                                                                  import_csv_mock,
                                                                                                                  product_mock,
                                                                                                                  update_mock):
        # Arrange
        id = str(uuid4())
        product_mock.sku = 'teste'
        get_mock.return_value = [product_mock]
        import_csv_mock.return_value = [{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                                         'validity': "2021-10-10", 'sku': 'teste', 'description': 'descricao',
                                         'category_line_id': id, 'supplier_id': id}]

        # Action
        response = insert_data(['import_csv'], 'sku', validate_by_supplier, [], [], [])

        # Assertions
        self.assertTrue(get_mock.called)
        self.assertTrue(import_csv_mock.called)
        self.assertEqual([product_mock], get_mock.return_value)
        self.assertEqual([update_mock()], response)
        self.assertEqual([{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                           'validity': "2021-10-10", 'sku': 'teste', 'description': 'descricao',
                           'category_line_id': id, 'supplier_id': id}], import_csv_mock.return_value)

    @patch('app.domains.products.actions.Product')
    @patch('app.domains.products.actions.save')
    @patch('app.domains.products.actions.import_product_csv_file')
    @patch('app.domains.products.actions.get')
    def test_action_inserting_products_from_the_csv_file_in_db_should_raise_a_id_error(self,
                                                                                       get_mock,
                                                                                       import_csv_mock,
                                                                                       save_mock,
                                                                                       product_mock):
        # Arrange
        id = str(uuid4())
        get_mock.return_value = [product_mock]
        save_mock.side_effect = SQLAlchemyError
        import_csv_mock.return_value = [{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                                         'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                                         'category_line_id': '342343', 'supplier_id': id}]
        with pytest.raises(IdNotExistError) as exc:
            # Action
            insert_data(['import_csv'], 'sku', validate_by_supplier, [], [], [])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.products.actions.get_category_by_id')
    @patch('app.domains.products.actions.get_category_line_by_id')
    def test_action_get_percentages(self,
                                    get_category_line_by_id_mock,
                                    get_category_by_id_mock):
        # Arrange
        id = str(uuid4())
        _id = str(uuid4())

        category_line = Mock()
        category_line.id = id
        category_line.category_id = _id
        category_line.profit_percentage = 15.0

        category = Mock()
        category.id = _id
        category.profit_percentage = 20.0

        get_category_line_by_id_mock.return_value = category_line
        get_category_by_id_mock.return_value = category

        # Action
        sum_of_porcentages = get_percentages(id)

        # Assertions
        self.assertTrue(get_category_by_id_mock.called)
        self.assertTrue(get_category_line_by_id_mock.called)
        self.assertEqual(sum_of_porcentages, 35.0)
