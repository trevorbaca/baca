# -*- encoding: utf-8 -*-
import abjad


class FlattenDivisionCallback(abjad.abctools.AbjadValueObject):
    r'''Flatten division callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Divisions'

    __slots__ = (
        '_depth',
        )

    ### INITIALIZER ###

    def __init__(self, depth=-1):
        self._depth = depth

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls flatten division callback on `expr`.

        Returns list of divisions or list of division lists.
        '''
        return abjad.sequencetools.flatten_sequence(
            expr, 
            depth=self.depth,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        r'''Gets depth of callback.

        Returns integer.
        '''
        return self._depth