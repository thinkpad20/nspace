import logging

logger = logging.getLogger(__name__)

class Module(object):
    def __init__(self, module, name):
        self.__mynames__ = set(['__name__', '__hide__',
                                '__mynames__', '__map__',
                                '__hide__', '__export__',
                                '__include__', '__dir__'])
        self.__name__ = name
        self.__map__ = {}
        self.__export__ = set()
        self.__hide__ = set()
        self.__include__(module)

    def __include__(self, module):
        for attr in dir(module):
            if attr in self.__mynames__:
                if attr == '__export__':
                    self.__export__ = set(getattr(module, attr))
                elif attr == '__hide__':
                    self.__hide__ = set(getattr(module, attr))
                elif attr == '__name__':
                    self.__name__ = getattr(module, attr)
                else:
                    raise ValueError("Illegal name `%s` found in module `%s`" %
                                     (attr, self.__name__))
            else:
                self.__map__[attr] = getattr(module, attr)
        export_and_hide = self.__export__.intersection(self.__hide__)
        if len(export_and_hide) > 0:
            raise ValueError("Some names are both hidden and exported: %s" %
                             list(export_and_hide))

    def __getattr__(self, attr):
        if attr == '__mynames__' or attr in self.__mynames__:
            return self.__getattribute__(attr)
        elif attr in self.__hide__:
            raise AttributeError("Attribute `%s` is hidden in module `%s`" %
                                 (attr, self.__name__))
        elif len(self.__export__) > 0 and attr not in self.__export__:
            raise AttributeError("Attribute `%s` is not exported in module `%s`" %
                                 (attr, self.__name__))
        else:
            try:
                return self.__map__[attr]
            except KeyError:
                raise AttributeError("Module `%s` has no attribute "
                                     "`%s`" % (self.__name__, attr))

    def __dir__(self):
        return sorted(list(self.__mynames__) + self.__map__.keys())


def include(mod_name):
    try:
        return Module(__import__(mod_name), mod_name)
    except ImportError:
        # later we'll add code to search in specific paths
        raise
    # Basically in this function we're going to have to do it by hand from
    # the AST up. We're going to need to decide what places we're going to
    # look, then look in each of those places for something with the
    # right name (and/or a `package` declaration that's appropriate), then
    # load that file, parse it into an AST, walk through that AST finding
    # all of the exports, build a table of the things to rename, rename
    # all of the appropriate references, compile the new AST into python
    # objects, and merge all of those objects into a python module object
    # (or in the case of an open import, merge it into the current module).
    # We could have a __package__.py file which records the package
    # information.

def export(func, *args, **kwargs):
    return func
