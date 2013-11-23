#!/usr/bin/env python3
"""pythonium

Usage: pythonium [-h][-d][-r][-V] FILE [FILE ...] [-o FILE]

Options:
  -h --help        show this
  -v --version     show version
  -V --veloce      use veloce mode, generated code is faster but least compliant
  -o --output FILE specify output file [default: stdout]
  -d --deep        generate file dependencies. If --output is not provided, it will generate for each source file a coresponding .js file.
  -r --requirejs   generate requirejs compatible module
"""
import sys
from .veloce import veloce_generate_js


__version__ = '0.4.0'


def main():
    from docopt import docopt
    args = docopt(__doc__, version='pythonium ' + __version__)
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
            raise NotImplementedError
    if output:
        output.close()

if __name__ == '__main__':
    main()
