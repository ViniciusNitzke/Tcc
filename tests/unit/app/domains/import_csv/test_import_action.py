import unittest
import pytest
from unittest.mock import patch

from app.domains.import_csv.actions import *
from app.exceptions.exceptions_of_import import *


class TestImportsActions(unittest.TestCase):

    @patch('app.domains.import_csv.actions.csv.DictReader')
    def test_action_import_should_return_a_list_of_dictionaries(self, dict_reader_mock):
        # Arrange
        dict_reader_mock.return_value = {'teste': '    catEgory 1    '}, {'teste': 'CATEGORY 2'}

        # Action
        response = import_csv_file(['teste', 'category 1', 'category 2'], 'teste')

        # Assertions
        dict_reader_mock.assert_called_once_with(['teste', 'category 1', 'category 2'], delimiter=',')
        self.assertEqual(list, type(response))
        self.assertEqual([{'teste': 'category 1'}, {'teste': 'category 2'}], response)

    def test_action_import_should_raise_a_data_already_exist_exception(self):
        # Arrange
        with pytest.raises(DataAlreadyExistsError) as exc:

            # Action
            import_csv_file(['teste'], 'teste')

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
            import_csv_file(['teste'], '')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual("Check that the columns were typed correctly in the file and that all fields are separated "
                         "by ',' ", exc.value.description)
