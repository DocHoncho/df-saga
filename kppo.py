#! python3
from saga.util.io import open_cp437
from saga.parsers.legends import LegendsParser

def bootstrap(n=0):
    t = LegendsParser()
    with open_cp437('data/worlds/test/legends.xml') as inf:
        d = t.parse(inf)

    return d
data = bootstrap()

def f(k):
    try:
        head, tail = k
    except ValueError:
        return k

    if type(tail) == str:
        return {head: tail}
    elif tail is None:
        return head
    else:
        data = {}
        for item in tail:
            r = f(item)
            items = None

            try:
                items = r.items()
            except AttributeError as e:
                try:
                    data[r] = []
                    items = []
                except TypeError:
                    items = r

            for k, v in items:
                if k in data:
                    try:
                        data[k].append(v)
                    except AttributeError:
                        data[k] = [data[k], v]
                else:
                    data[k] = v

        return {head: data}

import json
with open('foo', 'w') as outf:
    outf.write(json.dumps(f(data), indent=2, separators=(',', ':'), sort_keys=True))

