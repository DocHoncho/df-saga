#!/bin/env python3
import codecs
import functools
import re
from contextlib import contextmanager

def regexp(pattern, flags=None):
    return re.compile(pattern, flags or 0)

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
            return t
        else:
            return next(self._iterable)

    def peek(self):
        try:
            t = next(self._iterable)
            self.buf.append(t)
            return t
        except StopIteration:
            return None

class StopParser(Exception):
    def __init__(self, msg=None):
        super(StopParser, self).__init__('StopParser: {}'.format(msg or ''))

def parser_event_handler(f):
    @wraps(f)
    def wrapper(obj, line, data=None, context=None):
        context = context or []
        data = data or []

class BaseParser:
    def __init__(self, data_handlers=None, discard_blank_lines=True):
        self.discard_blank_lines = discard_blank_lines

        self.data_handlers = data_handlers or []

    def add_handler(self, name, pattern, func):
        # Compile pattern if it isn't already
        if not hasattr(pattern, 'search'):
            pattern = re.compile(pattern)

        self.data_handlers.append((name, pattern, func))

    def parse(self, obj):
        done = False
        data = []
        context = {}

        while not done:
            try:
                line = next(obj)
                if self.discard_blank_lines and line.strip() == '':
                    continue

                for n, p, f in self.data_handlers:
                    res = p.search(line)
                    if res:
                        print(n, res.groups())
                        res = f(obj, line, res, context)
            except StopIteration:
                done = True
                continue
            except StopParser:
                done = True
                continue

        return data

    def default_handler(self, obj, line, data=None, context=None):
        pass


    def end_parse(self, obj, line, data=None, context=None):
        raise StopParser()

def as_dict(keys, vals, base=None):
    if base is None:
        base = {}

    base.update(zip(keys, vals))

    return base

population_dict = functools.partial(as_dict, ('count', 'type'))

class PopulationListParser(BaseParser):
    def __init__(self):
        super(PopulationListParser, self).__init__()
        self.add_handler('default', r'^\t(\d+) (\s+)$', self.default_handler )
        self.add_handler('end', r'^[^\t].*', self.end_parse)

    def default_handler(self, obj, line, data=None, context=None):



    def parse_line(self, line):
        if line[0] != '\t':
            return None

        res = self.data_re.search(line)
        if res:
            return 'data', population_dict( res.groups())

@contextmanager
def open_cp437(fn, mode='r'):
    with codecs.open(fn, mode, 'cp437') as inf:
        yield inf

if __name__ == '__main__':
    parsers = [
            (regexp(r'^Civilized World Population'), PopulationListParser()),
            ]

    with open_cp437('data/world_sites_and_pops.txt') as inf:
        rdr = BufferedIterator(inf)

        for i, line in enumerate(rdr):
            for start_pat, handler in parsers:
               res = start_pat.search(line)
               if res:
                   d = handler.parse(rdr)
                   print(d)

