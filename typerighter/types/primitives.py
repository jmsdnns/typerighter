import re

from . import base
from . import domains
from .. import exceptions


class Primitive(base.Type):
    def __init__(self, choices=None, **kw):
        super().__init__(**kw)
        self.choices = choices

    def validate_choices(self, value):
        if self.choices and (value == base.Unset or value not in self.choices):
            e_msg = "Illegal choice for value: {}"
            raise exceptions.ValidationException(e_msg.format(value))


class BooleanType(Primitive):
    NATIVE = bool
    
    def to_primitive(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            vl = value.lower()
            if vl == 'true':
                return True
            elif vl == 'false':
                return False

        if isinstance(value, (int, float)):
            return bool(value)

        e_msg = "Value is not a boolean: {}"
        raise exceptions.TypeException(e_msg.format(value))

    def validate_boolean(self, value):
        try:
            self.to_primitive(value)
        except exceptions.TypeException as te:
            ve = exceptions.ValidationException(*te.args)
            raise ve


class StringType(Primitive):
    NATIVE = str

    def __init__(self, max_length=None, min_length=None, regex=None, **kw):
        super().__init__(**kw)
        domains.LengthDomain(self, max_length, min_length)
        
        self.regex = regex

        if self.regex:
            try:
                compiled = re.compile(self.regex)
                self._regex = compiled
            except:
                err_msg = "Regex failed to compile: {}"
                raise exceptions.TypeException(
                    err_msg.format(self.regex)
                )

    def is_falsy(self, value):
        if value == None or value == "":
            return True

        return super().is_falsy(value)

    def to_primitive(self, value):
        if isinstance(value, str):
            return value

        try:
            p = str(value)
            return p
        except:
            err_msg = "Could not convert to string: {}"
            raise exceptions.TypeException(
                err_msg.format(err_msg.format(value))
            )

    @base.skip_falsy
    def validate_regex(self, value):
        if self.regex and not self._regex.match(value):
            err_msg = "Value did not match regex: {}"
            raise exceptions.ValidationException(
                err_msg.format(self, self.regex)
            )


class Number(Primitive):
    def __init__(self, max=None, min=None, **kw):
        super().__init__(**kw)
        domains.RangeDomain(self, max, min)


class IntegerType(Number):
    NATIVE = int


class FloatType(Number):
    NATIVE = float
