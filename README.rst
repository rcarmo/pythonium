Pythonium
#########

(8 minutes)

Python 3 to Javascript translator written in Python that produces fast portable javascript code.

**tldr**: read the `tutorial <https://github.com/pythonium/pythonium/tree/master/examples/todo-list#todo-list>`_

Quick examples
==============

Hello, World!::

    $ echo "print('Hello, world')" >> hello.py
    $ pythonium -V hello.py
    console.log("Hello, world");

A loop. ::

    $ echo "for i in range(10): print(i)" >> loop.py
    $ pythonium -V loop.py
    var iterator_i = range(10);
    for (var i_iterator_index=0; i_iterator_index < iterator_i.length; i_iterator_index++) {
        var i = iterator_i[i_iterator_index];
        console.log(i);
    }




Getting started (2 minutes)
===========================

You will need Python 3 to run the translator. Refer to your operating system documentation to know how to do it (most Linux distributions have Python 3 readily available).

Then you can use pip to install the stable translator:

  pip install pythonium

The above package installs a ``pythonium`` command that has the following options:

  pythonium

  Usage::

    pythonium [-h][-d][-r][-V][FILE ...] [-o FILE]|[-g]


  Options::
  
    -h --help        show this
    -v --version     show version
    -o --output FILE specify output file [default: stdout]
    -d --deep        generate file dependencies. If --output is not provided, it will generate for each source file a coresponding .js file.
    -r --requirejs   generate requirejs compatible module
    -V --veloce      use veloce mode, Python syntax with JavaScript semantic
    -g --generate    generate pythonium library


What? (2 minutes)
=================

Pythonium will exist in two flavors, each with their own strengths and performance characteristics. As you go down the list the more features you'll have, and performance will, of course, decrease with sophistication (but not much):

- Pythonium **Veloce**

  - Fully portable
  - Native Javascript speed
  - Exact same syntax as Python 3
  - Compatible with existing Javascript libraries
  - Functions are translated to Javascript functions with support for keyword arguments, ``*args`` and ``**kwargs``
  - Automatic scope handling and ``global`` support
  - ``for`` iterates over Javascript arrays
  - Python types are mapped to Javascript types
  - Anonymous exceptions with ``__exception__`` special variable
  - Support of ``yield``
  - ``print`` is translated to ``console.log``
  - ``new(SomeObject, arg0, arg1)`` as a special function that translates to Javascript ``new SomeObject(arg0, args1)`` with any number of arguments
  - if ``__DOLLAR__`` is found in any name, it will be replaced by ``$`` character.
  - Support of ``from ... import ...`` via `requirejs <http://requirejs.org/>`_
  - Support of single inheritance classes via `classy <http://classy.pocoo.org/>`_ [1][2]

Also there is `cookbook <https://github.com/pythonium/pythonium/wiki/Pythonium-Veloce-Cookbook>`_.

- Pythonium **Compliant** 100% compliant with CPython 3

Why? (3 minutes)
================

Is 100% compliance of any interest right **now**? Do you need to build anything that uses **all the features** of CPython right now? **No**. 

Can you trade some features for speed? **Yes**.

For the industry, experienced programmers, and hobbyists, the best approach is to have something tailored to get things done in the browser with the syntax they prefer.

As things stand, APIs differ significantly between back-end and front-end environments, so there will always be differences. For instance, if you choose **pythonium core** you will need to learn to work with Javascript arrays and objects and work around their specificities. Working around specifities of the *language* can be boring, but it's the best that is available right now, and it's after all, not that bad.

As a programmer that knows both Python and Javascript, I prefer to focus on what is the easiest for me to do and maximise what I will be able to do next. The immediate answer to this answer is what is already available in the repository.

How? (1 minute)
===============

Ahah!

Want to help? (30 seconds)
==========================

- `Star this repository <https://github.com/pythonium/pythonium>`_
- `Follow the project on twitter <https://twitter.com/intent/user?screen_name=pythonium>`_
- `Join the mailling list <https://groups.google.com/forum/#!forum/pythonium-users>`_

Documentation
=============

Documentation is available in the `wiki <https://github.com/pythonium/pythonium/wiki>`_.

Licensing
=========

LGPL 2.1 or later

- [1] Nested class definition are not supported
- [2] Calling super method is done with ``super(arg0, arg1, arg2, ...)``

.. image:: https://d2weczhvl823v0.cloudfront.net/pythonium/pythonium/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

