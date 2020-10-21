import re

from . import base
from . import primitives
from . import domains


class UnixPathType(primitives.Primitive):
    NATIVE = str
    REGEX_UNIX_ABSPATH = r"^(\/[\w^ ]+)+\/?([\w.])+[^.]$"

    def __init__(self, regex=REGEX_UNIX_ABSPATH, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.I + re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)
