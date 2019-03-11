import re
from collections import OrderedDict

from . import base
from . import primitives
from . import domains
from .. import exceptions


class SumType(primitives.Primitive):
    def __init__(self, *types, **kwargs):
        super(SumType, self).__init__(**kwargs)
        self.types = types

    def _find_variant(self, value):
        for t in self.types:
            try:
                t.validate(value)
                return t
            except exceptions.ValidationException:
                pass
        else:
            err_msg = "No matching variant for value: {}"
            raise exceptions.TypeException(err_msg.format(value))
            
    def is_type_match(self, value):
        for t in self.types:
            print(t.is_type_match(value))
            print(isinstance(value, t.NATIVE))
            if t.is_type_match(value):
                return True
        else:
            return False

    def to_schematic(self):
        l = list()
        for t in self.types:
            schematic = t.to_schematic()
            l.append(schematic)
        return (self.__class__.__name__, l)

    def to_primitive(self, value):
        t = self._find_variant(value)
        return t.to_primitive(value)

    def to_native(self, value):
        t = self._find_variant(value)
        return t.to_native(value)

    def validate_by_variant_match(self, value):
        t = self._find_variant(value)
        if not t:
            e_msg = "Value did not pass any type checks: {}"
            raise exceptions.ValidationException(e_msg.format(value))


class Container(primitives.Primitive):
    def __init__(self, type, max_length=None, min_length=None, **kw):
        super().__init__(**kw)
        self.type = type
        domains.LengthDomain(self, max_length, min_length)

    def is_falsy(self, value):
        if value == None or super().is_falsy(value):
            return True

        # If calling len works, it's iterable
        try:
            if len(value) > 0:
                return False
        except:
            pass
    
        return True

    def validate_items(self, value):
        err_msg = "Container is an abstract type %s"
        raise exceptions.ValidationException(err_msg % (self.type))


class ListType(Container):
    NATIVE = list

    def to_schematic(self):
        l = list()
        for t in self.types:
            schematic = t.to_schematic()
            l.append(schematic)
        return (self.__class__.__name__, l)

    def to_primitive(self, value):
        if self.is_falsy(value):
            return value

        return [self.type.to_primitive(v) for v in value]

    def to_native(self, value):
        if self.is_falsy(value):
            return value

        return [self.type.to_native(v) for v in value]

    def validate_items(self, value):
        if self.is_falsy(value):
            return

        for v in value:
            try:
                self.type.validate(v)
                break
            except exceptions.ValidationException:
                pass
        else:
            e_msg = "No types in list match for item {}"
            raise exceptions.ValidationException(e_msg.format(value))
