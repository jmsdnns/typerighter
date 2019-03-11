import inspect

from typerighter import types


class Field(object):
    """A descriptor used to join a mutable View instance, that stores data,
    with the immutable Type instance, that only defines methods for operating
    on data.
    """
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if self.name in instance._data:
            return instance._data[self.name]
        return None

    def __set__(self, instance, value):
        instance._data[self.name] = value

    def __delete__(self, instance):
        del instance._data[self.name]


class View(object):
    """A View combines a `Record` with a dictionary to provide an object
    modeled after the record that can store data in a familiar object oriented
    manner.
    """
    def __init__(self, record, data=None):
        self._record = record
        self._data = data

    def to_primitive(self, **convert_args):
        return self._record.to_primitive(self._data, **convert_args)

    def to_native(self, **convert_args):
        return self._record.to_native(self._data, **convert_args)

    def validate(self):
        return self._record.validate(self._data)

    def __iter__(self):
        for k,v in self._data.items():
            if v is not types.Unset:
                yield k,v

    def __getattr__(self, name):
        if hasattr(self._record, name):
            return getattr(self._record, name)


def make_view(record, data=None):
    """Takes both a record and some data and produces View instance.

    :param Type record: The type that defines the view's shape
    :param dict data: Any initial data for the view's fields
    """
    if not data:
        data = {}

    # Wrap each field of the record in a `Field` instance
    attrs = {}
    for field_name, _ in record:
        attr = Field(field_name)
        attrs[field_name] = attr

    # Collect any factory setters
    for name in dir(record):
        if name.startswith('set_'):
            attr = getattr(record.__class__, name)
            attrs[name] = attr

    view_cls_name = '%sView' % (record.__class__.__name__)

    # Instantiate a View definition with the new fields
    RecordView = type(view_cls_name, (View,), attrs)

    return RecordView(record, data=data)

