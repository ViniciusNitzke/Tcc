from uuid import uuid4

from database import db
from app.validations.validations import *

MAX_NAME_LENGTH: int = 80


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    profit_percentage = db.Column(db.Float(), nullable=False)
    on_create = db.Column(db.DateTime, default=datetime.datetime.now)
    on_update = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def serialize(self) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'active': self.active,
            'name': self.name,
            'profit_percentage': self.profit_percentage,
            'on_create': self.on_create,
            'on_update': self.on_update
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validating_empty_fields([], **kwargs)
        validating_if_field_is_not_str(['active', 'on_create', 'on_update','profit_percentage'], **kwargs)
        validating_if_field_is_bool(['active'], **kwargs)
        validating_if_field_is_alpha(['name'], **kwargs)
        validating_if_field_is_float(['profit_percentage'], **kwargs)
        validating_size_of_fields(**kwargs)


def validating_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    size_list = []
    for key, value in data.items():
        size_value = len(str(value))
        if size_value > (size_maximum := MAX_NAME_LENGTH) and key == 'name':
            fields_list.append(key)
            size_list.append(size_maximum)
    if any(fields_list):
        raise SizeError(size_list, fields_list, 'maximum')
