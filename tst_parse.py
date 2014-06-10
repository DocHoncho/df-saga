from lxml import etree
from saga.core.handlers import FileWrapper
import sys

class Target:
    def __init__(self):
        self.stack = []


    def start(self, tag, attrib):
        self.stack.append((tag, None))


    def end(self, tag):
        if len(self.stack) < 1:
            return

        t = self.stack[-1]
        self.stack = self.stack[:-1]

        k = self.stack[-1]

        if k[1] is None:
            self.stack[-1] = (k[0], t)
        else:
            try:
                k[1].append(t)
            except AttributeError:
                k[1] = [k[1], t]


    def data(self, data):
        self.stack[-1] = (stack[-1][0], data)


    def comment(self, text):
        pass


    def close(self):
        return "Closed"

fn = sys.argv[1]

with open(fn, 'rb') as inf:
    parser = etree.XMLParser(target=Target())
    f = FileWrapper(inf)

    while True:
        try:
            etree.parse(f, parser)
            for c, e in enumerate(parser.target.events):
                print(c, e)
        except etree.XMLSyntaxError as e:
            print(e)
            sys.exit(1)

