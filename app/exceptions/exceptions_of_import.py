from typing import List, Any

from app.exceptions import BadRequestException


class NoFileError(BadRequestException):
    def __init__(self):
        message = f"No file"
        super().__init__(message)


class DataAlreadyExistsError(BadRequestException):
    def __init__(self):
        message = f"All the data in the file has already been added"
        super().__init__(message)


class ColumnsError(BadRequestException):
    def __init__(self):
        message = f"Check that the columns were typed correctly in the file and that all fields are separated by ',' "
        super().__init__(message)


class ConversionError(BadRequestException):
    def __init__(self):
        message = f"Check that the types of values match their columns"
        super().__init__(message)


class RepeatedDataError(BadRequestException):
    def __init__(self, fields: List[Any]):
        message = f"""The following values are repeated in the file, but will be added only once: {str(fields)[1:-1].replace("'", "")}"""
        super().__init__(message)
