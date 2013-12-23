HACKING
#######

Requirements
============

- Python 3.3+
- nodejs, tested with 0.11.9
- a recent browser (optional)

Installing nodejs
-----------------

**23/12/13 the following doesn't work, rely on your operating system documentation to install a recent version of nodejs**

cli dance in a **Python 2** environment, the build system does not support Python 3::

  git clone https://github.com/joyent/node.git
  cd node
  git checkout v0.11.9
  python2 configure
  make
  make install

Installing Python 3.3
---------------------

Download and install ``pythonz``::
    
  curl -kL https://raw.github.com/saghul/pythonz/master/pythonz-install | bash

Please add the following line to the end of your ``~/.bashrc``::

  [[ -s $HOME/.pythonz/etc/bashrc ]] && source $HOME/.pythonz/etc/bashrc

Then install python 3::

  pythonz install 3.3.2

``pythonium`` usage
===================

Compliant mode
--------------

Create ``pythonium.js`` with ``pythonium -g > pythonium.js``. 

Translate your ``app.py`` with ``pythonium app.py > app.py.js`` include both in your html page or use the following command to execute the script in nodejs::

  cat pythonium.js app.py.js | nodejs

Veloce mode
-----------

FIXME


Development workflow
====================

Add a test in ``./tests/`` prepend the name with ``compliant-`` if you are developping for the compliant mode, for instance::

  compliant-yield-from.py

Execute ``runtests.py`` to have the results. Depending on how it failed you can:

- run the python script with python3
- run the generated ``exec.js`` file in ``./tests/tmp/`` for instance for ``compliant-yield-from.py`` the generated file will be ``./tests/tmp/compliant-yield-from.pyexec.js``
  but if the test can be run in both modes like ``for-loop.py`` two files will be generated ``./tests/tmp/for-loop.pyexec-veloce.js`` and ``./tests/tmp/for-loop.pyexec-compliant.js``


Internals
=========

As you may already know there is two modes in pythonium, *veloce* and *compliant*. Compliant
mode is the default in ``pythonium`` command, to use *veloce* mode you need to provide de
``-V`` or ``--veloce`` option.

Veloce mode
-----------

Veloce is *Python syntax with JavaScript semantic*. The Veloce compiler transforms Python code 
to JavaScript with minimal addition and modification to the abstract syntax tree. Additions or modification 
of the abstract syntax tree are done to support features of Python that are not supported as-is by JavaScript.
Most of them are “syntaxic sugar”.

Veloce provide an object system similar to Python via classy.js. That said there is a known gotcha, inherited 
from the implementation of JavaScript prototype inheritance. If you assign a method to a variable, ``self`` in the context
of the “method” called through the variable will be the ``window`` object.

The following::

  caller(an_object.method)

Does not work as expected. Instead one must define a ``wrap`` function that feeds the method context with the correct value of ``this``::

  def wrap(object, method):
      def wrapped():
          return method.apply(object, arguments)
      return wrapped

The previous code, must be written as follow::

  caller(wrap(an_object, an_object.method))

This can not be automated in Veloce, but it's done in compliant mode.

Translations
^^^^^^^^^^^^

FIXME

Compliant mode
--------------

FIXME

Translations
^^^^^^^^^^^^

FIXME
