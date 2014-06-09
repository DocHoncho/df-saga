#!/bin/env python3
import codecs
from contextlib import contextmanager
from saga.parsers.world import WorldSitesAndPopsParser, WorldHistoryParser
from saga.core.handlers import FileWrapper

from lxml import objectify, etree

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

def dictify(node):
    items = node.findall('./*')
    d = []
    for x in items:
        tag = x.tag
        try:
            text = x.text.strip()
        except AttributeError:
            continue

        if text == '':
            p = dictify(x)
            if p:
                d.append((tag, p))
        else:
            d.append((tag,text))

    t = dict()
    for k, v in d:
        if k in t:
            try:
                t[k].append(v)
            except AttributeError:
                t[k] = [v]
        else:
            t[k] = v
    return t


def parse_legends(filelike):
    data = {
            'artifacts': {
                'tag': 'artifact',
                'data': [],
                },
            'entities': {
                'tag': 'entity',
                'data': [],
                },
            'entity_populations': {
                'tag': 'entity_population',
                'data': [],
                },
            'historical_eras': {
                'tag': 'historical_era',
                'data': [],
                },
            'historical_event_collections': {
                'tag': 'historical_event_collection',
                'data': [],
                },
            'historical_figures': {
                'tag': 'historical_figure',
                'data': [],
                },
            'historical_figures': {
                'tag': 'historical_figure',
                'data': [],
                },
            'regions': {
                'tag': 'region',
                'data': [],
                },
            'sites': {
                'tag': 'site',
                'data': [],
                },
            'underground_regions': {
                'tag': 'underground_region',
                'data': [],
                },
            }
    def df_workflow_sucks(filelike):
        for x in filelike:
            print(x)
            yield x

    keys = list(x['tag'] for _, x in data.items())
    for event, element in etree.iterparse(FileWrapper(filelike), events=['end']):
        if element.tag in keys:
            d = dictify(element)
            data[element.getparent().tag]['data'].append(d)
    return data

@contextmanager
def open_cp437(fn, mode='r'):
    with open(fn, mode) as inf:
        yield codecs.EncodedFile(inf, 'cp437', 'utf-8')

if __name__ == '__main__':
    import argparse
    import json
    import os
    import sys
    import yaml

    argp = argparse.ArgumentParser(description='Read and convert several types of exported Dwarf Fortress data files..')
    argp.add_argument(
            '-t', '--type',
            choices=['legends', 'worldsites', 'worldhistory'],
            dest='file_type',
            help='Specify type of data to process',
            required=True,
            )
    argp.add_argument(
            '-o', '--output',
            default=None,
            dest='output_file',
            help='Output filename, if omitted output goes to stdout',
            required=False,
            )
    argp.add_argument(
            '-f', '--format',
            choices=['json', 'yaml', 'csv'],
            default='json',
            dest='format',
            help='Format to use for output',
            required=False,
            )
    argp.add_argument(
            '--indent',
            default=2,
            dest='indent',
            help='Specify indent to use for output',
            required=False,
            )
    argp.add_argument(
            '--pretty',
            action='store_true',
            dest='emit_pretty',
            default=False,
            help='Prettify converted output, if format supports it',
            required=False,
            )
    argp.add_argument(
            '--sorted',
            action='store_true',
            dest='emit_sorted',
            default=False,
            help='Sort output',
            required=False
            )

    argp.add_argument(
            'input_file',
            metavar='FILE',
            help='File to process',
            )

    args = argp.parse_args()
    if not os.path.exists(args.input_file):
        print('File `{}` does not exist!'.format(args.input_file))
        sys.exit(3)

    with open_cp437(args.input_file, 'rb') as inf:
        if args.file_type == 'worldsites':
            rdr = BufferedIterator(enumerate(inf))
            parser = WorldSitesAndPopsParser()
            data = parser.parse(rdr)
        elif args.file_type == 'worldhistory':
            rdr = BufferedIterator(enumerate(inf))
            parser=WorldHistoryParser()
            data = parser.parse(rdr)
        elif args.file_type == 'legends':
            data = parse_legends(inf)

    if args.output_file is None:
        out_file = sys.stdout
    else:
        out_file = codecs.open(args.output_file, 'wb', 'utf-8')

    if args.format == 'json':
        if args.emit_pretty:
            formatted_data = json.dumps(data, sort_keys=args.emit_sorted, indent=args.indent, separators=(',', ':'))
        else:
            formatted_data = json.dumps(data, sort_keys=args.emit_sorted)
        out_file.write(formatted_data)

    elif args.format == 'yaml':
        flow_style = not (args.emit_pretty)
        out_file.write(yaml.dump(data, default_flow_style=flow_style, indent=args.indent))

    elif args.format == 'csv':
        print('Not yet supported!')
        sys.exit(2)


