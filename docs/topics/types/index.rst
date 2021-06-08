.. topics_types_index

===========
Types Guide
===========

The atomic unit of TypeRighter is the ``Type``.

A `Type` is an object that can validate data and convert it from the basic
types used across the Internet, which we call "primitives", and convert it to
the usual native types we'd use in Python.

It uses a metaclass to process `Type` implementations. This metaclass looks for
any functions that start with `validate_` and it puts them in a list of
functions that get called whenever validation occurs. This makes creating new
types easy and keeps the complexity of the framework driving it out of view,
much like the way a car's engine hides behind a steering wheel and pedals.

The classes implemented here are built around the metaprogramming and the way
it accumulates a list of validation functions, including across subclasses.

.. toctree::
   :maxdepth: 2

   base
   primitive
   record
   composite
   timekeeping
   net
   spatial
   cryptography
