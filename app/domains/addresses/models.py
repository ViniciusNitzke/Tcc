from uuid import uuid4

from database import db
from app.validations.validations import *

MAX_ZIP_CODE_LENGTH: int = 8
MAX_NUMBER_LENGTH: int = 10
MAX_COMPLEMENT_LENGTH: int = 100
MAX_LENGTH_OF_STREET_CITY_STATE: int = 50


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    street = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    complement = db.Column(db.String(300))
    zip_code = db.Column(db.String(11), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    on_create = db.Column(db.DateTime, default=datetime.datetime.now)
    on_update = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def serialize(self) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'active': self.active,
            'street': self.street,
            'number': self.number,
            'complement': self.complement,
            'zip_code': self.zip_code,
            'city': self.city,
            'state': self.state,
            'on_create': self.on_create,
            'on_update': self.on_update
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validating_empty_fields(['complement'], **kwargs)
        validating_if_field_is_not_str(['active', 'on_create', 'on_update'], **kwargs)
        validating_if_field_is_bool(['active'], **kwargs)
        validating_if_field_is_alpha_numeric(['street'], **kwargs)
        validating_if_field_is_numeric(['number', 'zip_code'], **kwargs)
        validating_if_field_is_alpha(['city', 'state'], **kwargs)
        validating_size_of_fields(**kwargs)


def validating_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    size_list = []

    for key, value in data.items():
        size_value = len(str(value))
        if (size_value > (size_maximum := MAX_ZIP_CODE_LENGTH) and key == 'zip_code') or \
           (size_value > (size_maximum := MAX_NUMBER_LENGTH) and key == 'number') or \
           (size_value > (size_maximum := MAX_COMPLEMENT_LENGTH) and key == 'complement') or \
           (size_value > (size_maximum := MAX_LENGTH_OF_STREET_CITY_STATE) and key in ['street', 'city', 'state']):
            fields_list.append(key)
            size_list.append(size_maximum)
    if any(fields_list):
        raise SizeError(size_list, fields_list, 'maximum')
