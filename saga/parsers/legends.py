import types
import sys

from collections import deque
from lxml import etree
from saga.util.io import CleanedLineReader
from saga.util import dictify

class LegendsEventTarget:
    def __init__(self):
        self.stack = deque()


    def start(self, tag, attrib):
        self.stack.append((tag, None))


    def end(self, tag):
        import pdb; pdb.set_trace()
        obj = self.stack.pop()
        if len(self.stack) == 0:
            self.stack.append(obj)
            return
        obj_dict = dictify(obj)

        operand = self.stack.pop()
        op_key, op_val = operand

        if op_val is None:
            self.stack.append((op_key, obj_dict))

        else:
            try:
                op_val.append(obj_dict)
                self.stack.append(operand)

            except AttributeError:
                self.stack.append((op_key, [op_val, obj_dict]))


    def data(self, data):
        obj = self.stack.pop()
        self.stack.append((obj[0], data))


    def comment(self, text):
        pass


    def close(self):
        return "Closed"


class LegendsParser(object):
    def _do_parse(self, iterable):
        """Perform actual XML parsing, returning results which should be a nested set of tuples
        """
        wrapped = CleanedLineReader(iterable)
        parser = etree.XMLParser(target=LegendsEventTarget())

        while True:
            try:
                etree.parse(wrapped, parser)
            except etree.XMLSyntaxError as e:
                print(e)
                break

        return parser.target.stack[0]


    def _fix_parse_output(self, data):
        """Strips df_world and the container keys out of the result dictionary.

        E.g., given { 'words': { 'word': [ "cat", "dog", "mouse"]}}
        return { "word": [ "cat", "dog", "mouse"]
    """
        nd = {}
        for k, v in data[1]:
            try:
                nd.update(**v)
            except TypeError:
                nd[k] = v[1]

        return nd


    def parse(self, iterable, data=None):
        data = self._do_parse(iterable)
        return self._fix_parse_output(data)


