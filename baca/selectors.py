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


def chead(n, exclude=None):
    def selector(argument):
        return _select.chead(argument, n, exclude=exclude)

    return selector


# TODO: remove *argument, **keywords to allow pair=None interface
def clparts(*arguments, **keywords):
    def selector(argument):
        return _select.clparts(argument, *arguments, **keywords)

    return selector


# TODO: remove *argument, **keywords to allow pair=None interface
def cmgroups(*arguments, **keywords):
    def selector(argument):
        return _select.cmgroups(argument, *arguments, **keywords)

    return selector


def leaf(n, grace=None):
    def selector(argument):
        return abjad.select.leaf(argument, n, grace=grace)

    return selector


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


def leaves(
    pair=None,
    *,
    exclude: abjad.typings.Strings = None,
    grace: bool = None,
    head: bool = None,
    lleak: bool = None,
    pitched: bool = None,
    prototype=None,
    reverse: bool = None,
    rleak: bool = False,
    tail: bool = None,
    trim: bool | int | None = None,
):
    def selector(argument):
        selection = abjad.select.leaves(
            argument,
            prototype=prototype,
            exclude=exclude,
            grace=grace,
            head=head,
            pitched=pitched,
            reverse=reverse,
            tail=tail,
            trim=trim,
        )
        selection = _handle_pair(selection, pair)
        if lleak is True:
            selection = abjad.select.with_previous_leaf(selection)
        if rleak is True:
            selection = abjad.select.with_next_leaf(selection)
        return selection

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


def lleaf(*arguments, **keywords):
    def selector(argument):
        return _select.lleaf(argument, *arguments, **keywords)

    return selector


def lparts(*arguments, **keywords):
    def selector(argument):
        return _select.lparts(argument, *arguments, **keywords)

    return selector


def lt(n):
    def selector(argument):
        return _select.lt(argument, n)

    return selector


def ltleaves(*arguments, **keywords):
    def selector(argument):
        return _select.ltleaves(argument, *arguments, **keywords)

    return selector


def ltleaves_rleak():
    def selector(argument):
        result = _select.ltleaves(argument)
        result = _select.rleak(result)
        return result

    return selector


def ltqruns(*arguments, **keywords):
    def selector(argument):
        return _select.ltqrun(argument, *arguments, **keywords)

    return selector


def lts(pair=None, *, nontrivial=None, omit=False):
    def selector(argument):
        result = _select.lts(argument, nontrivial=nontrivial)
        result = _handle_pair(result, pair)
        result = _handle_omit(result, omit)
        return result

    return selector


def mgroups(*arguments, **keywords):
    def selector(argument):
        return _select.mgroups(argument, *arguments, **keywords)

    return selector


def mmrest(*arguments, **keywords):
    def selector(argument):
        return _select.mmrest(argument, *arguments, **keywords)

    return selector


def mmrests(exclude=None):
    def selector(argument):
        return _select.mmrests(argument, exclude=exclude)

    return selector


def note(n):
    def selector(argument):
        return abjad.select.note(argument, n)

    return selector


def notes(pair=None):
    def selector(argument):
        result = abjad.select.notes(argument)
        result = _handle_pair(result, pair)
        return result

    return selector


def ntruns(*arguments, **keywords):
    def selector(argument):
        return _select.ntruns(argument, *arguments, **keywords)

    return selector


def omgroups(*arguments, **keywords):
    def selector(argument):
        return _select.omgroups(argument, *arguments, **keywords)

    return selector


def phead(n, exclude=None):
    def selector(argument):
        return _select.phead(argument, n, exclude=exclude)

    return selector


def pheads(pair=None, exclude=None, grace=None):
    def selector(argument):
        result = _select.pheads(argument, exclude=exclude, grace=grace)
        result = _handle_pair(result, pair)
        return result

    return selector


def pleaf(n, exclude=None, grace=None):
    def selector(argument):
        return _select.pleaf(argument, n, exclude=exclude, grace=grace)

    return selector


def pleaf_in_each_tuplet(n, pair=None):
    assert isinstance(n, int), repr(n)
    if pair is None:
        start, stop = None, None
    else:
        start, stop = pair

    def selector(argument):
        selection = abjad.select.tuplets(argument)[start:stop]
        return [_select.pleaf(_, n) for _ in selection]

    return selector


def pleaves(pair=None, exclude=None, grace=None, lleak=False, rleak=False):
    def selector(argument):
        result = _select.pleaves(argument, exclude=exclude, grace=grace)
        result = _handle_pair(result, pair)
        if lleak is True:
            result = abjad.select.with_previous_leaf(result)
        if rleak is True:
            result = abjad.select.with_next_leaf(result)
        return result

    return selector


def plt(n):
    def selector(argument):
        return _select.plt(argument, n)

    return selector


def plts(pair=None, *, exclude=None, grace=None, lleak=None, omit=None, rleak=None):
    def selector(argument):
        result = _select.plts(argument, exclude=exclude, grace=grace)
        result = _handle_pair(result, pair)
        result = _handle_omit(result, omit)
        if lleak is True:
            result = abjad.select.with_previous_leaf(result)
        if rleak is True:
            result = abjad.select.with_next_leaf(result)
        return result

    return selector


# def ptail(n, *, exclude=None):
#    def selector(argument):
#        return _select.ptail(argument, n, exclude=exclude)
#
#    return selector


# def ptail_in_each_tuplet(n, pair=None):
#    assert isinstance(n, int), repr(n)
#    if pair is None:
#        start, stop = None, None
#    else:
#        start, stop = pair
#
#    def selector(argument):
#        selection = abjad.select.tuplets(argument)[start:stop]
#        return [_select.ptail(_, n) for _ in selection]
#
#    return selector


# def ptails(pair=None, exclude=None):
#    def selector(argument):
#        result = _select.ptails(argument, exclude=exclude)
#        result = _handle_pair(result, pair)
#        return result
#
#    return selector


# def qruns(*arguments, **keywords):
#    def selector(argument):
#        return _select.qruns(argument, *arguments, **keywords)
#
#    return selector


# def rleaf(n=0, *, exclude: abjad.Strings = None):
#    assert isinstance(n, int), repr(n)
#
#    def selector(argument):
#        selection = _select.rleaf(argument, n=n, exclude=exclude)
#        return selection
#
#    return selector
