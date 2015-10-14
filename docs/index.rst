***************************************
Welcome to Distutilazy's documentation!
***************************************

Contents:

.. toctree::
   :maxdepth: 2

   command-classes
   commands-package


Introduction
============

Extra distutils commands, including:

* clean_pyc: clean compiled python files
* clean_jython_class: clean compiled .class files created by Jython
* clean_all: using ``distutils.clean``, ``clean_pyc`` and ``clean_jython_class`` to clean all temporary files
* bdist_pyinstaller: convenient calls for `PyInstaller <http://www.pyinstaller.org>`_ with sane defaults
* test: run unit tests

Installation
============

Use ``pip`` to install from PyPI:

.. code-block:: bash

    $ pip install distutilazy

To install from the source, download the source and run

.. code-block:: bash

    $ python setup.py install

There are no specific dependencies, it runs on Python 2.7+
(CPython 2.7, 3.2, 3.3, 3.4 and 3.5, PyPy 2.6 and PyPy3 2.4 are tested).
Tests pass on Jython so it should be fine for Jython as well.


How
===

After installing distutilazy, add :mod:`distutilazy.command` package to the list
of command packages in your ``setup.cfg`` file.

.. code-block:: ini

    [global]
    command_packages = distutilazy.command

That's it. Now you may use new commands directly from your ``setup.py``.

To run unit tests (using standard library ``unittest``) in your project
(by default runs `tests/test*.py` files from current path):

.. code-block:: bash

    $ python setup.py test

To clean compiled python files:

.. code-block:: bash

    $ python setup.py clean_pyc

To clean all temporary files (build artifacts, compiled files created by CPython or Jython, etc.):

.. code-block:: bash

    $ python setup.py clean_all

Available commands are in :mod:`distutilazy.command` package, each command as a separate module.

Development
-----------

* Code is hosted on `GitHub <https://github.com/farzadghanei/distutilazy>`_.
* Documentations are on `Read The Docs <https://distutilazy.readthedocs.org>`_.


Tests
^^^^^

If you have make available

.. code-block:: bash

    $ make test

You can always use ``setup.py`` to run tests:

.. code-block:: bash

    $ python setup.py test


License
-------

Distutilazy is released under the terms of `MIT license <http://opensource.org/licenses/MIT>`_.
