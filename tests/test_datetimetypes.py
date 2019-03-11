import pytest

from collections import OrderedDict
import datetime

from typerighter import types
from typerighter import exceptions


# Structural


# Conversion

def test_type_datetime_conversion():
    dt = types.DateTimeType()
    ds = '2019-03-01T01:46:04.958967'

    native = dt.to_native(ds)
    assert isinstance(native, datetime.datetime) == True

    assert native.year == 2019
    assert native.month == 3
    assert native.day == 1
    assert native.hour == 1
    assert native.minute == 46
    assert native.second == 4
    assert native.microsecond == 958967

    primitive = dt.to_primitive(native)
    assert primitive == ds

def test_type_datetime_timezone_offset():
    dt = types.DateTimeType()
    input_ds = '2012-07-24T23:14:29-07:00'
    output_ds = '2012-07-24T23:14:29.000000-0700'

    native = dt.to_native(input_ds)
    print(native)
    print(type(native))
    assert isinstance(native, datetime.datetime) == True

    assert native.year == 2012
    assert native.month == 7
    assert native.day == 24
    assert native.hour == 23
    assert native.minute == 14
    assert native.second == 29
    assert native.microsecond == 0

    primitive = dt.to_primitive(native)
    assert primitive == output_ds
