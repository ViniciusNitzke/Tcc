from flask import Blueprint, jsonify, request
from typing import Tuple, Any

from app.domains.suppliers.actions import get as get_suppliers, \
    create as create_supplier,\
    update as update_supplier,\
    get_by_id as get_supplier_by_id, \
    validating_if_json_is_correct


app_suppliers = Blueprint('app.suppliers', __name__)


@app_suppliers.route('/suppliers', methods=['POST'])
def post() -> Tuple[Any, int]:
    try:
        payload = request.get_json()
        supplier = create_supplier(payload)
        return jsonify(supplier.serialize()), 201
    except (TypeError, KeyError):
        validating_if_json_is_correct(['company_name', 'cnpj', 'trading_name', 'phone', 'email', 'address_id',
                                       'category_id'])


@app_suppliers.route('/suppliers/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    supplier = update_supplier(id, payload)
    return jsonify(supplier.serialize()), 200


@app_suppliers.route('/suppliers', methods=['GET'])
def get() -> Tuple[Any, int]:
    return jsonify([supplier.serialize_summed_version() for supplier in get_suppliers()]), 200


@app_suppliers.route('/suppliers/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    supplier = get_supplier_by_id(id)
    return jsonify(supplier.serialize()), 200
