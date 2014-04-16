Distutilazy
===========

Extra distutils commands, including:

 - clean_pyc: clean compiled python files
 - clean_all: using distutils.clean and clean_pyc to clean all temporary files
 - pyinstaller: convinient calls for `PyInstaller <http://www.pyinstaller.org>`_ with sane defaults

How
---
Make sure distutilazy package is in sys.path, then add ``distutilazy.command`` package to the list of command packages in your ``setup.cfg`` file.

::

    [global]
    command-packages = distutilazy.command

That's it. now you may use new commands direclty from your ``setup.py``:

.. code-block:: bash

    $ python setup.py clean_pyc

Available commands are in distutilazy.command package as separate modules.

A more detailed way is to use command classes, defined in distutilazy package root modules. Each module might define
more than a single command class.

The modules should be imported in setup.py, then desired classes might be assigned to command names using the ``cmdclasses`` parameter.

::

    import distutilazy.clean

    setup(
        cmdclass: {'clean_pyc': distutilazy.clean.clean_pyc}
    )

License
-------
Distutilazy is released under the temrs of `MIT license <http://opensource.org/licenses/MIT>`_.
