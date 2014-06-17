from saga.parsers import StopParser

class Handler(object):
    def __init__(self, name, *, data_keys=None, context_key=None):
        self.name = name
        self.data_keys = data_keys or []
        self.context_key = context_key


class EndParserHandler(Handler):
    def __call__(self, name, *args, **kw):
        raise StopParser()


class SimpleHandler(Handler):
    def __init__(self, data_keys, *, context_key=None):
        self.data_keys = data_keys
        self.context_key = context_key

    def __call__(self, iterable, data = None):
        data = data or []
        d = as_dict(data_keys, data)
        if context_key is None:
            return d
        else:
            return { context_ley: d }


class SubparserHandler(Handler):
    def __init__(self, parser_class, *, ):
        super(SubparserHandler, self).__init__(
