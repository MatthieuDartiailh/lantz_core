# -*- coding: utf-8 -*-
"""
    tests.features.test_alias
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the tools to customize feature and help in their writings.

    :copyright: 2015 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.

"""
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)

import pytest

from lantz_core.has_features import subsystem
from lantz_core.features import Bool
from lantz_core.features.alias import Alias

from ..testing_tools import DummyParent


@pytest.fixture
def tester():
    class AliasTester(DummyParent):

        state = Bool(True, True, mapping={True: True, False: False})
        _state = False

        r_alias = Alias('state')

        sub = subsystem()

        with sub as s:
            s.rw_alias = Alias('.state', True)

        def _get_state(self, feat):
            return self._state

        def _set_state(self, feat, value):
            self._state = value

    return AliasTester()


def test_alias_on_same_level(tester):

    assert tester.r_alias is False
    tester.state = True
    assert tester.r_alias is True

    with pytest.raises(AttributeError):
        tester.r_alias = False


def test_alias_on_parent(tester):

    assert tester.sub.rw_alias is False
    tester.state = True
    assert tester.sub.rw_alias is True

    tester.sub.rw_alias = False
    assert tester.state is False
