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
    def __init__(self, record, data=None, native=True, primitive=False):
        self._record = record
        self._config = {}

        if primitive:
            self._config['primitive'] = True
            self._data = self._record.to_primitive(data)
        elif native:
            self._config['native'] = True
            self._data = self._record.to_native(data)
        else:
            self._data = data

    def to_primitive(self, **convert_args):
        return self._record.to_primitive(self._data, **convert_args)

    def to_native(self, **convert_args):
        return self._record.to_native(self._data, **convert_args)

    def validate(self):
        return self._record.validate(self._data)

    def __iter__(self):
        for k, v in self._data.items():
            if v is not types.Unset:
                yield k, v

    def __getattr__(self, name):
        if hasattr(self._record, name):
            return getattr(self._record, name)


def to_view(record, data=None, **view_config):
    """Takes both a record and some data and produces View instance.

    :param Type record: The type that defines the view's shape
    :param dict data: Any initial data for the view's fields
    """
    if not data:
        data = {}

    # Wrap each field of the record in a `Field` instance
    attrs = {}
    for field_name, field_type in record:
        # All fields in the record are at least a View instance
        field = Field(field_name)

        # Records recurse to create RecordView instances instead
        if isinstance(field_type, types.Record):
            field = to_view(field_type, data[field_name])

        # Pair field with a name
        attrs[field_name] = field

    # Collect any factory setters
    for name in dir(record):
        if name.startswith('set_'):
            attr = getattr(record.__class__, name)
            attrs[name] = attr

    # Normalize class name
    view_cls_name = '%sView' % (record.__class__.__name__)

    # Instantiate a View definition with the new fields
    RecordView = type(view_cls_name, (View,), attrs)

    return RecordView(record, data=data, **view_config)
