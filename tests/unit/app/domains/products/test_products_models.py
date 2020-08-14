import unittest
from unittest.mock import patch
import pytest

from app.domains.products.models import *
from app.domains.products.models import Product


class TestProductModels(unittest.TestCase):
    @patch('app.domains.products.models.Product')
    def test_products_models_serialize_method(self, product_mock):
        # Arrange
        _id = str(uuid4())
        id = str(uuid4())
        product_mock.query.filter.return_value.first.return_value = []
        products = Product(id=_id, active=False, name='Nescau', cost_values=10.15, unit_box=5, weight_unit=0.550,
                           validity="2021-12-31", sku='09ub124ibbi413', description='Descrição...',
                           category_line_id=id, supplier_id=id,
                           on_create=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                           on_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Action
        response = products.serialize()

        # Assertions
        self.assertEqual(type(response), dict)
        self.assertIsInstance(products, Product)
        self.assertEqual({'id': _id, 'active': False, 'name': 'Nescau', 'cost_values': 10.15, 'unit_box': 5,
                          'weight_unit': 0.550, 'validity': "2021-12-31", 'sku': '09ub124ibbi413',
                          'description': 'Descrição...', 'category_line_id': id, 'supplier_id': id,
                          'on_create': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          'on_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}, response)

    def test_product_must_raise_an_empty_field_exception(self):
        # Arrange
        with pytest.raises(EmptyFieldsError) as exc:
            # Action
            Product(name=None, cost_values="", unit_box='  ', weight_unit=None, sku=None, description=None,
                    validity='', category_line_id=None, supplier_id=None)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) cannot be empty: name, cost_values, unit_box, weight_unit, sku, '
                         'validity, category_line_id, supplier_id', exc.value.description)

    def test_product_must_raise_a_str_field_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:
            # Action
            Product(name=1, cost_values=10.15, unit_box=5, weight_unit=0.550, validity="2021-12-31",
                    sku={'sku': ''}, description=123443423231314, category_line_id=1 * 36, supplier_id=1 * 36)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type str: name, sku, description, category_line_id, '
                         'supplier_id', exc.value.description)

    def test_product_must_raise_a_bool_field_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:
            # Action
            Product(active='0', name='Nescau', cost_values=10.15, unit_box=5, weight_unit=0.550, validity="2021-12-31",
                    sku='09ub124ibbi413', description='Descrição...',
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type bool: active', exc.value.description)

    def test_product_must_raise_an_int_field_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:
            # Action
            Product(name='Nescau', cost_values=10.15, unit_box=-5.0, weight_unit=0.550, validity="2021-12-31",
                    sku='09ub124ibbi413', description='Descrição...',
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type int positive: unit_box', exc.value.description)

    def test_product_must_raise_a_float_field_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:
            # Action
            Product(name='Nescau', cost_values=-10.15, unit_box=5, weight_unit=100, validity="2021-12-31",
                    sku='09ub124ibbi413', description='Descrição...',
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type float positive: cost_values, weight_unit',
                         exc.value.description)

    def test_product_must_raise_an_alpha_exception(self):
        # Arrange
        with pytest.raises(TextError) as exc:
            # Action
            Product(name='Teste 1', cost_values=10.15, unit_box=5, weight_unit=0.550, validity="2021-12-31",
                    sku='09ub124ibbi413', description='Descrição...',
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be only letters: name', exc.value.description)

    def test_product_must_raise_an_incorrect_validity_exception(self):
        # Arrange
        with pytest.raises(ValidityError) as exc:
            # Action
            Product(name='Teste', cost_values=10.15, unit_box=5, weight_unit=0.550, validity="2021/12/31",
                    sku='09ub124ibbi413', description='Descrição...',
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Incorrect data format. Validity date should be YYYY-MM-DD', exc.value.description)

    def test_product_must_raise_an_expired_validity_exception(self):
        # Arrange
        with pytest.raises(ValidityError) as exc:
            # Action
            Product(name='Teste', cost_values=10.15, unit_box=5, weight_unit=0.550, validity="2019-12-31",
                    sku='09ub124ibbi413', description='Descrição...',
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7ed",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7ed")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The validity date inserted is past it is expiry date', exc.value.description)

    def test_product_must_raise_a_size_exception(self):
        # Arrange
        with pytest.raises(SizeError) as exc:
            # Action
            Product(name='a' * 81, cost_values=10.151, unit_box=5, weight_unit=0.5501, validity="2021-12-31",
                    sku='09ub124ibbi413', description='D' * 151,
                    category_line_id="7d2d8d86-1908-4a8b-b84a-2ebeb160b7edd",
                    supplier_id="7d2d8d86-0000-4a8b-b84a-2ebeb160b7edd")

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'name', 'cost_values', 'weight_unit', 'description', 'category_line_id', "
                         "'supplier_id' must be the following maximum sizes respectively: 80, 2 decimal places, "
                         "3 decimal places, 150, 36, 36", exc.value.description)

    @patch('app.domains.products.models.Product')
    def test_products_models_serialize_final_cost_method(self, product_mock):
        # Arrange
        _id = str(uuid4())
        id = str(uuid4())
        product_mock.query.filter.return_value.first.return_value = []
        products = Product(id=_id, active=False, name='Nescau', cost_values=10.15, unit_box=5, weight_unit=0.550,
                           validity="2021-12-31", sku='09ub124ibbi413', description='Descrição...',
                           category_line_id=id, supplier_id=id,
                           on_create=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                           on_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Action
        response = products.serialize_final_cost(15.0)

        # Assertions
        self.assertEqual(type(response), dict)
        self.assertIsInstance(products, Product)
        self.assertEqual({'active': False,
                          'category_line_id': id,
                          'cost_values': 25.15,
                          'description': 'Descrição...',
                          'id': _id,
                          'name': 'Nescau',
                          'on_create': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          'on_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                          'sku': '09ub124ibbi413',
                          'supplier_id': id,
                          'unit_box': 5,
                          'validity': '2021-12-31',
                          'weight_unit': 0.55}, response)
