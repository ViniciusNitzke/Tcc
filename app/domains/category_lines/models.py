from uuid import uuid4

from database import db
from app.domains.categories.models import Category
from app.validations.validations import *

MAX_CATEGORY_LINE_LENGTH: int = 100
MAX_CATEGORY_ID_LENGTH: int = 36


class CategoryLine(db.Model):
    __tablename__ = 'category_lines'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    category_line = db.Column(db.String(100), unique=True, nullable=False)
    category = db.relationship(Category)
    profit_percentage = db.Column(db.Float(), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey(Category.id), nullable=False)
    on_create = db.Column(db.DateTime, default=datetime.datetime.now)
    on_update = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def serialize(self) -> Dict[str, Union[bool, str]]:
        return {
            'id': self.id,
            'active': self.active,
            'profit_percentage': self.profit_percentage,
            'category_line': self.category_line,
            'category_id': self.category_id,
            'on_create': self.on_create,
            'on_update': self.on_update
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validating_empty_fields([], **kwargs)
        validating_if_field_is_not_str(['active', 'on_create', 'on_update','profit_percentage'], **kwargs)
        validating_if_field_is_bool(['active'], **kwargs)
        validating_if_field_is_float(['profit_percentage'], **kwargs)
        validating_size_of_fields(**kwargs)


def validating_size_of_fields(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    size_list = []
    for key, value in data.items():
        size_value = len(str(value))
        if (size_value > (size_maximum := MAX_CATEGORY_LINE_LENGTH) and key == 'category_line') or \
           (size_value > (size_maximum := MAX_CATEGORY_ID_LENGTH) and key == 'category_id'):
            fields_list.append(key)
            size_list.append(size_maximum)
    if any(fields_list):
        raise SizeError(size_list, fields_list, 'maximum')
