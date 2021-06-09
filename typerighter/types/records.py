
from collections import OrderedDict

from . import base
from .. import cache
from .. import schematics
from .. import views


class RecordMeta(base.TypeMeta):
    def __new__(mcs, name, bases, namespace):
        # attribute accumulators
        fields = OrderedDict()
        field_functions = OrderedDict()
        validate_functions = OrderedDict()

        # gather values from base classes
        for b in reversed(bases):
            if hasattr(b, '_fields'):
                fields.update(b._fields)

            if hasattr(b, '_field_functions'):
                field_functions.update(b._field_functions)

            if hasattr(b, '_validate_functions'):
                validate_functions.update(b._validate_functions)

        # gather typerighter attributes
        for k, v in namespace.items():
            # collect type instances in fields dict
            if isinstance(v, base.Type):
                fields[k] = v

            # collect functions that generate fields
            elif k.startswith('field_') and callable(v):
                field_name = k[len('field_'):]
                field_functions[field_name] = v

            # collect validation functions
            elif k.startswith('validate_') and callable(v):
                validate_functions[k] = v

        # attach collected values
        namespace['_fields'] = fields
        namespace['_field_functions'] = field_functions
        namespace['_validate_functions'] = validate_functions

        # create the new type
        type_class = type.__new__(mcs, name, bases, namespace)

        # create schematic for type
        schematic = schematics.Schematic(type_class)
        setattr(type_class, '_schematic', schematic)

        # put type in cache
        cache.TypeCache().add(type_class)

        return type_class


class Record(base.Type, metaclass=RecordMeta):
    NATIVE = dict

    def __init__(
        self, strict=False, field_filters=None, export_nones=False, **kw
    ):
        super().__init__(**kw)
        self.strict = strict
        self.field_filters = field_filters
        self.export_nones = export_nones

    def __iter__(self):
        for field_name, type_instance in self._fields.items():
            yield field_name, type_instance

    def _filter(self, value, fields=None):
        """
        A generator for iterating across the types embedded in the record.

        Fields can be filtered by providing a list of strings to the ``fields``
        keyword arg.
        """
        for field_name, field_type in self:
            if fields and len(fields) > 0 and field_name in fields:
                if field_name in value or field_type.default:
                    yield field_name, field_type
            elif fields is None:
                if field_name in value or field_type.default:
                    yield field_name, field_type

    def _parse_field_list(self, fields):
        """
        Takes a list of strings that represent fields or nested fields and
        parsed them into two structures, a list of all the fields intended for
        this record, and a dict represented nested records and fields intended
        for the next recursive iteration.

        More simply, a structure like this:

          fields = ['name', 'hobby.name', 'hobby.started_at']

        Would return a structure like this:

          {'name': None, 'hobby': ['name', 'started_at']}

        The caller can then look for the name field when it works on the nested
        record named ``hobby``.

        The values are intended to be passed directly into the conversion
        function, including ``None``, which indicates no filtering is used.
        """
        subfield_map = {}

        if not fields:
            return (None, subfield_map)

        if fields:
            for f in fields:
                record_path = f.split(".")
                x, xs = record_path[0], '.'.join(record_path[1:])
                if len(xs) > 0:
                    if x not in subfield_map:
                        subfield_map[x] = []
                    subfield_map[x].append(xs)
                else:
                    subfield_map[x] = None

        top_level_fields = subfield_map.keys() or None
        return (top_level_fields, subfield_map)

    def _convert(self, value, converter, fields=None):
        """
        Converts all the fields in a record, using the converter function, and
        returns a dictionary of field names and values.

        Supports using a list of fields to filter which are included in the
        output structure.
        """
        top_level_fields, subfield_map = self._parse_field_list(fields)

        for fn, ti in self._filter(value, fields=top_level_fields):
            if fn in value:
                subfields = None
                if fn in subfield_map and subfield_map[fn]:
                    subfields = subfield_map[fn]
                    v = converter(value[fn], ti, fields=subfields)
                else:
                    v = converter(value[fn], ti)
                yield fn, v
            elif ti.default is not base.Unset:
                yield fn, ti.default

    @base.skip_falsy
    def to_primitive(self, value, **convert_args):
        converter = lambda value, ti, **kw: ti.to_primitive(value, **kw)
        return {
            k: v for k, v in self._convert(value, converter, **convert_args)
        }

    @base.skip_falsy
    def to_native(self, value, **convert_args):
        converter = lambda value, ti, **kw: ti.to_native(value, **kw)
        return {
            k: v for k, v in self._convert(value, converter, **convert_args)
        }

    def to_view(self, data=None, **view_config):
        return views.to_view(self, data=data, **view_config)

    @base.skip_falsy
    def validate_fields(self, value):
        for fn, ti in self:
            if fn in value:
                ti.validate(value[fn])
            else:
                ti.validate(base.Unset)
