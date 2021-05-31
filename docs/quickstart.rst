.. quickstart

==========
Quickstart
==========

Types
=======

This is a simple type, a `StringType`. ::

  >>> st = types.StringType(max_length=12)

A Type doesn't store data, but it knows how to validate it. ::

  >>> st.validate('short enough')

Here is a slightly more complicated `DateTimeType`. ::

  >>> import datetime
  >>> dt = types.DateTimeType()
  >>> dt.to_primitive(datetime.datetime.now())
  '2021-05-28T23:39:30.989377'
  >>> dt.to_native('2021-05-28T23:39:30.989377')
  datetime.datetime(2021, 5, 28, 23, 39, 30, 989377)

Here is an email address, using the `EmailType`. ::

  >>> et = types.EmailType()
  >>> et.validate('foo@gmail.com')
  >>> et.validate('not an email')
  ...
  typerighter.exceptions.ValidationException: EmailType regex rejected value: not an email


Errors
------

Exceptions are specific about errors ::

  >>> st.validate('not short enough')
  ...
  typerighter.exceptions.ValidationException: Value length above max: short enoughhhh > 12

Records
=======

A Record is a structure consisting of fields, or *named type instances*. ::

  >>> from typerighter import types
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

And it knows how to convert back and forth between native Python types and
values suitable for serialization and sharing with non-Python languages.

  >>> data = {
  ...     'name': u'American Food',
  ...     'website': 'http://soundcloud.com/americanfood',
  ...     'created_at': '2021-05-28T23:39:30.989377'
  ... }
  >>> artist_type.to_native(artist_data)
  {'name': 'American Food', 'website': 'http://soundcloud.com/americanfood', 'created_at': datetime.datetime(2021, 5, 28, 23, 39, 30, 989377)}
  >>> artist_type.to_primitive(artist_type.to_native(artist_data))
  {'name': 'American Food', 'website': 'http://soundcloud.com/americanfood', 'created_at': '2021-05-28T23:39:30.989377'}


Views
=====

A View is a mutable, configurable structure that stores Record data. Views
behave the way classes usually behave in Python, letting Types focus on the
definition and configuration of data structures. ::

  >>> from typerighter import views
  >>> artist_view = views.to_view(artist_type)
  >>> artist_view.name = 'American Food'
  >>> artist_view.website = 'https://soundcloud.com/americanfood/my-take-on-take-on-me'
  >>> artist_view.created_at = '2021-05-28T23:39:30.989377'

It also knows how to validate data, but assumes it validates itself. ::

  >>> artist_view.validate()

It also knows how to serialize the data it stores. ::

  >>> artist_view.to_native()
