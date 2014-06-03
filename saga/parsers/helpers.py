from saga.util import as_dict

def create_simple_handler(data_keys, *, context_key=None, make_list=False):
    def f(iterable, data):
        d = as_dict(data_keys, data)
        if context_key is None:
            return d
        else:
            return {context_key: d}

    return f


def create_parser_handler(data_keys, context_key, parser_class, *, make_list=False):
    def f(iterable, data):
        if data_keys is None:
            new_context = {}
        else:
            new_context = as_dict(data_keys, data)

        parser = parser_class()
        result = parser.parse(iterable, data)

        try:
            new_context.update(result)
        except AttributeError:
            new_context[context_key].append(result)
        except KeyError:
            new_context[context_key] = [result]

        return new_context

    return f


