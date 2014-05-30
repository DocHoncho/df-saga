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

def parse_xml(fn, **kwargs):
    verbose = kwargs.get('verbose', False)

    dat = {}
    with open(fn, 'r', errors='replace') as inf:
        root = etree.parse(FileWrapper(inf))

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

def count_attrs(data):
    events = list(filter(lambda x: True, data['historical_events']['data']))
    all_types = list(unique(lambda x: x['type'], events))
    all_sigs = []
    cnt = Counter()
    attrs = set()

    for t in all_types:
        t_events = list(events_by_type(t, events))
        t_sigs = list(unique(lambda x: x['sig'], t_events))

        for s in t_sigs:
            st = "{}~{}".format(t, s)
            all_sigs.append(st)
            for c in s.split(' '):
                attrs.add(c)
                cnt[c] += 1

    return attrs, cnt

if __name__ == '__main__':
    fn = 'c:/dev/df/data/ugc/region13/region13-legends.xml'
    data = parse_xml(fn)
    attrs, cnt = count_attrs(data)
    print(attrs, cnt)

