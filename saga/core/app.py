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
        #s = config.get_namespace('app')
        print(config)
        self.hostname = config['hostname']
        self.port = config['port']
        self.static_dir = config['static_dir']
        self.data_dir = '.'
        self.debug = config['debug']
        self.reloader = config['reloader']

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
    if settings['static_dir'] is not None:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': settings['static_dir']
            })
    return app


