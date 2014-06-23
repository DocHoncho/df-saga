#! python3
import argparse
import codecs
import json
import os
import sys
import yaml

from saga.util.io import open_cp437
from saga.parsers.legends import LegendsParser
from saga.parsers.world import WorldSitesAndPopsParser, WorldHistoryParser

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

file_type_map = {
        'worldsites': WorldSitesAndPopsParser,
        'legends': LegendsParser,
        'worldhistory': WorldHistoryParser,
        }

print('Parsing `{}` as a `{}` file...'.format(args.input_file, args.file_type))
with open_cp437(args.input_file, 'rb') as inf:
    parser_cls = file_type_map[args.file_type]
    parser = parser_cls()
    data = parser.parse(inf)

print('Generating `{}` data for output...'.format(args.format))
if args.format == 'json':
    if args.emit_pretty:
        formatted_data = json.dumps(data,
                                    sort_keys=args.emit_sorted,
                                    indent=args.indent,
                                    separators=(',', ':'))

    else:
        formatted_data = json.dumps(data, sort_keys=args.emit_sorted)

elif args.format == 'yaml':
    flow_style = not (args.emit_pretty)
    formatted_data = yaml.dump(data, default_flow_style=flow_style, indent=args.indent)

elif args.format == 'csv':
    print('Not yet supported!')
    sys.exit(2)

print('Writing output to `{}`...'.format(args.output_file or 'stdout'))
if args.output_file is None:
    out_file = sys.stdout
else:
    out_file = codecs.open(args.output_file, 'wb', 'utf-8')
out_file.write(formatted_data)
out_file.close()

