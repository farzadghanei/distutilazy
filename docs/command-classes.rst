***************
Command Classes
***************

Command classes are where the functionality of each command is implemented. Mutiple command classes
can be defined in a single module (for example the :mod:`distutilazy.clean` module, defines:

* :class:`~distutilazy.clean.CleanPyc`: Clean compiled files created by CPython (.pyc files and __pycache__ directories)
* :class:`~distutilazy.clean.CleanJythonClass`: Clean compiled .class files created by Jython
* :class:`~distutilazy.clean.CleanAll`: Clean all temporary file (compiled files, build and dist directories, etc.)


Using Command Classes
=====================
To use command classes, it's possible to pass them directly for ``cmdclass`` argument of :func:`setup` function,
or define another class that extends these command classes (may customize the behavior as required), and
use that custom class with ``cmdclass`` for :func:`setup`.

To use the command classes directly for :func:`setup`, modify the :file:`setup.py`:

.. code-block:: python

    import distutilazy.clean.CleanAll
    import distutilazy.test.RunTests
    from distutils.core import setup

    setup(
        cmdclasses= {
            "clear": distutilazy.clean.CleanAll,
            "unittests": distutilazy.test.RunTests
        }
    )


Now to run tests, run this command

.. code-block:: bash

    $ python setup.py unittests


To remove all temporary files run

.. code-block:: bash

    $ python setup.py clear


Extending the classes:

.. code-block:: python

    from import distutilazy.clean import CleanAll
    from distutils.core import setup

    class MyCleaner(CleanAll):
        pass

    setup(
        cmdclasses= {
            "clear": MyCleaner
        }
    )


All the command classes extend from :class:`distutils.core.Command` class, and they provide these methods:

.. method:: initialize_options()

    Initialize options of the command (as attributes of the object).
    This is called by `distutils.core.Command` after the command
    objet has been constructed.

.. method:: finalize_options()

    Finalize options of the command (for example to do validation)
    This is called by `distutils.core.Command` before `run` is called.

.. method:: run()

    Executes the command with current options state


Here we introduce available modules, and classes they provide.

:mod:`distutilazy.clean` -- Class commands to clean temporary files
===================================================================

.. module:: distutilazy.clean
    :synopsis: Define command classes to clean temporary files
.. moduleauthor:: Farzad Ghanei

.. class:: CleanPyc

    Command class to clean compiled and cached files created by CPython

    .. data:: root

        A command option, the path to root directory where cleaning process would affect.
        (default is currenct path).

    .. data:: extensions

        A command option, a comma separated string of file extensions that will be cleand

    .. data:: directories

        A command option, a comma separated string of directory names that will be cleaned
        recursively from root path

    .. method:: default_extensions()

        Returns list of file extensions that are used for compiled Python files

    .. method:: default_directories()

        Returns list of directory names that are used to store compiled Python files

    .. method:: find_compiled_files()

        Returns list of absolute paths of all compiled Python files found from
        the :attr:`~CleanPyc.root` directory recursively.

    .. method:: find_cache_directories()

        Returns list of absolute paths of all cache directories found from
        the :attr:`~CleanPyc.root` directory recursively.

.. class:: clean_pyc

    Alias to CleanPyc


.. class:: CleanJythonClass

    Command class to clean compiled class files created by Jython

    .. data:: root

        A command option, the path to root directory where cleaning process would affect.
        (default is currenct path).

    .. data:: extensions

        A command option, a comma separated string of file extensions that will be cleand

    .. data:: directories

        A command option, a comma separated string of directory names that will be cleaned
        recursively from root path

    .. method:: default_extensions()

        Returns list of file extensions that are used for compiled class files

    .. method:: default_directories()

        Returns list of directory names that are used to store class files

    .. method:: find_class_files()

        Returns list of absolute paths of all compiled class files found from
        the :attr:`~CleanPyc.root` directory recursively.
