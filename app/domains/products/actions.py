from io import StringIO
from typing import Callable
from sqlalchemy.exc import SQLAlchemyError

from app.domains.import_csv.actions import import_product_csv_file
from app.domains.products.models import *
from app.exceptions.exceptions_of_import import RepeatedDataError, DataAlreadyExistsError
from database.repository import save, commit

from app.domains.category_lines.actions import get_by_id as get_category_line_by_id

from app.domains.categories.actions import get_by_id as get_category_by_id


def create(data: Dict[str, Union[bool, str]]) -> Product:
    try:
        return save(Product(name=data['name'],
                            cost_values=data['cost_values'],
                            unit_box=data['unit_box'],
                            weight_unit=data['weight_unit'],
                            validity=data['validity'],
                            sku=data['sku'],
                            description=data['description'],
                            category_line_id=data['category_line_id'],
                            supplier_id=data['supplier_id']))
    except SQLAlchemyError:
        raise InvalidValueError(['sku'])


def get() -> List[Product]:
    return Product.query.all()


def get_by_id(id: str) -> Product:
    product = Product.query.get(id)
    if not product:
        raise IdNotExistError()
    return product


def update(id: str, data: Dict[str, Union[bool, str]]) -> Product:
    try:
        product = get_by_id(id)
        if not product:
            raise IdNotExistError()
        product.name = data.get('name')
        product.cost_values = data.get('cost_values')
        product.unit_box = data.get('unit_box')
        product.weight_unit = data.get('weight_unit')
        product.validity = data.get('validity')
        product.sku = data.get('sku')
        product.description = data.get('description')
        product.category_line_id = data.get('category_line_id')
        product.supplier_id = data.get('supplier_id')

        validating_empty_fields(['active', 'description'], **product.serialize())
        validating_if_field_is_not_str(['active', 'on_create', 'on_update', 'cost_values', 'unit_box', 'weight_unit',
                                        'validity'], **product.serialize())
        validating_if_field_is_bool(['active'], **product.serialize())
        validating_if_field_is_alpha(['name'], **product.serialize())
        validating_validity(['validity'], **product.serialize())
        validating_if_field_is_int(['unit_box'], **product.serialize())
        validating_if_field_is_float(['cost_values', 'weight_unit'], **product.serialize())
        validating_size_of_fields(**product.serialize())
        commit()
        return product

    except AttributeError:
        validating_if_json_is_correct(['name', 'cost_values', 'unit_box', 'weight_unit', 'validity', 'sku',
                                       'category_line_id', 'supplier_id'])
    except SQLAlchemyError:
        raise InvalidValueError(['sku'])


def get_percentages(category_line_id: str) -> float:
    category_line = get_category_line_by_id(category_line_id)
    category_id = category_line.category_id
    category_line_percentage = category_line.profit_percentage
    category = get_category_by_id(category_id)
    category_percentage = category.profit_percentage
    sum_of_percentages = category_percentage + category_line_percentage
    return sum_of_percentages


def inserting_products_from_the_csv_file_in_db(csv_file: StringIO, field: str, validate: Callable, new_products_list: List,
                                               list_of_sku_saved_in_db: List, product_id_list: List) -> List[Product]:
    get_products = get()
    for product in get_products:
        list_of_sku_saved_in_db.append(product.sku.strip())
        product_id_list.append(product.id)
    validate(csv_file, field, list_of_sku_saved_in_db, new_products_list, product_id_list)
    if not new_products_list:
        raise DataAlreadyExistsError()
    return new_products_list


def validating_if_the_product_sku_already_exists_in_the_db(csv_file: StringIO, field: str,
                                                           list_of_sku_saved_in_db: List,
                                                           new_products_list: List, product_id_list: List) -> NoReturn:
    for product_csv in import_product_csv_file(csv_file):
        if product_csv[field] not in list_of_sku_saved_in_db:
            try:
                new_products_list.append(save(Product(**product_csv)))
            except SQLAlchemyError:
                raise InvalidValueError(['sku'])


def validating_and_updating_if_the_product_sku_already_exists_in_the_db(csv_file: StringIO, field: str,
                                                                        list_of_sku_saved_in_db: List,
                                                                        new_products_list: List,
                                                                        product_id_list: List) -> NoReturn:
    for product_csv in import_product_csv_file(csv_file):
        try:
            if product_csv[field] not in list_of_sku_saved_in_db:
                new_products_list.append(save(Product(**product_csv)))
            else:
                position = list_of_sku_saved_in_db.index(product_csv[field].strip())
                id = product_id_list[position]
                new_products_list.append(update(id, product_csv))
        except SQLAlchemyError:
            raise IdNotExistError()