import codecs
import re

from itertools import zip_longest
from functools import partial

def init_parsers(items):
    data = {}
    for i in items:
        i['start_pattern_re'] = re.compile(i['start_pattern'])
        i['end_pattern_re'] = re.compile(i['end_pattern'])

        t = []
        for pat, func in i['line_handlers']:
            t.append((re.compile(pat), func))
        i['line_handlers'] = t

        data[i['name']] = i

    return data

def zipdict(a, b, fillvalue=None):

    return dict(zip_longest(a, b, fillvalue=fillvalue))

def simple_group(labels):
    return partial(zipdict, labels)

def simple_value(name):
    return lambda x: zipdict([name], [x])

parsers = init_parsers([
        {   'name': 'world_population',
            'start_pattern': 'Civilized World Population',
            'end_pattern': '^\w*',
            'line_handlers': [
                (r'^\t(\d+) (\w+)', simple_group(['count', 'type'])),
                (r'^\tTotal: (\d+)', simple_value('total')),
                ]
            }
        ])

def run_parser(parser, iterable):
    data = []

    last_line = ""
    line = ""

    for line in iterable:
        res = parser['end_pattern_re'].search(line)
        if res:
            last_line = line
            break

        for pat, func in parser['line_handlers']:
            res = pat.search(line)
            if res:
                data.append(func(res.groups()))

        last_line = line

    return data, last_line

def load_world_sites(filename):
    global parsers

    with codecs.open(filename, 'r', 'cp437') as inf:
        data = inf.readlines()

    data_itr = iter(data)

    for line in data_itr:
        for parser in parsers.values():
            res = parser['start_pattern_re'].search(line)
            if res:
                t = run_parser(parser, data_itr)
                print(t)

if __name__ == '__main__':
    print('Hallo!')
