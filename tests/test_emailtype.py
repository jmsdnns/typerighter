import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Conversion

def test_email_instance_config_default():
    e = types.EmailType()

    assert e.to_native("ih@ve.one") == "ih@ve.one"
    assert e.to_primitive("ih@ve.one") == "ih@ve.one"


# Validation

def test_email_basic_validation():
    e = types.EmailType()

    e.validate(types.Unset)
    e.validate("ih@ve.one")
    e.validate("word+something@google.com")
    e.validate("word@whatevuh.co.uk")

    with pytest.raises(exceptions.ValidationException):
        e.validate("weeeeeee")
    with pytest.raises(exceptions.ValidationException):
        e.validate("google.com")
