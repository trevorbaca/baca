# -*- coding: utf-8 -*-
import baca


class WrapLibrary(object):
    r'''Wrap interface.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Library'

    ### PUBLIC METHODS ###

    @staticmethod
    def first_leaf(specifier):
        r'''Wraps specifier with first leaf selector.

        Returns specifier wrapper.
        '''
        return baca.wrap.leaf(specifier, n=0)

    @staticmethod
    def first_note(specifier):
        r'''Wraps specifier with first note or chord selector.

        Returns specifier wrapper.
        '''
        return baca.wrap.note(specifier, n=0)

    @staticmethod
    def leaf(specifier, n=0):
        r'''Wraps specifier with leaf selector.

        Returns specifier wrapper.
        '''
        prototype = abjad.scoretools.Leaf
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

    @staticmethod
    def leaves(
        specifier,
        start=None,
        stop=None,
        with_next_leaf=None,
        with_previous_leaf=None,
        ):
        r'''Wraps specifier with leaves selector.

        Returns specifier wrapper.
        '''
        return baca.tools.SpecifierWrapper(
            specifier=specifier,
            start_index=start,
            stop_index=stop,
            with_next_leaf=with_next_leaf,
            with_previous_leaf=with_previous_leaf,
            )

    @staticmethod
    def note(
        specifier,
        n=0,
        ):
        r'''Wraps specifier with note selector.

        Returns specifier wrapper.
        '''
        if 0 < n:
            return baca.tools.SpecifierWrapper(
                prototype=(abjad.Note, abjad.Chord),
                specifier=specifier,
                start_index=n,
                stop_index=n+1,
                )
        elif n == 0:
            return baca.tools.SpecifierWrapper(
                prototype=(abjad.Note, abjad.Chord),
                specifier=specifier,
                stop_index=1
                )
        else:
            return baca.tools.SpecifierWrapper(
                prototype=(abjad.Note, abjad.Chord),
                specifier=specifier,
                start_index=n,
                stop_index=n+1
                )

    @staticmethod
    def notes(
        specifier,
        start=None,
        stop=None,
        with_next_leaf=None,
        with_previous_leaf=None,
        ):
        r'''Wraps specifier with notes selector.

        Returns specifier wrapper.
        '''
        return baca.tools.SpecifierWrapper(
            prototype=abjad.Note,
            specifier=specifier,
            start_index=start,
            stop_index=stop,
            with_next_leaf=with_next_leaf,
            with_previous_leaf=with_previous_leaf,
            )
