class BaseCustomException(Exception):
    pass


class FileTooBig(BaseCustomException):
    pass


class WrongContentType(BaseCustomException):
    pass
