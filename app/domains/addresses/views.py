from flask import Blueprint, jsonify, request
from typing import Tuple, Any

from app.domains.addresses.actions import \
    get as get_addresses, \
    create as create_address, \
    update as update_address, \
    get_by_id as get_address_by_id, \
    validating_if_json_is_correct


app_addresses = Blueprint('app.addresses', __name__)


@app_addresses.route('/addresses', methods=['POST'])
def post() -> Tuple[Any, int]:
    try:
        payload = request.get_json()
        address = create_address(payload)
        return jsonify(address.serialize()), 201
    except (TypeError, KeyError):
        validating_if_json_is_correct(['street', 'number', 'zip_code', 'city', 'state'])


@app_addresses.route('/addresses/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    address = update_address(id, payload)
    return jsonify(address.serialize()), 200


@app_addresses.route('/addresses', methods=['GET'])
def get() -> Tuple[Any, int]:
    return jsonify([address.serialize() for address in get_addresses()]), 200


@app_addresses.route('/addresses/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    address = get_address_by_id(id)
    return jsonify(address.serialize()), 200
