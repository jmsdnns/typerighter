.. views

==================
Working With Views
==================

Views are mutable structures that store data based on ``Record`` instances.
The field names are the same, except instead of getting type instances for all
the attributes, you get fields that can store and delete data.

In addition to essentially being a *Mutable Record*, a View makes it easy to
drop in place of existing modeling systems, *like maybe, Schematics...*

Views are created with ``Type`` instances, and they can be instantiated with
data. ::

  >>> view = SomeRecord().to_view({'foo': 'bar'})
  >>> view.foo
  'bar'

API
===

.. automodule:: typerighter.views
   :inherited-members:
   :members:
