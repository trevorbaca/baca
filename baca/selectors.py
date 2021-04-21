import typing

import abjad

from .classes import Selection

### NEW ###


def leaf_after_each_ptail():
    def selector(argument):
        selection = Selection(argument)
        selection = selection.ptails()
        list_ = [Selection(_).rleak()[-1] for _ in selection]
        return Selection(list_)

    return selector


def leaf_in_each_rleak_run(n):
    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        list_ = [Selection(_).leaves().rleak()[n] for _ in selection]
        return Selection(list_)

    return selector


def leaf_in_each_run(n):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        list_ = [Selection(_).leaf(n) for _ in selection]
        return Selection(list_)

    return selector


def leaf_in_each_tuplet(n):
    assert isinstance(n, int), repr(n)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.tuplets()
        list_ = [Selection(_).leaf(n) for _ in selection]
        return Selection(list_)

    return selector


def leaves_in_each_lt(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.lts()
        list_ = [Selection(_).leaves()[start:stop] for _ in selection]
        return Selection(list_)

    return selector


def leaves_in_each_plt(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.plts()
        list_ = [Selection(_).leaves()[start:stop] for _ in selection]
        return Selection(list_)

    return selector


def leaves_in_each_run(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        list_ = [Selection(_).leaves()[start:stop] for _ in selection]
        return Selection(list_)

    return selector


def leaves_in_each_tuplet(start=0, stop=None):
    assert isinstance(start, (int, type(None))), repr(start)
    assert isinstance(stop, (int, type(None))), repr(stop)

    def selector(argument):
        selection = Selection(argument)
        selection = selection.tuplets()
        list_ = [Selection(_).leaves()[start:stop] for _ in selection]
        return Selection(list_)

    return selector


def rleak_runs(start=0, stop=None):
    def selector(argument):
        selection = Selection(argument)
        selection = selection.runs()
        if start != 0 or stop is not None:
            selection = selection[start:stop]
        list_ = [Selection(_).leaves().rleak() for _ in selection]
        return Selection(list_)

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
