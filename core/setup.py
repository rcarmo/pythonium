#!/usr/bin/env python3
from setuptools import setup

from pythonium_core import __version__


setup(
    name='pythonium-core',
    version=__version__,
    description='Python 3 to Javascript translator written in Python that produce fast portable javascript code',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/pythonium/pythonium',
    zip_safe=False,
    long_description=open('../README.rst').read(),
    py_modules=['pythonium_core'],
    install_requires=['docopt'],
    entry_points="""
    [console_scripts]
    pythonium_core=pythonium_core:main
    """,
)
