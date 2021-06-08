from typerighter import types


def test_filtering_basic():
    class SongRecord(types.Record):
        name = types.StringType(required=True)
        author = types.StringType(required=True)

    sr = SongRecord()
    data = {
        'name': 'pride & joy',
        'author': 'stevie ray vaughn'
    }

    fields = ['name']
    filtered_data = sr.to_primitive(data, fields=fields)
    assert 'name' in filtered_data
    assert 'author' not in filtered_data


def test_filtering_messy_nested():

    class Song(types.Record):
        name = types.StringType(required=True)
        created_at = types.DateTimeType()
        file = types.UnixPathType()
        lyrics = types.StringType(max_length=255)

    class Album(types.Record):
        name = types.StringType(required=True)
        created_at = types.DateTimeType()
        songs = types.ListType(Song())

    class Artist(types.Record):
        name = types.StringType(required=True)
        created_at = types.DateTimeType()
        website = types.URLType()
        albums = types.ListType(Album())

    artist_type = Artist()

    artist_data = {
        'name': 'American Food',
        'created_at': '2021-05-29T00:00:01.001337',
        'albums': [{
            'name': 'Internet On The TV',
            'created_at': '2021-05-29T00:00:01.001337',
            'songs': [{
                'name': 'Cane Spiders (mispoke)',
                'created_at': '2021-05-29T00:00:00.001337',
                'lyrics': 'Oh my gawd! It\'s that red dot! Gonna catch that...'
            }, {
                'name': 'My Take On Take On Me',
                'created_at': '2021-05-30T00:00:00.001337',
                'lyrics': 'I know. I know. I talk in numbers...'
            }]
        }]
    }

    fields = [
        'name', 'albums.name', 'albums.songs.name', 'albums.songs.created_at'
    ]

    filtered_data = artist_type.to_primitive(artist_data, fields=fields)

    assert 'name' in filtered_data
    assert 'albums' in filtered_data

    assert 'created_at' not in filtered_data
    assert 'lyrics' not in filtered_data

    assert len(set(['name', 'albums']) - set(filtered_data.keys())) == 0

    first_album = filtered_data['albums'][0]
    assert len(set(['songs']) - set(first_album)) == 0

    first_song = filtered_data['albums'][0]['songs'][0]
    assert len(set(['name', 'created_at']) - set(first_song)) == 0

    second_song = filtered_data['albums'][0]['songs'][1]
    assert len(set(['name', 'created_at']) - set(second_song)) == 0
