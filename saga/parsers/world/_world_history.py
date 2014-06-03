from saga.parsers import BaseParser
from saga.parsers.helpers import create_simple_handler, create_parser_handler


class BareNamesParser(BaseParser):
    def __init__(self):
        super(BareNamesParser, self).__init__(
                'bare_names',
                'bare_names',
                rules = [
                    ('bare_name',
                        r'^([\w\s]+)$',
                        lambda i, d: d[0]
                        ),
                    ('end',
                        r'^.*\,',
                        self.end_parse
                        ),
                    ])


class WorldHistoryParser(BaseParser):
    def __init__(self):
        super(WorldHistoryParser, self).__init__(
                'world_history',
                'world_history',
                rules=[
                    ('bare_names',
                        r'^([\w\s]+)$',
                        create_parser_handler(None, 'bare_names', BareNamesParser)
                        ),
                    ('civ_list',
                        r'^([\w\s+])\, ([\w\s+])$',
                        self.civ_list_handler
                        ),
                    ])


    def civ_list_handler(self, iterable, data):
        pass


    def parse(self, iterable, data=None):
        result = super(WorldHistoryParser, self).parse(iterable, data)

        return result
