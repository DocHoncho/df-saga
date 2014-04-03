import json

_Settings_instance = None

_DEFAULT_NAMESPACES = []
def register_namespace(name, namespaces=None, defaults=None, data=None):

    global _DEFAULT_NAMESPACES, _Settings_instance

    _DEFAULT_NAMESPACES.append((name, (namespaces, defaults, data)))

    if _Settings_instance:
        t = _Settings_instance
        t.add_namespace(name, namespaces, defaults, data)


class Settings(object):

    def __init__(self, namespaces=None, defaults=None, data=None, ignore_defaults=False):

        global _DEFAULT_NAMESPACES
        if not ignore_defaults:
            t = dict()
            for name, data in _DEFAULT_NAMESPACES:
                print(name, data)
                t[name] = Settings(data[0], data[1], data[2], ignore_defaults=True)

            self._ns = t
            if namespaces:
                self._ns.update(namespaces)

        else:
            self._ns = dict() if namespaces is None else namespaces

        self._defaults = dict() if defaults is None else defaults
        self._data = dict() if data is None else data


    def add_namespace(self, name, namespaces=None, defaults=None, data=None):
        self._ns[name] = Settings(namespaces, defaults, data)


    def __getitem__(self, key):

        try:
            t, rest = key.split('/', 1)
            if t in self._ns:
                return self._ns[t][rest]
            else:
                raise KeyError("Namespace '%s' does not exist"%(t))

        except AttributeError:
            # Not a string, for now do nothing
            raise KeyError(key)

        except ValueError:
            if key in self._data:
                return self._data[key]
            elif key in self._defaults:
                return self._defaults[key]
            else:
                raise KeyError(key)


    def __setitem__(self, key, value):

        try:
            t, rest = key.split('/', 1)
            if t in self._ns:
                self._ns[t][rest] = value
            else:
                raise KeyError("Namespace '%s' does not exist"%(t))

        except AttributeError:
            # not a string, bad user, bad!
            raise KeyError(key)

        except ValueError:
            # No split performed, we've a single path item left
            self._data[key] = value


    @classmethod
    def from_json(cls, data):
        print(cls, type(data))
        t = Settings({}, data['defaults'], data['data'])
        for key, value in data['namespaces']:
            t.add_hive(key, Settings.from_json(value))

        return t


    def __dict__(self):
        return eval(repr(self))


    def __repr__(self):
        return repr({
                'namespaces': self._ns,
                'defaults': self._defaults,
                'data': self._data
                })


def load_settings(fn, defaults):

    global _Settings_instance
    with open(fn, 'r') as inf:
        try:
            t = json.load(inf)
        except ValueError:
            t = None

    if t is None:
        t = defaults
        with open(fn, 'w') as outf:
            outf.write(json.dumps(t))

    _Settings_instance = t

    return t


def get_settings():
    global _Settings_instance
    if _Settings_instance is None:
        _Settings_instance = Settings()

    return _Settings_instance


if __name__ == '__main__':
    import pprint

    t = Settings()
    t.add_namespace('blah', defaults={'foo':1, 'bar': 2, 'baz': 3})
    x = eval(repr(t))
    pprint.pprint(x)
