# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

pytest_plugins = "pytester",


class TestRepeat:

    def test_no_repeat(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest()
        result.stdout.fnmatch_lines(['*1 passed*'])
        assert result.ret == 0

    def test_can_repeat(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest('--count', '2')
        result.stdout.fnmatch_lines(['*2 passed*'])
        assert result.ret == 0

    def test_invalid_option(self, testdir):
        testdir.makepyfile("""
            def test_repeat():
                pass
        """)
        result = testdir.runpytest('--count', 'a')
        assert result.ret == 2
