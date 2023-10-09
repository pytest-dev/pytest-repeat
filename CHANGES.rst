Release Notes
-------------

**0.9.3 (2023-Oct-9)**

* No externally visible changes.
* Internal changes. 
  * Add tox and CI testing on Python 3.12
  * Add legacy pytest versions to CI.
  * Now testing pytest 4, 5, 6
  * Non-legacy testing uses pytest 7
  * setup.py -> pyproject.toml
  * using hatchling backend

**0.9.2 (2023-Oct-1)**

* Migrate CI to GitHub Actions
* Officially Support Python 3.7+

**0.9.1 (2020-10-31)**

* Using ``@pytest.mark.repeat(1)`` can now be used to disable repeating a test regardless of the ``--count`` parameter given in the command-line.

* Python 3.4 is no longer officially supported.

**0.9.0 (-)**

* Not released do PyPI due to a deploy problem.

**0.8.0 (2019-02-26)**

* Fix mark deprecation warnings in new pytest versions.

* ``pytest-repeat`` now requires pytest>=3.6.

**0.7.0 (2018-08-23)**

* Move step number to the end of the parametrisation ID

  * Thanks to `@gdyuldin <https://github.com/gdyuldin>`_ for suggesting
    this enhancement and providing a patch

**0.6.0 (2018-08-01)**

* Add option for controlling the scope of the repeat parameterisation

  * Thanks to `@gdyuldin <https://github.com/gdyuldin>`_ for suggesting
    this enhancement and providing a patch

**0.5.0 (2018-07-19)**

* Allow repeating a test using a decorator  (`#16 <https://github.com/pytest-dev/pytest-repeat/issues/16>`_)

  * Thanks to `@Peque <https://github.com/Peque>`_ for suggesting
    this enhancement and providing a patch

**0.4.0 (2016-08-25)**

* No changes - testing deploy to PyPI from Travis CI

**0.4.0 (2016-08-09)**

* Fix deprecation warning present in pytest 3.0 for type argument in addoption

**0.3.0 (2016-06-30)**

* Added support for repeating parameterised tests

**0.2 (2015-10-27)**

* README updates

**0.1 (2015-10-19)**

* Initial release
