from uuid import uuid4

from app.validations.validations import *
from database import db
from app.domains.addresses.models import Address
from app.domains.categories.models import Category
from app.exceptions.exceptions import *

MAX_COMPANY_TRADING_EMAIL_LENGTH: int = 200
MAX_ADDRESS_ID_CATEGORY_ID_LENGTH: int = 36
MAX_PHONE_LENGTH: int = 11
MIN_PHONE_LENGTH: int = 10
CNPJ_LENGTH: int = 14


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    company_name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    trading_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.relationship(Address)
    address_id = db.Column(db.String(36), db.ForeignKey(Address.id), nullable=False)
    category = db.relationship(Category)
    category_id = db.Column(db.String(36), db.ForeignKey(Category.id), nullable=False)
    on_create = db.Column(db.DateTime, default=datetime.datetime.now)
    on_update = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def serialize(self) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'active': self.active,
            'company_name': self.company_name,
            'cnpj': self.cnpj,
            'trading_name': self.trading_name,
            'phone': self.phone,
            'email': self.email,
            'address_id': self.address_id,
            'category_id': self.category_id,
            'on_create': self.on_create,
            'on_update': self.on_update
        }

    def serialize_summed_version(self) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'trading_name': self.trading_name,
            'on_create': self.on_create,
            'on_update': self.on_update
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validating_empty_fields(['description'], **kwargs)
        validating_if_field_is_not_str(['active', 'on_create', 'on_update'], **kwargs)
        validating_if_field_is_bool(['active'], **kwargs)
        validating_if_field_is_numeric(['phone', 'cnpj'], **kwargs)
        validating_if_field_is_alpha(['company_name', 'trading_name'], **kwargs)
        validating_email(**kwargs)
        validating_maximum_size_of_fields(**kwargs)
        validating_minimum_size_of_fields(**kwargs)
        validating_equal_size_of_fields(**kwargs)


def validating_maximum_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_maximum_list = []
    size_maximum_list = []
    for key, value in data.items():
        size_value = len(str(value))
        if (size_value > (size := MAX_COMPANY_TRADING_EMAIL_LENGTH) and key in ['company_name', 'trading_name', 'email']) or \
                (size_value > (size := MAX_ADDRESS_ID_CATEGORY_ID_LENGTH) and key in ['address_id', 'category_id']) or \
                (size_value > (size := MAX_PHONE_LENGTH) and key == 'phone'):
            fields_maximum_list.append(key)
            size_maximum_list.append(size)
    if any(fields_maximum_list):
        raise SizeError(size_maximum_list, fields_maximum_list, 'maximum')


def validating_minimum_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_minimum_list = []
    size_minimum_list = []
    for key, value in data.items():
        size_value = len(str(value))
        if size_value < (size := MIN_PHONE_LENGTH) and key == 'phone':
            fields_minimum_list.append(key)
            size_minimum_list.append(size)
    if any(fields_minimum_list):
        raise SizeError(size_minimum_list, fields_minimum_list, 'minimum')


def validating_equal_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_equal_list = []
    size_equal_list = []
    for key, value in data.items():
        size_value = len(str(value))
        if size_value != (size := CNPJ_LENGTH) and key == 'cnpj':
            fields_equal_list.append(key)
            size_equal_list.append(size)
    if any(fields_equal_list):
        raise SizeError(size_equal_list, fields_equal_list, 'exactly')
