# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import warnings
from unittest import TestCase

import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--count',
        action='store',
        default=1,
        type=int,
        help='Number of times to repeat each test')


class UnexpectedError(Exception):
    pass


@pytest.fixture(autouse=True)
def __pytest_repeat_step_number(request):
    if request.config.option.count > 1:
        try:
            return request.param
        except AttributeError:
            if issubclass(request.cls, TestCase):
                warnings.warn(
                    "Repeating unittest class tests not supported")
            else:
                raise UnexpectedError(
                    "This call couldn't work with pytest-repeat. "
                    "Please consider raising an issue with your usage.")


def pytest_generate_tests(metafunc):
    """
    Use command line option or test case decorator "repeat" to configure number of time each test case is repeated
    Sample decorator: @pytest.mark.repeat(2)
    :param metafunc: Metafunc objects are passed to the pytest_generate_tests
    hook. They help to inspect a test function and to generate tests
    according to test configuration or values specified in the class
    or module where a test
    function is defined.
    :return:
    """
    count = metafunc.config.option.count
    if hasattr(metafunc.function, 'repeat'):
        mark = metafunc.function.repeat
        if len(mark.args) > 0 and isinstance(mark.args[0], int):
            count = metafunc.function.repeat.args[0]

    if count > 1:

        def make_progress_id(i, n=count):
            return '{0}/{1}'.format(i + 1, n)

        metafunc.parametrize(
            '__pytest_repeat_step_number',
            range(count),
            indirect=True,
            ids=make_progress_id,
        )
