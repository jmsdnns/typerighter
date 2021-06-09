.. types_records

=======
Records
=======

Records are a definition of a data structure that consists of one or more
named types, eg. fields.

  >>> class SomeRecord(types.Record):
  ...     name = types.StringType()
  ...     date = types.DateTimeType()
  ...
  >>> sr = SomeRecord()
  >>> sr.validate({'name': 'Jms Dnns', 'date': '2021-04-01T12:34:56.001337'})


.. automodule:: typerighter.types.records
   :members:
   :inherited-members:
