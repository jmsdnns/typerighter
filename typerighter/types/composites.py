from . import primitives
from . import domains
from .. import exceptions


class SumType(primitives.Primitive):
    """
    Some languages call this a *Union Type*. The idea is to allow validation
    to pass if just one validator, from a list of two or more types, accepts
    it.
    """
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
        variant_schematics = list()
        for t in self.types:
            schematic = t.to_schematic()
            variant_schematics.append(schematic)
        return (self.__class__.__name__, variant_schematics)

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
    """
    A `Container` is a foundational type, like `Primitive`, that allows some
    number of things to be held in a group, with no additional type checking
    past what a `Primitive` does.

    New composite types should subclass this base type. It is not meant to be
    used directly.
    """
    def __init__(self, type, max_length=None, min_length=None, **kw):
        super().__init__(**kw)
        self.type = type
        domains.LengthDomain(self, max_length, min_length)

    def is_falsy(self, value):
        if value is None or super().is_falsy(value):
            return True

        # If calling len works, it's iterable
        try:
            if len(value) > 0:
                return False
        except Exception:
            pass

        return True

    def validate_items(self, value):
        err_msg = "Container is an abstract type %s"
        raise exceptions.ValidationException(err_msg % (self.type))


class ListType(Container):
    """
    A `ListType` is a `Container` implemented with a `list`.
    """
    NATIVE = list

    def to_schematic(self):
        variant_schematics = list()
        for t in self.types:
            schematic = t.to_schematic()
            variant_schematics.append(schematic)
        return (self.__class__.__name__, variant_schematics)

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
