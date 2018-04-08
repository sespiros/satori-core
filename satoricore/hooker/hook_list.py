"""The HookList class"""
import inspect
from collections import Iterable


class HookException(Exception):
    """A hook threw up!"""
    pass


class HookList(list):
    """Profesional grade list of hooks. Manages dependcy checking n' shit"""
    # If an extension is loaded before all its dependencies are loaded, put it
    # in this list and try to load it again after loading more extensions
    later = []

    def __call__(self, *args, **kwargs):
        if not self.later:
            raise HookException(
                "Dependencies not met for: %s" %
                ", ".join([x.__name__ + ":" + x.__module__
                           for x in self.later]))

        for func in self:
            print('Calling %s from module %s with args: %s and kwargs: %s' %
                  (func.__name__, func.__module__, args, kwargs))
            # Skip extension if it doens't accept the arguments passed
            try:
                inspect.signature(func).bind(*args, **kwargs)
            except TypeError:
                # TODO: Add logging for skipped extensions
                continue
            func(*args, **kwargs)

    def isloaded(self, name):
        """Checks if given hook module has been loaded"""
        if name is None:
            return True
        if isinstance(name, Iterable):
            return set(name).issubset(self)
        return name in [x.__module__ for x in self]

    def hook(self, function, dependencies=None):
        """Tries to load a hook"""
        if not isinstance(dependencies, (Iterable, type(None), str)):
            raise HookException("Invalid list of dependencies provided!")

        if not hasattr(function, "__deps__"):
            function.__deps__ = dependencies

        if self.isloaded(function.__deps__):
            self.append(function)
        else:
            self.later.append(function)

        for ext in self.later:
            if self.isloaded(ext.__deps__):
                self.later.remove(ext)
                self.hook(ext)
