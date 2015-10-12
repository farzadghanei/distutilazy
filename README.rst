***********
Distutilazy
***********

.. image:: https://travis-ci.org/farzadghanei/distutilazy.svg?branch=master
    :target: https://travis-ci.org/farzadghanei/distutilazy

Extra distutils commands, including:

 - clean_pyc: clean compiled python files
 - clean_jython_class: clean compiled .class files created by Jython
 - clean_all: using ``distutils.clean``, ``clean_pyc`` and ``clean_jython_class`` to clean all temporary files
 - bdist_pyinstaller: convenient calls for `PyInstaller <http://www.pyinstaller.org>`_ with sane defaults
 - test: run unit tests


How
---
Make sure distutilazy package is in ``sys.path``, then add ``distutilazy.command`` package
to the list of command packages in your ``setup.cfg`` file.

::

    [global]
    command_packages = distutilazy.command

That's it. now you may use new commands directly from your ``setup.py``:

To clean compiled python files from the project:

.. code-block:: bash

    $ python setup.py clean_pyc


To run unit tests (by default runs tests/test*.py files):

.. code-block:: bash

    $ python setup.py test

Available commands are in ``distutilazy.command`` package, each command as a separate module.

To use custom command names for the same functionality, use command classes defined in distutilazy modules
(each module might define more than a single command class).

The modules should be imported in `setup.py`, then desired classes might be assigned to command names using the ``cmdclass`` parameter.

::

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


License
-------
Distutilazy is released under the terms of `MIT license <http://opensource.org/licenses/MIT>`_.
