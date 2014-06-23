import types
import sys

from collections import deque
from lxml import etree
from saga.util.io import CleanedLineReader


xml_sections = [
        'regions',
        'underground_regions',
        '',
        ]


class LegendsEventTarget:
    def __init__(self):
        self.stack = deque()


    def start(self, tag, attrib):
        self.stack.append((tag, None))


    def end(self, tag):
        t = self.stack.pop()
        if len(self.stack) == 0:
            self.stack.append(t)
            return

        t2 = self.stack.pop()
        try:
            k2, v2 = t2
        except ValueError:
            import pdb; pdb.set_trace()

#        print('tag: %s t: %s t2: %s'%(tag, t, t2))

        if v2 is None:
            self.stack.append((k2, t))

        else:
            try:
                v2.append(t)
                self.stack.append(t2)

            except AttributeError:
                self.stack.append((k2, [t]))


    def data(self, data):
        t = self.stack.pop()
        k, _ = t

        self.stack.append((k, data))


    def comment(self, text):
        pass


    def close(self):
        return "Closed"


class LegendsParser(object):
    def parse(self, iterable, data=[]):
        wrapped = CleanedLineReader(iterable)
        parser = etree.XMLParser(target=LegendsEventTarget())

        while True:
            try:
                etree.parse(wrapped, parser)
            except etree.XMLSyntaxError:
                break

        d = parser.target.stack[0]
        return d

"""

# I'm having a hard time believing it would be so simple
# Thanks, lxml.objectify!  You're swell!
# Annnd it was too good to be true.  This version uses extreme amounts
# or memory.  But it's pretty cool anyway
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
"""

