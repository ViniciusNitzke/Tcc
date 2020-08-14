import unittest
import pytest

from app.domains.category_lines.models import *


class TestCategoryLine(unittest.TestCase):
    def test_serializing_the_category_lines_model(self):
        # Arrange
        id = str(uuid4())
        category_id = str(uuid4())
        category_line = CategoryLine(id=id,
                                     active=True,
                                     category_line='teste',
                                     category_id=category_id,
                                     on_create=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                     on_update=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Action
        json = category_line.serialize()

        # Assertions
        self.assertIsInstance(category_line, CategoryLine)
        self.assertEqual(json['id'], id)
        self.assertEqual(json['active'], True)
        self.assertEqual(json['category_line'], 'teste')
        self.assertEqual(json['category_id'], category_id)
        self.assertEqual(json['on_create'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(json['on_update'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    def test_category_line_must_raise_an_empty_field_exception(self):
        # Arrange
        with pytest.raises(EmptyFieldsError) as exc:

            # Action
            CategoryLine(category_line=' ', category_id=None)
            CategoryLine()

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) cannot be empty: category_line, category_id', exc.value.description)

    def test_cateogry_line_must_raise_a_not_str_exception(self):
        # Arrange
        with pytest.raises(TypeError) as exc:

            # Action
            CategoryLine(category_line=1, category_id=['Teste'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type str: category_line, category_id',
                         exc.value.description)

    def test_cateogry_line_must_raise_a_not_bool_exception(self):
        # Arrange
        id = str(uuid4())
        with pytest.raises(TypeError) as exc:

            # Action
            CategoryLine(active='true', category_line='Teste', category_id=id)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following field(s) must be of type bool: active', exc.value.description)

    def test_address_must_raise_an_size_exception(self):
        # Arrange
        id = str(uuid4())
        with pytest.raises(SizeError) as exc:

            # Action
            CategoryLine(category_line='A'*101, category_id=id+'1')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("The field(s) 'category_line', 'category_id' must be the following maximum sizes "
                         "respectively: 100, 36", exc.value.description)
