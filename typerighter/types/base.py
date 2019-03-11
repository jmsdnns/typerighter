import re
from collections import OrderedDict

from .. import cache
from .. import exceptions
from .. import schematics


class UnsetValue(object):
    """This class exists to put a label on the type of value that represents
    when a field does not _yet_ have a value.
    """
    pass

Unset = UnsetValue() # Module-level Singleton


class TypeMeta(type):
    def __new__(mcs, name, bases, namespace):
        # attribute accumulators
        validate_functions = OrderedDict()

        # gather values from base classes
        for b in reversed(bases):
            if hasattr(b, '_validate_functions'):
                validate_functions.update(b._validate_functions)

        # gather typerighter attributes
        for k, v in namespace.items():
            if k.startswith('validate_') and callable(v):
                validate_functions[k] = v

        # attach collected values
        namespace['_validate_functions'] = validate_functions
    
        # create the new type
        type_class = type.__new__(mcs, name, bases, namespace)

        # create schematic for type
        schematic = schematics.Schematic(type_class)
        setattr(type_class, '_schematic', schematic)

        # put type in cache
        cache.TypeCache().add(type_class)

        return type_class


def skip_falsy(method):
    """A decorator that intercepts method calls to prevent falsy inputs from
    being validated unnecessarily.
    """
    def wrapper(self, value, *a, **kw):
        if self.is_falsy(value):
            return value
        return method(self, value, *a, **kw)
    return wrapper


class Type(object, metaclass=TypeMeta):
    """This class represents the top, and thus most ambiguous, point of the
    Typerighter hierarchy.

    It's purpose is to define the baseline expectations for every other `Type`
    in this library.
    """
    NATIVE = object  # identity function

    def __init__(self, default=Unset, required=False, strict=False):
        """Base initializer for Types. Implements the basic features for Types
        and provides the Type config options, such as setting a default value.

        :param object default: Any value you want to be used as a default inside
        `to_primitive` and `to_native`.
        :param bool required: If `True`, `Unset` values will trigger an exception
        during validation
        :param bool strict: Enforces all values are exactly the right type by
        validating without type coercion.
        """
        self.required = required
        self.strict = strict

        self.default = default
        if default != Unset:
            self.to_primitive = self._apply_default(self.to_primitive)
            self.to_native = self._apply_default(self.to_native)

    def is_falsy(self, value):
        """Checks a value and responds saying whether the `Type` considers it
        falsy.

        :param object value: The value to inspect
        :return: True or False
        """
        if value == Unset or value == None:
            return True
        return False

    def is_coercible(self, value):
        """Checks a value for whether or not it can be converted to the correct
        type. Falls back to the stricter `is_type_match` if `self.strict` is
        True.

        :param object value: The value to inspect
        """
        if self.strict:
            return self.is_type_match(value)
        try:
            self.to_native(value)
            return True
        except:
            return False

    def is_type_match(self, value):
        """Checks if a value is an instance of this Type's native type.
        :param object value: The value to inspect
        """
        return isinstance(value, self.NATIVE)

    def to_schematic(self):
        """Returns a Type's Schematic
        """
        return (self.__class__.__name__, self._schematic.init_args)

    def _apply_default(self, method):
        def wrapper(value, *a, **kw):
            if value == Unset and self.default != Unset:
                return self.default
            return method(value, *a, **kw)
        return wrapper

    def to_primitive(self, value):
        """Converts a value to the primitive form of this type

        :param object value: The value to convert
        """
        return value

    def to_native(self, value):
        """Converts a value to the native form of this type

        :param object value: The value to convert
        """
        if self.is_falsy(value):
            return value
        
        if self.NATIVE != object:
            return self.NATIVE(value)

        return value

    def validate(self, value):
        """This validation function is the primary function responsible for
        calling all associated validators and for managing any details
        related to aggregation of validation results.

        :param object value: The value to convert
        """
        self._validate_required(value)
        self._validate_type_match(value)

        native = self.to_native(value)

        for func in self._validate_functions.values():
            func(self, native)

    def _validate_required(self, value):
        if self.required and value == Unset:
            e_msg = "Value required but not found"
            raise exceptions.ValidationException(e_msg)

    @skip_falsy
    def _validate_type_match(self, value):
        if self.strict and self.is_type_match(value):
            return
        elif self.is_coercible(value):
            return
        e_msg = "Value doesnt match type format {}".format(value)
        raise exceptions.ValidationException(e_msg)

    def __setattr__(self, name, value):
        """This method makes it impossible to overwrite any attributes
        that are subclasses of `Type`.
        """
        propobj = getattr(self.__class__, name, None)
        if propobj and isinstance(propobj, Type):
            return
        super().__setattr__(name, value)

