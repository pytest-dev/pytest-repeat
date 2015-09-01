pytest-repeat
===================

pytest-repeat is a plugin for `py.test <http://pytest.org>`_ that makes it easy
to repeat a single test, or multiple tests, a specific number of times.

.. image:: https://img.shields.io/pypi/l/pytest-repeat.svg
   :target: https://github.com/bobsilverberg/pytest-repeat/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-repeat.svg
   :target: https://pypi.python.org/pypi/pytest-repeat/
   :alt: PyPI
.. image:: https://img.shields.io/travis/bobsilverberg/pytest-repeat.svg
   :target: https://travis-ci.org/bobsilverberg/pytest-repeat/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/bobsilverberg/pytest-repeat.svg
   :target: https://github.com/bobsilverberg/pytest-repeat/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/bobsilverberg/pytest-repeat.svg
   :target: https://requires.io/github/bobsilverberg/pytest-repeat/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-repeat:

- Python 2.6, 2.7, 3.2, 3.3, 3.4 or PyPy
- py.test 2.4 or newer

Installation
------------
To install pytest-repeat::

  pip install pytest-repeat

Repeating a test
----------------

Use the :code:`--count` command line option to specify how many times you want
your test, or tests, to be run::

  py.test --count=10 test_file.py

Each test collected by py.test will be run :code:`count` times.

Resources
---------

- `Issue Tracker <http://github.com/bobsilverberg/pytest-repeat/issues>`_
- `Code <http://github.com/bobsilverberg/pytest-repeat/>`_
