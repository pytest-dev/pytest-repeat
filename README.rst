pytest-repeat
===================

pytest-repeat is a plugin for `pytest <https://docs.pytest.org>`_ that makes it
easy to repeat a single test, or multiple tests, a specific number of times.

|license| |python| |version| |anaconda| |ci| |issues|

.. |license| image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/pytest-dev/pytest-repeat/blob/master/LICENSE

.. |version| image:: http://img.shields.io/pypi/v/pytest-repeat.svg
  :target: https://pypi.python.org/pypi/pytest-repeat

.. |anaconda| image:: https://img.shields.io/conda/vn/conda-forge/pytest-repeat.svg
    :target: https://anaconda.org/conda-forge/pytest-repeat

.. |ci| image:: https://github.com/pytest-dev/pytest-repeat/workflows/test/badge.svg
  :target: https://github.com/pytest-dev/pytest-repeat/actions

.. |python| image:: https://img.shields.io/pypi/pyversions/pytest-repeat.svg
  :target: https://pypi.python.org/pypi/pytest-repeat/

.. |issues| image:: https://img.shields.io/github/issues-raw/pytest-dev/pytest-repeat.svg
   :target: https://github.com/pytest-dev/pytest-repeat/issues


Requirements
------------

You will need the following prerequisites in order to use pytest-repeat:

- Python 3.9+ or PyPy3
- pytest 5 or newer

Installation
------------
To install pytest-repeat:

.. code-block:: bash

  $ pip install pytest-repeat

Repeating a test
----------------

Use the :code:`--count` command line option to specify how many times you want
your test, or tests, to be run:

.. code-block:: bash

  $ pytest --count=10 test_file.py

Each test collected by pytest will be run :code:`count` times.

If you want to mark a test in your code to be repeated a number of times, you
can use the :code:`@pytest.mark.repeat(count)` decorator:

.. code-block:: python

   import pytest


   @pytest.mark.repeat(3)
   def test_repeat_decorator():
       pass

If you want to override default tests executions order, you can use :code:`--repeat-scope`
command line option with one of the next values: :code:`session`,  :code:`module`, :code:`class` or :code:`function` (default).
It behaves like a scope of the pytest fixture.

:code:`function` (default) scope repeats each test :code:`count` or :code:`repeat` times before executing next test.
:code:`session` scope repeats whole tests session, i.e. all collected tests executed once, then all such tests executed again and etc.
:code:`class` and :code:`module` behaves similar :code:`session` , but repeating set of tests is a tests from class or module, not all collected tests.

Repeating a test until failure
------------------------------

If you are trying to diagnose an intermittent failure, it can be useful to run the same
test over and over again until it fails. You can use pytest's :code:`-x` option in
conjunction with pytest-repeat to force the test runner to stop at the first failure.
For example:

.. code-block:: bash

  $ pytest --count=1000 -x test_file.py

This will attempt to run test_file.py 1000 times, but will stop as soon as a failure
occurs.

UnitTest Style Tests
--------------------

Unfortunately pytest-repeat is not able to work with unittest.TestCase test classes.
These tests will simply always run once, regardless of :code:`--count`, and show a warning.

Resources
---------

- `Release Notes <https://github.com/pytest-dev/pytest-repeat/blob/master/CHANGES.rst>`_
- `Issue Tracker <https://github.com/pytest-dev/pytest-repeat/issues>`_
- `Code <https://github.com/pytest-dev/pytest-repeat/>`_
