Cybele
======

A simple monitor which summarises multiple logs. Comes with a web app for
viewing.

Usage
~~~~~

Cybele monitor
--------------

::

    usage: cybele-monitor [-h] [--output OUTPUT] [input [input ...]]

    positional arguments:
      input            absolute file path(s) of the log(s) to be watched

    optional arguments:
      -h, --help       show this help message and exit
      --output OUTPUT  path to output directory [~/.cybele]

    The `monitor` module runs as a continuing process which reads a
    number of log files. It produces a summary of each and places the
    summary in a configured location.

    The module also defines two API functions to access the summary
    files:

        * get_channels
        * get_summary

Cybele viewer
-------------

::

    usage: cybele-viewer [-h] [--input INPUT] [-v]

    optional arguments:
      -h, --help     show this help message and exit
      --input INPUT  path to input directory [~/.cybele]
      -v, --verbose  increase the verbosity of output

    The `viewer` module runs as a web service on your local host (port 5000).
    It displays the summaries of monitored files.

Develop on Linux
~~~~~~~~~~~~~~~~

Make a virtual environment of Python 2.7::

    $ virtualenv -p python2.7 pyenv2.7

Install Flask::

    $ ./pyenv2.7/bin/pip install Flask

Run the tests from the project directory::

    $ ./pyenv2.7/bin/python -m unittest discover -v cybele

Run on Windows
~~~~~~~~~~~~~~

Install Python 2.7
------------------

1.  Download and install python-2.7.5.msi_ from the Python website. In
    this example, we install to `C:\\Users\\Demo\\Python2.7.5`.

2.  Download and install the `setuptools binary package`_ and the
    `binary package for pip`_. Pick the right ones for your architecture.
    I tested with `setuptools-0.7.8.win-amd64-py2.7.exe` and
    `pip-1.3.1.win-amd64-py2.7.exe`.

3.  Install `virtualenv`::

        C:\Users\Demo>Python2.7.5\Scripts\pip.exe install virtualenv

Create a virtualenv
-------------------

4.  Create a virtual build environment by running these commands::

        C:\Users\Demo>Python2.7.5\Scripts\virtualenv.exe pyenv2.7
        C:\Users\Demo>pyenv2.7\Scripts\pip.exe install Flask

Install the project code
------------------------

5.  Download and unzip the `project code`_ which will create a directory called
    `cybele-master`. Change to this directory and install the `cybele` package::

        C:\Users\Demo\Downloads\cybele-master\cybele-master>C:\Users\Demo\pyenv2.7\Scripts\python.exe setup.py install

    You will find ``cybele-monitor.exe`` and ``cybele-viewer.exe`` in
    `C:\\Users\\Demo\\pyenv2.7\\Scripts`. They work the same way as their Linux
    counterparts.

.. _python-2.7.5.msi: http://python.org/ftp/python/2.7.5/python-2.7.5.msi
.. _setuptools binary package: http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
.. _binary package for pip: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip
.. _project code: https://github.com/Atalanta/cybele/archive/master.zip
