from io import StringIO
from sqlalchemy.exc import SQLAlchemyError

from app.domains.categories.models import *
from app.exceptions.exceptions_of_import import *
from database.repository import save, commit
from app.domains.import_csv.actions import import_csv_file


def create(data: Dict[str, str]) -> Category:
    try:
        return save(Category(name=data['name'],profit_percentage=data['profit_percentage']))
    except SQLAlchemyError:
        raise RepeatedValueError([data['name']])


def get() -> List[Category]:
    return Category.query.all()


def get_by_id(id: str) -> Category:
    category = Category.query.get(id)
    if not category:
        raise IdNotExistError()
    return category


def update(id: str, data: Dict[str, str]) -> Category:
    try:
        category = get_by_id(id)
        if not category:
            raise IdNotExistError()
        category.active = data.get('active')
        category.name = data.get('name')

        validating_empty_fields([], **category.serialize())
        validating_if_field_is_not_str(['active', 'on_create', 'on_update'], **category.serialize())
        validating_if_field_is_bool(['active'], **category.serialize())
        validating_if_field_is_alpha(['name'], **category.serialize())
        validating_size_of_fields(**category.serialize())
        validating_if_field_is_float(['profit_percentage'], **category.serialize())
        commit()
        return category

    except AttributeError:
        validating_if_json_is_correct(['name'])
    except SQLAlchemyError:
        raise RepeatedValueError([data['name']])


def inserting_categories_names_from_the_csv_file_in_db(csv_file: StringIO, field: str) -> List[Category]:
    new_categories_list = []
    list_of_names_saved_in_db = []
    get_categories = get()
    for category in get_categories:
        list_of_names_saved_in_db.append(category.name.strip().lower())
    validating_if_the_category_name_already_exists_in_the_db(csv_file, field, list_of_names_saved_in_db, new_categories_list)
    if not new_categories_list:
        raise DataAlreadyExistsError()
    return new_categories_list


def validating_if_the_category_name_already_exists_in_the_db(csv_file: StringIO, field: str,
                                                             list_of_names_saved_in_db: list,
                                                             new_categories_list: list) -> NoReturn:
    for category_csv in import_csv_file(csv_file, field):
        if category_csv[field] not in list_of_names_saved_in_db:
            try:
                new_categories_list.append(save(Category(name=category_csv[field])))
            except SQLAlchemyError:
                raise RepeatedDataError([category_csv[field]])
