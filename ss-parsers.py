#!/bin/env python3
import codecs
from contextlib import contextmanager
from saga.parsers.world import WorldSitesAndPopsParser, WorldHistoryParser

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



@contextmanager
def open_cp437(fn, mode='r'):
    with codecs.open(fn, mode, 'cp437') as inf:
        yield inf

if __name__ == '__main__':
    import json
    import sys

    with open_cp437(sys.argv[1]) as inf:
        rdr = BufferedIterator(enumerate(inf))
        parser = WorldSitesAndPopsParser()
#        parser=WorldHistoryParser()
        data = parser.parse(rdr)

    print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
