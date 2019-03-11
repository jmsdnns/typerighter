import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Conversion

def test_url_instance_config_default():
    e = types.URLType()

    assert e.to_native("http://word.com") == "http://word.com"
    assert e.to_primitive("http://word.com") == "http://word.com"


# Validation

def test_url_basic_validation():
    e = types.URLType()

    e.validate(types.Unset)
    e.validate("http://word.com")
    e.validate("http://word.co.uk")
    e.validate("spotify://workspace/ohyeah")

    with pytest.raises(exceptions.ValidationException):
        e.validate("weeeeeee")
    with pytest.raises(exceptions.ValidationException):
        e.validate("word.com")
    with pytest.raises(exceptions.ValidationException):
        e.validate("file:///some/path")
