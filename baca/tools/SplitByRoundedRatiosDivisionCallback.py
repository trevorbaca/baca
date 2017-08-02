# -*- coding: utf-8 -*-
import abjad
import baca


class SplitByRoundedRatiosDivisionCallback(abjad.AbjadValueObject):
    r'''Split-by-rounded-ratios division callback.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Makes divisions with ``2:1`` ratios:

        ::

            >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
            ...     ratios=[abjad.Ratio([2, 1])],
            ...     )
            >>> lists = maker([(7, 4), (6, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division((5, 4)), Division((2, 4))]
            [Division((4, 4)), Division((2, 4))]

    ..  container:: example

        Makes divisions with alternating ``2:1`` and ``1:1:1`` ratios:

        ::

            >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
            ...     ratios=[abjad.Ratio([2, 1]), abjad.Ratio([1, 1, 1])],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division((5, 4)), Division((2, 4))]
            [Division((2, 4)), Division((2, 4)), Division((2, 4))]
            [Division((3, 4)), Division((2, 4))]
            [Division((1, 4)), Division((2, 4)), Division((1, 4))]

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested
    list of divisions as output. Output structured one output list per input
    division.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Divisions'

    __slots__ = (
        '_ratios',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ratios=None,
        ):
        if ratios is not None:
            ratios = ratios or ()
            ratios = [abjad.Ratio(_) for _ in ratios]
            ratios = tuple(ratios)
        self._ratios = ratios

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls rounded ratio division-maker on `divisions`.

        ..  container:: example

            Calls maker on nonempty input:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division((4, 4)), Division((3, 4))]
                [Division((3, 4)), Division((3, 4))]

            Returns list of division lists.

        ..  container:: example

            Calls maker on empty input:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([1, 1])],
                ...     )
                >>> maker([])
                []

            Returns empty list.

        ..  container:: example

            Works with start offset:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([1, 1])],
                ...     )

            ::

                >>> divisions = [(7, 4), (6, 4)]
                >>> divisions = [baca.Division(_) for _ in divisions]
                >>> divisions[0]._start_offset = abjad.Offset(1, 4)
                >>> divisions
                [Division((7, 4), start_offset=Offset(1, 4)), Division((6, 4))]

            ::

                >>> division_lists = maker(divisions)
                >>> len(division_lists)
                2

            ::

                >>> for division in division_lists[0]:
                ...     division
                ...
                Division((4, 4), start_offset=Offset(1, 4))
                Division((3, 4), start_offset=Offset(5, 4))

            ::

                >>> for division in division_lists[1]:
                ...     division
                ...
                Division((3, 4), start_offset=Offset(2, 1))
                Division((3, 4), start_offset=Offset(11, 4))

        Returns possibly empty list of division lists.
        '''
        divisions = divisions or []
        if not divisions:
            return []
        divisions, start_offset = baca.DivisionMaker._to_divisions(
            divisions)
        start_offset = divisions[0].start_offset
        division_lists = []
        ratios = self._get_ratios()
        for i, division in enumerate(divisions):
            ratio = ratios[i]
            numerators = abjad.mathtools.partition_integer_by_ratio(
                division.numerator,
                ratio,
                )
            division_list = [
                baca.Division((numerator, division.denominator))
                for numerator in numerators
                ]
            division_lists.append(division_list)
        division_lists, start_offset = baca.DivisionMaker._to_divisions(
            division_lists,
            start_offset=start_offset,
            )
        return division_lists

    ### PRIVATE METHODS ###

    def _get_ratios(self):
        if self.ratios:
            ratios = self.ratios
        else:
            ratios = (abjad.Ratio([1]),)
        ratios = abjad.CyclicTuple(ratios)
        return ratios

    ### PUBLIC PROPERTIES ###

    @property
    def ratios(self):
        r'''Gets ratios of rounded ratio division-maker.

        ..  container:: example

            Gets trivial ratio of ``1`` by default:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division((7, 4))]
                [Division((6, 4))]

        ..  container:: example

            Gets ratios equal to ``1:1``:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division((4, 4)), Division((3, 4))]
                [Division((3, 4)), Division((3, 4))]

        ..  container:: example

            Gets ratios equal to ``2:1``:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([2, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division((5, 4)), Division((2, 4))]
                [Division((4, 4)), Division((2, 4))]

        ..  container:: example

            Gets ratios equal to ``1:1:1``:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([1, 1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division((2, 4)), Division((3, 4)), Division((2, 4))]
                [Division((2, 4)), Division((2, 4)), Division((2, 4))]

        ..  container:: example

            Gets ratios equal to ``2:1`` and ``1:1:1`` alternately:

            ::

                >>> maker = baca.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[abjad.Ratio([2, 1]), abjad.Ratio([1, 1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division((5, 4)), Division((2, 4))]
                [Division((2, 4)), Division((2, 4)), Division((2, 4))]
                [Division((3, 4)), Division((2, 4))]
                [Division((1, 4)), Division((2, 4)), Division((1, 4))]

        Set to ratios or none.
        '''
        return self._ratios
