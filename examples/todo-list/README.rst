todo list
#########

This is a small tutorial coming with `Pythonium <https://github.com/pythonium/pythonium>`_ that will help you get started.

Getting started
===============

First you will need Python 3, refer to your OS documentation to know how to get it.

The second step is to install Pythonium, similarly refer to your OS documentation to know how to do it. Most likely you will use ``pip``::

  pip install pythonium

Or ``easy_install``::

  easy_install pythonium

It's assumed you have recent browser and an editor. Create a file named ``index.html`` with the following content::

  <!DOCTYPE html>
  <html>
    <head>
      <title>todo list by Pythonium</title>
      <meta http-equiv="content-type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
      <h1>A todo list</h1>
      <div id="container"></div>
      <script src="jquery.js"></script>
      <script src="pythonium.js"></script>
      <script src="app.py.js"></script>
    </body>
  </html>

In the same directory download ``jquery.js``::

  wget https://code.jquery.com/jquery.js

The second dependency is generated from python sources included in the *Pythonium* package downloaded previously, it can be found under ``path/site-packages/pythonium/lib/``. You don't need to read that code. It's the runtime library needed by scripts generated with Pythonium to run in JavaScript environments like browsers. It's always accessible online at `github <https://github.com/pythonium/pythonium/tree/master/pythonium/lib>`_. 

Anyway, the command to generate ``pythonium.js`` under GNU/Linux is the following::

  pythonium -g > pythonium.js

It's assumed the following command was executed in the same directory as the one where you created the ``index.html`` file.

Now create an empty ``app.py`` file::

  touch app.py

The command to compile a Python file to Javascript using the compliant mode, is the following::

  pythonium app.py -o app.py.js

Try it. It will create an empty file.

Add something in the file like a print::

  echo "print('Héllo')" > app.py

And use the previous command to generate ``app.py.js``::

  pythonium app.py -o app.py.js

**If** you have *nodejs*, you can execute the following command::

  cat pythonium.js app.py.js | nodejs

It will print the following::

  Héllo

You can also open ``index.html`` it should also print the same message in the developer console. Refer to your browser documentation to know how to get access to it.
