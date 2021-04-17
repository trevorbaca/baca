import typing

import abjad

from .classes import Selection


class Selector:

    __slots__ = ("function",)

    def __init__(self, function):
        self.function = function

    def __call__(self, selection):
        return self.function(selection)

    def __repr__(self):
        return self.__class__.__name__


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
    def select(argument):
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

    return Selector(select)


def rleaf_(n: int = 0, *, exclude: abjad.Strings = None):
    def select(argument):
        selection = Selection(argument).rleaf(n=n, exclude=exclude)
        return selection

    return Selector(select)
