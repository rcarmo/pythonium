#!/usr/bin/env python3
from setuptools import setup


setup(
    name='pythonium-core',
    version='0.1',
    description='Python 3 to Javascript translator written in Python that produce fast portable javascript code',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    url='https://github.com/pythonium/pythonium',
    zip_safe=False,
    py_modules=['pythonium_core'],
    entry_points="""
    [console_scripts]
    pythonium_core=pythonium_core:main
    """,
)
