from sqlalchemy.exc import SQLAlchemyError

from app.domains.category_lines.models import *
from database.repository import save, commit
from app.domains.categories.actions import get_by_id as get_category_by_id

def create(data: Dict[str, str]) -> CategoryLine:
    try:
        return save(CategoryLine(category_line=data['category_line'], category_id=data['category_id'],profit_percentage=data['profit_percentage']))
    except SQLAlchemyError:
        raise InvalidValueError(['category_line'])


def get() -> List[CategoryLine]:
    return CategoryLine.query.all()


def get_by_id(id: str) -> CategoryLine:
    category_line = CategoryLine.query.get(id)
    if not category_line:
        raise IdNotExistError()
    return category_line


def get_category_percentage(id: str) -> float:
    category_line = get_by_id(id)
    category = get_category_by_id(category_line.category_id)
    percentage = category.profit_percentage
    return percentage


def update(id: str, data: Dict[str, str]) -> CategoryLine:
    try:
        category_line = get_by_id(id)
        if not category_line:
            raise IdNotExistError()
        category_line.category_line = data.get("category_line")
        category_line.category_id = data.get("category_id")
        category_line.profit_percentage = data.get("profit_percentage")

        validating_empty_fields([], **category_line.serialize())
        validating_if_field_is_not_str(['active', 'on_create', 'on_update', 'profit_percentage'], **category_line.serialize())
        validating_if_field_is_bool(['active'], **category_line.serialize())
        validating_size_of_fields(**category_line.serialize())
        validating_if_field_is_float(['profit_percentage'], **category_line.serialize())
        commit()
        return category_line

    except AttributeError:
        validating_if_json_is_correct(['category_line', 'category_id'])
    except SQLAlchemyError:
        raise InvalidValueError(['category_line'])
