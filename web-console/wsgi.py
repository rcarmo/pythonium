#!/usr/bin/env python3
import json
import random
import string
import resource
from ast import parse
from logging import getLogger
from traceback import print_exc
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

import html5lib
from webob import Request
from webob import Response
from fileserver import file_response

from pythonium.veloce import Veloce
from pythonium.pythonium import Pythonium

import settings


resource.setrlimit(resource.RLIMIT_AS, (1000 * 1048576, -1))


class Nerfed(object):

    def __init__(self):
        self.handlers = dict()

    def register(self, view, path):
        self.handlers[getattr(settings, 'ROOT_URL', '') + path] = view

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            # first match the domain if any try to match the path
            view = self.handlers.get(request.path, None)
            if view is None:
                response = Response('<h1>Not found</h1>', 404)
            else:
                try:
                    response = view(self, request)
                except Exception:
                    print_exc()
                    response = Response('<h1>Internal Server Error</h1>', 500)
            return response(environ, start_response)
        except MemoryError:
            global cache
            del cache
            cache = dict()
            return self(environ, start_response)

    def redirect(self, url):
        return Response(status=302, location=url)

    def reverse(self, view):
        for path, v in self.handlers.items():
            if v == view:
                return path

#

cache = dict()

#

def static(path):
    def view(self, request):
        return file_response(path)
    return view

app = Nerfed()

# INDEX

app.register(static('index.html'), '/')


# COMPILE

def compile(app, request):
    response = Response('', 200)
    token = request.cookies.get('token', None)
    if token is None:
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(512))
        response.set_cookie('token', token, domain=getattr(settings, 'COOKIE_DOMAIN', None))
    POST = request.POST
    mode = POST['mode']
    python = POST['python']
    tree = parse(python)
    if mode == 'veloce':
        veloce = Veloce()
        veloce.visit(tree)
        js = veloce.writer.value()
    else:
        pythonium = Pythonium()
        pythonium.visit(tree)
        js = pythonium.writer.value()
    css = POST['css']
    html = POST['html']
    html = html5lib.parse(html, namespaceHTMLElements=False)
    body = html.find('body')
    if js:
        script = Element("script")
        script.set('type', 'text/javascript')
        script.text = js        
        body.insert(0, script)
    if css:
        style = Element("style")
        style.text = css
        body.insert(0, style)
    if mode == 'compliant':
        script = Element("script")
        script.set('type', 'text/javascript')
        script.set('src', '/js/pythonium.js')
        script.text = "/* nothing */"
        body.insert(0, script)
    page = tostring(html)
    cache[token] = page
    return response

app.register(compile, '/compile')

# COMPILED

def compiled(app, request):
    token = request.cookies.get('token', None)
    if token is None:
        return static('howto.html')(app, request)
    try:
        page = cache[token]
    except:
        response = static('howto.html')(app, request)
        response.delete_cookie('token', domain==getattr(settings, 'COOKIE_DOMAIN', None))
        return response
    return Response(page, 200)

app.register(compiled, '/compiled')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from server_reloader import main as reloader
    app.register(static('js/ace/src-noconflict/ace.js'), '/js/ace/src-noconflict/ace.js')
    app.register(static('js/ace/src-noconflict/theme-monokai.js'), '/js/ace/src-noconflict/theme-monokai.js')
    app.register(static('js/ace/src-noconflict/mode-css.js'), '/js/ace/src-noconflict/mode-css.js')
    app.register(static('js/ace/src-noconflict/worker-css.js'), '/js/ace/src-noconflict/worker-css.js')
    app.register(static('js/ace/src-noconflict/mode-html.js'), '/js/ace/src-noconflict/mode-html.js')
    app.register(static('js/ace/src-noconflict/mode-python.js'), '/js/ace/src-noconflict/mode-python.js')
    app.register(static('js/classy.js'), '/js/classy.js')
    app.register(static('js/jquery.js'), '/js/jquery.js')
    app.register(static('js/app.py.js'), '/js/app.py.js')
    app.register(static('js/pythonium.js'), '/js/pythonium.js')
    app.register(static('css/app.css'), '/css/app.css')
    def run_server():
        server = make_server('localhost', 8000, app)
        print('Starting server at http://127.0.0.1:8000')
        server.serve_forever()
    reloader(run_server)
