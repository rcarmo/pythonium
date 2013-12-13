#!/usr/bin/env python3
from setuptools import setup

from pythonium.main import __version__


setup(
    name='pythonium',
    version=__version__,
    description='Python 3 to Javascript translator written in Python that produce fast portable javascript code',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/pythonium/pythonium',
    zip_safe=False,
    packages=['pythonium', 'pythonium.compliant', 'pythonium.compliant.builtins', 'pythonium.veloce'],
    install_requires=['docopt'],
    entry_points="""
    [console_scripts]
    pythonium=pythonium.main:main
    """,
)
