
class Import(object):
    def __init__(self, mod_name, alias=None, sub_objects=None, parent=None):
        self.mod_name = mod_name
        self.alias = alias or mod_name
        sub_objects = sub_objects or []

    def _run(self):
        # get current pythonpath
        # build full module name
        # search for module in that path
        # parse the module
        # build exports dictionary
        # filter the objects
        # recurse on sub_objects
        return

class Include(object):
    '''
    Wraps information needed for what type of include statement is being made
    '''
    def __init__(self, mod):
        if isinstance(mod, basestring):
            # ex: import_("foo.bar.baz")
            names = mod.split(".")
            self.name = names[0]
            self.alias = mod
            self.sub_objects = [Include(name) for name in names[1:]]
            imports.append(Import(name))
            # from_("foo.bar.baz", ("blob", "blorp"))
        elif isinstance(mod, tuple):
            imports.append(Import(mod_name=name[0],
                                  sub_objects=mod[1:],
                                  parent=parent))

# regular import
# import_("foo.bar.baz", "boz.booz", "qux")

# from import
# from_("foo.bar", import_("baz"))

# aliased import
# import_(as_("foo.bar", "fb"))

def import_(*modules):
    for module in modules:
        if isinstance(module, basestring):
            run_import(module, namespace=_TOP_NAMESPACE)
        elif isinstance(module, tuple):
            run_aliased_import(module[0], module[1], namespace=_TOP_NAMESPACE)

def as_(name, alias):
    return (name, alias)

def from_(mod_name, _import):
    # find the file corresponding to the module name
    # build the ast and inspect it for the imports
    file_to_load(get_file(mod_name))

    pass

def include(*module_names):
    includes = [Include(mod) for mod in module_names]
    for inc in includes:
        Import(inc)._run()

def filter_objects(mod, exports):
    for name in dir(mod):
        if name not in exports:
             obj = globals()[name]
             del globals()[name]
             globals()["__private__" + name] = obj


