.. typerighter documentation master file

===========
Typerighter
===========

.. rubric:: Data Types for Cynical Humans.

Welcome to Typerighter, a project that makes it easy to structure and process
data using concepts from type systems.


Example
=======

A Type. ::

  >>> st = types.StringType(max_length=12)

A Record. ::

  >>> class Artist(types.Record):
  ...     name = types.StringType(required=True)
  ...     website = types.URLType()
  ...
  >>> artist_type = Artist()

Validate data. ::

  >>> data = 'Take Five'
  >>> st.validate(data)
  >>>
  >>> data = {
  ...     'name': u'American Food',
  ...     'website': 'http://soundcloud.com/americanfood'
  ... })
  >>> artist_type.validate(data)


Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   Intro <self>
   installation
   quickstart


.. toctree::
   :maxdepth: 2
   :caption: API Guide

   api/index.rst


.. toctree::
   :maxdepth: 2
   :caption: Development Guide

   developing/index.rst


.. toctree::
   :maxdepth: 2
   :caption: Additional Notes

   notes/contributing
   notes/license
