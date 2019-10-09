.. quickstart

==========
Quickstart
==========

Types
=======

This is a simple Type. ::

  >>> st = types.StringType(max_length=12)

A Type doesn't store data, but it knows how to validate it. ::

  >>> st.validate('short enough')

Errors
------

Exceptions are specific about errors ::

  >>> st.validate('not short enough')
  Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jmsdnns/Projects/typerighter/typerighter/types/base.py", line 90, in validate
      func(self, native)
  File "/home/jmsdnns/Projects/typerighter/typerighter/types/domains.py", line 73, in validate_max_length
      err_msg.format(value, instance.max_length)
  typerighter.exceptions.ValidationException: Value length above max: short enoughhhh > 12

Records
=======

A Record is a structure consisting of fields, or *named type instances*. ::

  >>> from typerighter import types
  >>> class Artist(types.Record):
  ...     name = types.StringType(required=True)
  ...     website = types.URLType()
  ...
  >>> artist_type = Artist()

A Record is a Type, so it doesnt store data, but knows how to validate it. ::

  >>> data = {
  ...     'name': u'American Food',
  ...     'website': 'http://soundcloud.com/americanfood'
  ... })
  >>> artist_type.validate(data)

Views
=====

A View is a mutable, configurable structure that stores Record data. ::

  >>> artist_view = artist_type.make_view(artist)
  >>> artist_view.website = 'https://soundcloud.com/americanfood/my-take-on-take-on-me'

It also knows how to validate data, but assumes it validates itself. ::

  >>> artist_view.validate()
