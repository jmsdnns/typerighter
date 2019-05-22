import datetime
import re

from . import base
from . import primitives
from . import domains
from .. import exceptions


# Patterns

REGEX_FROM_ISO8601 = r"""(?P<year>\d{4})-(?P<month>\d\d)-(?P<day>\d\d)(?:T|\ )
    (?P<hour>\d\d):(?P<minute>\d\d)
    (?::(?P<second>\d\d)(?:(?:\.|,)(?P<sec_frac>\d{1,6}))?)?
    (?:(?P<tzd_offset>(?P<tzd_sign>[+−-])(?P<tzd_hour>\d\d):?(?P<tzd_minute>\d\d)?)
    |(?P<tzd_utc>Z))?$"""

REGEX_TO_ISO8601 = '%Y-%m-%dT%H:%M:%S.%f%z'

REGEX_FROM_TIME = r"""(?P<hour>\d\d):(?P<minute>\d\d)
    (?::(?P<second>\d\d)(?:(?:\.|,)(?P<sec_frac>\d{1,6}))?)?$"""


# Types

class DateTimeType(primitives.Primitive):
    NATIVE = datetime.datetime

    def __init__(self, regex=REGEX_FROM_ISO8601, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)
    
    @base.skip_falsy
    def to_native(self, value):
        if self.is_type_match(value):
            return value

        elif not isinstance(value, str):
            e_msg = "Value is not a string: {}"
            raise exceptions.TypeException(e_msg.format(value))

        # Verify regex
        match = self._regex.match(value)
        if not match:
            e_msg = "Value did not match date pattern: {}"
            raise exceptions.TypeException(e_msg.format(value))

        # Extract components
        parts = dict(((k, v) for k, v in match.groupdict().items() if v is not None))
        p = lambda name: int(parts.get(name, 0))
        microsecond = p('sec_frac') and p('sec_frac') * 10 ** (6 - len(parts['sec_frac']))

        # Timezones
        if 'tzd_utc' in parts:
            tz = datetime.timezone.utc
        elif 'tzd_offset' in parts:
            tz_sign = 1 if parts['tzd_sign'] == '+' else -1
            tz_offset = (p('tzd_hour') * 60 + p('tzd_minute')) * tz_sign
            if tz_offset == 0:
                tz = datetime.timezone.utc
            else:
                tz = datetime.timezone(datetime.timedelta(minutes=tz_offset))
        else:
            tz = None

        return self.NATIVE(
            p('year'), p('month'), p('day'), p('hour'), p('minute'),
            p('second'), microsecond, tz
        )

    @base.skip_falsy
    def to_primitive(self, value, context=None):
        if isinstance(value, str) and self._regex.match(value):
            return value
        elif isinstance(value, self.NATIVE):
            return value.strftime(REGEX_TO_ISO8601)
        e_msg = "Value must be iso8601 string or datetime.datetime: {}"
        raise exceptions.TypeException(e_msg.format(value))


class TimeType(primitives.Primitive):
    NATIVE = datetime.time

    def __init__(self, regex=REGEX_FROM_TIME, **kw):
        super().__init__(**kw)
        domains.RegexDomain(self, regex, re.X)

    @base.skip_falsy
    def validate(self, value):
        super().validate(value)

    @base.skip_falsy
    def to_native(self, value):
        if isinstance(value, self.NATIVE):
            return value

        parts = {}
        match = self._regex.match(value)
        for k, v in match.groupdict().items():
            if v is not None:
                parts[k] = int(v)
        return datetime.time(**parts)

    @base.skip_falsy
    def to_primitive(self, value):
        if isinstance(value, self.NATIVE):
            return value.isoformat()
        if isinstance(value, str):
            return value
        e_msg = "Value must be time string or datetime.time: {}"
        raise exceptions.TypeException(e_msg.format(value))
