import json
import os

from jinja2 import Environment, FileSystemLoader
from urllib import parse as urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect

DEFAULT_APP_SETTINGS = {
        'hostname': '127.0.0.1',
        'port': 5000,
        'debug': True,
        'reloader': True,
        'static_dir': None,
        'data_dir': '.'
        }

class App(object):

    def __init__(self, config):
        s = config.get_namespace('app')

        self.hostname = config['app/hostname']
        self.port = config['app/port']
        self.static_dir = config['app/static_dir']

    def dispatch_request(self, request):
        return Response('Hello World')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(settings):
    app = App(settings)
    if static_dir is not None:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': static_dir
            })
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    settings = load_settings('settings.json', DEFAULT_APP_SETTINGS)

    app = create_app(settings['static_dir'])
    run_simple(settings['hostname'],
               settings['port'],
               app,
               use_debugger=settings['debug'],
               use_reloader=settings['reloader'])

