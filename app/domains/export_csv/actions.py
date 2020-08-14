import csv
import io
from typing import Dict, List, Any
from flask import make_response

from app.exceptions.exceptions_of_export import InvalidExportError


def create_csv_file(list_of_registries: List[Dict[str, Any]]):
    if not list_of_registries:
        raise InvalidExportError()
    csv_file = io.StringIO()
    fieldnames = [key for key in list_of_registries[0].keys()]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in list_of_registries:
        writer.writerow(row)
    return csv_file


def send_csv_file(csv_file: io.StringIO, filename: str):
    output = make_response(csv_file.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"
    output.headers["Content-type"] = "text/csv"
    return output
