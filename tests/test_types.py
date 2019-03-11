import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


def test_unset_exists():
    assert hasattr(types, 'Unset')


# Structural

def test_typemeta_new():
    empty_namespace = {}
    new_class = types.TypeMeta('TestType', (types.Type,), empty_namespace)
    assert hasattr(new_class, '_schematic')
    assert hasattr(new_class, '_validate_functions')


def test_type_class_meta_defaults():
    class TestType(types.Type):
        pass

    assert hasattr(TestType, '_validate_functions')
    assert len(TestType._validate_functions) == 0

    assert hasattr(TestType, '_schematic')
    assert isinstance(TestType._schematic, schematics.Schematic)

    # `_fields` only appears on records
    assert not hasattr(TestType, '_fields')


def test_type_instance_meta_defaults():
    class TestType(types.Type):
        pass

    tt = TestType()

    assert hasattr(tt, '_validate_functions')
    assert len(tt._validate_functions) == 0

    assert hasattr(tt, '_schematic')
    assert isinstance(tt._schematic, schematics.Schematic)

    # `_fields` only appears on records
    assert not hasattr(tt, '_fields')


# Conversion

def test_type_basic_conversion():
    class TestType(types.Type):
        s = types.StringType()
        b = types.BooleanType()

    tt = TestType()
    tt_data = {'s': 'some string', 'b': True}

    assert tt.to_primitive(tt_data) == tt_data
    assert tt.to_native(tt_data) == tt_data


def test_type_default():
    t = types.Type(default='foo')

    assert t.to_native(types.Unset) == 'foo'
    assert t.to_primitive(types.Unset) == 'foo'

    t = types.Type(default=5)

    assert t.to_native(types.Unset) == 5
    assert t.to_primitive(types.Unset) == 5

    d = {'foo': 'bar'}
    t = types.Type(default=d)

    assert t.to_native(types.Unset) == d
    assert t.to_primitive(types.Unset) == d


# Validation

def test_type_class_with_validators():
    class TestTypeA(types.Type):
        def validate_foo(self, value):
            return True

    assert hasattr(TestTypeA, '_validate_functions')
    assert len(TestTypeA._validate_functions) == 1

    class TestTypeB(types.Type):
        def validate_a(self, value):
            return True
        def validate_b(self, value):
            return True
        def validate_c(self, value):
            return True

    assert hasattr(TestTypeB, '_validate_functions')
    assert len(TestTypeB._validate_functions) == 3


def test_type_validator_function_order():
    class TestType(types.Type):
        def validate_a(self, value):
            return True
        def validate_b(self, value):
            return True
        def validate_c(self, value):
            return True
        def validate_d(self, value):
            return True

    expected_order = [
        'validate_a',
        'validate_b',
        'validate_c',
        'validate_d'
    ]
    actual_order = TestType._validate_functions

    for expected_name, actual_name in zip(expected_order, actual_order):
        assert expected_name == actual_name


def test_type_validator_name_clash():
    class TestType(types.Type):
        def validate_a(self, value):
            return 'first'
        def validate_a(self, value):
            return 'last'

    assert hasattr(TestType, '_validate_functions')
    assert len(TestType._validate_functions) == 1

    unbound_method = TestType._validate_functions['validate_a']
    validate = lambda value: unbound_method(TestType, value)
    assert validate('blabla') == 'last'


def test_type_validation_calls_order():
    call_order = list()

    class TestType(types.Type):
        def validate_first(self, value):
            call_order.append('first')
        def validate_second(self, value):
            call_order.append('second')
        def validate_third(self, value):
            call_order.append('third')
        def validate_fourth(self, value):
            call_order.append('fourth')
        def validate_fifth(self, value):
            call_order.append('fifth')

    TestType().validate(None)

    assert call_order == ['first', 'second', 'third', 'fourth', 'fifth']
