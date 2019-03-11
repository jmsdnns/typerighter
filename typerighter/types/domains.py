import re

from typerighter import exceptions
from . import base


def skip_falsy(method):
    def wrapper(self, instance, value, *a, **kw):
        if self.is_falsy(instance, value):
            return value
        return method(self, instance, value, *a, **kw)
    return wrapper


class Domain:
    def __init__(self, instance):
        for attr_name in (a for a in dir(self) if a.startswith("validate_")):
            attr = getattr(self, attr_name)
            instance._validate_functions[attr_name] = attr

    def is_falsy(self, instance, value):
        return instance.is_falsy(value)


class RangeDomain(Domain):
    def __init__(self, instance, max=None, min=None):
        super().__init__(instance)
        instance.min = min
        instance.max = max

    def validate_min(self, instance, value):
        if not instance.min or value == base.Unset:
            return

        if instance.min and instance.is_falsy(value):
            err_msg = "Empty value not allowed with min: {}"
            raise exceptions.ValidationException(
                err_msg.format(instance.min)
            )

        if value < instance.min:
            err_msg = "Value below allowed min: {} < {}"
            raise exceptions.ValidationException(
                err_msg.format(value, instance.min)
            )

    def validate_max(self, instance, value):
        if not instance.max or instance.is_falsy(value):
            return

        if value > instance.max:
            err_msg = "Value exceeds allowed max: {} > {}"
            raise exceptions.ValidationException(
                err_msg.format(value, instance.max)
            )


class LengthDomain(Domain):
    def __init__(self, instance, max_length=None, min_length=None):
        super().__init__(instance)
        instance.max_length = max_length
        instance.min_length = min_length

    def validate_min_length(self, instance, value):
        if not instance.min_length or value == base.Unset:
            return

        if instance.min_length and instance.is_falsy(value):
            err_msg = "Empty value below min length: {}"
            raise exceptions.ValidationException(
                err_msg.format(instance.min_length)
            )

        if len(value) < instance.min_length:
            err_msg = "Value below min length: {} < {}"
            raise exceptions.ValidationException(
                err_msg.format(value, instance.min_length)
            )

    def validate_max_length(self, instance, value):
        if not instance.max_length or instance.is_falsy(value):
            return

        if len(value) > instance.max_length:
            err_msg = "Value length above max: {} > {}"
            raise exceptions.ValidationException(
                err_msg.format(value, instance.max_length)
            )


class RegexDomain(Domain):
    def __init__(self, instance, regex, *compile_args):
        super().__init__(instance)
        instance.regex = regex

        if instance.regex:
            try:
                compiled = re.compile(instance.regex, *compile_args)
                instance._regex = compiled
            except:
                err_msg = "Regex failed to compile: {}"
                raise exceptions.TypeException(
                    err_msg.format(instance.regex)
                )

    def validate_regex(self, instance, value):
        if instance.is_falsy(value):
            return
        if not isinstance(value, str):
            return

        if instance._regex and not instance._regex.match(value):
            err_msg = "Value did not match regex: {}"
            raise exceptions.ValidationException(
                err_msg.format(value, instance.regex)
            )
