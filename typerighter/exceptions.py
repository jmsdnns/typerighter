class BaseException(Exception):
    pass


class UnsetException(BaseException):
    pass


class TypeException(BaseException):
    pass


class RecordException(BaseException):
    pass


class ValidationException(BaseException):
    pass


class ConfigException(BaseException):
    pass


class CacheMissException(BaseException):
    pass


class UncachableException(BaseException):
    pass