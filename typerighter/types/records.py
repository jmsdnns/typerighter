from collections import OrderedDict
import inspect

from . import base
from .. import cache
from .. import exceptions
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
        for field_name, field_type in self:
            # Field name is in fields list and has a value
            if fields and field_name in fields and field_name in value:
                yield field_name, field_type
            # Field name has value
            elif field_name in value:
                yield field_name, field_type
            # Field can provide a value
            elif field_type.default:
                yield field_name, field_type

    def _convert(self, value, converter, fields=None):
        for fn, ti in self._filter(value, fields=fields):
            if fields and fn in fields and fn in value:
                v = converter(value[fn], ti)
                yield fn, v
            elif fn in value:
                v = converter(value[fn], ti)
                yield fn, v
            elif fn not in value and ti.default is not base.Unset:
                yield fn, ti.default
    
    @base.skip_falsy
    def to_primitive(self, value, **convert_args):
        converter = lambda field_value, ti: ti.to_primitive(field_value)
        return {
            fn: ti for fn, ti in self._convert(value, converter, **convert_args)
        }
        
    @base.skip_falsy
    def to_native(self, value, **convert_args):
        converter = lambda field_value, ti: ti.to_native(field_value)
        return {
            fn: ti for fn, ti in self._convert(value, converter, **convert_args)
        }

    def to_view(self, data=None):
        return views.make_view(self, data=data)

    @base.skip_falsy
    def validate_fields(self, value):
        for fn, ti in self:
            if fn in value:
                ti.validate(value[fn])
            else:
                ti.validate(base.Unset)

