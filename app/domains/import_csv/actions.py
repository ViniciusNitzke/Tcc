import csv
from io import StringIO
from typing import Dict

from app.exceptions.exceptions_of_import import *


def import_csv_file(csv_file: StringIO, field: str) -> List[Dict[str, str]]:
    try:
        csv_list = []
        ordered_dict = csv.DictReader(csv_file, delimiter=',')
        for column in ordered_dict:
            csv_dictionary = {field: column[field].strip().lower()}
            csv_list.append(csv_dictionary)
        if not csv_list:
            raise DataAlreadyExistsError()
        return csv_list
    except KeyError:
        raise ColumnsError()


def import_product_csv_file(csv_file: StringIO) -> List[Dict[str, str]]:
    try:
        csv_list = []
        ordered_dict = csv.DictReader(csv_file, delimiter=',')
        for column in ordered_dict:
            csv_dictionary = {'name': column['name'].strip().lower(), 'cost_values': float(column['cost_values']),
                              'unit_box': int(column['unit_box']),
                              'weight_unit': float(column['weight_unit']), 'validity': column['validity'],
                              'sku': column['sku'], 'description': column['description'],
                              'category_line_id': column['category_line_id'].strip().lower(),
                              'supplier_id': column['supplier_id']}
            csv_list.append(csv_dictionary)
        if not csv_list:
            raise DataAlreadyExistsError()
        return csv_list
    except KeyError:
        raise ColumnsError()
    except ValueError:
        raise ConversionError()
