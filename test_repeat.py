# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

pytest_plugins = "pytester",


class TestRepeat:

    def test_no_repeat(self, testdir):
        testdir.makepyfile("""
            def test_no_repeat():
                pass
        """)
        result = testdir.runpytest('-v', '--count', '1')
        result.stdout.fnmatch_lines([
            '*test_no_repeat.py::test_no_repeat PASSED*',
            '*1 passed*',
        ])
        assert result.ret == 0

    def test_can_repeat(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest('--count', '2')
        result.stdout.fnmatch_lines(['*2 passed*'])
        assert result.ret == 0

    def test_mark_repeat_decorator_is_registered(self, testdir):
        result = testdir.runpytest('--markers')
        result.stdout.fnmatch_lines([
            '@pytest.mark.repeat(n): run the given test function `n` times.'])
        assert result.ret == 0

    def test_mark_repeat_decorator(self, testdir):
        testdir.makepyfile("""
            import pytest
            @pytest.mark.repeat(3)
            def test_mark_repeat_decorator():
                pass
        """)
        result = testdir.runpytest()
        result.stdout.fnmatch_lines(['*3 passed*'])
        assert result.ret == 0

    def test_parametrize(self, testdir):
        testdir.makepyfile("""
            import pytest
            @pytest.mark.parametrize('x', ['a', 'b', 'c'])
            def test_repeat(x):
                pass
        """)
        result = testdir.runpytest('--count', '2')
        result.stdout.fnmatch_lines(['*6 passed*'])
        assert result.ret == 0

    def test_parametrized_fixture(self, testdir):
        testdir.makepyfile("""
            import pytest
            @pytest.fixture(params=['a', 'b', 'c'])
            def parametrized_fixture(request):
                return request.param

            def test_repeat(parametrized_fixture):
                pass
        """)
        result = testdir.runpytest('--count', '2')
        result.stdout.fnmatch_lines(['*6 passed*'])
        assert result.ret == 0

    def test_step_number(self, testdir):
        testdir.makepyfile("""
            import pytest
            expected_steps = iter(range(5))
            def test_repeat(__pytest_repeat_step_number):
                assert next(expected_steps) == __pytest_repeat_step_number
                if __pytest_repeat_step_number == 4:
                    assert not list(expected_steps)
        """)
        result = testdir.runpytest('-v', '--count', '5')
        result.stdout.fnmatch_lines([
            '*test_step_number.py::test_repeat[[]1/5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]2/5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]3/5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]4/5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]5/5[]] PASSED*',
            '*5 passed*',
        ])
        assert result.ret == 0

    def test_invalid_option(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest('--count', 'a')
        assert result.ret == 2

    def test_unittest_test(self, testdir):
        testdir.makepyfile("""
            from unittest import TestCase

            class ClassStyleTest(TestCase):
                def test_this(self):
                    assert 1
        """)
        result = testdir.runpytest('-v', '--count', '2')
        result.stdout.fnmatch_lines([
            '*test_unittest_test.py::ClassStyleTest::test_this PASSED*',
            '*1 passed*',
        ])
