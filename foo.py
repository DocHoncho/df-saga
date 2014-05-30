class Deco(object):
    def __init__(self, template_name):
        self._template_name = template_name

    def __call__(self, f):
        def wrapper_f(*args, **kwargs):
            f(*args, **kwargs)
            print("TEMPALA!! {}".format(self._template_name))
        return wrapper_f

@Deco('smoosh')
def wakka():
    print("DOO")


wakka()
