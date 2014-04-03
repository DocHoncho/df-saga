from saga.core import settings
from pprint import pprint

settings.register_namespace('app')
settings.register_namespace('something')

t = settings.get_settings()
pprint(t.__dict__())

