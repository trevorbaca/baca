# -*- coding: utf-8 -*-
from abjad.tools import scoretools


def first_leaf(specifier):
    r'''Selects first leaf.

    Returns specifier wrapper.
    '''
    import baca
    return baca.select_.leaf(specifier, n=0)

def first_note(specifier):
    r'''Selects first note or chord.

    Returns specifier wrapper.
    '''
    import baca
    return baca.select_.note(specifier, n=0)

def leaf(specifier, n=0):
    r'''Selects leaf `n`.

    Returns specifier wrapper.
    '''
    import baca
    prototype = scoretools.Leaf
    if 0 < n:
        return baca.tools.SpecifierWrapper(
            prototype=prototype,
            specifier=specifier,
            start_index=n,
            stop_index=n+1,
            )
    elif n == 0:
        return baca.tools.SpecifierWrapper(
            prototype=prototype,
            specifier=specifier,
            stop_index=1
            )
    else:
        return baca.tools.SpecifierWrapper(
            prototype=prototype,
            specifier=specifier,
            start_index=n,
            stop_index=n+1
            )

def leaves(
    specifier,
    start=None,
    stop=None,
    with_next_leaf=None,
    with_previous_leaf=None,
    ):
    r'''Selects leaves from `start` to `stop`.

    Returns specifier wrapper.
    '''
    import baca
    return baca.tools.SpecifierWrapper(
        specifier=specifier,
        start_index=start,
        stop_index=stop,
        with_next_leaf=with_next_leaf,
        with_previous_leaf=with_previous_leaf,
        )

def notes(
    specifier,
    start=None,
    stop=None,
    with_next_leaf=None,
    with_previous_leaf=None,
    ):
    r'''Selects leaves from `start` to `stop`.

    Returns specifier wrapper.
    '''
    import baca
    return baca.tools.SpecifierWrapper(
        prototype=scoretools.Note,
        specifier=specifier,
        start_index=start,
        stop_index=stop,
        with_next_leaf=with_next_leaf,
        with_previous_leaf=with_previous_leaf,
        )

def note(
    specifier,
    n=0,
    ):
    r'''Selects note or chord `n`.

    Returns specifier wrapper.
    '''
    import baca
    if 0 < n:
        return baca.tools.SpecifierWrapper(
            prototype=(scoretools.Note, scoretools.Chord),
            specifier=specifier,
            start_index=n,
            stop_index=n+1,
            )
    elif n == 0:
        return baca.tools.SpecifierWrapper(
            prototype=(scoretools.Note, scoretools.Chord),
            specifier=specifier,
            stop_index=1
            )
    else:
        return baca.tools.SpecifierWrapper(
            prototype=(scoretools.Note, scoretools.Chord),
            specifier=specifier,
            start_index=n,
            stop_index=n+1
            )
