# -*- encoding: utf-8 -*-
from abjad import *


class GlissandoSpecifier(abctools.AbjadObject):
    r'''Glissando specifier.

    ..  container:: example

        **Example 1.** Initializes from a single pattern:

        ::

            >>> import baca
            >>> specifier = baca.makers.GlissandoSpecifier(
            ...     patterns=rhythmmakertools.select_all(),
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.makers.GlissandoSpecifier(
                patterns=(
                    rhythmmakertools.BooleanPattern(
                        indices=(0,),
                        period=1,
                        ),
                    ),
                )

    ..  container:: example

        **Example 2.** Initializes from multiple patterns:

        ::

            >>> specifier = baca.makers.GlissandoSpecifier(
            ...     patterns=[
            ...         rhythmmakertools.select_first(1),
            ...         rhythmmakertools.select_last(1),
            ...         ],
            ...     )

        ::
            
            >>> print(format(specifier))
            baca.makers.GlissandoSpecifier(
                patterns=(
                    rhythmmakertools.BooleanPattern(
                        indices=(0,),
                        ),
                    rhythmmakertools.BooleanPattern(
                        indices=(-1,),
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
        if isinstance(patterns, rhythmmakertools.BooleanPattern):
            patterns = (patterns,)
        patterns = patterns or ()
        patterns = tuple(patterns)
        prototype = rhythmmakertools.BooleanPattern
        assert all(isinstance(_, prototype) for _ in patterns)
        self._patterns = patterns

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan):
        logical_tie_count = len(logical_ties)
        for index, logical_tie in enumerate(logical_ties):
            for pattern in reversed(self.patterns):
                if pattern.matches_index(index, logical_tie_count):
                    self._apply_pattern(pattern, logical_tie)
                    break

    ### PRIVATE METHODS ###

    def _apply_pattern(self , pattern, logical_tie):
        if isinstance(pattern, rhythmmakertools.SilenceMask):
            return
        make_glissando_prototype = (
            rhythmmakertools.BooleanPattern,
            rhythmmakertools.SustainMask,
            )
        assert isinstance(pattern, make_glissando_prototype)
        note_or_chord = (scoretools.Note, scoretools.Chord)
        if isinstance(pattern, make_glissando_prototype):
            last_leaf = logical_tie.tail
            if not isinstance(last_leaf, note_or_chord):
                return
            next_leaf = inspect_(last_leaf).get_leaf(1)
            if not isinstance(next_leaf, note_or_chord):
                return
            leaves = [last_leaf, next_leaf]
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