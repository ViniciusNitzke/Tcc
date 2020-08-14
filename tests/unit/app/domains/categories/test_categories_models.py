import unittest
from unittest.mock import patch, Mock
import pytest

from app.domains.categories.models import *


class TestCategoriesModels(unittest.TestCase):
    def test_category_model_serialize_method(self):
        # Arrange
        id = str(uuid4())
        categories_mock = Mock()
        categories_mock.id = id
        categories_mock.name = 'Teste'
        categories_mock.active = True
        categories_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        categories_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Assertions
        self.assertEqual(categories_mock.id, id)
        self.assertEqual(categories_mock.name, 'Teste')
        self.assertEqual(categories_mock.active, True)
        self.assertEqual(categories_mock.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(categories_mock.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.categories.models.Category')
    def test_category_serialize_return_dict(self, category_mock):
        # Arrange
        id = str(uuid4())
        category_mock.id = id
        category_mock.name = 'Teste'
        category_mock.profit_percentage = 15.0
        category_mock.active = True
        category_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Action
        serialized = Category.serialize(category_mock)

        # Assertions
        self.assertEqual(serialized, {
            'id': id,
            'active': True,
            'name': 'Teste',
            'profit_percentage': 15.0,
            'on_create': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'on_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })

    def test_category_must_raise_an_empty_field_exception(self):
        # Arrange
        with pytest.raises(EmptyFieldsError) as exc:

            # Action
            Category(name=None)
            Category()

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) cannot be empty: name', exc.value.description)

    def test_cateogry_must_raise_a_not_str_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:

            # Action
            Category(name=1)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type str: name',
                         exc.value.description)

    def test_cateogry_must_raise_a_not_bool_exception(self):
        # Arrange
        id = str(uuid4())
        with pytest.raises(TypeError) as exc:

            # Action
            Category(active='true', name='Teste', profit_percentage=15.0)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type bool: active', exc.value.description)

    def test_address_must_raise_a_size_exception(self):
        # Arrange
        id = str(uuid4())
        with pytest.raises(SizeError) as exc:

            # Action
            Category(name='A'*81)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'name' must be the following maximum sizes respectively: 80",
                         exc.value.description)
