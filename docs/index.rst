.. typerighter documentation master file

===========
TypeRighter
===========

.. rubric:: Data Types for Cynical Humans.

Welcome to TypeRighter, a project that makes it easy to structure and process
data using concepts from type systems.


Overview
========

We start with _types_. A lot has been said about this concept and folks
sometimes have different mental models for what one is.

This library defines it as something that can audit some data for coherence. We
can take this further too, for some helpful tooling, but we start with this
simple foundation.

For this library, a _type_ is essentially something with a validation function.

From there, we create structures of data by using associating names with types
in a _record_.

We then use some of the builtin functions to convert, filter, and repackage
various messes of data that may or may not resemble the messes typical of
working with data.

Types
-----

A *Type* is a definition of some data, including functions that know how to
validate the boundaries of when data is too messy to accept. ::

  >>> from typerighter import types
  >>> short_string = types.StringType(max_length=12)

Types dont store data themselves. They only describe how to validate it,
convert it to a native Python representation, or convert it to a
representation that can be easily parsed by simple serialization systems,
like JSON. ::

  >>> short_string.validate('Take Five')
  >>> 
  >>> short_string.validate('Took too many Fives!')
  ...
  typerighter.exceptions.ValidationException: Value length above max: Took too many fives > 12

Records
-------

A *Record* is special kind of type used to store multiple values. ::

  >>> class Artist(types.Record):
  ...     name = types.StringType(required=True)
  ...     website = types.URLType()
  ...     created_at = types.DateTimeType()
  ...
  >>> artist_type = Artist()

We can validate data, because Records are Types too. ::

  >>> data = {
  ...     'name': u'American Food',
  ...     'website': 'https://soundcloud.com/americanfood',
  ...     'created_at': '2016-04-01T12:34:56.001337'
  ... }
  >>> artist_type.validate(data)

Converting Data
---------------

We can use the *DateTimeType* to convert a value from a string to a
*datetime.datetime* and back. ::

  >>> dt = types.DateTimeType()
  >>> dt.to_native('2016-04-01T12:34:56.001337')
  datetime.datetime(2016, 4, 1, 12, 34, 56, 1337)
  >>> dt.to_primitive(datetime.datetime(2016, 4, 1, 12, 34, 56, 1337))
  '2016-04-01T12:34:56.001337'

And because Records are Types, they give us a way to convert large structures
of data too (*with lots of options for handling complexity*). ::

  >>> artist_type.to_native()
  {
      'name': 'American Food',
      'website': 'https://soundcloud.com/americanfood',
      'created_at': datetime.datetime(2016, 4, 1, 12, 34, 56, 1337)
  }

Data Filtering
--------------

Pushing data through a record with a filter list

  >>> artist_type.to_native(data, filter=['name', 'website'])
  {
      'name': 'American Food',
      'website': 'https://soundcloud.com/americanfood'
  }

And roughly the same idea with a view

  >>> artist.to_native(filter=['name', 'website'])
  {
      'name': 'American Food',
      'website': 'https://soundcloud.com/americanfood'
  }

Messy Structures
----------------

  >>> class 

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   Intro <self>
   installation
   quickstart


.. toctree::
   :maxdepth: 2
   :caption: Topics

   topics/types/index
   topics/views
   topics/schematics
   topics/project

.. toctree::
   :maxdepth: 2
   :caption: Cookbook

   cookbook/json_api

.. toctree::
   :maxdepth: 2
   :caption: Contributing

   contributing/environment
   contributing/testing
   contributing/docs


.. toctree::
   :maxdepth: 2
   :caption: Additional Notes

   notes/license
