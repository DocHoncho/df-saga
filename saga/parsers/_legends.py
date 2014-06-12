from lxml import etree
from saga.util.io import CleanedLineReader
import sys

from collections import deque

class XMLEventTarget:
    def __init__(self):
        self.stack = deque()


    def start(self, tag, attrib):
        self.stack.append({tag: None})


    def end(self, tag):
        t = self.stack.pop()
        if len(self.stack) == 0:
            print('only one item on stack at end')
            self.stack.append(t)
            return

        t2 = self.stack.pop()
        print(t, t2)
        if t2[1] is None:
            self.stack.append((t2[0], t))
        else:
            try:
                t2[1].append(t)
                self.stack.append(t2)

            except AttributeError:
                self.stack.append((t2[0], [t]))


    def data(self, data):
        t = self.stack.pop()
        t = (t[0], data)
          self.stack.append(t)


    def comment(self, text):
        pass


    def close(self):
        return "Closed"


def parse_legends(filelike):
    wrapped_file = CleanedLineReader(filelike)
    parser = etree.XMLParser(target=XMLEventTarget())

    while True:
        try:
            etree.parse(wrapped_file, parser)
        except etree.XMLSyntaxError as e:
            print(e)
            sys.exit(1)

    return parser.target.stack


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
"""

