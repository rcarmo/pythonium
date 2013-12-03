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
  -g --generate    generate pythonium runtime (exclusive option)

The default mode, without -V or --veloce option is *experimental*.

If you generate code without -V or --veloce you will need to use the library generated with -g or --generate option to run the code.
"""
import os
import sys

from .veloce import veloce_generate_js
from .pythonium import pythonium_generate_js


__version__ = '0.4.7'


def main():
    from docopt import docopt
    args = docopt(__doc__, version='pythonium ' + __version__)
    if args['--generate']:
        from pythonium import lib
        path = lib.__path__[0]
        output = sys.stdout
        for name in ['runtime.py']:
            sys.stderr.write('Processing {}\n'.format(name))
            veloce_generate_js(os.path.join(path, name), False, None, output, False)
        for name in os.listdir(path):
            if name == '__pycache__':
                continue
            if name in ['runtime.py']:
                continue
            else:
                sys.stderr.write('Processing {}\n'.format(name))
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
