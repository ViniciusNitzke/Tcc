import pytest
import io
import csv
from uuid import uuid4
from unittest.mock import patch, MagicMock, Mock

from tests.unit import AbstractViewUnitTest
from app.exceptions.exceptions import JsonError
from app.domains.products.views import validating_if_json_is_correct


class TestProductsViews(AbstractViewUnitTest):

    @patch('app.domains.products.views.get_products')
    @patch('app.domains.products.views.get_percentages')
    def test_get_products_should_be_1(self, get_percentages_mock, get_products_mock):
        # Arrange
        obj = Mock()
        get_percentages_mock.return_value = [50]
        obj.serialize_final_cost = MagicMock(return_value={})
        get_products_mock.return_value = [obj]

        # Action
        response = self._client.get('/products')
        data = response.get_json()

        # Assertions
        self.assertEqual(len(data), 1)
        get_products_mock.assert_called_once()

    @patch('app.domains.products.views.get_percentages')
    @patch('app.domains.products.views.get_products_by_id')
    def test_get_products_by_id_should_be_1(self, get_products_by_id_mock, get_percentages_mock):
        # Arrange
        id = str(uuid4())
        obj = Mock()
        get_percentages_mock.return_value = [50]
        obj.serialize_final_cost = MagicMock(return_value={})
        get_products_by_id_mock.id = id
        get_products_by_id_mock.return_value = obj

        # Action
        response = self._client.get('/products/{}'.format(id))

        # Assertions
        self.assertEqual(response.status_code, 200)
        get_products_by_id_mock.assert_called_once_with(id)

    @patch('app.domains.products.views.create_products')
    def test_post_products_should_be_created(self, create_products_mock):
        # Arrange
        payload = {
            'name': 'produto',
            'cost_values': '10',
            'line': 'AAA',
            'unit_box': '5',
            'weight_unit': '0,5',
            'validity': '20/12/2021',
            'sku': '09ub124ibbi413',
            'description': 'Descrição...'}
        obj = Mock()
        obj.serialize = MagicMock(return_value={})
        create_products_mock.return_value = obj

        # Action
        response = self._client.post('/products', json=payload)

        # Assertions
        self.assertEqual(response.status_code, 201)
        create_products_mock.assert_called_once_with({
            'name': 'produto',
            'cost_values': '10',
            'line': 'AAA',
            'unit_box': '5',
            'weight_unit': '0,5',
            'validity': '20/12/2021',
            'sku': '09ub124ibbi413',
            'description': 'Descrição...'})

    def test_post_products_should_raise_a_exception(self):
        # Arrange
        with pytest.raises(JsonError) as exc:
            # Action
            self._client.post('/products', json={})
            validating_if_json_is_correct(['sku'])

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('The JSON data must contain the following field(s): sku', exc.value.description)

    @patch('app.domains.products.views.update_products')
    def test_put_products_should_be_updated(self, update_products_mock):
        # Arrange
        _id = '1f6d2021-0e2a-4ba3-0011-5472b6df7244'
        obj = Mock()
        obj.serialize = MagicMock(return_value={
            'name': 'produto',
            'cost_values': '10',
            'line': 'AAA',
            'unit_box': '5',
            'weight_unit': '0,5',
            'validity': '20/12/2021',
            'sku': '09ub124ibbi413',
            'description': 'Descrição...'})
        update_products_mock.return_value = obj

        # Action
        response = self._client.put('/products/{}'.format(_id), json={
            'name': 'produto',
            'cost_values': '10',
            'line': 'AAA',
            'unit_box': '5',
            'weight_unit': '0,5',
            'validity': '20/12/2021',
            'sku': '09ub124ibbi413',
            'description': 'Descrição...'})

        # Assertions
        self.assertEqual(response.status_code, 200)
        update_products_mock.assert_called_once_with('1f6d2021-0e2a-4ba3-0011-5472b6df7244', {
            'name': 'produto',
            'cost_values': '10',
            'line': 'AAA',
            'unit_box': '5',
            'weight_unit': '0,5',
            'validity': '20/12/2021',
            'sku': '09ub124ibbi413',
            'description': 'Descrição...'
        })

    @patch('app.domains.products.views.get_products')
    def test_if_export_is_sending_file_to_download(self, get_product_mock):
        # Arrange
        obj_view = Mock()
        obj_view.serialize = MagicMock(return_value={})
        get_product_mock.return_value = [obj_view]

        # Action
        response = self._client.get('/products:export')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=Products.csv")
        self.assertEqual(response.headers["Content-type"], "text/csv")

    @patch('app.domains.products.actions.save')
    def test_import_product_route_method(self, save_mock):
        # Arrange
        id = str(uuid4())
        data1 = {'name': 'teste um', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                 'validity': "2021-10-10", 'sku': '34234323', 'description': 'descricao', 'category_line_id': id,
                 'supplier_id': id}
        data = {key: str(value) for key, value in data1.items()}
        csv_file = io.StringIO()
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
        bytes_data = bytes(csv_file.getvalue(), 'utf-8')
        data['data_file'] = (io.BytesIO(bytes_data), 'import.csv')

        # Action
        response = self._client.post('/products:import', data=data, follow_redirects=True,
                                     content_type='multipart/form-data')
        data = response.get_json()
        save_mock(data)

        # Assertions
        save_mock.assert_called_with(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(data))

    def test_import_route_method_if_has_no_file(self):
        # Arrange
        data = {}
        data = {key: str(value) for key, value in data.items()}
        data['data_file'] = ([])

        # Action
        response = self._client.post(
            '/products:import', data=data, follow_redirects=True,
            content_type='multipart/form-data')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'{"code": 400, "message": "No file"}')

    @patch('app.domains.products.actions.save')
    def test_import_product_by_supplier_route_method(self, save_mock):
        # Arrange
        id = str(uuid4())
        data1 = {'name': 'teste um', 'cost_values': 12.54, 'unit_box': 20, 'weight_unit': 25.23,
                 'validity': "2021-10-10", 'sku': '34234323', 'description': 'descricao', 'category_line_id': id,
                 'supplier_id': id}
        data = {key: str(value) for key, value in data1.items()}
        csv_file = io.StringIO()
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
        bytes_data = bytes(csv_file.getvalue(), 'utf-8')
        data['data_file'] = (io.BytesIO(bytes_data), 'import.csv')

        # Action
        response = self._client.post('/products:import-by-supplier', data=data, follow_redirects=True,
                                     content_type='multipart/form-data')
        save_mock(response)

        # Assertions
        save_mock.assert_called_with(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(data))

    def test_import_by_supplier_route_method_if_has_no_file(self):
        # Arrange
        data = {}
        data = {key: str(value) for key, value in data.items()}
        data['data_file'] = ([])

        # Action
        response = self._client.post('/products:import-by-supplier', data=data, follow_redirects=True,
                                     content_type='multipart/form-data')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'{"code": 400, "message": "No file"}')
