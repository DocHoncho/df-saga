class Rule(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, iterable, data=None):
        pass


class RegexpRule(Rule):
    def __init__(self, name, pattern):
        super(RegexpRule, self).__init__(name)
        self.pattern = re.compile(pettern)


    def __call__(self, line_no, line):
        return self.pattern.match(line)


    def __str__(self):
        return "RegexpRule({}, {})".format(self.name, setf.pattern)


class LineRule(RegexpRule):
    def __init__(self, name, line_num, pattern):
        super(LineRule, self).__init__(name, pattern)
        self.line_num = line_num


    def __call__(self, line_num, line):
        if line_num == self.line_num:
            res = super(LineRule, self).__call__(line_num, line)
            return res
        return


class EndParseRule(RegexpRule):
    def __init__(self, pattern, func=None):
        super(EndParseRule, self).__init__('end', pattern)
        self.func = func or self.default_action

    def __call_(self, line_no, line):
        t = super(EndParseRule, self).__call__(line_no, line)
        if t:
            return self.func(t)

        return

