import abjad
import baca
import collections


class DivisionSequence(abjad.Sequence):
    r'''Division sequence.

    ..  container:: example

        >>> baca.DivisionSequence([(3, 8), (3, 8), (2, 8)])
        DivisionSequence([Division((3, 8)), Division((3, 8)), Division((2, 8))])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Divisions'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        items = items or []
        if not isinstance(items, collections.Iterable):
            items = [items]
        items_ = []
        for item in items:
            try:
                item = baca.Division(item)
            except (TypeError, ValueError):
                pass
            items_.append(item)
        superclass = super(DivisionSequence, self)
        superclass.__init__(items=items_)

    ### PUBLIC METHODS ###

    def split_by_durations(
        self,
        compound_meter_multiplier=None,
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=abjad.Right,
        remainder_fuse_threshold=None,
        ):
        r'''Splits each division in division sequence by `durations`.

        Returns new division sequence.
        '''
        maker = baca.SplitByDurationsDivisionCallback(
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
