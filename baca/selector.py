# -*- coding: utf-8 -*-
import abjad


def first_leaf():
    selector = abjad.select()
    selector = selector.by_leaf(flatten=True)
    selector = selector.get_slice(stop=1, apply_to_each=False)
    return selector