from app.domains.addresses.models import *
from database.repository import save, commit


def create(data: Dict[str, Union[bool, str]]) -> Address:
    return save(Address(street=data["street"], number=data["number"], complement=data["complement"],
                        zip_code=data["zip_code"], city=data["city"], state=data["state"]))


def get() -> List[Address]:
    return Address.query.all()


def get_by_id(id: str) -> Address:
    address = Address.query.get(id)
    if not address:
        raise IdNotExistError()
    return address


def update(id: str, data: Dict[str, Union[bool, str]]) -> Address:
    try:
        address = get_by_id(id)
        if not address:
            raise IdNotExistError()
        address.active = data.get("active")
        address.street = data.get("street")
        address.number = data.get("number")
        address.complement = data.get("complement")
        address.zip_code = data.get("zip_code")
        address.city = data.get("city")
        address.state = data.get("state")

        validating_empty_fields(['active', 'complement'], **address.serialize())
        validating_if_field_is_not_str(['active', 'on_create', 'on_update'], **address.serialize())
        validating_if_field_is_bool(['active'], **address.serialize())
        validating_if_field_is_alpha_numeric(['street'], **address.serialize())
        validating_if_field_is_numeric(['number', 'zip_code'], **address.serialize())
        validating_if_field_is_alpha(['city', 'state'], **address.serialize())
        validating_size_of_fields(**address.serialize())
        commit()
        return address
    except AttributeError:
        validating_if_json_is_correct(['street', 'number', 'zip_code', 'city', 'state'])
