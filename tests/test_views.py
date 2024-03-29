import pytest

from typerighter import types
from typerighter import views


def test_views_have_fields():
    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = types.StringType(required=True)

    sr = SongRecord()
    data = {
        'name': 'pride & joy',
        'author': 'stevie ray vaughn'
    }

    srv = views.to_view(sr, data)
    assert isinstance(srv, views.View)
    assert hasattr(srv, 'name')
    assert hasattr(srv, 'author')
    assert srv.name == data['name']
    assert srv.author == data['author']


def test_views_have_record_views_as_fields():
    class MusicianRecord(types.Record):
        name = types.StringType(required=True)

    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = MusicianRecord()

    sr = SongRecord()
    data = {
        'name': 'pride & joy',
        'author': {
            'name': 'stevie ray vaughn'
        }
    }

    srv = views.to_view(sr, data)
    assert isinstance(srv, views.View)
    assert isinstance(srv.author, views.View)
    assert hasattr(srv, 'name')
    assert hasattr(srv, 'author')
    assert hasattr(srv.author, 'name')
    assert srv.name == data['name']
    assert srv.author.name == 'stevie ray vaughn'


def test_views_partial_data_to_view():
    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = types.StringType(required=True)
        instruments = types.ListType(types.StringType())

    sr = SongRecord()

    srv = views.to_view(sr, {
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


def test_views_have_starting_types():
    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = types.StringType()
        created_at = types.DateTimeType()

    import datetime

    sr = SongRecord()
    data = {
        'name': 'pride & joy',
        'author': 'stevie ray vaughn',
        'created_at': datetime.datetime.now()
    }

    pnj = views.to_view(sr, data, primitive=True)
    assert isinstance(pnj.created_at, str)

    pnj = views.to_view(sr, data)
    assert isinstance(pnj.created_at, datetime.datetime)

    # primitive is favored if both are True
    pnj = views.to_view(sr, data, primitive=True, native=True)
    assert isinstance(pnj.created_at, str)
