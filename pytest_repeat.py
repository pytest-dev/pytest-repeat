# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
import copy
import warnings
from collections import OrderedDict
from unittest import TestCase

import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--count',
        action='store',
        default=1,
        type=int,
        help='Number of times to repeat each test')

    parser.addoption(
        '--repeat-scope',
        action='store',
        default='function',
        type=str,
        choices=('function', 'class', 'module', 'session'),
        help='Scope for repeating tests')


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'repeat(n): run the given test function `n` times.')


_REPEAT_FIXTURE = "__pytest_repeat_step_number"
_REPEAT_STEP = "__pytest_repeat_step_number"


@pytest.fixture()
def __pytest_repeat_step_number(request):
    return getattr(request.node, _REPEAT_STEP, None)


def _get_repeat_count(item):
    marker = item.get_closest_marker('repeat')
    if marker is not None:
        return int(marker.args[0])
    return item.config.option.count


def _make_repeat_name(item, step, count):
    progress_id = f'{step + 1}-{count}'
    if item.name.endswith(']'):
        return f'{item.name[:-1]}-{progress_id}]'
    return f'{item.name}[{progress_id}]'


def _copy_item_state(item, clone):
    clone.own_markers = list(item.own_markers)
    clone.extra_keyword_matches = set(item.extra_keyword_matches)
    clone.user_properties = list(item.user_properties)
    clone._report_sections = list(item._report_sections)
    clone.fixturenames = list(item.fixturenames)
    if _REPEAT_FIXTURE not in clone.fixturenames:
        clone.fixturenames.append(_REPEAT_FIXTURE)

    clone.keywords = copy.copy(item.keywords)
    if hasattr(clone.keywords, '_markers'):
        clone.keywords._markers = dict(item.keywords._markers)
        clone.keywords._markers.pop(item.name, None)
        clone.keywords._markers[clone.name] = True
    if hasattr(clone.keywords, 'node'):
        clone.keywords.node = clone
    if hasattr(clone.keywords, 'parent'):
        clone.keywords.parent = clone.parent

    if hasattr(item, 'stash'):
        clone.stash = copy.copy(item.stash)
        clone.stash._storage = dict(item.stash._storage)
        if hasattr(clone, '_store'):
            clone._store = clone.stash

    clone._initrequest()


def _clone_item(item, step, count):
    clone = copy.copy(item)
    clone.name = _make_repeat_name(item, step, count)
    clone._nodeid = f'{item.parent.nodeid}::{clone.name}'
    _copy_item_state(item, clone)
    setattr(clone, _REPEAT_STEP, step)
    return clone


def _expand_item(item):
    count = _get_repeat_count(item)
    if count <= 1:
        return [item]
    if not isinstance(item, pytest.Function):
        return [item]
    if item.cls is not None and issubclass(item.cls, TestCase):
        warnings.warn("Repeating unittest class tests not supported")
        return [item]
    return [_clone_item(item, step, count) for step in range(count)]


def _scope_key(item, scope):
    if scope == 'session':
        return item.session
    if scope == 'module':
        return item.getparent(pytest.Module)
    if scope == 'class':
        return item.getparent(pytest.Class) or item.getparent(pytest.Module)
    return item


def _expand_scope(items, scope):
    groups = OrderedDict()
    for item in items:
        groups.setdefault(_scope_key(item, scope), []).append(item)

    expanded = []
    for group in groups.values():
        repeated = [(item, _expand_item(item)) for item in group]
        max_count = max((len(repeats) for _, repeats in repeated), default=0)
        for step in range(max_count):
            for _, repeats in repeated:
                if step < len(repeats):
                    expanded.append(repeats[step])
    return expanded


def _update_terminal_collection_count(config, items):
    terminal = config.pluginmanager.getplugin('terminalreporter')
    if terminal is None or not hasattr(terminal, '_numcollected'):
        return
    deselected = len(terminal.stats.get('deselected', ()))
    terminal._numcollected = len(items) + deselected


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    yield
    scope = config.option.repeat_scope
    if scope == 'function':
        items[:] = [repeat for item in items for repeat in _expand_item(item)]
    else:
        items[:] = _expand_scope(items, scope)
    session.testscollected = len(items)
    _update_terminal_collection_count(config, items)
