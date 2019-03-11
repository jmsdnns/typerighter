import pytest

from typerighter import types
from typerighter import cache
from typerighter import exceptions


@pytest.fixture
def gen_musical_types():
    class SongType(types.Record):
        name = types.StringType(required=True)

    class AlbumType(types.Record):
        name = types.StringType()
        songs = types.ListType(SongType())

    class ArtistType(types.Record):
        name = types.StringType()
        epoch = types.StringType()
        albums = types.ListType(AlbumType())

    return (SongType, AlbumType, ArtistType)


def test_created_classes_in_cache(gen_musical_types):
    (song_cls, album_cls, artist_cls) = gen_musical_types

    new_keys = set([t.__name__ for t in (song_cls, album_cls, artist_cls)])
    cache_keys = set(cache.TypeCache().keys())

    assert len(new_keys - cache_keys) == 0


def test_created_classes_in_cache(gen_musical_types):
    (song_cls, album_cls, artist_cls) = gen_musical_types

    new_keys = set([t.__name__ for t in (song_cls, album_cls, artist_cls)])
    cache_keys = set(cache.TypeCache().keys())

    assert len(new_keys - cache_keys) == 0
