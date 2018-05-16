import abjad
import baca
import collections
import inspect
from .SplitByDurationsDivisionCallback import SplitByDurationsDivisionCallback
from .SplitByRoundedRatiosDivisionCallback import \
    SplitByRoundedRatiosDivisionCallback


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

    @abjad.Signature(
        is_operator=True,
        method_name='r',
        subscript='n',
        )
    def rotate(self, n=0) -> 'DivisionSequence':
        r'''Rotates division sequence by index `n`.

        ..  container:: example

            Rotates sequence to the left:

            ..  container:: example

                >>> sequence = baca.DivisionSequence([
                ...     baca.Division((10, 16), start_offset=(0, 1)),
                ...     baca.Division((12, 16), start_offset=(5, 8)),
                ...     baca.Division((12, 16), start_offset=(11, 8)),
                ...     baca.Division((12, 16), start_offset=(17, 8)),
                ...     baca.Division((8, 16), start_offset=(23, 8)),
                ...     baca.Division((15, 16), start_offset=(27, 8)),
                ...     ])

                >>> for division in sequence.rotate(n=-1):
                ...     division
                ...
                Division((12, 16), start_offset=Offset(0, 1))
                Division((12, 16), start_offset=Offset(3, 4))
                Division((12, 16), start_offset=Offset(3, 2))
                Division((8, 16), start_offset=Offset(9, 4))
                Division((15, 16), start_offset=Offset(11, 4))
                Division((10, 16), start_offset=Offset(59, 16))

            ..  container:: example expression

                >>> expression = baca.DivisionSequenceExpression(name='J')
                >>> expression = expression.division_sequence()
                >>> expression = expression.rotate(n=-1)

                >>> for division in expression(sequence):
                ...     division
                ...
                Division((12, 16), start_offset=Offset(0, 1))
                Division((12, 16), start_offset=Offset(3, 4))
                Division((12, 16), start_offset=Offset(3, 2))
                Division((8, 16), start_offset=Offset(9, 4))
                Division((15, 16), start_offset=Offset(11, 4))
                Division((10, 16), start_offset=Offset(59, 16))

                >>> expression.get_string()
                'r-1(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    -1
                                \bold
                                    J
                            }
                        }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        n = n or 0
        items = []
        if len(self):
            first_start_offset = self[0].start_offset
            n = n % len(self)
            for item in self[-n:len(self)] + self[:-n]:
                items.append(item)
        start_offset = first_start_offset
        for item in items:
            duration = item.duration
            item._start_offset = start_offset
            start_offset += duration
        return type(self)(items=items)

    @abjad.Signature()
    def split_by_durations(
        self,
        compound_meter_multiplier=None,
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=abjad.Right,
        remainder_fuse_threshold=None,
        ) -> 'DivisionSequence':
        r'''Splits each division in division sequence by `durations`.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        callback = SplitByDurationsDivisionCallback(
            compound_meter_multiplier=compound_meter_multiplier,
            cyclic=cyclic,
            durations=durations,
            pattern_rotation_index=pattern_rotation_index,
            remainder=remainder,
            remainder_fuse_threshold=remainder_fuse_threshold,
            )
        division_lists = callback(self)
        sequences = [type(self)(_) for _ in division_lists]
        return type(self)(sequences)

    @abjad.Signature()
    def split_by_rounded_ratios(
        self,
        ratios,
        ) -> 'DivisionSequence':
        r'''Splits each division in division sequence by rounded `ratios`.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        callback = SplitByRoundedRatiosDivisionCallback(ratios=ratios)
        division_lists = callback(self)
        sequences = [type(self)(_) for _ in division_lists]
        return type(self)(sequences)
