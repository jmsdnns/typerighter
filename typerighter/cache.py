import inspect
import importlib

from .exceptions import CacheMissException, UncachableException


class CacheMeta(type):
    """A metaclass for turning objects into singletons. Intended for use only
    with the `TypeCache`.
    """
    _instances = {}

    def __call__(cls, *a, **kw):
        if cls not in cls._instances:
            cls._instances[cls] = super(CacheMeta, cls).__call__(*a, **kw)
        return cls._instances[cls]


class TypeCache(object, metaclass=CacheMeta):
    """A store for every type defined inside some project. This store caches
    the classes that define types, but does not store any type instances.

    This cache is primarily useful to those who need scaffolding for types
    defined across multiple libraries.
    """
    def __init__(self):
        self._cache = {}

    def __str__(self):
        return repr(self)

    def items(self):
        return self._cache.items()

    def keys(self):
        return self._cache.keys()

    def get(self, name):
        if name in self._cache:
            return self._cache[name]
        else:
            err_msg = "Cache miss for type: %s" % (name)
            raise CacheMissException(err_msg)

    def add(self, item):
        type_name = item.__name__
        
        if not inspect.isclass(item):
            return False
        
        # By storing the first added `Type` as `_basetype`, we leverage the
        # convenience of `Type` being defined immediately after the first
        # metaclass to use `TypeCache`.
        #
        # As a result, we have access to `Type` without a circular import
        # error.
        if not hasattr(self, '_basetype'):
            self._basetype = item

        if self.cacheable(item):
            self._cache[type_name] = item
        else:
            err_msg = "Type not cachable: %s" % (type_name)
            raise UncachableException(err_msg)

    def cacheable(self, item):
        if not inspect.isclass(item):
            return False

        if issubclass(item, self._basetype):
            return True

        return False
