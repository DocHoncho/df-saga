import re
from saga.util.collections import Collector

__all__ = ['as_dict', 'regexp', 'dictify']

def as_dict(keys, vals, base=None):
    if base is None:
        base = {}

    base.update(zip(keys, vals))

    return base


def regexp(pattern, flags=None):
    return re.compile(pattern, flags or 0)


def dictify(arg):
    if type(arg) == str:
        return arg

    try:
        head, tail = arg

    except ValueError:
        # Nothing to do, just return argument
        return arg

    if type(tail) == list:
        # List of items. process each one
        # into the collector dict
        data = Collector()
        for item in tail:
            key, val = dictify(item)
            data[key] = val
        return (head, data)

    elif type(tail) == str:
        # terminal case, return input argument
        return (head, tail)

    elif tail is None:
        # Occurs on empty tags
        return arg

    else:
        # General case, recurse and return result
        res = dictify(tail)
        return (head, res)


