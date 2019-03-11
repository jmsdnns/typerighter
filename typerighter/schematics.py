"""
"""


from collections import OrderedDict
import inspect


def extract_argspec(klass):
    """Inspects a klass and creates a dict of keyword arguments and their
    default values.

    :param class klass: The class definition to inspect
    :return: a dictionary of default values found in argspec for class's init
    """
    argspec = OrderedDict()

    ka = inspect.getfullargspec(klass.__init__)
    if ka.defaults:
        for keyword, default_value in zip(ka.args[1:], ka.defaults):
            argspec[keyword] = default_value

    return argspec


def init_arg_capture(method):
    """A decorator that wraps a Type's `__init__` method for the purpose of
    capturing the arguments used when a Type is instantiated so it can then
    update the instance's argspec with what was actually used.
    """
    def wrapper(self, *a, **kw):
        method(self, *a, **kw)

        init_args = OrderedDict()
        init_args.update(self._schematic._argspec)
        for k, v in kw.items():
            init_args[k] = v

        self._schematic._init_args = init_args

    return wrapper


class Schematic(object):
    """A Schematic is a object that maintains a Type's argspec. It exists as a
    class to provide a namespace for relevant values.
    """
    def __init__(self, klass):
        """Initialize a Schematic instance with a Typerighter Type instance.

        :param class klass:
        """
        argspec = OrderedDict()

        # aggregate argspec from base classes
        base_classes = inspect.getmro(klass)
        for base in base_classes:
            if hasattr(base, '_schematic'):
                if hasattr(base._schematic, '_argspec'):
                    argspec.update(base._schematic._argspec)

        # add argspec
        k_argspec = extract_argspec(klass)
        argspec.update(k_argspec)
        self._argspec = argspec

        # this decorator must be applied *after* argspec is read
        klass.__init__ = init_arg_capture(klass.__init__)
