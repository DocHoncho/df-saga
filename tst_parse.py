from lxml import etree
from saga.core.handlers import FileWrapper
import sys

from collections import deque

class Target:
    def __init__(self):
        self.stack = deque()


    def start(self, tag, attrib):
        self.stack.append((tag, None))


    def end(self, tag):
        t = self.stack.pop()
        if len(self.stack) == 0:
            print('only one item on stack at end')
            self.stack.append(t)
            return

        t2 = self.stack.pop()

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

