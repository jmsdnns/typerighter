.. developing_architecture

============
Architecture
============

TypeRighter is a toolkit for structuring, validating, and reshaping data.

Using the toolkit means using one or more of the following things:

+ :code:`Type`: a classification of some data which describes how to verify arbitrary
  data for coherence.
+ :code:`Record`: a structure of data that has type instances, called _fields_, for
  attributes.
+ :code:`Schematic`: the map of arguments used to instantiate either a :code:`Type` or a
  :code:`Record`.
+ :code:`View`: a class that let's you interact with a :code:`Record` and some data as
  though it were an object instance.


Metaprogramming
===============

The design of both :code:`Type` and :code:`Record` relies on metaprogramming to
collect information about the way you choose to use them.

Generally speaking, metaprogramming is a way for programs to treat code like
data. We can read, generate, analyze, or transform code, or modify it while
running.

More specifically, TypeRighter can inspect the attributes and functions on any
type at the moment a user creates one. This allows it to:

+ make lists of all member variables
+ make a list of all functions that start with `someprefix_`

And with that metadata users can:

+ map out the steps for complex data validation
+ generate a SQL statement automatically
+ easily define datatype conversion pipelines


Attributes
==========

All :code:`Type` and :code:`Record` definitions have values for:

+ :code:`_validate_functions`
+ :code:`_schematic`

Records use two extra fields:

+ :code:`_fields`
+ :code:`_field_functions`


Types
-----

A type's :code:`validate()` function will call each function listed in
:code:`_validate_functions` on its input.

The metaclass can be told about new validation functions by adding functions
with :code:`validate_` as a prefix, ie. :code:`validate_uppercase`.

::

    class StrictStringType(StringType):
        def validate_strict(self, value):
            ...

Records
-------

Records introduce the concept of a field by associating a name with a type. It
adds two fields of metadata to the class definition.

Let's define a record with a string stored as field :code:`s`.

::

    class Foo(Record):
        s = StringType(required=True)

Fields defined like this are stored as :code:`_fields`.

It is also possible to use a function to generate field values.

::

    class Foo(Record):
        def field_s(self):
            return 'an actual string'

Functions that behave like fields have a prefix :code:`field_`, similar to the
behavior for validation functions. This field is stored as
:code:`_field_functions`.
