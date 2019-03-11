.. typerighter documentation master file

===========
Typerighter
===========

.. rubric:: Data Types for Cynical Humans.

Welcome to Typerighter, a project that makes it easy to structure and process
data using concepts from type systems.

Example
=======

This is a simple Type. ::

  >>> st = types.StringType(max_length=12)

A Type doesn't store data, but it knows how to validate it. ::

  >>> st.validate('short enough')

Or ::

  >>> st.validate('not short enough')
  Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/jmsdnns/Projects/typerighter/typerighter/types/base.py", line 90, in validate
      func(self, native)
  File "/home/jmsdnns/Projects/typerighter/typerighter/types/domains.py", line 73, in validate_max_length
      err_msg.format(value, instance.max_length)
  typerighter.exceptions.ValidationException: Value length above max: short enoughhhh > 12

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

A View is a mutable, configurable structure that stores Record data. ::

  >>> artist_view = artist_type.make_view(artist)
  >>> artist_view.website = 'https://soundcloud.com/americanfood/my-take-on-take-on-me'

It also knows how to validate data, but assumes it validates itself. ::

  >>> artist_view.validate()

User's Guide
============

.. toctree::
   :maxdepth: 2

   Intro <self>
   install
   quickstart
   types


Development
===========

We welcome ideas and code.  We ask that you follow some of our guidelines
though.

See the :doc:`development` for more information.

.. toctree::
   :maxdepth: 2

   api
   testing


Everything Else
===============

.. toctree::
   :maxdepth: 2

   license
   contributing
