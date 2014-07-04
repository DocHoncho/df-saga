#! python3
from saga.util.io import open_cp437
from saga.parsers.legends import LegendsParser

def bootstrap(fn):
    t = LegendsParser()
    with open_cp437(fn) as inf:
        d = t.parse(inf)

    return d

def proc(x, n=0):
    head, *rest = x
    if type(rest) == list and len(rest) > 0:
        rest  = rest[0]
    print("{}: h:{} r:{}".format(n, head, rest))
    if rest:
        if type(rest) == str:
            return x

        return proc(rest, n+1)

if __name__ == '__main__':
    import json
    data = ('entities',
            ('entity',
                ('id', '1'),
                ('name', 'wakka wakka wakka')),
            ('entity',
                ('id', '2')),
            ('entity',
                ('id', '3'),
                ('name', 'Blorrt')))

    ree = { 'entity': [
        {'id': '1', 'name': 'wakka wakka wakka'},
        {'id': '2'},
        {'id': '3', 'name': 'Blorrt'}
        ]}
    proc(data)
