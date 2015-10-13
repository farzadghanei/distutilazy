***************
Command Classes
***************

Command classes are where the functionality of each command is implemented. Multiple command classes
can be defined in a single module, for example the :mod:`distutilazy.clean` defines:

* :class:`~distutilazy.clean.CleanPyc`: Clean compiled files created by CPython (.pyc files and __pycache__ directories)
* :class:`~distutilazy.clean.CleanJythonClass`: Clean compiled .class files created by Jython
* :class:`~distutilazy.clean.CleanAll`: Clean all temporary file (compiled files, build and dist directories, etc.)


Using Command Classes
=====================
To use command classes, pass the classes (or custom classes extending them) as ``cmdclass`` argument
of :func:`setup` function in :file:`setup.py` file.

.. code-block:: python

    import distutilazy.clean.CleanAll
    import distutilazy.test.RunTests
    from distutils.core import setup

    setup(
        cmdclass= {
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


Or create a custom class, to extend the ones provided by default:

.. code-block:: python

    from import distutilazy.clean import CleanAll
    from distutils.core import setup

    class MyCleaner(CleanAll):
        pass

    setup(
        cmdclass= {
            "clear": MyCleaner
        }
    )


All the command classes extend from :class:`distutils.core.Command` class, and they provide these methods:

.. method:: initialize_options()

    Initialize options of the command (as attributes of the object).
    This is called by `distutils.core.Command` after the command
    object has been constructed.

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

        Command option, the path to root directory where cleaning process would affect.
        (default is current path).

    .. data:: extensions

        Command option, a comma separated string of file extensions that will be cleaned

    .. data:: directories

        Command option, a comma separated string of directory names that will be cleaned
        recursively from root path

    .. method:: default_extensions()

        Return list of file extensions that are used for compiled Python files

    .. method:: default_directories()

        Return list of directory names that are used to store compiled Python files

    .. method:: find_compiled_files()

        Return list of absolute paths of all compiled Python files found from
        the :attr:`~CleanPyc.root` directory recursively.

    .. method:: find_cache_directories()

        Return list of absolute paths of all cache directories found from
        the :attr:`~distutilazy.clean.CleanPyc.root` directory recursively.

.. class:: clean_pyc

    Alias to :class:`~distutilazy.clean.CleanPyc`


.. class:: CleanJythonClass

    Command class to clean compiled class files created by Jython

    .. data:: root

        Command option, the path to root directory where cleaning process would affect.
        (default is current path).

    .. data:: extensions

        Command option, a comma separated string of file extensions that will be cleaned

    .. data:: directories

        Command option, a comma separated string of directory names that will be cleaned
        recursively from root path

    .. method:: default_extensions()

        Return list of file extensions that are used for compiled class files

    .. method:: default_directories()

        Return list of directory names that are used to store class files

    .. method:: find_class_files()

        Return list of absolute paths of all compiled class files found from
        the :attr:`~distutilazy.clean.CleanJythonClass.root` directory recursively.


.. class:: CleanAll

    Command class to clean all temporary files (compiled files created by Jython, CPython),
    build and dist directories, etc.

    .. data:: root

        Command option, the path to root directory where cleaning process would affect.
        (default is current path).

    .. data:: extensions

        A command option, a comma separated string of file extensions that will be cleaned

    .. data:: directories

        Command option, a comma separated string of directory names that will be cleaned
        recursively from root path

    .. method:: default_extensions()

        Return list of file extensions that are used for file extensions to be cleaned
        by default.

    .. method:: default_directories()

        Return list of directory names that are going to be cleaned by default.


.. class:: clean_all

    Alias to :class:`~distutilazy.clean.CleanAll`


:mod:`distutilazy.test` -- Class command to run unit tests
==========================================================

.. module:: distutilazy.test
    :synopsis: Define command class to run unit tests
.. moduleauthor:: Farzad Ghanei

.. function:: test_suite_for_modules(modules) -> unittest.TestSuite

    Return a test suite containing test cases found in all the specified modules.


.. class:: RunTests

    Command class to find test cases and run them (using standard library :mod:`unittest`)

    .. data:: root

        Command option, the path to root directory to find test modules from.
        If this path is a package and provides ``__all__``, then this list
        is considered as the list of test modules and no more search happens
        for other files (Default is "tests").

    .. data:: pattern

        Command option, a Unix file name pattern (like :mod:`fnmatch`) to match
        tests files with.
        This is used when no files are specified to run, and the
        :attr:`~distutilazy.test.RunTests.root` is
        not a package that specifies the tests with its ``__all__`` attr
        (Default is "test*.py").

    .. data:: files

        Command option, a comma separated string of file names to search for
        test cases. If specified, only the test cases in these files run.

    .. data:: verbosity

        Command option, an integer (1 .. 3) specifying the verbosity of the test runner
        (Default is 1).

    .. method:: get_modules_from_files(files)

        Accept a list of file paths, import them as modules and return
        a list of module objects.

    .. method:: find_test_modules_from_package_path(self, package_path)

        Find modules from the package specified by package_path ``__all__`` attr,
        import them and return the modules.

    .. method:: find_test_modules_from_test_files(self, root, pattern)

        Find files whose name matches the ``pattern`` from the ``root`` path,
        then import them and return the modules.

    .. method:: get_test_runner()

        Return a `TestRunner` to run the test suite, configured with the
        :attr:`~distutilazy.test.RunTests.verbosity` option.

.. class:: run_tests

    Alias to :class:`~distutilazy.test.RunTests`

