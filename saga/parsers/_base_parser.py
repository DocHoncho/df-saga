import re
from saga.util.io import BufferedIterator


class StopParser(Exception):
    def __init__(self, msg=None):
       super(StopParser, self).__init__('StopParser: {}'.format(msg or ''))


class BaseParser(object):
    def __init__(self, name, key, iterable, *, rules=None, discard_blank_lines=True):
        self.name = name
        self.discard_blank_lines = discard_blank_lines
        self.key = key
        self.rules = []
        self.add_rules(rules or [])
        if type(iterable) != BufferedIterator:
            self.iterable = BufferedIterator(enumerate(iterable))
        else:
            self.iterable = iterable


    def add_rule(self, name, pattern, func):
        self.rules.append((name, re.compile(pattern), func))


    def add_rules(self, rules):
        for rule in rules:
            self.add_rule(*rule)


    def parse(self):
        done = False
        context = {}

        while not done:
            try:
                i, line = next(self.iterable)
                if self.discard_blank_lines and line.strip() == '':
                    continue

                for rule_name, rule_pattern, rule_func in self.rules:
                    res = rule_pattern.search(line.rstrip())
                    if res:
                        res_data = [x.strip() for x in res.groups()]
                        rule_result = rule_func(self.iterable, res_data)
                        #import pdb; pdb.set_trace()
                        if self.key is None:
                            # With key==None, merge results with context.
                            # Duplicate keys are converted into lists, otherwise values
                            # are left as is.
                            for key, val in rule_result.items():
                                if key in context:
                                    try:
                                        context[key].append(val)

                                    except AttributeError:
                                        # The key exists, but isn't a list
                                        old = context[key]
                                        context[key] = [old, val]
                                else:
                                    context[key] = val
                        else:
                            try:
                                context[self.key].append(rule_result)
                            except KeyError:
                                context[self.key] = [rule_result]

                        break

            except StopIteration:
                done = True
                continue

            except StopParser:
                self.terable.cancel()
                done = True
                continue


        return context


    def end_parse(self, iterable, data=None):
        raise StopParser()


    def __str__(self):
        return "Parser<{}>".format(self.name)



