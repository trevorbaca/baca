# -*- coding: utf-8 -*-
import baca


def test_tools_replace_nested_elements_with_unary_subruns_01():

    sequence_ = [[1, 3, -4], [1, 2, -2, -4]]
    result = baca.tools.replace_nested_elements_with_unary_subruns(sequence_)

    assert result == [[1, 1, 1, 1, -4], [1, 1, 1, -2, -4]]


def test_tools_replace_nested_elements_with_unary_subruns_02():

    sequence_ = [[1, -2, 3], [-4, 5]]
    result = baca.tools.replace_nested_elements_with_unary_subruns(sequence_)

    assert result == [[1, -2, 1, 1, 1], [-4, 1, 1, 1, 1, 1]]
