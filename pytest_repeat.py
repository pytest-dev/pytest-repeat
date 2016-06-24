# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def pytest_addoption(parser):
    parser.addoption(
        '--count',
        action='store',
        default='1',
        type='int',
        help='Number of times to repeat each test')


def pytest_generate_tests(metafunc):
    count = metafunc.config.option.count
    if count > 1:
        metafunc.fixturenames.append('tmp_ct')
        metafunc.parametrize('tmp_ct', range(count))
