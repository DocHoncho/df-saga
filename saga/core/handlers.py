class ScalarAttribute(object):

    def __init__(self, tag, path=None, name=None, required=True, default=None, value=None):

        self.tag = tag
        self.path = path
        self.name = tag if name is None else name
        self.required = required
        self.default = default
        self.value = value

    def __call__(self, value=None):
        t = ScalarAttribute(self.tag, self.path, self.name, self.required, self.default)

        try:
            t = value.text
        except AttributeError:
            t = value

        return t

    def __repr__(self):
        if self.value is None:
            return self.tag
        else:
            return repr(self.value)


class FlagAttribute(ScalarAttribute):

    def __init__(self, tag, path=None, name=None, required=False, default=False, value=None):
        super(FlagAttribute, self).__init__(tag, path, name, required, default, value)


    def __call__(self, value=None):
        #
        retval = value is not None
        return super(FlagAttribute, self).__call__(retval)


class ListAttribute(ScalarAttribute):

    def __init__(self, tag, path=None, name=None, required=False, default=None, value=None):
        super(ListAttribute, self).__init__(tag, path, name, required, default, value)
        self.data = []

    def __call__(self, value=None):
        self.data.append(super(ListAttribute, self).__call__(value))
        return self.data


class ComplexAttribute(ScalarAttribute):

    def __init__(self, tag, attributes, path=None, name=None, required=True, default=None, value=None):

        super(ComplexAttribute, self).__init__(tag, path, name, required, default, value)
        self.attributes = attributes

        self.handler = BaseHandler('ComplexAttributeHandler', attributes)

#
    def __call__(self, value):

        t = self.handler.process_data(value)
        return t


class CatchAllAttribute(ScalarAttribute):
    def __init__(self, tag, path=None, name=None, required=False, default=None, value=None):
        super(CatchAllAttribute, self).__init__(tag, path, name, required, default, value)

    def __call__(self, value):
        import pdb; pdb.set_trace()


class BaseHandler(object):

    def __init__(self, name, attributes, keep_extra=False, cull_empty=True):
        self.name = name
        self.attributes = attributes
        self.keep_extra = keep_extra
        self.cull_empty = cull_empty

    @property
    def attr_keys(self):
        return [x.tag for x in self.attributes]

    def process_data(self, xml_data):
        data = {}
        extra = {}

        elem_attributes = xml_data.xpath('./*')
        for e_attr in elem_attributes:
            if e_attr.tag in self.attr_keys:
                attribute = list(filter(lambda x: x.tag==e_attr.tag, self.attributes))[0]
                pth = attribute.tag if attribute.path is None else attribute.path

                t = xml_data.xpath(pth)
                if t is None:
                    if attribute.required:
                        raise AttributeError("Missing attribute '{}'".format(attribute.tag))

                elif len(t) == 1:
                    r = attribute(t[0])
                    if r is not None:
                        data[attribute.tag] = r
                else:
                    data[attribute.tag] = list(filter(lambda y: y is not None, [attribute(x) for x in t]))[0]
            else:
                extra[e_attr.tag] = e_attr

        return data


class EntityPopulationHandler(BaseHandler):
    def __init__(self):
        super(EntityPopulationHandler, self).__init__('entity_population', [ScalarAttribute('id')])


class EntityHandler(BaseHandler):
    def __init__(self):
        super(EntityHandler, self).__init__('entity', [
            ScalarAttribute('id'),
            ScalarAttribute('name', required=False, default=''),
            ])


class HistoricalEraHandler(BaseHandler):
    def __init__(self):
        super(HistoricalEraHandler, self).__init__('historical_era', [])


