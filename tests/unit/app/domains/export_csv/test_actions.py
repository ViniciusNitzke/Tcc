import unittest
import pytest
from flask import Flask

from app.domains.export_csv.actions import create_csv_file, send_csv_file
from app.exceptions.exceptions_of_export import InvalidExportError


class TestExportCsv(unittest.TestCase):

    def test_if_create_csv_file_is_creating_csv_file(self):
        # Arrange
        list_of_registries = [{'id': '12345', 'name': 'foo', 'is_active': 'True'},
                              {'id': '54321', 'name': 'bar', 'is_active': 'True'}]
        csv_file = create_csv_file(list_of_registries)

        # Actions
        csv_data = csv_file.getvalue().splitlines()

        # Assertions
        self.assertEqual(csv_data[0], """id,name,is_active""")
        self.assertEqual(csv_data[1], """12345,foo,True""")
        self.assertEqual(csv_data[2], """54321,bar,True""")

    def test_if_create_csv_file_with_no_data(self):
        # Arrange
        list_of_registries = []
        with pytest.raises(InvalidExportError) as exc:
            csv_file = create_csv_file(list_of_registries)

            # Action
            csv_file.getvalue().splitlines()

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('There is no data to be exported to a csv file', exc.value.description)

    def test_send_csv_file_is_sending_the_file(self):
        # Arrange
        app = Flask(__name__)
        ctx = app.app_context()
        ctx.push()
        list_of_registries = [{'id': '12345', 'name': 'foo', 'is_active': 'True'},
                              {'id': '54321', 'name': 'bar', 'is_active': 'True'}]
        csv_file = create_csv_file(list_of_registries)

        # Action
        response = send_csv_file(csv_file, 'Test_filename')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=Test_filename.csv")
        self.assertEqual(response.headers["Content-type"], "text/csv")

    def test_send_csv_file_is_sending_the_file_with_no_data(self):
        # Arrange
        app = Flask(__name__)
        ctx = app.app_context()
        ctx.push()
        list_of_registries = []

        with pytest.raises(InvalidExportError) as exc:
            csv_file = create_csv_file(list_of_registries)

            # Action
            send_csv_file(csv_file, 'Test_filename')

        # Assertions
        self.assertEqual(400, exc.value.code)
        self.assertEqual('Bad Request', exc.value.name)
        self.assertEqual('There is no data to be exported to a csv file', exc.value.description)
