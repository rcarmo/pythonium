todo list
#########

This is a small tutorial coming with `Pythonium <https://github.com/pythonium/pythonium>`_ that will help you get started.

Admonition
==========

Pythonium just allows to translate programs written in Python 3 to be run in the browser. So what? So you still need to learn HTML5. This is not difficult, documentation is all over the web `dochub.io <http://dochub.io/>`_ is very nice. `jQuery API <http://api.jquery.com/>`_ is well documented. With the knowledge that you can directly call Javascript objects from Python with Pythonium you can do most of the things. That's why the following don't dive into how to use jQuery or how to build a full blown application but only walk through the step to create a simple todo list.

Enjoy!

Getting Ready
=============

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
      <input type="text"><input type="submit" value="Add">
      <ul id="todos">
      </ul>
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

Jumping
=======

First thing, first we need to be able to add a task. For that matter contains an input field with a button. jQuery is tailored manipulate HTML. The first thing you need is to retrieve HTML nodes, for this, you use `selectors <http://www.w3.org/TR/CSS2/selector.html>`_. Selectors are similar to XPATH, it's specialized for HTML documents. jQuery can be compared is JavaScript class, that once instantiated represents one or several HTML nodes that match the selector given to the constructor. To retrieve the input and the button the following code can be used::

  input = jQuery('[type="text"]')
  button = jQuery('[type="submit"]')

If you write this directly and compile it. It will fail, because jQuery takes a JavaScript string as argument and strings in the source Python are converted to Python strings. This is the same for floats and integers. 

There is several workarounds.

``JS`` special function
-----------------------

First you can tell the compiler that the string is actually JavaScript code, and that it should not try to compile it. For that matter there is special function named ``JS`` which string argument is inlined in the generated code, it can be used in this context as follow::

  input = jQuery(JS("""'[type="text"]'"""))

Mind the extra care needed to handle the different types of quotes. This is a bit ugly, but it allows to bypass the translation process. It can come handy in some situations, where the JavaScript syntax is not compatible with the Python syntax. For instance there is no new keyword in Python, so the following valid Javascript code::

  now = new Date()

The above is invalid in code written to be compiled by Pythonium. You can use the ``JS`` function to circuvent this limitation as follow::

  now = JS('new Date()')

This looks pretty good. And you can call ``now`` methods transparently from Python::

  year = now.getFullYear()

``year`` is now, the current year as a **JavaScript integer**. 

You must be carful when interacting with JavaScript objects, depending on what you need, to convert to Python and call Python methods and keep them as JavaScript objects and call JavaScript methods. Mind the fact that the following code will fail::

  delta = Date.now() - Date.now()

Because the compiler only knows how to call methods, it can find out whether one object is a native JavaScript object and call its JavaScript method. But it can not convert automatically JavaScript objects to their Python version on-the-fly. In this case, Pythonium will try to call ``__add__`` method of the JavaScript integer returned by ``Date.now()`` and will fail, because it doesn't exists.

Anyway, if you really want do the above operation you can use ``JS`` function::

  delta = JS('Date.now() - Date.now()')

But ``delta`` will still be a JavaScript object. It's possible to convert the JavaScript integer to a Python integer with the following code::

  year = int(JS('Date.now() - Date.now()'))

``list``, ``dict``, ``int`` and ``float`` can be used in a similar fashion.

``jstype`` function
-------------------

``jstype`` allows to convert a Python type to a JavaScript object, it can be used to solve the above problem as follow::

  input = jQuery(jstype('[type="text"]'))

Solution
--------

Let's define a another ``jQuery`` function that automatically convert it argument to a JavaScript string, since that's what we will use all the time::

  def jQuery(selector):
      return __DOLLAR__(jstype(selector))

``__DOLLAR__`` is replaced by the ``$`` character anywhere it's found. ``$`` is another name of the jQuery object.

At this point ``app.py`` is::

  def jQuery(selector):
      return __DOLLAR__(jstype(selector))
  
  input = jQuery('[type="text"]')
  button = jQuery('[type="submit"]')


Call me back!
=============

Frontend dev is full of callbacks. At least when you don't use ``yield`` or ``yield from``. When the user clicks on the button we want to check the content of field and if it has content, add the content as a task. Let's define an ``on_click`` function::

  def on_click(event):
      # event is JavaScript Event
      text = str(input.val())  # convert the JavaScript string to a Python string
      if len(text):
          add_todo(text)

To attach this method to ``button``, use its ``click`` method::

  button.click(on_click)

add a todo
==========

Add todo takes a str and need to add it to list of todos. First we need to fetch the list of todos::

  todos = jQuery("#todos")

Then a new ``li`` node must be added to the dom. For that matter we write a string of html with what we want to add to ``ul``::

  li = '<li>' + text + '</li>'

Now add it to the dom, for that let's use `jQuery.append <http://api.jquery.com/append/>`_,
append expects a JavaScript string so we need to convert li to javascript first::

  li = jstype(li)
  todos.append(li)

Done!

Checkout ``app.py`` file for the complete solution.

Diving
======

Read `MDN <https://developer.mozilla.org/en-US/>`_, `webplatform <http://docs.webplatform.org/>`_ and create beautiful things :-)
