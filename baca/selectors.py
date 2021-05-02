import typing

import abjad

from .classes import Selection


def _handle_omit(selection, pair):
    if isinstance(pair, tuple):
        if isinstance(pair[0], list):
            assert len(pair) == 2, repr(pair)
            indices, period = pair
            selection = selection.exclude(indices, period)
        else:
            start, stop = pair
            selection = selection[start:stop]
    elif isinstance(pair, list):
        selection = selection.exclude(pair)
    elif isinstance(pair, abjad.Pattern):
        selection = selection.exclude(pair)
    return selection


def _handle_pair(selection, pair):
    if isinstance(pair, tuple):
        if isinstance(pair[0], list):
            assert len(pair) == 2, repr(pair)
            indices, period = pair
            selection = selection.get(indices, period)
        else:
            start, stop = pair
            selection = selection[start:stop]
    elif isinstance(pair, list):
        selection = selection.get(pair)
    elif isinstance(pair, abjad.Pattern):
        selection = selection.get(pair)
    return selection


def clparts(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).clparts(*arguments, **keywords)

    return selector


def cmgroups(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).cmgroups(*arguments, **keywords)

    return selector


def leaf(n, grace=None):
    def selector(argument):
        return Selection(argument).leaf(n, grace=grace)

    return selector


def leaf_after_each_ptail():
    def selector(argument):
        selection = Selection(argument)
        selection = selection.ptails()
        return Selection(Selection(_).rleak()[-1] for _ in selection)

    return selector


def leaf_in_each_rleak_run(n):
    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        return Selection(Selection(_).leaves().rleak()[n] for _ in selection)

    return selector


def leaf_in_each_run(n):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        return Selection(Selection(_).leaf(n) for _ in selection)

    return selector


