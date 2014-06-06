from saga.core.handlers import FileWrapper
from lxml import etree
from itertools import count
from collections import Counter, defaultdict

def get_sig(node):
    attributes = node.find('.')
    s = set([x.tag for x in attributes])
    i = " ".join(sorted([x for x in s]))

    return "{}:{}".format(node.tag, i)

def sig_count(sig):
    e, rest = sig.split(':')
    return len(rest.split(' '))

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

import json
def dump_json(fn, data):
    with open(fn, 'w') as outf:
        outf.write(json.dumps(data, indent=2, separators=(',', ': '), sort_keys=True))

def unique(func, data):
    s = set()
    for d in data:
        s.add(func(d))

    return sorted(s)

def events_by_type(t, data):
    return filter(lambda x: x['type'] == t, data)

def parse_legends(f, **kwargs):
    verbose = kwargs.get('verbose', False)

    dat = {}
    root = etree.parse(f)

    top_levels = root.find('.')
    for x in top_levels:
        items = x.find('.')
        td = []
        if verbose:
            print('Processing "{}" ({} items)'.format(x.tag, len(items)))

        sig_set = set()
        for item in items:
            d = dictify(item)
            sig = get_sig(item)
            d['sig'] = sig
            sig_set.add(sig)

            td.append(d)
        dat[x.tag] = {'sigs': sorted(sig_set), 'data': td}
    return dat

