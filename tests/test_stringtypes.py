import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import exceptions


def test_stringtype_validates_the_basics():
    st = types.StringType()
    # Accepted
    st.validate(types.Unset)
    st.validate(None)
    st.validate("This is a string")
    st.validate("")
    st.validate(1)
    st.validate(3.14)


def test_stringtype_check_required():
    st = types.StringType(required=True)

    st.validate("This is a string")
    st.validate("")
    st.validate(None)
    with pytest.raises(exceptions.ValidationException):
        st.validate(types.Unset)



def test_stringtype_check_strict():
    st = types.StringType(strict=True)
    # Accepted
    st.validate(types.Unset)
    st.validate(None)
    st.validate("This is a string")
    st.validate("")
    with pytest.raises(exceptions.ValidationException):
        st.validate(1)
    with pytest.raises(exceptions.ValidationException):
        st.validate(3.14)


def test_stringtype_max_length():
    st = types.StringType(max_length=3)

    st.validate("hi")
    st.validate("")
    st.validate(None)
    st.validate(types.Unset)

    with pytest.raises(exceptions.ValidationException):
        st.validate("hello")


def test_stringtype_max_length_and_required():
    st = types.StringType(max_length=3, required=True)

    st.validate("hi")
    st.validate("")
    st.validate(None)

    with pytest.raises(exceptions.ValidationException):
        st.validate(types.Unset)
    with pytest.raises(exceptions.ValidationException):
        st.validate("hello")


def test_stringtype_min_length():
    st = types.StringType(min_length=3)

    st.validate("hello")
    st.validate(types.Unset)

    with pytest.raises(exceptions.ValidationException):
        st.validate(None)
    with pytest.raises(exceptions.ValidationException):
        st.validate("")
    with pytest.raises(exceptions.ValidationException):
        st.validate("hi")


def test_stringtype_min_length_and_required():
    st = types.StringType(min_length=3, required=True)

    st.validate("hello")

    with pytest.raises(exceptions.ValidationException):
        st.validate(None)
    with pytest.raises(exceptions.ValidationException):
        st.validate(types.Unset)
    with pytest.raises(exceptions.ValidationException):
        st.validate("")
    with pytest.raises(exceptions.ValidationException):
        st.validate("hi")
