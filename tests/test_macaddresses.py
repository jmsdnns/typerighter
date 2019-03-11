import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Conversion

def test_mac_address_instance_config_default():
    e = types.MACAddressType()

    example = "00:25:96:FF:FE:12:34:56"
    assert e.to_native(example) == example
    assert e.to_primitive(example) == example


# Validation

def test_mac_address_basic_validation():
    e = types.MACAddressType()

    e.validate(types.Unset)
    e.validate("00:25:96:FF:FE:12")

    with pytest.raises(exceptions.ValidationException):
        e.validate("weeeeeee")
    with pytest.raises(exceptions.ValidationException):
        e.validate("00:25:96:FF:FE")
