#!/usr/bin/env python3
"""pythonium

Usage: pythonium [-h][-d][-r][-V] [FILE ...] [-o FILE] | [-g]

Options:
  -h --help        show this
  -v --version     show version
  -V --veloce      use veloce mode, generated code is faster but least compliant
  -o --output FILE specify output file [default: stdout]
  -d --deep        generate file dependencies. If --output is not provided, 
                   it will generate for each source file a coresponding .js file.
  -r --requirejs   generate requirejs compatible module
  -g --generate    generate pythonium runtime (exclusive option)

The default mode, without -V or --veloce option is *experimental*.

If you generate code without -V or --veloce you will need to use the library 
generated with -g or --generate option to run the code.
"""
import os
import sys
from docopt import docopt

from .veloce.veloce import veloce_generate_js
from .compliant.compliant import compliant_generate_js

__version__ = '0.5.0'


def main(argv=None):
    args = docopt(__doc__, argv, version='pythonium ' + __version__)
    if args['--generate']:
        # call ourself for each file in pythonium.lib:
        from pythonium.compliant import lib

        # runtime is built separatly
        # it must appear first in the file
        # and it must be built using veloce mode
        path = lib.__path__[0]
        argv = ['--veloce', os.path.join(path, 'runtime.py')]
        main(argv)
        for path in lib.__path__:
            for name in os.listdir(path):
                if name.endswith('.py'):
                    if name == 'runtime.py':
                        continue
                    argv = [os.path.join(path, name)]
                    main(argv)
        return

    filepaths = args['FILE']
    if not filepaths:
        main(['--help'])
        return

    generator = veloce_generate_js if args['--veloce'] else compliant_generate_js
    options = {'requirejs': args['--requirejs'],
               'deep': args['--deep'],
               }

    outfile = args['--output']
    if outfile:
        with open(outfile, 'w') as output:
            for filepath in filepaths:
                generator(filepath, output=output, **options)
    else:
        for filepath in filepaths:
            generator(filepath, output=sys.stdout, **options)


if __name__ == '__main__':
    main()
