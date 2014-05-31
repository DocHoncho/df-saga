#!/bin/env python3
import codecs
import functools
import re
from contextlib import contextmanager

def regexp(pattern, flags=None):
    return re.compile(pattern, flags or 0)

def add_item(_dict, key, data):
    try:
        _dict[key].append(data)
    except KeyError:
        _dict[key] = [data]

    return _dict




class BufferedIterator:
    def __init__(self, iterable):
        self.buf = []
        self._iterable = iterable


    def __iter__(self):
        return  self


    def __next__(self):
        #print(self.buf)
        if len(self.buf) > 0:
            t = self.buf[0]
            self.buf = self.buf[1:]
            self.current_item = t

        else:
            self.current_item = next(self._iterable)

        return self.current_item


    def peek(self):
        try:
            t = next(self._iterable)
            self.buf.append(t)
            return t
        except StopIteration:
            raise StopParser(


                    )
    def current(self):
        return self.current_item


class StopParser(Exception):
    def __init__(self, msg=None):
       super(StopParser, self).__init__('StopParser: {}'.format(msg or ''))

def create_simple_handler(data_keys, context_key=None, *, make_list=False):
    make_list = kwargs.get('make_list', False)
    def f(iterable, data, context):
        d = as_dict(data_keys, data)
        if context_key is None:
            context.update(d)
        else:
            if make_list:
                try:
                    context[context_key].append(d)

                except KeyError:
                    context[context_key] = [d]
            else:
                context[context_key] = d

        return d

    return f


def create_parser_handler(data_keys, context_key, parser_class, *, make_list=False):
    def f(iterable, data, context):
        new_context = as_dict(data_keys, dat)
        parser = parser_class()
        result = parser.parse(iterable, [], new_context)
        new_context.update(result)

        if make_list:
            add_item(context, context_key, new_context)
        else:
            context[context_key] = new_context

        return result
    return f


class BaseParser:
    def __init__(self, name, data_handlers=None, discard_blank_lines=True):
        self.name = name
        self.discard_blank_lines = discard_blank_lines
        self.data_handlers = data_handlers or []

    def add_handler(self, name, pattern, func):
        # Compile pattern if it isn't already
        if not hasattr(pattern, 'search'):
            pattern = re.compile(pattern)

        self.data_handlers.append((name, pattern, func))


    def parse(self, iterable, data=None, context=None):
        done = False
        data = data or []
        context = context or {}

        while not done:
            try:
                i, line = iterable.peek()
                line_strip = line.strip()

                if self.discard_blank_lines and line_strip == '':
                    next(iterable)
                    continue

                print('<{}> [{:05d}] `{}`'.format(self.name, i, line_strip), end='')
                for n, p, f in self.data_handlers:
                    res = p.search(line)
                    if res:
                        print(' match `{}`'.format(n), end='')
                        next(iterable)
                        data = list(map(lambda x: x.strip(), res.groups()))
                        f_res = f(iterable, data, context)
                        print(' returned `{}`'.format(f_res))
                        break
                    else:
                        print()

            except StopIteration:
                done = True
                continue

            except StopParser:
                data = context
                done = True
                continue

            except TypeError:
                import pdb; pdb.set_trace()
        return data

    def default_handler(self, iterable, data=None, context=None):
        return


    def end_parse(self, iterable, data=None, context=None):
        print('End {}'.format(self.name))

        raise StopParser()


    def __str__(self):
        return self.name


def as_dict(keys, vals, base=None):
    if base is None:
        base = {}

    base.update(zip(keys, vals))

    return base


class PopulationParser(BaseParser):
    def __init__(self):
        super(PopulationParser, self).__init__('PopulationListParser')
        self.add_handler(
                'default',
                r'^\t(\d+) (.+)$',
                create_simple_handler(('type', 'count'), 'population', make_list=True))
        self.add_handler(
                'total',
                r'\t(Total): (\d+)',
                create_simple_handler(('count', 'type'), 'population', make_list=True))
        self.add_handler('end', r'^[^\t].*', self.end_parse)

class SitesParser(BaseParser):
    def __init__(self):
        super(SitesParser, self).__init__('SitesHandler')
        self.add_handler(
                'header',
                r'^(\d+): ([\w\s]+), "(.*)", (\w+)$',
                create_parser_handler(('id', 'real_name', 'name', type'), 'sites', SiteParser, make_list=True))


class SiteParser(BaseParser):
    def __init__(self):
        super(SiteParser, self).__init__('SiteParser')
        self.add_handler(
                'owner',
                r'^\tOwner: ([\w\s]+), (\w+)$',
                create_simple_handler(('name', 'race'), 'owner'))
        self.add_handler(
                'parent',
                r'^\tParent Civ: ([\w\s]+), (\w+)$',
                create_simple_handler(('name', 'race'), 'parent'))
        self.add_handler(
                'population',
                r'^\t(\d+) (.*)$',
                create_simple_handler(('count', 'type'), 'population', make_list=True))
        self.add_handler('end', r'^[^\t].*', self.end_parse)


class WorldSitesAndPopsParser(BaseParser):
    def __init__(self):
        super(WorldSitesAndPopsParser, self).__init__('WorldSitesAndPops')

        self.add_handler(
            'world_pops',
            r'^Civilized World Population',
            self.population_handler)
        self.add_handler(
            'sites',
            r'^Sites$',
            self.sites_handler)

    def population_handler(self, iterable, data, context):
        p = PopulationParser()
        d = p.parse(iterable, data, {})
        print(d)
        return d

    def sites_handler(self, iterable, data, context):
        p = SitesParser()
        d = p.parse(iterable, data, {})
        print(d)
        return d

@contextmanager
def open_cp437(fn, mode='r'):
    with codecs.open(fn, mode, 'cp437') as inf:
        yield inf

if __name__ == '__main__':
    with open_cp437('data/worlds/test/world_sites_and_pops.txt') as inf:
        rdr = BufferedIterator(enumerate(inf))
        parser = WorldSitesAndPopsParser()
        data = parser.parse(rdr)
        print(data)
