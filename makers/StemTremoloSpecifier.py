# -*- encoding: utf-8 -*-
from abjad import *


class StemTremoloSpecifier(abctools.AbjadObject):
    r'''Stem tremolo specifier.

    ..  container:: example

        **Example 1.** Initializes with boolean patterns:

        ::

            >>> import baca
            >>> specifier = baca.makers.StemTremoloSpecifier(
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
            baca.makers.StemTremoloSpecifier(
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

    def __call__(self, logical_ties, timespan=None):
        total_logical_ties = len(logical_ties)
        for i, logical_tie in enumerate(logical_ties):
            for durations in self.patterns:
                if durations.matches_index(i, total_logical_ties):
                    hash_mark_count = 32
                    stem_tremolo = indicatortools.StemTremolo(hash_mark_count)
                    for leaf in logical_tie:
                        attach(stem_tremolo, leaf)
                    break

    ### PUBLIC PROPERTIES ###

    @property
    def patterns(self):
        r'''Gets patterns of stem tremolo specifier.

        ..  container:: example

            ::

                >>> import baca
                >>> specifier = baca.makers.StemTremoloSpecifier(
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