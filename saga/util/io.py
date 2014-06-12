import codecs
from contextlib import contextmanager

class BufferedIterator(object):
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


class CleanedLineReader(object):
    def __init__(self, data):
        self.data = data

    def read(self, *args):
        line = self.data.readline().strip()
        n = []
        for x in line:
            if x > 255:
                x=255
            n.append(x)
        return bytes(n)


@contextmanager
def open_cp437(fn, mode='r'):
    with open(fn, mode) as inf:
        yield codecs.EncodedFile(inf, 'cp437', 'utf-8')

