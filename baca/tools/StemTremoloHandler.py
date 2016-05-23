# -*- coding: utf-8 -*-
import abjad
from baca.tools.Handler import Handler


class StemTremoloHandler(Handler):
    r'''Stem tremolo handler.
    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Handlers'

    __slots__ = (
        '_hash_mark_counts',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(self, hash_mark_counts=None, pattern=None):
        if hash_mark_counts is not None:
            hash_mark_counts = tuple(hash_mark_counts)
            assert abjad.mathtools.all_are_nonnegative_integers(
                hash_mark_counts)
        self._hash_mark_counts = hash_mark_counts
        if pattern is not None:
            prototype = (
                abjad.patterntools.Pattern,
                abjad.patterntools.CompoundPattern,
                )
            assert isinstance(pattern, prototype), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        prototype = (abjad.scoretools.Note, abjad.scoretools.Chord)
        hash_mark_counts = abjad.datastructuretools.CyclicTuple(
            self.hash_mark_counts)
        leaves = list(abjad.iterate(expr).by_class(prototype))
        total_length = len(leaves)
        for i, leaf in enumerate(leaves):
            if self.pattern is not None:
                if not self.pattern.matches_index(i, total_length):
                    continue
            hash_mark_count = hash_mark_counts[i]
            stem_tremolo = abjad.indicatortools.StemTremolo(hash_mark_count)
            abjad.attach(stem_tremolo, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def hash_mark_counts(self):
        r'''Gets hash mark counts of handler.

        ..  todo:: Rename to something that indicates power-of-two
            requirement.

        Set to nonnegative integers or none.
        '''
        return self._hash_mark_counts

    @property
    def pattern(self):
        r'''Gets pattern.

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        '''
        return self._pattern