#!/bin/env python3
import codecs
from contextlib import contextmanager
from saga.parsers.world import WorldSitesAndPopsParser, WorldHistoryParser

from lxml import objectify

class BufferedIterator:
    def __init__(self, iterable):
        self.buf = []
        self._iterable = iterable


    def __iter__(self):
        return  self


    def __next__(self):
        if len(self.buf) > 0:
            t = self.buf[0]
            self.buf = self.buf[1:]
            self.current_item = t
        else:
            self.current_item = next(self._iterable)

        return self.current_item


    def cancel(self):
        self.buf.append(self.current_item)


    def current(self):
        return self.current_item

# I'm having a hard time believing it would be so simple
# Thanks, lxml.objectify!  You're swell!
def parse_legends(root, func=dict):
    data = {}

    def f(elem, func):
        d = list((f(child, func) for child in elem.iterchildren()))

        try:
            r =  func(d) or (elem.tag, elem.text)

        # ValueError should be thrown by func when it cannot process the data given to it
        # In the default case, dict throws an error when passed a list of other dicts, which
        # indicates that all items in the original root have been processed.
        except ValueError:
            return d

        return r

    return dict(( (item.tag, f(item, func)) for item in root.findall('./') ))

@contextmanager
def open_cp437(fn, mode='r'):
    with codecs.open(fn, mode, 'cp437') as inf:
        yield inf

if __name__ == '__main__':
    import json
    import sys

    import os

    def usage():
        print('Usage: {} <filename> <format:worldsites|worldhistory|legends>'.format(sys.argv[0]))
        sys.exit(2)

    try:
        in_fn = sys.argv[1]
        fmt = sys.argv[2]
    except IndexError:
        usage()

    if not os.path.exists(in_fn):
        print('File `{}` does not exist!'.format(in_fn))
        sys.exit(3)

    with open_cp437(in_fn) as inf:
        if fmt == 'worldsites':
            rdr = BufferedIterator(enumerate(inf))
            parser = WorldSitesAndPopsParser()
            data = parser.parse(rdr)
        elif fmt == 'worldhistory':
            rdr = BufferedIterator(enumerate(inf))
            parser=WorldHistoryParser()
            data = parser.parse(rdr)
        elif fmt == 'legends':
            root = objectify.parse(inf)
            data = parse_legends(root)
        else:
            usage()

#    print(data)
    print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
