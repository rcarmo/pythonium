#!/usr/bin/env python3
import os

from rororo import GET
from rororo import manage
from rororo import create_app
from rororo.static import static
from rororo.manager import runserver


ROUTES = []

# statics

DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))
ROUTES.append(static('css', 'css'))
ROUTES.append(static('js', 'js'))

# index page

with open('index.html') as f:
    index_content = f.read()

index = lambda: index_content
ROUTES.append(GET('/', index))

# compile
CSS = ""
HTML = ""
PYTHON = ""

def compile():
    global CSS, HTML, PYTHON
    CSS = ""
    HTML = ""
    PYTHON = ""

ROUTES.append(GET('/compile', compile))

# COMPILED

with open('howto.html') as f:
    HOWTO = f.read()

def compiled():
    if not PYTHON:
        return HOWTO
        


ROUTES.append(GET('/compiled', compiled))


app = create_app(routes=ROUTES)
runserver(app, autoreload=True)
