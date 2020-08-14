import unittest
from uuid import uuid4
import pytest
from unittest.mock import patch

from app.domains.import_csv.actions import *
from app.exceptions.exceptions_of_import import *


class TestImportsActions(unittest.TestCase):

    @patch('app.domains.import_csv.actions.csv.DictReader')
    def test_action_import_should_return_a_list_of_dictionaries(self, dict_reader_mock):
        # Arrange
        id = str(uuid4())
        dict_reader_mock.return_value = {'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                                         'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                                         'category_line_id': id, 'supplier_id': id}, \
                                        {'name': 'name dois', 'cost_values': 12.54, 'unit_box': 20,
                                         'weight_unit': 25.23, 'validity': "2021-10-10", 'sku': '342343',
                                         'description': 'descricao', 'category_line_id': id, 'supplier_id': id}

        # Action
        response = import_product_csv_file(['import_file'])

        # Assertions
        dict_reader_mock.assert_called_once_with(['import_file'], delimiter=',')
        self.assertEqual(list, type(response))
        self.assertEqual([{'name': 'name', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                           'validity': "2021-10-10", 'sku': '342343', 'description': 'descricao',
                           'category_line_id': id, 'supplier_id': id}, {'name': 'name dois', 'cost_values': 12.54,
                                                                        'unit_box': 20, 'weight_unit': 25.23,
                                                                        'validity': "2021-10-10", 'sku': '342343',
                                                                        'description': 'descricao',
                                                                        'category_line_id': id, 'supplier_id': id}],
                         response)

    def test_action_import_should_raise_a_data_already_exist_exception(self):
        # Arrange
        with pytest.raises(DataAlreadyExistsError) as exc:

            # Action
            import_product_csv_file(['teste'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('All the data in the file has already been added', exc.value.description)

    @patch('app.domains.import_csv.actions.csv.DictReader')
    def test_action_import_should_raise_a_column_exception(self, dict_reader_mock):
        # Arrange
        dict_reader_mock.side_effect = KeyError
        with pytest.raises(ColumnsError) as exc:

            # Action
            import_product_csv_file(['teste'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("Check that the columns were typed correctly in the file and that all fields are separated "
                         "by ',' ", exc.value.description)

    @patch('app.domains.import_csv.actions.csv.DictReader')
    def test_action_import_should_raise_a_type_exception(self, dict_reader_mock):
        # Arrange
        dict_reader_mock.side_effect = ValueError
        with pytest.raises(ConversionError) as exc:

            # Action
            import_product_csv_file(['name'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("Check that the types of values match their columns", exc.value.description)
