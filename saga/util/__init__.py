import re

__all__ = ['as_dict', 'regexp']

def as_dict(keys, vals, base=None):
    if base is None:
        base = {}

    base.update(zip(keys, vals))

    return base


def regexp(pattern, flags=None):
    return re.compile(pattern, flags or 0)
