import imp
from importlib import import_module
def discover_modules(name, namespace):
    found = []
    for item in namespace:
        print('Trying {}'.format(item))
        try:
            module = import_module(item)
            imp.find_module(name)
            found.append(module)
        except AttributeError:
            pass
        except ImportError:
            pass

        print("Nope, nuffin")

    return found

plugins = [
        'plugins.blah',
        'plugins.boop'
        ]
command_modules = discover_modules('command', plugins)

