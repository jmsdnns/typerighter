![Typerighter](art/TypeRighter-bw.png)

Data Types for Cynical Humans

## Overview

Welcome to TypeRighter, a project that wants to make it easier to deal with
data that is messier than we'd prefer.

A user can create *types* or *records* and use those to validate data, convert
it to and from native Python types, or adjust its structure somehow.

TypeRighter is a fundamentally a system for structuring data such that it can
be used inside Python's metaprogramming API.

## Read The Docs

If you are new to TypeRighter, the quickstart guide should be your first stop.

Learn more about it with [our great documentation](https://typerighter.readthedocs.io/en/latest/).

## Example

Define a record with fields and instantiate it.

```
>>> class Artist(types.Record):
...     name = types.StringType(required=True)
...     website = types.URLType()
...     created_at = types.DateTimeType()
...
>>> artist_type = Artist()
```

Validate some data with that record.

```
>>> band_data = {
...     'name': 'American Food',
...     'website': 'https://soundcloud.com/americanfood',
...     'created_at': '2021-05-28T23:39:30.989377'
... })
>>> artist_type.validate(band_data)
```

Get all values back in Python native types for the listed fields.

```
>>> artist_type.to_native(band_data, fields=['name', 'created_at'])
{
    'name': u'American Food',
    'created_at': datetime.datetime(2021, 5, 28, 23, 39, 30, 989377)
}
```
