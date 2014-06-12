from saga.parsers import BaseParser
from saga.parsers.helpers import create_simple_handler, create_parser_handler
from saga.util.io import BufferedIterator


class PopulationParser(BaseParser):
    def __init__(self, name, key):
        super(PopulationParser, self).__init__(
                name,
                key,
                rules = [
                    (
                        'default',
                        r'^\t(\d+) (.+)$',
                        create_simple_handler(('count', 'type'), make_list=True)
                        ),
                    (
                        'total',
                        r'\t(Total): (\d+)',
                        create_simple_handler(('type', 'count'), make_list=True)
                        ),
                    (
                        'unnumbered',
                        r'\t(Unnumbered) ([\w\s]+)',
                        create_simple_handler(('count', 'type'), make_list=True)
                        ),
                    (
                        'end',
                        r'^[^\t].+',
                        self.end_parse
                        ),
                    ])


class SiteParser(BaseParser):
    def __init__(self):
        super(SiteParser, self).__init__(
                'site',
                None,
                rules = [
                    (
                        'owner',
                        r'^\tOwner: ([\w\s]+), (\w+)',
                        create_simple_handler(('name', 'race'), context_key='owner')
                        ),
                    (
                        'parent',
                        r'^\tParent Civ: ([\w\s]+), (\w+)',
                        create_simple_handler(('name', 'race'), context_key='parent')
                        ),
                    (
                        'population',
                        r'^\t(\d+) (.*)',
                        create_simple_handler(('count', 'type'),
                            context_key='population', make_list=True)
                        ),
                    (
                        'end',
                        r'^[^\t].+',
                        self.end_parse
                        ),
                    ])


class SitesParser(BaseParser):
    def __init__(self):
        super(SitesParser, self).__init__(
                'sites',
                'sites',
                rules=[
                    (
                        'header',
                        r'^(\d+): ([\w\s]+), "(.*)", ([\w\s]+)$',
                        create_parser_handler(('id', 'real_name', 'name', 'type'),
                            'sites', SiteParser, make_list=True)
                        ),
                    (
                        'end',
                        r'^Outdoor Animal Populations',
                        self.end_parse
                        ),
                    ])


class WorldSitesAndPopsParser(BaseParser):
    def __init__(self, filelike):
        super(WorldSitesAndPopsParser, self).__init__(
                'world_sites_and_pops',
                'world_sites_and_pops',
                BufferedIterator(enumerate(filelike)),
                rules = [
                    (
                        'world_pops',
                        r'^Civilized World Population',
                        self.pops_handler('civ_populations')
                        ),
                    (
                        'sites',
                        r'^Sites',
                        self.sites_handler
                        ),
                    (
                        'outside_pops',
                        r'^Outdoor Animal Populations.*$',
                        self.pops_handler('outside_populations')
                        ),
                    (
                        'underground_pops',
                        r'^Underground Animal Populations.*$',
                        self.pops_handler('underground_populations')
                        ),
                    ],
                )

    def pops_handler(self, name):
        def f(iterable, data):
            parser = PopulationParser(name, name)
            result = parser.parse(iterable, [])
            return result
        return f


    def sites_handler(self, iterable, data):
        parser = SitesParser()
        result = parser.parse(iterable, [])
        return result


