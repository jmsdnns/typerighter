.. types_primitives

==========
Primitives
==========

Primitive Types represent the types that are found all over the Internet, like
in JSON, and implements the basics:

* `bool`
* `str`
* `int`
* `float`.

Here is a boolean validator. ::

  >>> true_or_false = types.BooleanType()
  >>> true_or_false.validate(True)
  True
  >>> true_or_false.validate(1)
  True
  >>> true_or_false.validate("")
  False

Here is an integer validator. ::

  >>> int_type = types.IntegerType()
  >>> int_type.validate(123)
  >>> int_type.validate("foo")
  ...
  typerighter.exceptions.ValidationException: Value doesnt match type format foo
  

.. automodule:: typerighter.types.primitives
   :members:
