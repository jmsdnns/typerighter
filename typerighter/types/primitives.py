import re

from . import base
from . import domains
from .. import exceptions


class Primitive(base.Type):
    """
    A `Primitive` is the first `Type` that validates data by looking at its
    contents. It is intended as a common base class among primitive types and
    is not intended for regular use.

    It extends validation by checking if input values match a list of possible
    choices.

    It inherits `object` as its native type, allowing any data to pass
    validation.
    """
    def __init__(self, choices=None, **kw):
        super().__init__(**kw)
        self.choices = choices

    def validate_choices(self, value):
        """
        Checks if a choices list has been set and then if `value` is in that
        list.
        """
        if self.choices and (value == base.Unset or value not in self.choices):
            e_msg = "Illegal choice for value: {}"
            raise exceptions.ValidationException(e_msg.format(value))


class BooleanType(Primitive):
    """
    This validator implements booleans as falsy values. This is done by passing
    the value directly into Python's `bool` and using Python's native behavior.
    """
    NATIVE = bool

    def to_primitive(self, value):
        """
        Attempts to convert the input value into a Python `bool`.
        """
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
        """
        Confirms the value is compatible with `bool`.
        """
        try:
            self.to_primitive(value)
        except exceptions.TypeException as te:
            ve = exceptions.ValidationException(*te.args)
            raise ve


class StringType(Primitive):
    """A type that captures the core needs for validating strings, which can
    then be extended in subclasses for validating specific types of strings.

    Validation can be extended by using `min_length` or `max_length`, or by
    providing a regular expression compatible with Python's `re` module.
    """
    NATIVE = str

    def __init__(self, max_length=None, min_length=None, regex=None, **kw):
        super().__init__(**kw)
        domains.LengthDomain(self, max_length, min_length)

        self.regex = regex

        if self.regex:
            try:
                compiled = re.compile(self.regex)
                self._regex = compiled
            except Exception:
                err_msg = "Regex failed to compile: {}"
                raise exceptions.TypeException(
                    err_msg.format(self.regex)
                )

    def is_falsy(self, value):
        if value is None or value == "":
            return True

        return super().is_falsy(value)

    def to_primitive(self, value):
        """
        Converts the value to `str`.
        """
        if isinstance(value, str):
            return value

        try:
            p = str(value)
            return p
        except Exception:
            err_msg = "Could not convert to string: {}"
            raise exceptions.TypeException(
                err_msg.format(err_msg.format(value))
            )

    @base.skip_falsy
    def validate_regex(self, value):
        if self.regex and not self._regex.match(value):
            err_msg = "Value did not match regex: {}"
            raise exceptions.ValidationException(
                err_msg.format(self.regex)
            )


class Number(Primitive):
    """
    Used for tracking the functionality common to numbers. The current
    implementation simply supports ranges of numbers.
    """
    def __init__(self, max=None, min=None, **kw):
        super().__init__(**kw)
        domains.RangeDomain(self, max, min)


class IntegerType(Number):
    """
    A `Number` implementation based on Python `int`.
    """
    NATIVE = int


class FloatType(Number):
    """
    A `Number` implementation based on Python `float`.
    """
    NATIVE = float
