import unittest
import pytest
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch, MagicMock, Mock

from app.domains.categories.models import *
from app.domains.category_lines.actions import get_by_id, update, create, get, get_category_percentage


class TestSuppliersActions(unittest.TestCase):
    @patch('app.domains.category_lines.actions.CategoryLine')
    @patch('app.domains.category_lines.actions.save')
    def test_if_category_lines_actions_creates_a_new_category_line(self, save_mock, category_lines_mock):
        # Arrange
        model_id = str(uuid4())
        category_id = str(uuid4())
        category_lines_mock.id = model_id
        category_lines_mock.category_line = 'Teste'
        category_lines_mock.profit_percentage = 15.0
        category_lines_mock.category_id = category_id
        category_lines_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_lines_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        query = Mock()
        category_lines_mock.query = query
        category_lines_mock.query.filter.return_value.first.return_value = []

        # Action
        create({'category_line': category_lines_mock.category_line,
                'category_id': category_lines_mock.id,
                'profit_percentage': category_lines_mock.profit_percentage})

        # Assertions
        self.assertTrue(save_mock.called)
        self.assertEqual(category_lines_mock.category_line, 'Teste')
        self.assertEqual(category_lines_mock.profit_percentage, 15.0)
        self.assertEqual(category_lines_mock.category_id, category_id)
        self.assertEqual(category_lines_mock.on_create, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.assertEqual(category_lines_mock.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.category_lines.actions.save')
    def test_category_line_create_must_raise_a_sql_alchemy_error(self, save_mock):
        # Arrange
        id = str(uuid4())
        save_mock.side_effect = SQLAlchemyError
        with pytest.raises(InvalidValueError) as exc:

            # Action
            create({'category_line': 'Teste', 'category_id': id, 'profit_percentage': 15.0})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be '
                         'unique: category_line', exc.value.description)

    @patch('app.domains.category_lines.actions.CategoryLine')
    def test_if_get_by_id_returns_a_category_line(self, category_line_mock):
        # Arrange
        category_id = str(uuid4())
        category_saved = Mock()
        category_saved.category_line = 'teste'
        category_saved.category_id = category_id
        category_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = Mock()
        query.get = MagicMock(return_value=category_line_mock)
        category_line_mock.query = query

        # Action
        category_line = get_by_id(category_line_mock.id)

        # Assertions
        category_line_mock.query.get.assert_called_once_with(category_line_mock.id)
        self.assertEqual(category_line_mock, category_line)

    @patch('app.domains.category_lines.actions.CategoryLine')
    def test_actions_get_by_id_should_raise_a_id_exception(self, category_line_mock):
        # Arrange
        category_line_mock.query.get.return_value = None
        with pytest.raises(IdNotExistError) as exc:
            # Action
            get_by_id(category_line_mock.id)

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The ID(s) inserted does not exist in the database', exc.value.description)

    @patch('app.domains.category_lines.actions.CategoryLine')
    def test_if_get_returns_category_lines(self, category_line_mock):
        # Arrange
        category_id = str(uuid4())
        category_line_mock.category_line = 'Test'
        category_line_mock.category_id = category_id
        category_line_mock.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_line_mock.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        query = Mock()
        query.all = MagicMock(return_value=[category_line_mock])
        category_line_mock.query = query

        # Action
        category_lines = get()

        # Assertions
        self.assertTrue(category_line_mock.query.all.called)
        self.assertEqual(len(category_lines), 1)

    @patch('app.domains.category_lines.actions.get_by_id')
    @patch('app.domains.category_lines.actions.commit')
    def test_action_update_should_be_updated_category_line(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        category_id = str(uuid4())
        category_line_saved = Mock()
        category_line_saved.category_line_saved = 'teste'
        category_line_saved.category_id = category_id
        category_line_saved.on_create = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        category_line_saved.on_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        get_by_id_mock.return_value = category_line_saved
        category_line_saved.serialize.return_value = {}

        # Action
        category_line = update(id,
                               {'category_line': 'teste',
                                'category_id': category_id})

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertTrue(commit_mock.called)
        self.assertEqual(category_line.category_line, 'teste')
        self.assertEqual(category_line.category_id, category_id)
        self.assertEqual(category_line.on_create, category_line_saved.on_create)
        self.assertEqual(category_line.on_update, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    @patch('app.domains.category_lines.actions.get_by_id')
    @patch('app.domains.category_lines.actions.commit')
    def test_category_line_must_raise_a_json_exception(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        with pytest.raises(JsonError) as exc:

            # Action
            update(id, [])

        # Assertions
        get_by_id_mock.assert_called_once_with(id)
        self.assertFalse(commit_mock.called)
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): category_line, category_id',
                         exc.value.description)

    @patch('app.domains.category_lines.actions.get_by_id')
    @patch('app.domains.category_lines.actions.commit')
    def test_category_line_must_raise_an_id_exception(self, commit_mock, get_by_id_mock):
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

    @patch('app.domains.category_lines.actions.get_by_id')
    @patch('app.domains.category_lines.actions.commit')
    def test_category_line_must_raise_a_sql_alchemy_error(self, commit_mock, get_by_id_mock):
        # Arrange
        id = str(uuid4())
        commit_mock.side_effect = SQLAlchemyError
        with pytest.raises(InvalidValueError) as exc:

            # Action
            update(id, {'category_line': 'Teste1', 'category_id': id})

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('Check if the ID field(s) are entered correctly. If so, the following field(s) must be '
                         'unique: category_line', exc.value.description)

    @patch('app.domains.category_lines.actions.get_category_by_id')
    @patch('app.domains.category_lines.actions.get_by_id')
    def test_get_category_percentage(self,
                                     get_by_line_id_mock,
                                     get_category_by_id_mock):
        # Arrange
        id = str(uuid4())
        _id = str(uuid4())

        category_line = Mock()
        category_line.id = id
        category_line.category_id = _id
        category = Mock()
        category.profit_percentage = 15.0

        get_by_line_id_mock.return_value = category_line
        get_category_by_id_mock.return_value = category

        # Action
        percentage = get_category_percentage(id)

        # Assertions
        self.assertTrue(get_by_line_id_mock.called)
        self.assertTrue(get_category_by_id_mock.called)
        self.assertEqual(percentage, category.profit_percentage)
