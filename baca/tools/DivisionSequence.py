# -*- coding: utf-8 -*-
from abjad.tools.sequencetools.Sequence import Sequence


class DivisionSequence(Sequence):
    r'''Division sequence.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-maker components'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def split_by_durations(
        self, 
        compound_meter_multiplier=None,
        cyclic=True,
        durations=(), 
        pattern_rotation_index=0,
        remainder=Right,
        remainder_fuse_threshold=None,
        ):
        r'''Splits each division in division sequence by `durations`.

        Returns new division sequence.
        '''
        import baca
        maker = baca.tools.SplitByDurationsDivisionCallback(
            compound_meter_multiplier=compound_meter_multiplier,
            cyclic=cyclic,
            durations=durations,
            pattern_rotation_index=pattern_rotation_index,
            remainder=remainder,
            remainder_fuse_threshold=remainder_fuse_threshold,
            )
        division_lists = maker(self)
        sequences = [type(self)(_) for _ in division_lists]
        return type(self)(sequences)