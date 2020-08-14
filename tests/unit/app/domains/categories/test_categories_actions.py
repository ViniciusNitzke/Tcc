import unittest
import pytest
from unittest.mock import patch, MagicMock, Mock
from sqlalchemy.exc import SQLAlchemyError

from app.domains.categories.models import *
from app.exceptions.exceptions_of_import import *
from app.domains.categories.actions import get_by_id, \
    update, \
    create, \
    get, \
    inserting_categories_names_from_the_csv_file_in_db


class TestCategoriesActions(unittest.TestCase):

    @patch('app.domains.categories.actions.Category')
    @patch('app.domains.categories.actions.save')
    def test_action_create_should_be_created_new_category(self, save_mock, category_mock):
        # Arrange
        model_id = str(uuid4())

        category_mock.id = model_id
        category_mock.active = True
        category_mock.name = 'Teste'
        category_mock.profit_percentage = 15.0
        category_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        category_mock.query = query
        category_mock.query.filter.return_value.first.return_value = []

        # Action
        create({'active': category_mock.active, 'name': category_mock.name,
                'profit_percentage': category_mock.profit_percentage})

        # Assertions
        self.assertTrue(save_mock.called)
        self.assertEqual(category_mock.active, True)
        self.assertEqual(category_mock.name, 'Teste')
        self.assertEqual(category_mock.profit_percentage, 15.0)
        self.assertEqual(category_mock.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(category_mock.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.categories.actions.save')
    def test_category_create_must_raise_a_sql_alchemy_error(self, save_mock):
        # Arrange
        id = str(uuid4())
        save_mock.side_effect = SQLAlchemyError
        with pytest.raises(RepeatedValueError) as exc:

            # Action
            create({'name': 'Teste', 'profit_percentage': 15.0})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following values already exist in the database: Teste', exc.value.description)

    @patch('app.domains.categories.actions.Category')
    def test_action_get_by_id_should_be_return_category(self, category_mock):
        # Arrange
        id = str(uuid4())
        category_saved = Mock()
        category_saved.id = id
        category_saved.active = True
        category_saved.name = 'Teste'
        category_saved.profit_percentage = 15.0
        category_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        query.get = MagicMock(return_value=category_saved)
        category_mock.query = query

        # Action
        category = get_by_id(category_mock.id)

        # Assertions
        category_mock.query.get.assert_called_once_with(category_mock.id)
        self.assertEqual(category_saved, category)

    @patch('app.domains.categories.actions.Category')
    def test_actions_get_by_id_should_raise_a_id_exception(self, category_mock):
        # Arrange
        category_mock.query.get.return_value = None
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id(category_mock.id)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.categories.actions.Category')
    def test_action_get_should_be_return_categories(self, category_mock):
        # Arrange
        category_mock.active = str(uuid4())
        category_mock.active = True
        category_mock.name = 'Name'
        category_mock.profit_percentage = 15.0
        category_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        query.all = MagicMock(return_value=[category_mock])
        category_mock.query = query

        # Action
        categories = get()

        # Assertions
        self.assertTrue(category_mock.query.all.called)
        self.assertEqual(len(categories), 1)

    @patch('app.domains.categories.actions.get_by_id')
    @patch('app.domains.categories.actions.commit')
    def test_action_update_should_be_updated_category(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        category_saved = Mock()
        category_saved.active = True
        category_saved.name = 'Name'
        category_saved.profit_percentage = 20.0
        category_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        get_by_id_mock.return_value = category_saved
        category_saved.serialize.return_value = {}

        # Action
        category = update(id,
                          {'name': 'Teste Update',
                           'profit_percentage': 20.0,
                           'active': False})

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertTrue(commit_mock.called)
        self.assertEqual(category.active, False)
        self.assertEqual(category.name, 'Teste Update')
        self.assertEqual(category.profit_percentage, 20.0)
        self.assertEqual(category.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(category.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.categories.actions.get_by_id')
    @patch('app.domains.categories.actions.commit')
    def test_category_update_must_raise_a_sql_alchemy_error(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        commit_mock.side_effect = SQLAlchemyError
        with pytest.raises(RepeatedValueError) as exc:

            # Action
            update(id, {'name': 'Teste'})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following values already exist in the database: Teste', exc.value.description)

    @patch('app.domains.categories.actions.get_by_id')
    @patch('app.domains.categories.actions.commit')
    def test_category_must_raise_a_json_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        with pytest.raises(JsonError) as exc:

            # Action
            update(id, None)

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): name', exc.value.description)

    @patch('app.domains.categories.actions.get_by_id')
    @patch('app.domains.categories.actions.commit')
    def test_category_must_raise_an_id_exception(self, commit_mock, get_by_id_mock):
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

    @patch('app.domains.categories.actions.Category')
    @patch('app.domains.categories.actions.save')
    @patch('app.domains.categories.actions.import_csv_file')
    @patch('app.domains.categories.actions.get')
    def test_action_inserting_categories_names_from_the_csv_file_in_db_should_return_a_list_of_saved_categories(self,
                                                                                                                get_mock,
                                                                                                                import_csv_mock,
                                                                                                                save_mock,
                                                                                                                category_mock):
        # Arrange
        category = Mock()
        category.name = 'category 1'
        get_mock.return_value = [category]
        import_csv_mock.return_value = [{'name': 'category 2'}]

        # Action
        response = inserting_categories_names_from_the_csv_file_in_db(['name', 'category 2'], 'name')

        # Assertions
        self.assertTrue(get_mock.called)
        self.assertTrue(import_csv_mock.called)
        self.assertTrue(save_mock.called)
        self.assertTrue(category_mock.called)
        self.assertEqual(category.name, 'category 1')
        self.assertEqual([category], get_mock.return_value)
        self.assertEqual([{'name': 'category 2'}], import_csv_mock.return_value)
        self.assertEqual([save_mock()], response)

    @patch('app.domains.categories.actions.Category')
    @patch('app.domains.categories.actions.save')
    @patch('app.domains.categories.actions.import_csv_file')
    @patch('app.domains.categories.actions.get')
    def test_action_inserting_categories_names_from_the_csv_file_in_db_should_raise_a_repeated_data_error(self,
                                                                                                          get_mock,
                                                                                                          import_csv_mock,
                                                                                                          save_mock,
                                                                                                          category_mock):
        # Arrange
        id = str(uuid4())
        get_mock.return_value = [category_mock]
        save_mock.side_effect = SQLAlchemyError
        import_csv_mock.return_value = [{'name': 'category 1'}, 'name']
        with pytest.raises(RepeatedDataError) as exc:

            # Action
            inserting_categories_names_from_the_csv_file_in_db(['name', 'category 1', 'category 1'], 'name')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The following values are repeated in the file, but will be added only once: category 1',
                         exc.value.description)

    @patch('app.domains.categories.actions.Category')
    @patch('app.domains.categories.actions.save')
    @patch('app.domains.categories.actions.import_csv_file')
    @patch('app.domains.categories.actions.get')
    def test_action_inserting_categories_names_from_the_csv_file_in_db_should_raise_a_data_already_exists_error(self,
                                                                                                                get_mock,
                                                                                                                import_csv_mock,
                                                                                                                save_mock,
                                                                                                                category_mock):
        # Arrange
        category_mock.side_effect = DataAlreadyExistsError
        with pytest.raises(DataAlreadyExistsError) as exc:

            # Action
            inserting_categories_names_from_the_csv_file_in_db(['name', 'category 2'], 'name')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('All the data in the file has already been added', exc.value.description)
