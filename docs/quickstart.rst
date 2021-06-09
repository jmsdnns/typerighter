.. quickstart

==========
Quickstart
==========

We start with *types*. A lot has been said about this concept and folks
sometimes have different mental models for what one is.

This library defines it as something that can audit some data for coherence. We
can take this further too, for some helpful tooling, but we start with this
simple foundation.

For this library, a *type* is essentially something with a validation function.

From there, we create structures of data by using associating names with types
in a *record*.

We then use some of the builtin functions to convert, filter, and repackage
various messes of data that may or may not resemble the messes typical of
working with data.

Types
=======

We'll start by creating a type for short strings.

  >>> short = types.StringType(max_length=12)

A type *instance* can then be used for validating data. ::

  >>> short.validate('short enough')

Exceptions are thrown for validation errors. ::

  >>> short.validate('not short enough')
  ...
  typerighter.exceptions.ValidationException: Value length above max: short enoughhhh > 12

Conversion
----------

They can also convert between Python native types and something safely language
agnostic. ::

  >>> dt = types.DateTimeType()
  >>> dt.to_native('2021-05-28T23:39:30.989377')
  datetime.datetime(2021, 5, 28, 23, 39, 30, 989377)

To native and back again. ::

  >>> native_datetime = dt.to_native('2021-05-28T23:39:30.989377')
  >>> dt.to_primitive(native_datetime)
  '2021-05-28T23:39:30.989377'

Records
=======

A Record is a structure consisting of fields, or *named type instances*. ::

  >>> class Artist(types.Record):
  ...     name = types.StringType(required=True)
  ...     website = types.URLType()
  ...     created_at = types.DateTimeType()
  ...
  >>> artist_type = Artist()

A Record is a Type, so it doesnt store data, but knows how to validate it. ::

  >>> artist_data = {
  ...     'name': u'American Food',
  ...     'website': 'http://soundcloud.com/americanfood',
  ...     'created_at': '2021-05-28T23:39:30.989377'
  ... }
  >>> artist_type.validate(artist_data)

Conversion
----------

And it knows how to convert back and forth between native Python types and
values suitable for serialization and sharing with non-Python languages.

  >>> artist_type.to_native(artist_data)
  {'name': 'American Food', 'website': 'http://soundcloud.com/americanfood', 'created_at': datetime.datetime(2021, 5, 28, 23, 39, 30, 989377)}
  >>> artist_type.to_primitive(artist_type.to_native(artist_data))
  {'name': 'American Food', 'website': 'http://soundcloud.com/americanfood', 'created_at': '2021-05-28T23:39:30.989377'}

Filtering
---------

Pushing data through a record with a filter list

  >>> artist_type.to_native(data, filter=['name', 'website'])
  {
      'name': 'American Food',
      'website': 'https://soundcloud.com/americanfood'
  }

Nested Records
--------------

Let's consider a record, that has a list of records, which each contain a list
of records, eg. something messy.

We'll start with a record for a song. ::

  class Song(types.Record):
      name = types.StringType(required=True)
      created_at = types.DateTimeType()
      file = types.UnixPathType()
      lyrics = types.StringType(max_length=255)

An album as a list of songs. ::

  class Album(types.Record):
      name = types.StringType(required=True)
      created_at = types.DateTimeType()
      songs = types.ListType(Song())

And an artist has a list of albums. ::

  class Artist(types.Record):
      name = types.StringType(required=True)
      created_at = types.DateTimeType()
      website = types.URLType()
      albums = types.ListType(Album())

Make an artist type instance. ::

  >>> artist_type = Artist()

Structure some example data and validate it. ::

  >>> artist_data = {
  ...     'name': 'American Food',
  ...     'created_at': '2021-05-29T00:00:01.001337',
  ...     'albums': [{
  ...         'name': 'Internet On The TV',
  ...         'created_at': '2021-05-29T00:00:01.001337',
  ...         'songs': [{
  ...             'name': 'Cane Spiders (mispoke)',
  ...             'created_at': '2021-05-29T00:00:00.001337',
  ...             'lyrics': 'Oh my gawd! It\'s that red dot! Gonna catch that...'
  ...         }, {
  ...             'name': 'My Take On Take On Me',
  ...             'created_at': '2021-05-30T00:00:00.001337',
  ...             'lyrics': 'I know. I know. I talk in numbers...'
  ...         }]
  ...     }]
  ... }
  >>> artist_type.validate(artist_data)

Dot syntax is used for listing fields in nested records. ::

  >>> fields = ['name', 'albums.songs.name', 'albums.songs.created_at']
  >>> some_type.to_primitive(data, fields=fields)
  {
      'name': 'American Food',
      'albums': [
          'songs': [{
              'name': 'Cane Spiders (mispoke)',
              'created_at': '2021-05-29T00:00:00.001337',
          }, {
              'name': 'My Take On Take On Me',
              'created_at': '2021-05-30T00:00:00.001337',
          }]
      ]
  }

Views
=====

A View is a mutable, configurable structure that stores Record data. Views
behave the way classes usually behave in Python, letting Types focus on the
definition and configuration of data structures. ::

  >>> from typerighter import views
  >>> artist_view = views.to_view(artist_type)

Working with a view looks about the same as if it were any Python class. ::

  >>> artist_view.name = 'American Food'
  >>> artist_view.website = 'https://soundcloud.com/americanfood/my-take-on-take-on-me'
  >>> artist_view.created_at = '2021-05-28T23:39:30.989377'

It also knows how to validate data, but assumes it validates itself. ::

  >>> artist_view.validate()

It also knows how to serialize the data it stores. ::

  >>> artist_view.to_native()
