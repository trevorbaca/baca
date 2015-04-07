# -*- encoding: utf-8 -*-
from abjad import *


class DisplacementSpecifier(abctools.AbjadObject):
    r'''Displacement specifier.

    ..  container:: example

        **Example 1.** Initializes with octave displacements vector:

        ::

            >>> import baca
            >>> specifier = baca.makers.DisplacementSpecifier(
            ...     displacements=[0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.makers.DisplacementSpecifier(
                displacements=datastructuretools.CyclicTuple(
                    [0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2]
                    ),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_displacements',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        displacements=None,
        ):
        from abjad.tools import pitchtools
        displacements = tuple(displacements)
        assert self._is_octave_displacement_vector(displacements)
        displacements = datastructuretools.CyclicTuple(displacements)
        self._displacements = displacements

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan):
        for i, logical_tie in enumerate(logical_ties):
            assert isinstance(logical_tie, selectiontools.LogicalTie)
            displacement = self.displacements[i]
            interval = pitchtools.NumberedInterval(displacement * 12)
            for note in logical_tie:
                assert isinstance(note, Note), repr(note)
                written_pitch = note.written_pitch
                written_pitch += interval
                note.written_pitch = written_pitch

    ### PRIVATE METHODS ###

    def _is_octave_displacement_vector(self, expr):
        if isinstance(expr, (tuple, list)):
            if all(isinstance(_, int) for _ in expr):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def displacements(self):
        r'''Gets displacements of displacement specifier.

        ..  container:: example

            ::

        
                >>> specifier = baca.makers.DisplacementSpecifier(
                ...     displacements=[0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
                ...     )

            ::

                >>> specifier.displacements
                CyclicTuple([0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2])

        Set to integers or none.
        '''
        return self._displacements