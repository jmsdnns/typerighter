import pytest

from typerighter import types
from typerighter import views


def test_views_have_fields():
    class SongRecord(types.Record):
        author = types.StringType(required=True)

    sr = SongRecord()

    srv = views.make_view(sr, {'author': 'stevie ray vaughn'})

    assert hasattr(sr, 'author')
    assert isinstance(sr.author, types.Type)

    assert hasattr(srv, 'author')
    assert srv.author == 'stevie ray vaughn'


def test_views_partial_data_make_view():
    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = types.StringType(required=True)
        instruments = types.ListType(types.StringType())

    sr = SongRecord()

    srv = views.make_view(sr, {
        'author': 'stevie ray vaughn',
        'instruments': ['guitar', 'drums', 'bass']
    })

    assert hasattr(sr, 'author')
    assert isinstance(sr.author, types.Type)
    assert isinstance(sr.author, types.StringType)

    assert hasattr(srv, 'author')
    assert srv.author == 'stevie ray vaughn'

    assert hasattr(srv, 'instruments')
    assert srv.instruments == ['guitar', 'drums', 'bass']

    assert hasattr(srv, 'name')
    assert srv.name == None


def test_views_partial_data_to_view():
    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = types.StringType(required=True)
        instruments = types.ListType(types.StringType())

    sr = SongRecord()

    srv = sr.to_view({
        'author': 'stevie ray vaughn',
        'instruments': ['guitar', 'drums', 'bass']
    })

    assert hasattr(sr, 'author')
    assert isinstance(sr.author, types.Type)
    assert isinstance(sr.author, types.StringType)

    assert hasattr(srv, 'author')
    assert srv.author == 'stevie ray vaughn'

    assert hasattr(srv, 'instruments')
    assert srv.instruments == ['guitar', 'drums', 'bass']

    assert hasattr(srv, 'name')
    assert srv.name == None
