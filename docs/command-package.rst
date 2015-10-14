***************
Command Package
***************

Distutils allows to specify a package so extra command can be loaded from there.
Each command should be defined in a separate module named after the command, which defines
a class with the same name.

As a convenient method of using Distutilazy commands, a separate :mod:`distutilazy.command`
package is provided. For all the command classes available in Distutilazy, a command module
exists in this package.


Using Command Package
=====================

To use the commands from this package add :mod:`distutilazy.command` package to the list
of `command_packages` in :file:`setup.cfg` file.

.. code-block:: ini

    [global]
    command_packages = distutilazy.command


Commands
========

Available modules (hence commands) are:

* bdist_pyinstaller
* clean_all
* clean_jython_classes
* clean_pyc
* test
