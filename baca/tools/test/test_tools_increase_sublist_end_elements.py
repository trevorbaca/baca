# -*- coding: utf-8 -*-
import baca


def test_tools_increase_sublist_end_elements_01():

    sequence_ = [[2, 2, 2, 2], [2, 2], [2, 2, 2]]
    sequence_ = baca.tools.increase_sublist_end_elements(sequence_, [1, 5, 10])

    assert sequence_ == [[12, 2, 2, 7], [3, 12], [7, 2, 3]]
