from flask import Blueprint, request, jsonify
from typing import Tuple, Any

from app.domains.category_lines.actions import get_by_id as get_by_id_category_line, \
    get as get_category_line, \
    create as create_category_line, \
    update as update_category_line, \
    validating_if_json_is_correct


app_categories_line = Blueprint('app.categories_line', __name__)


@app_categories_line.route('/category_line', methods=['POST'])
def post() -> Tuple[Any, int]:
    try:
        payload = request.get_json()
        category_line = create_category_line(payload)
        return jsonify(category_line.serialize()), 201
    except (TypeError, KeyError):
        validating_if_json_is_correct(['category_line'])


@app_categories_line.route('/category_line/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    category_line = update_category_line(id, payload)
    return jsonify(category_line.serialize()), 200


@app_categories_line.route('/category_line', methods=['GET'])
def get() -> Tuple[Any, int]:
    return jsonify([category_line.serialize() for category_line in get_category_line()]), 200


@app_categories_line.route('/category_line/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    category_line = get_by_id_category_line(id)
    return jsonify(category_line.serialize()), 200
