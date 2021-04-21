import typing

import abjad

from .classes import Selection

### NEW ###


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


def leaves_in_get_tuplets(pattern, pair):
    start, stop = pair
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument).tuplets()
        selection = selection.get(*pattern)
        return Selection(Selection(_).leaves()[start:stop] for _ in selection)

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


def rleak_runs(start=0, stop=None):
    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        if start != 0 or stop is not None:
            selection = selection[start:stop]
        return Selection(Selection(_).leaves().rleak() for _ in selection)

    return selector


### REPLACEMENTS ###


def leaves_(
    prototype=None,
    *,
    exclude: abjad.typings.Strings = None,
    grace: bool = None,
    head: bool = None,
    pitched: bool = None,
    reverse: bool = None,
    start: bool = None,
    stop: bool = None,
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
        selection = selection[start:stop]
        return selection

    return selector


def rleaf_(n=0, *, exclude: abjad.Strings = None):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = Selection(argument).rleaf(n=n, exclude=exclude)
        return selection

    return selector
