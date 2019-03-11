import pytest

from typerighter import types
from typerighter import exceptions


# Structural


# Conversion

def test_type_list_conversion():
    lt = types.ListType(types.StringType(min_length=5))

    lt_data = ['a', 'b', 'meow']

    assert lt.to_primitive(lt_data) == lt_data
    assert lt.to_native(lt_data) == lt_data

    lt_data = ['data', 4]

    assert lt.to_primitive(lt_data) != lt_data
    assert lt.to_primitive(lt_data)[1] == '4'
    assert lt.to_native(lt_data) != lt_data
    assert lt.to_native(lt_data)[1] == '4'


# Validation

def test_listtype_validates_the_basics():
    list_of_strings = types.ListType(types.StringType())

    list_of_strings.validate(['list', 'of', 'strings'])
    list_of_strings.validate([])
    list_of_strings.validate(None)
    list_of_strings.validate(types.Unset)


def test_listtype_check_required():
    list_of_strings = types.ListType(types.StringType(), required=True)

    list_of_strings.validate(['list', 'of', 'strings'])
    list_of_strings.validate([])
    list_of_strings.validate(None)

    with pytest.raises(exceptions.ValidationException):
        list_of_strings.validate(types.Unset)

    list_of_strings.validate([types.Unset])


def test_listtype_item_type_is_required():
    list_of_strings = types.ListType(types.StringType(required=True))

    list_of_strings.validate(['list', 'of', 'strings'])
    list_of_strings.validate([])
    list_of_strings.validate(None)
    list_of_strings.validate(types.Unset)

    with pytest.raises(exceptions.ValidationException):
        list_of_strings.validate([types.Unset])


def test_listtype_validates_min_size():
    list_of_strings = types.ListType(types.StringType(), min_length=3)

    list_of_strings.validate(['list', 'of', 'strings'])
    list_of_strings.validate(types.Unset)

    with pytest.raises(exceptions.ValidationException):
        list_of_strings.validate([])
    with pytest.raises(exceptions.ValidationException):
        list_of_strings.validate(None)


def test_listtype_validates_max_size():
    list_of_strings = types.ListType(types.StringType(), max_length=3)

    list_of_strings.validate(['list', 'of', 'strings'])
    list_of_strings.validate([])
    list_of_strings.validate(None)
    list_of_strings.validate(types.Unset)

    with pytest.raises(exceptions.ValidationException):
        list_of_strings.validate(['li', 'st', 'of', 'strings'])
