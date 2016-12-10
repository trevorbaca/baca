# -*- coding: utf-8 -*-
import abjad


def first_leaf():
    selector = abjad.select()
    selector = selector.by_leaf(flatten=True)
    selector = selector.get_slice(stop=1, apply_to_each=False)
    return selector

def leaf(n=0):
    selector = abjad.select()
    selector = selector.by_leaf(flatten=True)
    selector = selector.get_item(n, apply_to_each=False)
    return selector

def logical_tie(n=0):
    selector = abjad.select()
    selector = selector.by_logical_tie(flatten=True)
    selector = selector.get_item(n, apply_to_each=False)
    return selector

def pitched_logical_tie(n=0):
    selector = abjad.select()
    selector = selector.by_logical_tie(flatten=True, pitched=True)
    selector = selector.get_item(n, apply_to_each=False)
    return selector

def pitched_logical_ties(n=0):
    selector = abjad.select()
    selector = selector.by_logical_tie(flatten=True, pitched=True)
    if 0 <= n:
        selector = selector.get_slice(stop=n, apply_to_each=False)
    else:
        selector = selector.get_slice(start=n, apply_to_each=False)
    return selector
