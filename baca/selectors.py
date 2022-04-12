"""
Selectors.
"""

import abjad

from . import select as _select


def _handle_omit(selection, pair):
    if isinstance(pair, tuple):
        if isinstance(pair[0], list):
            assert len(pair) == 2, repr(pair)
            indices, period = pair
            selection = abjad.select.exclude(selection, indices, period)
        else:
            start, stop = pair
            selection = selection[start:stop]
    elif isinstance(pair, list):
        selection = abjad.select.exclude(selection, pair)
    elif isinstance(pair, abjad.Pattern):
        selection = abjad.select.exclude(selection, pair)
    return selection


def _handle_pair(selection, pair):
    if isinstance(pair, tuple):
        if isinstance(pair[0], list):
            assert len(pair) == 2, repr(pair)
            indices, period = pair
            selection = abjad.select.get(selection, indices, period)
        else:
            start, stop = pair
            selection = selection[start:stop]
    elif isinstance(pair, list):
        selection = abjad.select.get(selection, pair)
    elif isinstance(pair, abjad.Pattern):
        selection = abjad.select.get(selection, pair)
    return selection


def leaf_after_each_ptail():
    def selector(argument):
        selection = _select.ptails(argument)
        return [_select.rleak(_)[-1] for _ in selection]

    return selector


def leaf_in_each_rleak_run(n):
    def selector(argument):
        selection = abjad.select.runs(argument)
        return [_select.rleaf(_, n) for _ in selection]

    return selector


def leaf_in_each_run(n):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = abjad.select.runs(argument)
        return [abjad.select.leaf(_, n) for _ in selection]

    return selector


def leaf_in_each_tuplet(n):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = abjad.select.tuplets(argument)
        return [abjad.select.leaf(_, n) for _ in selection]

    return selector


def leaves_in_each_lt(start=0, stop=None):
    assert isinstance(start, int | type(None)), repr(start)
    assert isinstance(stop, int | type(None)), repr(stop)

    def selector(argument):
        selection = _select.lts(argument)
        return [abjad.select.leaves(_)[start:stop] for _ in selection]

    return selector


def leaves_in_each_plt(start=0, stop=None):
    assert isinstance(start, int | type(None)), repr(start)
    assert isinstance(stop, int | type(None)), repr(stop)

    def selector(argument):
        selection = _select.plts(argument)
        return [abjad.select.leaves(_)[start:stop] for _ in selection]

    return selector


def leaves_in_each_run(start=0, stop=None):
    assert isinstance(start, int | type(None)), repr(start)
    assert isinstance(stop, int | type(None)), repr(stop)

    def selector(argument):
        selection = abjad.select.runs(argument)
        return [abjad.select.leaves(_)[start:stop] for _ in selection]

    return selector


def leaves_in_each_tuplet(start=0, stop=None):
    assert isinstance(start, int | type(None)), repr(start)
    assert isinstance(stop, int | type(None)), repr(stop)

    def selector(argument):
        selection = abjad.select.tuplets(argument)
        return [abjad.select.leaves(_)[start:stop] for _ in selection]

    return selector


def _leaves_in_get_tuplets(pattern, pair, exclude=False):
    start, stop = pair
    assert isinstance(start, int | type(None)), repr(start)
    assert isinstance(stop, int | type(None)), repr(stop)

    def selector(argument):
        selection = abjad.select.tuplets(argument)
        if exclude is True:
            method = abjad.select.exclude
        else:
            method = abjad.select.get
        if isinstance(pattern, tuple):
            selection = method(selection, *pattern)
        else:
            assert isinstance(pattern, list)
            selection = method(selection, pattern)
        return [abjad.select.leaves(_)[start:stop] for _ in selection]

    return selector


def leaves_in_get_tuplets(pattern, pair):
    return _leaves_in_get_tuplets(pattern, pair)


def leaves_in_exclude_tuplets(pattern, pair):
    return _leaves_in_get_tuplets(pattern, pair, exclude=True)
