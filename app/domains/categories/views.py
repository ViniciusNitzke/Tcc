from flask import Blueprint, jsonify, request
from typing import Tuple, Any
import io

from app.domains.export_csv.actions import create_csv_file, send_csv_file
from app.exceptions.exceptions_of_import import NoFileError
from app.domains.categories.actions import get as get_category, \
    create as create_category, update as update_category, \
    get_by_id as get_category_by_id, \
    inserting_categories_names_from_the_csv_file_in_db as insert_data, \
    validating_if_json_is_correct


app_categories = Blueprint('app.categories', __name__)


@app_categories.route('/categories', methods=['POST'])
def post() -> Tuple[Any, int]:
    try:
        payload = request.get_json()
        category = create_category(payload)
        return jsonify(category.serialize()), 201
    except (TypeError, KeyError):
        validating_if_json_is_correct(['name'])


@app_categories.route('/categories/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    category = update_category(id, payload)
    return jsonify(category.serialize()), 200


@app_categories.route('/categories', methods=['GET'])
def get() -> Tuple[Any, int]:
    return jsonify([category.serialize() for category in get_category()]), 200


@app_categories.route('/categories/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    category = get_category_by_id(id)
    return jsonify(category.serialize()), 200


@app_categories.route('/categories:export', methods=['GET'])
def export() -> Tuple[Any, int]:
    category_list = get_category()
    csv_file = create_csv_file([category.serialize() for category in category_list])
    return send_csv_file(csv_file, 'Categories')


@app_categories.route('/categories:import', methods=['POST'])
def import_route():
    try:
        file = request.files['data_file']
    except:
        raise NoFileError()
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    insert_data(stream, 'name')
    return jsonify([category.serialize() for category in get_category()]), 200
