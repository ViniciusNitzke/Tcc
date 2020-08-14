from sqlalchemy.exc import SQLAlchemyError

from app.domains.suppliers.models import *
from database.repository import save, commit


def create(data: Dict[str, Union[bool, str]]) -> Supplier:
    try:
        return save(Supplier(company_name=data["company_name"],
                             cnpj=data["cnpj"],
                             trading_name=data["trading_name"],
                             phone=data["phone"],
                             email=data["email"],
                             address_id=data["address_id"],
                             category_id=data["category_id"]))
    except SQLAlchemyError:
        raise InvalidValueError(['cnpj'])


def get() -> List[Supplier]:
    return Supplier.query.all()


def get_by_id(id: str) -> Supplier:
    supplier = Supplier.query.get(id)
    if not supplier:
        raise IdNotExistError()
    return supplier


def update(id: str, data: Dict[str, Union[bool, str]]) -> Supplier:
    try:
        supplier = get_by_id(id)
        if not supplier:
            raise IdNotExistError()
        supplier.active = data.get("active")
        supplier.company_name = data.get("company_name")
        supplier.cnpj = data.get("cnpj")
        supplier.trading_name = data.get("trading_name")
        supplier.phone = data.get("phone")
        supplier.email = data.get("email")
        supplier.address_id = data.get("address_id")
        supplier.category_id = data.get("category_id")

        validating_empty_fields([], **supplier.serialize())
        validating_if_field_is_not_str(['active', 'on_create', 'on_update'], **supplier.serialize())
        validating_if_field_is_bool(['active'], **supplier.serialize())
        validating_if_field_is_numeric(['phone', 'cnpj'], **supplier.serialize())
        validating_if_field_is_alpha(['company_name', 'trading_name'], **supplier.serialize())
        validating_maximum_size_of_fields(**supplier.serialize())
        validating_minimum_size_of_fields(**supplier.serialize())
        validating_equal_size_of_fields(**supplier.serialize())
        commit()
        return supplier
    except AttributeError:
        validating_if_json_is_correct(['company_name', 'cnpj', 'trading_name', 'phone', 'email', 'address_id',
                                       'category_id'])
    except SQLAlchemyError:
        raise InvalidValueError(['cnpj'])
