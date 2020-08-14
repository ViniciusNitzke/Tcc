from app.exceptions import BadRequestException


class InvalidExportError(BadRequestException):
    def __init__(self):
        msg: str = 'There is no data to be exported to a csv file'
        super().__init__(msg)
