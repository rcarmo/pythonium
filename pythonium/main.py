#!/usr/bin/env python3
"""pythonium

Usage: pythonium [-h][-d][-r][-V] [FILE ...] [-o FILE]|[-g]

Options:
  -h --help        show this
  -v --version     show version
  -V --veloce      use veloce mode, generated code is faster but least compliant
  -o --output FILE specify output file [default: stdout]
  -d --deep        generate file dependencies. If --output is not provided, it will generate for each source file a coresponding .js file.
  -r --requirejs   generate requirejs compatible module
  -g --generate    generate pythonium runtime
"""
import os
import sys

from .veloce import veloce_generate_js
from .pythonium import pythonium_generate_js


__version__ = '0.4.2'


def main():
    from docopt import docopt
    args = docopt(__doc__, version='pythonium ' + __version__)
    if args['--generate']:
        import lib
        path = lib.__path__._path[0]
        output = sys.stdout
        for name in ['runtime.py', 'builtins.py']:
            sys.stderr.write('Processing {}\n'.format(name))
            veloce_generate_js(os.path.join(path, name), False, None, output, False)
        for name in os.listdir(path):
            sys.stderr.write('Processing {}\n'.format(name))
            if name in ['runtime.py', 'builtins.py']:
                continue
            else:
                pythonium_generate_js(os.path.join(path, name), False, None, output, False)
        output.close()
    else:
        requirejs = args['--requirejs']
        filepaths = args['FILE']
        output = args['--output']
        if output is None:
            output = sys.stdout
        else:
            output = open(output, 'w')
        deep = args['--deep']
        for filepath in filepaths:
            if args['--veloce']:
                veloce_generate_js(filepath, requirejs, None, output, deep)
            else:
                pythonium_generate_js(filepath, requirejs, None, output, deep)
        if output:
            output.close()

if __name__ == '__main__':
    main()
