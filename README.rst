Pythonium
#########

(9 minutes)

Python 3 to Javascript translator written in Python that produce fast portable javascript code.

What? (2 minutes)
=================

Pythonium will exists in several flavors, each of which with their own strength and performance. The more you dive into the list to more feature you have, the less performance you can except:

- Pythonium **Core**

  - No external dependency
  - Exact same syntax as Python
  - Compatible with existing Javascript libraries
  - Function with positional arguments to javascript functions
  - Automatic scope handling and ``global`` support
  - Use ``for`` to iterate over javascript arrays
  - Python types are mapped to javascript types
  - Single inheritance classes with mixins
  - Anonymous exceptions with ``__exception__`` special variable
  - Support of ``yield``
  - Javascript ``new`` is a special function that translates to Javascript ``new``
  - if ``__DOLLAR__`` is found in any name, it will be remplaced by ``$`` character.
  - Optionnal support of ``import ... from ...`` with `requirejs <http://requirejs.org/>`_

- Pythonium **Veloce** support all the above features and adds the following: 

  - One dependency ``pythonium.veloce.js`` expected to be 10kb
  - Full Python function signature support with ``*args`` and ``**kwargs``
  - Support of ``__getattribute__`` and ``__getattr__`` hooks
  - Support of metaclass
  - Support for ``list``, ``dict``, ``set``, ``float``, ``int``, ``str``
  - ``for`` 

- Pythonium **Compliant** 100% compliant with CPython 3

Why? (5 minutes)
================

Is 100% is of any interest right **now**? Do you need to build anything that use **all the features** of CPython right now? **No**. 

Can you trade some features for speed? **Yes**.

For the industry, experienced programers, and hobbyst, what is best is to have something tailored to get things done in the browser with the syntax they prefer. 

Anyway, the APIs are different from backend and desktop, so there will be things to learn. For instance, if you choose **pythonium core** you will need to learn to work with Javascript arrays and objects and work around their specificities. So working, around specifities of the *language* can be boring, but it's the best that is available right now, and it's after all, not that bad.

As a programmer that knows both Python and Javascript, I prefer to focus on what is the easiest for me to do and maximise what I will be able to do next. The immediate answer to this answer is what is already available in the repository.

I understand, that in the long run it's nice to have fully compliant Python in the browser, for learning purpose, to avoid bugs that are not reported correctly and many things. That said, I prefer to focus on tooling, library support, demos and other things that can people like me get actually things done.

I've already done it in `PythonJS <https://github.com/PythonJS/PythonJS>`_, I know it's possible to even have 100% compliance. PythonJS code is poor, I though it was possible to improve the things so I started this new project.

How? (1 minute)
===============

Ahah!

Want to help? (30 seconds)
==========================

- `Star this repository <https://github.com/pythonium/pythonium/star>`_
- `Follow the project on twitter <https://twitter.com/intent/user?screen_name=pythonium>`_
- `Join the mailling list <https://groups.google.com/forum/#!forum/pythonium-users>`_
