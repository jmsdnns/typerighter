import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Conversion

def test_ip_address_instance_config_default():
    e = types.IPAddressType()

    example = "192.168.1.1"
    assert e.to_native(example) == example
    assert e.to_primitive(example) == example


# Validation

def test_ip_address_basic_validation():
    e = types.IPAddressType()

    e.validate(types.Unset)
    e.validate("192.168.1.1")
    e.validate("FE80:CD00:0000:0CDE:1257:0000:211E:729C")

    with pytest.raises(exceptions.ValidationException):
        e.validate("weeeeeee")
    with pytest.raises(exceptions.ValidationException):
        e.validate("00:25:96:FF:FE")


def test_ipv6_address_basic_validation():
    e = types.IPv6Type()

    e.validate(types.Unset)
    e.validate("FE80:CD00:0000:0CDE:1257:0000:211E:729C")

    with pytest.raises(exceptions.ValidationException):
        e.validate("weeeeeee")
    with pytest.raises(exceptions.ValidationException):
        e.validate("192.168.1.1")


def test_ipv4_address_basic_validation():
    e = types.IPv4Type()

    e.validate(types.Unset)
    e.validate("192.168.1.1")

    with pytest.raises(exceptions.ValidationException):
        e.validate("weeeeeee")
    with pytest.raises(exceptions.ValidationException):
        e.validate("FE80:CD00:0000:0CDE:1257:0000:211E:729C")
