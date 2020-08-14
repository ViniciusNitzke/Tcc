import re
from typing import Dict, Union, NoReturn
import datetime

from app.exceptions.exceptions import *


def validating_if_json_is_correct(list_of_allowed_fields: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    count = 0
    for key, value in data.items():
        if value and key in list_of_allowed_fields:
            count += 1
    if count < len(list_of_allowed_fields):
        raise JsonError(list_of_allowed_fields)


def validating_empty_fields(list_of_fields_not_mandatory: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if (not value or str(value).strip() == '') and key not in list_of_fields_not_mandatory:
            fields_list.append(key)
    if any(fields_list):
        raise EmptyFieldsError(fields_list)


def validating_if_field_is_not_str(list_of_fields_not_str: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if value and not isinstance(value, str) and key not in list_of_fields_not_str:
            fields_list.append(key)
    if any(fields_list):
        raise TypeError(fields_list, 'str')


def validating_if_field_is_bool(list_of_fields_bool: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if value and not isinstance(value, bool) and key in list_of_fields_bool:
            fields_list.append(key)
    if any(fields_list):
        raise TypeError(fields_list, 'bool')


def validating_if_field_is_int(list_of_fields_int: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if (value and not isinstance(value, int) and key in list_of_fields_int) or (isinstance(value, int) and value < 0):
            fields_list.append(key)
    if any(fields_list):
        raise TypeError(fields_list, 'int positive')


def validating_if_field_is_float(list_of_fields_float: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if (value and not isinstance(value, float) and key in list_of_fields_float) or (isinstance(value, float) and value < 0):
            fields_list.append(key)
    if any(fields_list):
        raise TypeError(fields_list, 'float positive')


def validating_if_field_is_alpha_numeric(list_of_fields_alphanumerics: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        value = ''.join(str(value).split())
        if (not value.isalpha() and not value.isnumeric() and not value.isalnum()) and key in list_of_fields_alphanumerics:
            fields_list.append(key)
    if any(fields_list):
        raise TextError(fields_list, 'letters or / and numbers')


def validating_if_field_is_numeric(list_of_fields_numerics: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if not ''.join(str(value).split()).isnumeric() and key in list_of_fields_numerics:
            fields_list.append(key)
    if any(fields_list):
        raise TextError(fields_list, 'numbers')


def validating_if_field_is_alpha(list_of_fields_alpha: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    fields_list = []
    for key, value in data.items():
        if not ''.join(str(value).split()).isalpha() and key in list_of_fields_alpha:
            fields_list.append(key)
    if any(fields_list):
        raise TextError(fields_list, 'letters')


def validating_validity(list_of_fields_of_validy: List[str], **data: Dict[str, Union[bool, str]]) -> NoReturn:
    for key, value in data.items():
        if key in list_of_fields_of_validy:
            try:
                datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValidityError('incorrect')
            date = datetime.datetime.strptime(value, "%Y-%m-%d")
            if date < datetime.datetime.now():
                raise ValidityError('expired')


def validating_email(**data: Dict[str, Union[bool, str]]) -> NoReturn:
    for key, value in data.items():
        if key == 'email' and not re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', value):
            raise EmailError()
