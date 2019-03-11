import pytest

from typerighter import types


def test_schematics_from_type():
    class SongType(types.Record):
        name = types.StringType(required=True)

    st = SongType()

    assert st._schematic._argspec['strict'] == False
    assert st._schematic._argspec['field_filters'] == None
    assert st._schematic._argspec['export_nones'] == False

    st = SongType(strict=True, field_filters=[])

    assert st._schematic._argspec['strict'] == False
    assert st._schematic._argspec['field_filters'] == None
    assert st._schematic._argspec['export_nones'] == False

    assert st._schematic._init_args['strict'] == True
    assert st._schematic._init_args['field_filters'] == []
    assert st._schematic._init_args['export_nones'] == False