class HistoricalEventCollectionHandler(BaseHandler):
    def __init__(self):
        super(HistoricalEventCollectionHandler, self).__init__('historical_event_collection', [
            ScalarAttribute('id'),
            ScalarAttribute('start_year'),
            ScalarAttribute('start_seconds72'),
            ScalarAttribute('end_year'),
            ScalarAttribute('end_seconds72'),
            ListAttribute('event'),
            ScalarAttribute('type'),
            ScalarAttribute('parent_eventcol'),
            ScalarAttribute('subregion_id'),
            ScalarAttribute('feature_layer_id'),
            ScalarAttribute('site_id'),
            ScalarAttribute('coords'),
            ScalarAttribute('attacking_enid'),
            ScalarAttribute('defending_enid'),
            ScalarAttribute('ordinal'),
            ])


class HistoricalEventHandler(BaseHandler):
    def __init__(self):
        super(HistoricalEventHandler, self).__init__('historical_event', [
            ScalarAttribute('id'),
            ScalarAttribute('year'),
            ScalarAttribute('seconds72'),
            ScalarAttribute('type'),
            ScalarAttribute('site_id'),
            ScalarAttribute('subregion_id'),
            ScalarAttribute('feature_layer_id'),
            ScalarAttribute('coords'),

            CatchAllAttribute('data', path='./*'),
            ])


class HistoricalFigureHandler(BaseHandler):
    def __init__(self):
        super(HistoricalFigureHandler, self).__init__('historical_figure', [
            ScalarAttribute('id'),
            ScalarAttribute('race', required=False),
            ScalarAttribute('caste', required=False),
            ScalarAttribute('appeared'),
            ScalarAttribute('birth_year'),
            ScalarAttribute('death_year'),
            ScalarAttribute('associated_type', required=False),

            ComplexAttribute('hf_skill', [ScalarAttribute('skill'), ScalarAttribute('total_ip')], required=False),
            ComplexAttribute('entity_link', [ScalarAttribute('link_type'), ScalarAttribute('entity_id')], required=False),
            ComplexAttribute('interaction_knowledge', [ScalarAttribute('.')], required=False),
            ScalarAttribute('sphere', required=False),

            ScalarAttribute('birth_seconds72'),
            ScalarAttribute('death_seconds72'),
            ])


class RegionHandler(BaseHandler):
    def __init__(self):
        super(RegionHandler, self).__init__('region', [
            ScalarAttribute('id'),
            ScalarAttribute('name'),
            ScalarAttribute('type'),
            ])


class SiteHandler(BaseHandler):

    def __init__(self):

        super(SiteHandler, self).__init__('site', [
            ScalarAttribute('id'),
            ScalarAttribute('type'),
            ScalarAttribute('name'),
            ScalarAttribute('coords'),
            FlagAttribute('structures'),
            ])


class UndergroundRegionHandler(BaseHandler):

    def __init__(self):

        super(UndergroundRegionHandler, self).__init__('underground_region', [
            ScalarAttribute('id'),
            ScalarAttribute('type'),
            ScalarAttribute('depth'),
            ])


handler_map = {
        'region': RegionHandler(),
        'historical_figure': HistoricalFigureHandler(),
        'underground_region': UndergroundRegionHandler(),
        'site': SiteHandler(),
        'entity_population': EntityPopulationHandler(),
        'entity': EntityHandler(),
        'historical_event': HistoricalEventHandler(),
        'historical_event_collection': HistoricalEventCollectionHandler(),
        'historical_era': HistoricalEraHandler(),
        }


bad_chars = [
        '\xae',
        '\xaf',
    ]


class FileWrapper(object):
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


if __name__ == '__main__':
    import sys
    from lxml import etree
    from itertools import count

    def filter_type(t, func, data):
        return list(filter(lambda x: x[0] == t and func(x), data))

    fn = sys.argv[1]

    tags = []

    out_data = []
    with open(fn, 'r', errors='replace') as inf:
        inf = FileWrapper(inf)

        for c, data in zip(count(), etree.iterparse(inf)):

            event, element = data
            if tags and element.tag not in tags:
                continue

            if element.tag in handler_map:
                print("\r%08d"%(c), end='')

                try:
                    res = handler_map[element.tag].process_data(element)
                    out_data.append([element.tag, res])

                except AttributeError as e:
                    print("Unknown attribute", e)
                    import pdb; pdb.set_trace()

