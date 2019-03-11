import pytest

from collections import OrderedDict

from typerighter import types
from typerighter import schematics
from typerighter import exceptions


# Structural

def test_record_meta_defaults():
    class TestRecord(types.Record):
        pass

    # Records have a `validate_fields` function`
    assert hasattr(TestRecord, '_validate_functions')
    assert len(TestRecord._validate_functions) == 1

    assert hasattr(TestRecord, '_schematic')
    assert isinstance(TestRecord._schematic, schematics.Schematic)

    # `_fields` only appears on records
    assert hasattr(TestRecord, '_fields')
    assert len(TestRecord._fields) == 0

    # `_fields` only appears on records
    assert hasattr(TestRecord, '_field_functions')
    assert len(TestRecord._field_functions) == 0


def test_record_config_default():
    class TestRecord(types.Record):
        pass

    tr = TestRecord()

    assert tr.strict == False
    assert tr.field_filters == None
    assert tr.export_nones == False


def test_record_config_inheritance():
    class TestRecord(types.Record):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.strict = True

    class SubTestRecord(TestRecord):
        pass

    tr = TestRecord()
    sttr = SubTestRecord()

    assert tr.strict == sttr.strict
    assert tr.field_filters == sttr.field_filters
    assert tr.export_nones == sttr.export_nones


def test_record_class_config_hierarchy_inheritance():
    class TestRecordA(types.Record):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.strict = True

    class TestRecordB(TestRecordA):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.field_filters = ['foo', 'bar']

    class TestRecordC(TestRecordB):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.choices = ['asdf', 'jkl;']

    class TestRecordD(TestRecordC):
        pass

    trd = TestRecordD()

    assert trd.strict == True
    assert trd.field_filters == ['foo', 'bar']
    assert trd.choices == ['asdf', 'jkl;']


def test_record_class_config_multiple_inheritance():
    class TestRecordA(types.Record):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.choices = ["A"]

    class TestRecordB(types.Record):
        def __init__(self, **kw):
            super().__init__(**kw)
            self.choices = ["B"]

    class SubTestRecord(TestRecordA, TestRecordB):
        pass

    stt = SubTestRecord()

    assert stt.choices == ["A"]


def test_record_validation_calls_validators():
    call_order = list()

    class TestRecord(types.Record):
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

    TestRecord().validate({})

    assert call_order == ['first', 'second', 'third', 'fourth', 'fifth']


def test_records_as_field():
    class TestRecord(types.Record):
        s = types.StringType(required=True)

    class ParentRecord(types.Record):
        tr = TestRecord(required=True)

    class GrandparentRecord(types.Record):
        pr = ParentRecord()

    class GreatGrandparentRecord(types.Record):
        gr = GrandparentRecord()

    ggr = GreatGrandparentRecord()

    assert isinstance(ggr, GreatGrandparentRecord)
    assert isinstance(ggr.gr, GrandparentRecord)
    assert isinstance(ggr.gr.pr, ParentRecord)
    assert isinstance(ggr.gr.pr.tr, TestRecord)
    assert isinstance(ggr.gr.pr.tr.s, types.StringType)


# Validation

def test_record_validates_the_basics():
    class TestRecord(types.Record):
        s = types.StringType()

    tr = TestRecord()

    tr.validate({'s': 'This is a string'})
    tr.validate({'s': None})
    tr.validate({})
    tr.validate(None)


def test_record_validates_required():
    class TestRecord(types.Record):
        s = types.StringType(required=True)

    tr = TestRecord()

    tr.validate({'s': 'This is a string'})
    tr.validate({'s': None})
    tr.validate(None)

    with pytest.raises(exceptions.ValidationException):
        tr.validate({'s': types.Unset})

    with pytest.raises(exceptions.ValidationException):
        tr.validate({})


def test_record_as_field():
    class TestRecord(types.Record):
        s = types.StringType(required=True)

    class ParentRecord(types.Record):
        tr = TestRecord()

    pr = ParentRecord()

    assert isinstance(pr.tr, TestRecord)

    data = {'tr': {'s': 'This is a string'}}
    pr.validate(data)

    data = {'tr': {'s': types.Unset}}
    with pytest.raises(exceptions.ValidationException):
        pr.validate(data)


def test_records_validate_records_as_fielda():
    class TestRecord(types.Record):
        s1 = types.StringType(required=True)
        s2 = types.StringType()

    class ParentRecord(types.Record):
        tr = TestRecord()

    class GrandparentRecord(types.Record):
        pr = ParentRecord()

    class GreatGrandparentRecord(types.Record):
        gr = GrandparentRecord()

    ggr = GreatGrandparentRecord()

    ggr.validate({'gr': {'pr': {'tr': {'s1': None}}}})
    ggr.validate({'gr': {'pr': {'tr': {'s1': None, 's2': None}}}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {'pr': {'tr': {'s2': None}}}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {'pr': {'tr': {'s1': types.Unset}}}})

    ggr.validate({'gr': {'pr': {'tr': None}}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {'pr': {'tr': {}}}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {'pr': {'tr': types.Unset}}})

    ggr.validate({'gr': {'pr': None}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {'pr': {}}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {'pr': types.Unset}})

    ggr.validate({'gr': None})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': {}})
    with pytest.raises(exceptions.ValidationException):
        ggr.validate({'gr': types.Unset})

    ggr.validate(None)
    with pytest.raises(exceptions.ValidationException):
        ggr.validate(types.Unset)


def test_records_validate_records_as_fielda():
    class TestRecord(types.Record):
        s1 = types.StringType()

    tr1 = TestRecord(required=True)
    with pytest.raises(exceptions.ValidationException):
        tr1.validate(types.Unset)

    tr2 = TestRecord()
    tr2.validate(types.Unset)
