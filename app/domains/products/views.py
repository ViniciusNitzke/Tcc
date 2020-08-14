from flask import Blueprint, jsonify, request
from typing import Tuple, Any
import io

from app.domains.products.models import *
from app.exceptions.exceptions_of_import import NoFileError
from app.domains.export_csv.actions import create_csv_file, send_csv_file
from app.domains.products.actions import get as get_products, \
    create as create_products, \
    update as update_products, \
    get_by_id as get_products_by_id, \
    inserting_products_from_the_csv_file_in_db as insert_data, \
    validating_if_the_product_sku_already_exists_in_the_db as validate, \
    validating_and_updating_if_the_product_sku_already_exists_in_the_db as validate_by_supplier, \
    validating_if_json_is_correct, get_percentages

app_products = Blueprint('app.products', __name__)


@app_products.route('/products', methods=['POST'])
def post() -> Tuple[Any, int]:
    try:
        payload = request.get_json()
        products = create_products(payload)
        return jsonify(products.serialize()), 201
    except (TypeError, KeyError):
        validating_if_json_is_correct(['name', 'cost_values', 'unit_box', 'weight_unit', 'validity', 'sku',
                                       'category_line_id', 'supplier_id'])


@app_products.route('/products/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    products = update_products(id, payload)
    return jsonify(products.serialize()), 200


@app_products.route('/products', methods=['GET'])
def get() -> Tuple[Any, int]:
    return jsonify([products.serialize_final_cost(get_percentages(products.category_line_id))
                    for products in get_products()]), 200


@app_products.route('/products/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    products = get_products_by_id(id)
    return jsonify([products.serialize_final_cost(get_percentages(products.category_line_id))]), 200


@app_products.route('/products:export', methods=['GET'])
def export():
    products_list = get_products()
    csv_file = create_csv_file([product.serialize() for product in products_list])
    return send_csv_file(csv_file, 'Products')


@app_products.route('/products:import', methods=['POST'])
def import_route():
    try:
        file = request.files['data_file']
    except:
        raise NoFileError()
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    insert_data(stream, 'sku', validate, [], [], [])
    return jsonify([product.serialize() for product in get_products()]), 200


@app_products.route('/products:import-by-supplier', methods=['POST'])
def import_route_by_supplier():
    try:
        file = request.files['data_file']
    except:
        raise NoFileError()
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    insert_data(stream, 'sku', validate_by_supplier, [], [], [])
    return jsonify([product.serialize() for product in get_products()]), 200
