import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import exceptions


# Conversion

def test_type_sum_conversion():
    class TestType(types.Type):
        st = types.SumType(types.StringType(min_length=10), types.BooleanType())
        b = types.BooleanType()

    tt = TestType()
    tt_data = {'st': 'some string', 'b': True}

    assert tt.to_primitive(tt_data) == tt_data
    assert tt.to_native(tt_data) == tt_data

    tt = TestType()
    tt_data = {'st': False, 'b': True}

    assert tt.to_primitive(tt_data) == tt_data
    assert tt.to_native(tt_data) == tt_data

    tt = TestType()
    tt_data = {'b': True}

    assert tt.to_primitive(tt_data) == tt_data
    assert tt.to_native(tt_data) == tt_data


# Validation

def test_sumtype_validates_the_basics():
    big_strings = types.StringType(min_length=7)
    small_strings = types.StringType(max_length=3)
    big_or_small_strings = types.SumType(big_strings, small_strings)
    
    with pytest.raises(exceptions.ValidationException):
        big_strings.validate('li')
    with pytest.raises(exceptions.ValidationException):
        big_strings.validate('st')
    big_strings.validate('of strings')

    small_strings.validate('li')
    small_strings.validate('st')
    with pytest.raises(exceptions.ValidationException):
        small_strings.validate('of strings')

    big_or_small_strings.validate('li')
    big_or_small_strings.validate('st')
    big_or_small_strings.validate('of strings')
    big_or_small_strings.validate(None)
    big_or_small_strings.validate(types.Unset)


def test_sumtype_check_required():
    st = types.SumType(types.StringType(strict=True), required=True)

    st.validate("")
    st.validate(None)

    with pytest.raises(exceptions.ValidationException):
        st.validate(types.Unset)
    with pytest.raises(exceptions.ValidationException):
        st.validate(1)
    with pytest.raises(exceptions.ValidationException):
        st.validate(3.14)



def test_sumtype_item_type_honors_required():
    st = types.SumType(
        types.Primitive(required=True),
        types.Primitive(required=True),
        types.Primitive(required=True),
        types.Primitive(required=True),
    )

    st.validate('foo')

    with pytest.raises(exceptions.TypeException):
        st.validate(types.Unset)

    st = types.SumType(
        types.Primitive(required=True),
        types.Primitive(required=True),
        types.Primitive(required=True),
        types.Primitive(),
    )

    st.validate(types.Unset)

