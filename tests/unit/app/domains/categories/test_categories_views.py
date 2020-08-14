import io
from unittest.mock import patch, MagicMock, Mock
import pytest

from app.exceptions.exceptions import JsonError
from app.domains.products.views import validating_if_json_is_correct
from app.domains.export_csv.actions import create_csv_file
from tests.unit import AbstractViewUnitTest


class TestCategoriesViews(AbstractViewUnitTest):

    @patch('app.domains.categories.views.get_category')
    def test_get_categories(self, get_category_mock):
        # Arrange
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={})
        get_category_mock.return_value = [obj_view]

        # Action
        response = self._client.get('/categories')
        data = response.get_json()

        # Assertions
        get_category_mock.assert_called_once()
        self.assertEqual(1, len(data))

    @patch('app.domains.categories.views.get_category_by_id')
    def test_get_category_by_id_should_be_1(self, get_category_by_id_mock):
        # Arrange
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': '06c17fbe-55fd-49e2-a616-0b9fd173223c',
                                                     'name': 'Laticínios'})
        get_category_by_id_mock.return_value = obj_view
        id = '06c17fbe-55fd-49e2-a616-0b9fd173223c'

        # Action
        response = self._client.get('/categories/{}'.format(id))

        # Assertions
        get_category_by_id_mock.assert_called_once_with(id)
        self.assertEqual(response.status_code, 200)

    @patch('app.domains.categories.views.create_category')
    def test_post_category_should_be_created(self, create_category_mock):
        # Arrange
        payload = {'name': 'Laticínios'}
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': 'cd26c599-9978-4216-b209-b55a954d36ba',
                                                     'name': 'Laticínios'})
        create_category_mock.return_value = obj_view

        # Action
        response = self._client.post('/categories', json=payload)

        # Assertions
        create_category_mock.assert_called_once_with({'name': 'Laticínios'})
        self.assertEqual(response.status_code, 201)

    @patch('app.domains.categories.views.create_category')
    def test_post_category_should_raise_a_exception(self, create_category_mock):
        # Arrange
        with pytest.raises(JsonError) as exc:

            # Action
            self._client.post('/categories', json={})
            validating_if_json_is_correct(['name'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): name',
                         exc.value.description)

    @patch('app.domains.categories.views.update_category')
    def test_put_category_should_be_updated(self, update_category_mock):
        # Arrange
        _id = '06c17fbe-55fd-49e2-a616-0b9fd173223c'
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={'id': '06c17fbe-55fd-49e2-a616-0b9fd173223c', 'name': 'BBB'})
        update_category_mock.return_value = obj_view

        # Action
        response = self._client.put('/categories/{}'.format(_id), json={'name': 'BBB'})

        # Assertions
        update_category_mock.assert_called_once_with(_id, {'name': 'BBB'})
        self.assertEqual(response.status_code, 200)

    @patch('app.domains.categories.views.get_category')
    def test_if_export_is_sending_file_to_download(self, get_category_mock):
        # Arrange
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={})
        get_category_mock.return_value = [obj_view]

        # Action
        response = self._client.get('/categories:export')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=Categories.csv")
        self.assertEqual(response.headers["Content-type"], "text/csv")

    @patch('app.domains.categories.views.insert_data')
    @patch('app.domains.categories.views.get_category')
    def test_import_route_method(self, get_mock, insert_mock):
        # Arrange
        insert_mock.return_value = None
        category1 = Mock()
        category1.serialize = MagicMock(return_value={'teste': 'teste'})
        category1.name = 'Teste1'
        category2 = Mock()
        category2.serialize = MagicMock(return_value={'teste2': 'teste2'})
        category2.name = 'Teste2'
        get_mock.return_value = [category1, category2]

        data = {'id': 'id', 'name': 'name'}
        data = {key: str(value) for key, value in data.items()}
        data['data_file'] = (io.BytesIO(b'\xef\xbb\xbfage,name\r\n'
                                        b'18,Categoria A\r\n'
                                        b'12, CATEGORIA B \r\n'
                                        b'1, categoria C\r\n'), 'import.csv')

        # Action
        response = self._client.post('/categories:import', data=data, follow_redirects=True,
                                     content_type='multipart/form-data')
        json = response.get_json()

        # Assertions
        get_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, len(data))
        self.assertEqual(json, [{'teste': 'teste'}, {'teste2': 'teste2'}])

    def test_import_route_method_if_has_no_file(self):
        # Arrange
        data = {'id': 'id', 'name': 'name'}
        data = {key: str(value) for key, value in data.items()}
        data['data_file'] = ([])

        # Action
        response = self._client.post(
            '/categories:import', data=data, follow_redirects=True,
            content_type='multipart/form-data')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'{"code": 400, "message": "No file"}')
