from uuid import uuid4

from app.domains.category_lines.models import CategoryLine
from app.domains.suppliers.models import Supplier
from app.validations.validations import *
from database import db

MAX_NAME_LENGTH: int = 80
MAX_CATEGORY_LINE_ID_LENGTH: int = 36
MAX_DESCRIPTION_LENGTH: int = 150
MAX_COST_VALUES_DECIMAL_PLACES: int = 2
MAX_WEIGHT_UNIT_DECIMAL_PLACES: int = 3


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    name = db.Column(db.String(80), nullable=False)
    cost_values = db.Column(db.Float(), nullable=False)
    category_line = db.relationship(CategoryLine)
    category_line_id = db.Column(db.String(36), db.ForeignKey(CategoryLine.id), nullable=False)
    supplier = db.relationship(Supplier)
    supplier_id = db.Column(db.String(36), db.ForeignKey(Supplier.id), nullable=False)
    unit_box = db.Column(db.Integer(), nullable=False)
    weight_unit = db.Column(db.Float(), nullable=False)
    validity = db.Column(db.DateTime(), nullable=False)
    sku = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(150))
    on_create = db.Column(db.DateTime, default=datetime.datetime.now)
    on_update = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validating_empty_fields(['active', 'description'], **kwargs)
        validating_if_field_is_not_str(['active', 'on_create', 'on_update', 'cost_values', 'unit_box', 'weight_unit',
                                        'validity'], **kwargs)
        validating_if_field_is_bool(['active'], **kwargs)
        validating_if_field_is_alpha(['name'], **kwargs)
        validating_validity(['validity'], **kwargs)
        validating_if_field_is_int(['unit_box'], **kwargs)
        validating_if_field_is_float(['cost_values', 'weight_unit'], **kwargs)
        validating_size_of_fields(**kwargs)

    def serialize(self) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'active': self.active,
            'name': self.name,
            'cost_values': self.cost_values,
            'category_line_id': self.category_line_id,
            'supplier_id': self.supplier_id,
            'unit_box': self.unit_box,
            'weight_unit': self.weight_unit,
            'validity': self.validity,
            'sku': self.sku,
            'description': self.description,
            'on_create': self.on_create,
            'on_update': self.on_update
        }

    def serialize_final_cost(self, sum_of_percentages) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'active': self.active,
            'name': self.name,
            'cost_values': self.cost_values + sum_of_percentages,
            'category_line_id': self.category_line_id,
            'supplier_id': self.supplier_id,
            'unit_box': self.unit_box,
            'weight_unit': self.weight_unit,
            'validity': self.validity,
            'sku': self.sku,
            'description': self.description,
            'on_create': self.on_create,
            'on_update': self.on_update
        }


def validating_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    size_list = []
    for key, value in data.items():
        size_value = len(str(value))
        if (size_value > (size_maximum := MAX_NAME_LENGTH) and key == 'name') or \
           (size_value > (size_maximum := MAX_DESCRIPTION_LENGTH) and key == 'description') or \
           (size_value > (size_maximum := MAX_CATEGORY_LINE_ID_LENGTH) and key in ['category_line_id', 'supplier_id']):
            fields_list.append(key)
            size_list.append(size_maximum)
        elif len(str(value).rsplit('.')[-1]) > MAX_COST_VALUES_DECIMAL_PLACES and key == 'cost_values':
            fields_list.append(key)
            size_list.append('2 decimal places')
        elif len(str(value).rsplit('.')[-1]) > MAX_WEIGHT_UNIT_DECIMAL_PLACES and key == 'weight_unit':
            fields_list.append(key)
            size_list.append('3 decimal places')
    if any(fields_list):
        raise SizeError(size_list, fields_list, 'maximum')
