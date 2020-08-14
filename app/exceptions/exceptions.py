from typing import List, Any

from app.exceptions import BadRequestException


class EmptyFieldsError(BadRequestException):
    def __init__(self, fields: List[Any]):
        message = f"""The following field(s) cannot be empty: {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)


class TypeError(BadRequestException):
    def __init__(self, fields: List[Any], type: str):
        message = f"""The following field(s) must be of type {type}: {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)


class TextError(BadRequestException):
    def __init__(self, fields: List[Any], text: str):
        message = f"""The following field(s) must be only {text}: {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)


class JsonError(BadRequestException):
    def __init__(self, fields: List[Any]):
        message = f"""The JSON data must contain the following field(s): {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)


class SizeError(BadRequestException):
    def __init__(self, sizes: List[int], fields: List[Any], max_or_min_or_exactly: str):
        message = f"""The field(s) {str(fields)[1:-1]} must be the following {max_or_min_or_exactly} sizes respectively: {str(sizes)[1:-1].replace("'", "")}"""
        super().__init__(message)


class IdNotExistError(BadRequestException):
    def __init__(self):
        message = 'The ID(s) inserted does not exist in the database'
        super().__init__(message)


class InvalidValueError(BadRequestException):
    def __init__(self, fields: List[Any]):
        message = f"""Check if the ID field(s) are entered correctly. If so, the following field(s) must be unique: {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)


class RepeatedValueError(BadRequestException):
    def __init__(self, fields: List[Any]):
        message = f"""The following values already exist in the database: {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)


class ValidityError(BadRequestException):
    def __init__(self, validity: str):
        incorrect = f"Incorrect data format. Validity date should be YYYY-MM-DD"
        expired = f"The validity date inserted is past it is expiry date"
        if validity == 'incorrect':
            super().__init__(incorrect)
        elif validity == 'expired':
            super().__init__(expired)


class EmailError(BadRequestException):
    def __init__(self):
        message = f"E-mail must be a valid email"
        super().__init__(message)
