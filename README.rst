***********
Distutilazy
***********

.. image:: https://travis-ci.org/farzadghanei/distutilazy.svg?branch=master
    :target: https://travis-ci.org/farzadghanei/distutilazy

.. image:: https://ci.appveyor.com/api/projects/status/q4lhncemrsnpftgv?svg=true
    :target: https://ci.appveyor.com/project/farzadghanei/distutilazy?branch=master

Extra distutils commands, including:

* clean_pyc: clean compiled python files
* clean_jython_class: clean compiled .class files created by Jython
* clean_all: using ``distutils.clean``, ``clean_pyc`` and ``clean_jython_class`` to clean all temporary files
* bdist_pyinstaller: convenient calls for `PyInstaller <http://www.pyinstaller.org>`_ with sane defaults
* test: run unit tests

An entry point script is also provided to call commands directly, currently only
the clean commands are exposed via the script.

Installation
------------
Use ``pip`` to install from PyPI:

.. code-block:: bash

    $ pip install distutilazy

To install from the source, download the source and run

.. code-block:: bash

    $ python setup.py install

There are no specific dependencies, distutilazy runs on Python 2.7+
(CPython 2.7, 3.3, 3.4, 3.5, 3.6, PyPy 2.6 and PyPy3.5 are tested).
Tests pass on Jython so it should be fine for Jython as well.


How
---
After installing distutilazy, add ``distutilazy.command`` package to the list
of command packages in your ``setup.cfg`` file.

.. code-block:: ini

    [global]
    command_packages = distutilazy.command

That's it. Now you may use new commands directly from your ``setup.py``.

To clean compiled python files:

.. code-block:: bash

    $ python setup.py clean_pyc

To clean all temporary files (build artifacts, compiled files created by CPython or Jython, etc.):

.. code-block:: bash

    $ python setup.py clean_all


Available commands are in ``distutilazy.command`` package, each command as a separate module.

To use custom command names for the same functionality, use command classes defined in distutilazy modules
(each module might define more than a single command class).

The modules should be imported in `setup.py`, then desired classes might be assigned to command names
using the ``cmdclass`` parameter.

.. code-block::

    import distutilazy.clean

    setup(
        cmdclass: {
            'clean_pyc': distutilazy.clean.CleanPyc,
            'clean_jython': distutilazy.clean.CleanJythonClass,
            'clear': distutilazy.clean.CleanAll
        }
    )

To extend (or customize) the behavior of the command classes define a class extending from these command classes,
and use that custom class in ``cmdclass``.

Entry Point Script
^^^^^^^^^^^^^^^^^^
The `distutilazy` script provides a direct access to the commands. call it with
`-h` or `--help` to see available commands. For example this command runs
the `clean_all` command (provided by distutilazy package) directly, even
without a `setup.py` or `setup.cfg`.


.. code-block:: bash

    $ distutilazy clean_all


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

The MIT License (MIT)

Copyright (c) 2014-2018 Farzad Ghanei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
