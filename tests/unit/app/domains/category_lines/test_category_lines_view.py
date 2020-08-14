import pytest
from unittest.mock import patch, MagicMock, Mock

from app.exceptions.exceptions import JsonError
from app.domains.products.views import validating_if_json_is_correct
from tests.unit import AbstractViewUnitTest


class TestCategoryView(AbstractViewUnitTest):

    @patch('app.domains.category_lines.views.get_category_line')
    def test_get_category_line(self, get_category_line_mock):
        # Arrange
        object_view = Mock()
        object_view.serialize = MagicMock(return_value={})
        get_category_line_mock.return_value = [object_view]

        # Action
        response = self._client.get('/category_line')
        data = response.get_json()

        # Assertions
        get_category_line_mock.assert_called_once()
        self.assertEqual(1, len(data))

    @patch('app.domains.category_lines.views.get_by_id_category_line')
    def test_get_by_id_category_line_should_be_1(self, get_by_id_category_line_mock):
        # Arrange
        object_view = Mock()
        object_view.serialize = MagicMock(
            return_value={'id': '06c17ft-55fd-49a2-a616-0b9fd173223c', 'category_line': 'Nescau',
                          'category_id': '06c17ft-55fd-50b3-m777-0b9fd173223c'})
        get_by_id_category_line_mock.return_value = object_view
        id = '06c17ft-55fd-49a2-a616-0b9fd173223c'

        # Action
        response = self._client.get(f'/category_line/{id}')

        # Assertions
        self.assertEqual(response.status_code, 200)
        get_by_id_category_line_mock.assert_called_once_with(id)

    @patch('app.domains.category_lines.views.create_category_line')
    def test_post_category_line_should_be_created(self, create_category_line_mock):
        # Arrange
        payload = {
            'category_line': 'Nescau',
            'category_id': '06c17ft-55fd-50b3-m777-0b9fd173223c',
        }

        object_view = Mock()
        object_view.serialize = MagicMock(
            return_value={'id': '06c17ft-55fd-49a2-a616-0b9fd173223c', 'category_line': 'Nescau',
                          'category_id': '06c17ft-55fd-50b3-m777-0b9fd173223c'})
        create_category_line_mock.return_value = object_view

        # Action
        response = self._client.post('/category_line', json=payload)

        # Assertions
        self.assertEqual(response.status_code, 201)
        create_category_line_mock.assert_called_once_with({'category_line': 'Nescau',
                                                           'category_id': '06c17ft-55fd-50b3-m777-0b9fd173223c'})

    @patch('app.domains.category_lines.views.create_category_line')
    def test_post_category_line_should_raise_a_exception(self, create_category_line_mock):
        # Arrange
        with pytest.raises(JsonError) as exc:

            # Action
            self._client.post('/category_line', json={})
            validating_if_json_is_correct(['category_line'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): category_line',
                         exc.value.description)

    @patch('app.domains.category_lines.views.update_category_line')
    def test_put_category_line_should_be_updated(self, update_category_line_mock):
        # Arrange
        _id = '06c17ft-55fd-49a2-a616-0b9fd173223c'
        object_view = Mock()
        object_view.serialize = MagicMock(
            return_value={'id': '06c17ft-55fd-49a2-a616-0b9fd173223c', 'category_line': 'Leite Ninho'})
        update_category_line_mock.return_value = object_view

        # Action
        response = self._client.put(f'/category_line/{_id}', json={'category_line': 'Leite Ninho'})

        # Assertions
        self.assertEqual(response.status_code, 200)
        update_category_line_mock.assert_called_once_with(_id, {'category_line': 'Leite Ninho'})
