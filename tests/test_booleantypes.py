import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Conversion

def test_boolean_instance_config_default():
    b = types.BooleanType(default=True)

    assert b.to_native(types.Unset) == True
    assert b.to_native(False) == False


# Validation

def test_boolean_basic_validation():
    b = types.BooleanType()

    b.validate(True)
    b.validate(False)

    with pytest.raises(exceptions.ValidationException):
        b.validate(types.Unset)


def test_boolean_string_validation():
    b = types.BooleanType()

    b.validate('true')
    b.validate('false')


def test_boolean_strict_validation():
    b = types.BooleanType(strict=True)

    b.validate(True)
    b.validate(False)

    with pytest.raises(exceptions.ValidationException):
        b.validate('true')

    with pytest.raises(exceptions.ValidationException):
        b.validate('false')