def leaf_in_each_tuplet(n):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.tuplets()
        return Selection(Selection(_).leaf(n) for _ in selection)

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
    trim: typing.Union[bool, int] = None,
):
    def selector(argument):
        selection = abjad.select(argument).leaves(
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
            selection = Selection(selection).lleak()
        if rleak is True:
            selection = Selection(selection).rleak()
        return selection

    return selector


def leaves_in_each_lt(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.lts()
        return Selection(Selection(_).leaves()[start:stop] for _ in selection)

    return selector


def leaves_in_each_plt(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.plts()
        return Selection(Selection(_).leaves()[start:stop] for _ in selection)

    return selector


def leaves_in_each_run(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        return Selection(Selection(_).leaves()[start:stop] for _ in selection)

    return selector


def leaves_in_each_tuplet(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.tuplets()
        return Selection(Selection(_).leaves()[start:stop] for _ in selection)

    return selector


def _leaves_in_get_tuplets(pattern, pair, exclude=False):
    start, stop = pair
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument).tuplets()
        if exclude is True:
            method = selection.exclude
        else:
            method = selection.get
        if isinstance(pattern, tuple):
            selection = method(*pattern)
        else:
            assert isinstance(pattern, list)
            selection = method(pattern)
        return Selection(Selection(_).leaves()[start:stop] for _ in selection)

    return selector


def leaves_in_get_tuplets(pattern, pair):
    return _leaves_in_get_tuplets(pattern, pair)


def leaves_in_exclude_tuplets(pattern, pair):
    return _leaves_in_get_tuplets(pattern, pair, exclude=True)


def lleaf(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).lleaf(*arguments, **keywords)

    return selector


def lparts(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).lparts(*arguments, **keywords)

    return selector


def lt(n):
    def selector(argument):
        return Selection(argument).lt(n)

    return selector


def ltleaves(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).ltleaves(*arguments, **keywords)

    return selector


def ltleaves_rleak():
    def selector(argument):
        return Selection(argument).ltleaves().rleak()

    return selector


def ltqruns(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).ltqrun(*arguments, **keywords)

    return selector


def lts(pair=None, *, nontrivial=None, omit=False):
    def selector(argument):
        result = Selection(argument).lts(nontrivial=nontrivial)
        result = _handle_pair(result, pair)
        result = _handle_omit(result, omit)
        return result

    return selector


def mgroups(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).mgroups(*arguments, **keywords)

    return selector


def mmrest(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).mmrest(*arguments, **keywords)

    return selector


def note(n):
    def selector(argument):
        return Selection(argument).note(n)

    return selector


def notes(pair=None):
    def selector(argument):
        result = Selection(argument).notes()
        result = _handle_pair(result, pair)
        return result

    return selector


def ntruns(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).ntruns(*arguments, **keywords)

    return selector


def omgroups(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).omgroups(*arguments, **keywords)

    return selector


def phead(n, exclude=None):
    def selector(argument):
        return Selection(argument).phead(n, exclude=exclude)

    return selector


def pheads(pair=None, exclude=None, grace=None):
    def selector(argument):
        result = Selection(argument).pheads(exclude=exclude, grace=grace)
        result = _handle_pair(result, pair)
        return result

    return selector


def pleaf(n, exclude=None, grace=None):
    def selector(argument):
        return Selection(argument).pleaf(n, exclude=exclude, grace=grace)

    return selector


def pleaf_in_each_tuplet(n, pair=None):
    assert isinstance(n, int), repr(n)
    if pair is None:
        start, stop = None, None
    else:
        start, stop = pair

    def selector(argument):
        selection = Selection(argument).tuplets()[start:stop]
        return Selection(Selection(_).pleaf(n) for _ in selection)

    return selector


def pleaves(pair=None, exclude=None, grace=None, lleak=False, rleak=False):
    def selector(argument):
        result = Selection(argument).pleaves(exclude=exclude, grace=grace)
        result = _handle_pair(result, pair)
        if lleak is True:
            result = result.lleak()
        if rleak is True:
            result = result.rleak()
        return result

    return selector


def plt(n):
    def selector(argument):
        return Selection(argument).plt(n)

    return selector


def plts(pair=None, exclude=None):
    def selector(argument):
        result = Selection(argument).plts(exclude=exclude)
        result = _handle_pair(result, pair)
        return result

    return selector


def ptail(n):
    def selector(argument):
        return Selection(argument).ptail(n)

    return selector


def ptail_in_each_tuplet(n, pair=None):
    assert isinstance(n, int), repr(n)
    if pair is None:
        start, stop = None, None
    else:
        start, stop = pair

    def selector(argument):
        selection = Selection(argument).tuplets()[start:stop]
        return Selection(Selection(_).ptail(n) for _ in selection)

    return selector


def ptails(pair=None, exclude=None):
    def selector(argument):
        result = Selection(argument).ptails(exclude=exclude)
        result = _handle_pair(result, pair)
        return result

    return selector


def qruns(*arguments, **keywords):
    def selector(argument):
        return Selection(argument).qruns(*arguments, **keywords)

    return selector


def rest(n):
    def selector(argument):
        return Selection(argument).rest(n)

    return selector


def rests(pair=None):
    def selector(argument):
        result = Selection(argument).rests()
        result = _handle_pair(result, pair)
        return result

    return selector


def rleaf(n=0, *, exclude: abjad.Strings = None):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = Selection(argument).rleaf(n=n, exclude=exclude)
        return selection

    return selector


def rleak_runs(start=0, stop=None):
    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        if start != 0 or stop is not None:
            selection = selection[start:stop]
        return Selection(Selection(_).leaves().rleak() for _ in selection)

    return selector


def rleaves(pair=None):
    def selector(argument):
        result = Selection(argument).rleaves()
        result = _handle_pair(result, pair)
        return result

    return selector


def run(n):
    def selector(argument):
        return Selection(argument).run(n)

    return selector


def runs(pair=None, exclude=None, rleak=False):
    def selector(argument):
        result = Selection(argument).runs(exclude=exclude)
        result = _handle_pair(result, pair)
        if rleak is True:
            result = result.rleak()
        return result

    return selector


def skip(n):
    def selector(argument):
        return Selection(argument).skip(n)

    return selector


def tleaves(pair=None, exclude=None, grace=None, rleak=False):
    def selector(argument):
        result = Selection(argument).tleaves(exclude=exclude, grace=grace)
        result = _handle_pair(result, pair)
        if rleak is True:
            result = result.rleak()
        return result

    return selector


def tuplet(n):
    def selector(argument):
        return Selection(argument).tuplet(n)

    return selector


def tuplets(pair=None):
    def selector(argument):
        result = Selection(argument).tuplets()
        result = _handle_pair(result, pair)
        return result

    return selector
