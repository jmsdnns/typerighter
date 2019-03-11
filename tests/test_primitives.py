import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Structural

def test_type_instance_config_default():
    class TestType(types.Primitive):
        pass

    tt = TestType()

    assert tt.default == types.Unset
    assert tt.required == False
    assert tt.choices == None


def test_type_config_inheritance():
    class TestType(types.Primitive):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.required = True

    class SubTestType(TestType):
        pass

    tt = TestType()
    stt = SubTestType()

    assert tt.default == stt.default
    assert tt.required == stt.required
    assert tt.choices == stt.choices


def test_type_class_config_hierarchy_inheritance():
    class TestTypeA(types.Primitive):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.required = True

    class TestTypeB(TestTypeA):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.choices = ['drums', 'guitar']

    class TestTypeC(TestTypeB):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.default = 'drums'

    class TestTypeD(TestTypeC):
        pass

    ttd = TestTypeD()

    assert ttd.required == True
    assert ttd.choices == ['drums', 'guitar']
    assert ttd.default == 'drums'


def test_type_class_config_multiple_inheritance():
    class TestTypeA(types.Primitive):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.default = "A"

    class TestTypeB(types.Primitive):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.default = "B"

    class SubTestType(TestTypeA, TestTypeB):
        pass

    stt = SubTestType()

    assert stt.default == "A"

# Conversion

def test_primitive_skips_conversion():
    p = types.Primitive()

    p_data = 'foo'

    assert p.to_primitive(p_data) == p_data
    assert p.to_native(p_data) == p_data

    p_data = 5

    assert p.to_primitive(p_data) == p_data
    assert p.to_native(p_data) == p_data

    p_data = {'foo': 'bar'}

    assert p.to_primitive(p_data) == p_data
    assert p.to_native(p_data) == p_data


def test_primitive_default():
    p = types.Primitive(default='foo')

    assert p.to_native(types.Unset) == 'foo'
    assert p.to_primitive(types.Unset) == 'foo'

    p = types.Primitive(default=5)

    assert p.to_native(types.Unset) == 5
    assert p.to_primitive(types.Unset) == 5

    d = {'foo': 'bar'}
    p = types.Primitive(default=d)

    assert p.to_native(types.Unset) == d
    assert p.to_primitive(types.Unset) == d


# Validation

def test_primitive_validates_literally_anything():
    p = types.Primitive()
    p.validate(types.Unset)
    p.validate(None)
    p.validate("This is a string")
    p.validate("")
    p.validate(1)
    p.validate(3.14)


def test_primitive_required():
    p = types.Primitive(required=True)
    with pytest.raises(exceptions.ValidationException):
        p.validate(types.Unset)
    p.validate(None)
    p.validate(None)
    p.validate("This is a string")
    p.validate("")
    p.validate(1)
    p.validate(3.14)


def test_primitive_choices():
    p = types.Primitive(choices=['foo', 'bar'])

    with pytest.raises(exceptions.ValidationException):
        p.validate(types.Unset)

    with pytest.raises(exceptions.ValidationException):
        p.validate(None)

    with pytest.raises(exceptions.ValidationException):
        p.validate("This is a string")

    with pytest.raises(exceptions.ValidationException):
         p.validate(3.14)

    p.validate("foo")
    p.validate("bar")
