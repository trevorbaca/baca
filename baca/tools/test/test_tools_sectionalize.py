# -*- coding: utf-8 -*-
import baca


def test_tools_sectionalize_01():

    result = baca.tools.sectionalize(20, (1, 1, 1))
    assert result == [6, 1, 6, 1, 6]

    result = baca.tools.sectionalize(97, (1, 1, 1))
    assert result == [32, 1, 31, 1, 32]

    result = baca.tools.sectionalize(97, (1, 1, 2))
    assert result == [24, 1, 24, 1, 47]
