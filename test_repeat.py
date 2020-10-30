# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.

import pytest

pytest_plugins = "pytester",


class TestRepeat:

    def test_no_repeat(self, testdir):
        testdir.makepyfile("""
            def test_no_repeat(request):
                fixtures = request.fixturenames
                assert "__pytest_repeat_step_number" not in fixtures
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

    def test_mark_repeat_decorator_repeat_once(self, testdir):
        testdir.makepyfile("""
            import pytest
            @pytest.mark.repeat(1)
            def test_mark_repeat_decorator_repeat_once():
                pass
        """)
        result = testdir.runpytest('--count', '10')
        result.stdout.fnmatch_lines(['*1 passed*'])
        assert result.ret == 0

    def test_parametrize(self, testdir):
        testdir.makepyfile("""
            import pytest
            @pytest.mark.parametrize('x', ['a', 'b', 'c'])
            def test_repeat(x):
                pass
        """)
        result = testdir.runpytest('-v', '--count', '2')
        result.stdout.fnmatch_lines([
            '*test_parametrize.py::test_repeat[[]a-1-2[]] PASSED*',
            '*test_parametrize.py::test_repeat[[]a-2-2[]] PASSED*',
            '*test_parametrize.py::test_repeat[[]b-1-2[]] PASSED*',
            '*test_parametrize.py::test_repeat[[]b-2-2[]] PASSED*',
            '*test_parametrize.py::test_repeat[[]c-1-2[]] PASSED*',
            '*test_parametrize.py::test_repeat[[]c-2-2[]] PASSED*',
            '*6 passed*',
        ])
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
            '*test_step_number.py::test_repeat[[]1-5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]2-5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]3-5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]4-5[]] PASSED*',
            '*test_step_number.py::test_repeat[[]5-5[]] PASSED*',
            '*5 passed*',
        ])
        assert result.ret == 0

    def test_invalid_option(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest('--count', 'a')
        assert result.ret == 4

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

    @pytest.mark.parametrize(['scope', 'lines'], [
        ('session', [
            '*test_1.py::test_repeat1[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat1[[]2-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]2-2[]] PASSED*',
            '*16 passed*',
        ]),
        ('module', [
            '*test_1.py::test_repeat1[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat1[[]2-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]2-2[]] PASSED*',
            '*16 passed*',
        ]),
        ('class', [
            '*test_1.py::test_repeat1[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat1[[]2-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]2-2[]] PASSED*',
            '*16 passed*',
        ]),
        ('function', [
            '*test_1.py::test_repeat1[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat1[[]2-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]1-2[]] PASSED*',
            '*test_1.py::test_repeat2[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat3[[]2-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]1-2[]] PASSED*',
            '*test_2.py::test_repeat4[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat5[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat1::test_repeat6[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat7[[]2-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]1-2[]] PASSED*',
            '*test_3.py::TestRepeat2::test_repeat8[[]2-2[]] PASSED*',
            '*16 passed*',
        ]),
    ])
    def test_scope(self, testdir, scope, lines):
        testdir.makepyfile(test_1="""
            def test_repeat1():
                pass

            def test_repeat2():
                pass
        """)
        testdir.makepyfile(test_2="""
            def test_repeat3():
                pass

            def test_repeat4():
                pass
        """)
        testdir.makepyfile(test_3="""
            class TestRepeat1(object):
                def test_repeat5(self):
                    pass
                def test_repeat6(self):
                    pass
            class TestRepeat2(object):
                def test_repeat7(self):
                    pass
                def test_repeat8(self):
                    pass
        """)
        result = testdir.runpytest('-v', '--count', '2', '--repeat-scope',
                                   scope)
        result.stdout.fnmatch_lines(lines)
        assert result.ret == 0

    def test_omitted_scope(self, testdir):
        testdir.makepyfile("""
            def test_repeat1():
                pass

            def test_repeat2():
                pass
        """)
        result = testdir.runpytest('-v', '--count', '2')
        result.stdout.fnmatch_lines([
            '*test_omitted_scope.py::test_repeat1[[]1-2[]] PASSED*',
            '*test_omitted_scope.py::test_repeat1[[]2-2[]] PASSED*',
            '*test_omitted_scope.py::test_repeat2[[]1-2[]] PASSED*',
            '*test_omitted_scope.py::test_repeat2[[]2-2[]] PASSED*',
            '*4 passed*',
        ])
        assert result.ret == 0

    def test_invalid_scope(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest('--count', '2', '--repeat-scope', 'a')
        assert result.ret == 4
