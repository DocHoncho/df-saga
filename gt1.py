import importlib
import types

def find_modules(inside):
    im = importlib.import_module(inside)

    def f(i, p):
        data = []
        for item in dir(i):
            name = "{}.{}".format(p, item)
            obj = eval(name)
            print("n: {} t: {}".format(name, type(obj)), end='')
            if type(obj) == types.ModuleType:
                data.append(obj)
                r = f(obj, name)
                data.extend(r)
            print()
        return data

    return f(im, inside)
import saga
t = find_modules('saga')
print(t)
