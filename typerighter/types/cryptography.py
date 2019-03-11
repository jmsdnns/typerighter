from . import base


class HashType(base.Type):
    pass


class MD5Type(HashType):
    LENGTH = 32


class SHA1Type(HashType):
    LENGTH = 40
