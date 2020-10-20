import uuid
import re

from . import base
from . import primitives
from . import domains


REGEX_UUID4 = '^[a-z0-9]{32}$'


class UUIDType(primitives.Primitive):
    NATIVE = str

    def __init__(self, regex=REGEX_UUID4, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)
