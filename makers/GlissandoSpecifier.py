# -*- encoding: utf-8 -*-
from abjad import *


class GlissandoSpecifier(abctools.AbjadObject):
    r'''Glissando specifier.

    ..  container:: example

        Initializes with boolean patterns:

        ::

            >>> import baca
            >>> specifier = baca.makers.GlissandoSpecifier(
            ...     patterns=[
            ...         rhythmmakertools.BooleanPattern(
            ...             indices=[0, 1],
            ...             period=2,
            ...             ),
            ...         rhythmmakertools.BooleanPattern(
            ...             indices=[0],
            ...             ),
            ...         ],
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.makers.GlissandoSpecifier(
                patterns=(
                    rhythmmakertools.BooleanPattern(
                        indices=(0, 1),
                        period=2,
                        ),
                    rhythmmakertools.BooleanPattern(
                        indices=(0,),
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_patterns',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        patterns=None,
        ):
        from abjad.tools import pitchtools
        if patterns is not None:
            patterns = tuple(patterns)
            prototype = rhythmmakertools.BooleanPattern
            assert all(isinstance(_, prototype) for _ in patterns)
        self._patterns = patterns

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan):
        total_logical_ties = len(logical_ties)
        for i, logical_tie in enumerate(logical_ties):
            assert logical_tie.is_trivial, repr(logical_tie)
            for durations in self.patterns:
                if durations.matches_index(i, total_logical_ties):
                    first_leaf = logical_tie.head
                    next_leaf = inspect_(first_leaf).get_leaf(1)
                    leaves = [first_leaf, next_leaf]
                    attach(spannertools.Glissando(), leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def patterns(self):
        r'''Gets patterns of glissando specifier.

        ..  container:: example

            ::

                >>> specifier = baca.makers.GlissandoSpecifier(
                ...     patterns=[
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0, 1],
                ...             period=2,
                ...             ),
                ...         rhythmmakertools.BooleanPattern(
                ...             indices=[0],
                ...             ),
                ...         ],
                ...     )
        

            ::

                >>> specifier.patterns
                (BooleanPattern(indices=(0, 1), period=2), BooleanPattern(indices=(0,)))

        Set to boolean patterns or none.
        '''
        return self._patterns