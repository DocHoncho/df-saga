#!/bin/env python3
import argparse
import codecs
import json
import os
import sys
from saga.util.io import open_cp437, BufferedIterator, CleanedLineReader
from saga.parsers import parse_legends
from saga.parsers.world import WorldSitesAndPopsParser, WorldHistoryParser

def usage():
    print('Usage: {} <filename> <format:worldsites|worldhistory|legends> <output filename>'.format(sys.argv[0]))
    sys.exit(2)

try:
    in_fn = sys.argv[1]
    fmt = sys.argv[2]
    out_fn = sys.argv[3]
except IndexError:
    usage()

if not os.path.exists(in_fn):
    print('File `{}` does not exist!'.format(in_fn))

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
    elif fmt == 'legends':
        print('Loading XML...', flush=True)
#            root = objectify.parse(inf)
        data = parse_legends(inf)
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


with open(out_fn, 'w') as outf:
    outf.write(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))

