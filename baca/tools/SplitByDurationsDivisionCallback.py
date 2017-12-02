import abjad
import baca


class SplitByDurationsDivisionCallback(abjad.AbjadValueObject):
    r'''Split-by-durations division callback.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        Makes quarter-valued divisions with remainder at right:

        >>> division_maker = baca.SplitByDurationsDivisionCallback(
        ...     durations=[(1, 4)]
        ...     )

        >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
        >>> division_lists = division_maker(time_signatures)
        >>> for division_list in division_lists:
        ...     division_list
        ...
        [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
        [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
        [Division((1, 4)), Division((3, 16))]

        >>> rhythm_maker = rhythmos.NoteRhythmMaker()
        >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
        >>> music = rhythm_maker(divisions)
        >>> lilypond_file = division_maker.show(music, time_signatures)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
            \new RhythmicStaff {
                { % measure
                    \time 7/8
                    c'4
                    c'4
                    c'4
                    c'8
                } % measure
                { % measure
                    c'4
                    c'4
                    c'4
                    c'8
                } % measure
                { % measure
                    \time 7/16
                    c'4
                    c'8.
                } % measure
            }

    ..  container:: example

        Makes quarter-valued divisions with remainder at left:

        >>> division_maker = baca.SplitByDurationsDivisionCallback(
        ...     durations=[(1, 4)],
        ...     remainder=abjad.Left,
        ...     )

        >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
        >>> division_lists = division_maker(time_signatures)
        >>> for division_list in division_lists:
        ...     division_list
        ...
        [Division((1, 8)), Division((1, 4)), Division((1, 4)), Division((1, 4))]
        [Division((1, 8)), Division((1, 4)), Division((1, 4)), Division((1, 4))]
        [Division((3, 16)), Division((1, 4))]

        >>> rhythm_maker = rhythmos.NoteRhythmMaker()
        >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
        >>> music = rhythm_maker(divisions)
        >>> lilypond_file = division_maker.show(music, time_signatures)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
            \new RhythmicStaff {
                { % measure
                    \time 7/8
                    c'8
                    c'4
                    c'4
                    c'4
                } % measure
                { % measure
                    c'8
                    c'4
                    c'4
                    c'4
                } % measure
                { % measure
                    \time 7/16
                    c'8.
                    c'4
                } % measure
            }

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested
    list of divisions as output. Output structured one output list per input
    division.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Divisions'

    __slots__ = (
        '_callbacks',
        '_compound_meter_multiplier',
        '_cyclic',
        '_pattern',
        '_pattern_rotation_index',
        '_remainder',
        '_remainder_fuse_threshold',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        compound_meter_multiplier=abjad.Multiplier(1),
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=abjad.Right,
        remainder_fuse_threshold=None,
        ):
        compound_meter_multiplier = compound_meter_multiplier or 1
        compound_meter_multiplier = abjad.Multiplier(compound_meter_multiplier)
        self._compound_meter_multiplier = compound_meter_multiplier
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        durations = durations or ()
        pattern_ = []
        for division in durations:
            division = baca.Division(division)
            pattern_.append(division)
        durations = tuple(pattern_)
        self._pattern = durations
        assert remainder in (abjad.Left, abjad.Right), repr(remainder)
        self._remainder = remainder
        assert isinstance(pattern_rotation_index, int)
        self._pattern_rotation_index = pattern_rotation_index
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
        self._remainder_fuse_threshold = remainder_fuse_threshold
        self._callbacks = ()

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls division-maker on `divisions`.

        ..  container:: example

            Splits divisions without remainder:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(3, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 4))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    } % measure
                }

        ..  container:: example

            Splits divisions with remainder:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(7, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                    } % measure
                }

            Positions remainder at right of output because divison-maker
            `remainder` defaults to right.

        ..  container:: example

            Multiple divisions:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(2, 4), (3, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4))]
            [Division((1, 4)), Division((1, 4)), Division((1, 4))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 2/4
                        c'4
                        c'4
                    } % measure
                    { % measure
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    } % measure
                }

        ..  container:: example

            No durations:

            >>> division_maker = baca.SplitByDurationsDivisionCallback()

            >>> time_signatures = [(6, 32)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((6, 32))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 6/32
                        c'8.
                    } % measure
                }

            Returns input division unchanged.

        ..  container:: example

            Empty input:

            >>> maker = baca.SplitByDurationsDivisionCallback(durations=[(1, 4)])
            >>> maker()
            []

            Returns empty list.

        ..  container:: example

            Works with start offset:

            >>> callback = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 4)],
            ...     )

            >>> divisions = [(2, 4), (3, 4)]
            >>> divisions = [baca.Division(_) for _ in divisions]
            >>> divisions[0]._start_offset = abjad.Offset(1, 4)
            >>> divisions
            [Division((2, 4), start_offset=Offset(1, 4)), Division((3, 4))]

            >>> division_lists = callback(divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [Division((1, 4), start_offset=Offset(1, 4)), Division((1, 4), start_offset=Offset(1, 2))]
            [Division((1, 4), start_offset=Offset(3, 4)), Division((1, 4), start_offset=Offset(1, 1)), Division((1, 4), start_offset=Offset(5, 4))]

            Works with start offset:

            >>> division_maker = baca.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=abjad.Infinity,
            ...     )
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 16)],
            ...     remainder=abjad.Left,
            ...     )

            >>> divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> divisions = [baca.Division(_) for _ in divisions]
            >>> divisions[0]._start_offset = abjad.Offset(1, 4)

            >>> division_lists = division_maker(divisions)
            >>> len(division_lists)
            1

            >>> for division in division_lists[0]:
            ...     division
            Division((1, 8), start_offset=Offset(1, 4))
            Division((3, 16), start_offset=Offset(3, 8))
            Division((3, 16), start_offset=Offset(9, 16))
            Division((3, 16), start_offset=Offset(3, 4))
            Division((3, 16), start_offset=Offset(15, 16))
            Division((3, 16), start_offset=Offset(9, 8))
            Division((3, 16), start_offset=Offset(21, 16))
            Division((3, 16), start_offset=Offset(3, 2))
            Division((3, 16), start_offset=Offset(27, 16))
            Division((3, 16), start_offset=Offset(15, 8))
            Division((3, 16), start_offset=Offset(33, 16))

        Returns possibly empty list of division lists.
        '''
        divisions = divisions or []
        if not divisions:
            return divisions
        divisions, start_offset = baca.DivisionMaker._to_divisions(
            divisions)
        start_offset = divisions[0].start_offset
        division_lists = []
        for i, division in enumerate(divisions):
            input_division = baca.Division(division)
            input_duration = abjad.Duration(input_division)
            input_meter = abjad.Meter(input_division)
            assert 0 < input_division, repr(input_division)
            if not self.durations:
                division_list = [input_division]
                division_lists.append(division_list)
                continue
            if input_meter.is_simple or not self.durations:
                durations = self.durations[:]
            elif input_meter.is_compound:
                multiplier = self.compound_meter_multiplier
                durations = [
                    abjad.Duration(multiplier * _)
                    for _ in self.durations
                    ]
            division_list = list(durations)
            pattern_rotation_index = self.pattern_rotation_index or 0
            pattern_rotation_index *= i
            division_list = baca.Sequence(
                division_list).rotate(n=pattern_rotation_index)
            division_list = list(division_list)
            if self.cyclic:
                division_list = baca.Sequence(division_list).repeat_to_weight(
                    input_division,
                    allow_total=abjad.Less,
                    )
                division_list = list(division_list)
            total_duration = abjad.Duration(sum(division_list))
            if total_duration == input_duration:
                division_lists.append(division_list)
                continue
            if self.remainder is None:
                raise Exception(f'bad fill {input_division} from {durations}.')
            remainder = input_division - total_duration
            remainder = baca.Division(remainder)
            if self.remainder == abjad.Left:
                if self.remainder_fuse_threshold is None:
                    division_list.insert(0, remainder)
                elif remainder <= self.remainder_fuse_threshold:
                    fused_value = division_list[0] + remainder
                    fused_value = baca.Division(fused_value)
                    division_list[0] = fused_value
                else:
                    division_list.insert(0, remainder)
            elif self.remainder == abjad.Right:
                if self.remainder_fuse_threshold is None:
                    division_list.append(remainder)
                elif remainder <= self.remainder_fuse_threshold:
                    fused_value = division_list[-1] + remainder
                    fused_value = baca.Division(fused_value)
                    division_list[-1] = fused_value
                else:
                    division_list.append(remainder)
            else:
                raise ValueError((self.remainder, remainder))
            total_duration = abjad.Duration(sum(division_list))
            pair = total_duration, input_duration
            assert total_duration == input_duration, pair
            division_lists.append(division_list)
        for _ in division_lists:
            assert isinstance(_, list), repr(_)
        division_lists, start_offset = baca.DivisionMaker._to_divisions(
            division_lists,
            start_offset
            )
        return division_lists

    ### PRIVATE METHODS ###

    def _get_storage_format_specification(self):
        agent = abjad.StorageFormatManager(self)
        keyword_argument_names = agent.signature_keyword_names
        keyword_argument_names = list(keyword_argument_names)
        if bool(self.cyclic):
            keyword_argument_names.remove('cyclic')
        if not self.durations:
            keyword_argument_names.remove('durations')
        if self.remainder == abjad.Right:
            keyword_argument_names.remove('remainder')
        if self.pattern_rotation_index == 0:
            keyword_argument_names.remove('pattern_rotation_index')
        return abjad.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def compound_meter_multiplier(self):
        r'''Gets compound meter multiplier of callback.

        ..  container:: example

            No compound meter multiplier:

            >>> division_maker = baca.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(3, 4), (6, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 4))]
            [Division((1, 4)), Division((1, 4)), Division((1, 4))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    } % measure
                    { % measure
                        \time 6/8
                        c'4
                        c'4
                        c'4
                    } % measure
                }

        ..  container:: example

            Compound meter multiplier equal to ``3/2``:

            >>> division_maker = baca.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     compound_meter_multiplier=abjad.Multiplier(3, 2),
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(3, 4), (6, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 4))]
            [Division((3, 8)), Division((3, 8))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    } % measure
                    { % measure
                        \time 6/8
                        c'4.
                        c'4.
                    } % measure
                }

        Defaults to ``1``.

        Set to multiplier.

        Returns multiplier.
        '''
        return self._compound_meter_multiplier

    @property
    def cyclic(self):
        r'''Is true when division-maker reads durations cyclically for each
        input division.

        Is false when division-maker reads durations only once per input
        division.

        ..  container:: example

            Reads durations cyclically for each input division:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
            [Division((1, 4)), Division((3, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                    } % measure
                    { % measure
                        c'4
                        c'4
                        c'4
                        c'8
                    } % measure
                    { % measure
                        \time 7/16
                        c'4
                        c'8.
                    } % measure
                }

        ..  container:: example

            Reads durations only once per input division:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=False,
            ...     durations=[(1, 4)],
            ...     )

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((5, 8))]
            [Division((1, 4)), Division((5, 8))]
            [Division((1, 4)), Division((3, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/8
                        c'4
                        c'2
                        ~
                        c'8
                    } % measure
                    { % measure
                        c'4
                        c'2
                        ~
                        c'8
                    } % measure
                    { % measure
                        \time 7/16
                        c'4
                        c'8.
                    } % measure
                }

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._cyclic

    @property
    def durations(self):
        r'''Gets durations of division-maker.

        ..  container:: example

            Returns input division unchanged when durations is empty:

                >>> division_maker = baca.SplitByDurationsDivisionCallback()

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((7, 8))]
            [Division((7, 8))]
            [Division((7, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/8
                        c'2..
                    } % measure
                    { % measure
                        c'2..
                    } % measure
                    { % measure
                        \time 7/16
                        c'4..
                    } % measure
                }

        ..  container:: example

            Applies durations to each input division:

                >>> division_maker = baca.SplitByDurationsDivisionCallback(
                ...     durations=[(1, 4)],
                ...     )

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
            [Division((1, 4)), Division((3, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                    } % measure
                    { % measure
                        c'4
                        c'4
                        c'4
                        c'8
                    } % measure
                    { % measure
                        \time 7/16
                        c'4
                        c'8.
                    } % measure
                }

        Defaults to none.

        Set to durations or none.

        Returns durations or none.
        '''
        return self._pattern

    @property
    def pattern_rotation_index(self):
        r'''Gets durations rotation index of division-maker.

        ..  container:: example

            Does not rotate durations:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 16), (1, 8), (1, 4)],
            ...     )

            >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 16)), Division((1, 8)), Division((1, 4))]
            [Division((1, 16)), Division((1, 8)), Division((1, 4))]
            [Division((1, 16)), Division((1, 8)), Division((1, 4))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/16
                        c'16
                        c'8
                        c'4
                    } % measure
                    { % measure
                        c'16
                        c'8
                        c'4
                    } % measure
                    { % measure
                        c'16
                        c'8
                        c'4
                    } % measure
                }

        ..  container:: example

            Rotates durations one element to the left on each new input
            division:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 16), (1, 8), (1, 4)],
            ...     pattern_rotation_index=-1,
            ...     )

            >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
            >>> division_lists = division_maker([(7, 16), (7, 16), (7, 16)])
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 16)), Division((1, 8)), Division((1, 4))]
            [Division((1, 8)), Division((1, 4)), Division((1, 16))]
            [Division((1, 4)), Division((1, 16)), Division((1, 8))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/16
                        c'16
                        c'8
                        c'4
                    } % measure
                    { % measure
                        c'8
                        c'4
                        c'16
                    } % measure
                    { % measure
                        c'4
                        c'16
                        c'8
                    } % measure
                }

        ..  container:: example

            Rotates durations one element to the right on each new input
            division:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 16), (1, 8), (1, 4)],
            ...     pattern_rotation_index=1,
            ...     )

            >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 16)), Division((1, 8)), Division((1, 4))]
            [Division((1, 4)), Division((1, 16)), Division((1, 8))]
            [Division((1, 8)), Division((1, 4)), Division((1, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 7/16
                        c'16
                        c'8
                        c'4
                    } % measure
                    { % measure
                        c'4
                        c'16
                        c'8
                    } % measure
                    { % measure
                        c'8
                        c'4
                        c'16
                    } % measure
                }

        Defaults to 0.

        Set to integer.

        Returns integer.
        '''
        return self._pattern_rotation_index

    @property
    def remainder(self):
        r'''Gets direction to which any remainder will be positioned.

        ..  container:: example

            Positions remainder to right of noncyclic durations:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=False,
            ...     durations=[(4, 16), (1, 16)],
            ...     )

            >>> time_signatures = [(3, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((4, 16)), Division((1, 16)), Division((7, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'4
                        c'16
                        c'4..
                    } % measure
                }

        ..  container:: example

            Positions remainder to right of cyclic durations:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     durations=[(4, 16), (1, 16)],
            ...     )

            >>> time_signatures = [(3, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((4, 16)), Division((1, 16)), Division((4, 16)), Division((1, 16)), Division((1, 8))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'4
                        c'16
                        c'4
                        c'16
                        c'8
                    } % measure
                }

        ..  container:: example

            Positions remainder to left of noncyclic durations:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=False,
            ...     durations=[(1, 4), (1, 16)],
            ...     remainder=abjad.Left,
            ...     )

            >>> time_signatures = [(3, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((7, 16)), Division((1, 4)), Division((1, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'4..
                        c'4
                        c'16
                    } % measure
                }

        ..  container:: example

            Positions remainder to left of cyclic durations:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 4), (1, 16)],
            ...     remainder=abjad.Left,
            ...     )

            >>> time_signatures = [(3, 4)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 8)), Division((1, 4)), Division((1, 16)), Division((1, 4)), Division((1, 16))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 3/4
                        c'8
                        c'4
                        c'16
                        c'4
                        c'16
                    } % measure
                }

        Defaults to right.

        Set to left or right.

        Returns left or right.
        '''
        return self._remainder

    @property
    def remainder_fuse_threshold(self):
        r'''Gets remainder fuse threshold of division-maker.

        ..  container:: example

            No threshold. Remainder unfused to the right:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     durations=[(1, 4)],
            ...     remainder_fuse_threshold=None,
            ...     )

            >>> time_signatures = [(5, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((1, 4)), Division((1, 8))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 5/8
                        c'4
                        c'4
                        c'8
                    } % measure
                }

        ..  container:: example

            Remainder less than or equal to ``1/8`` fused to the right:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     durations=[(1, 4)],
            ...     remainder_fuse_threshold=abjad.Duration(1, 8),
            ...     )

            >>> time_signatures = [(5, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 4)), Division((3, 8))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 5/8
                        c'4
                        c'4.
                    } % measure
                }

        ..  container:: example

            No threshold. Remainder unfused to the left:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 4)],
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=None,
            ...     )

            >>> time_signatures = [(5, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((1, 8)), Division((1, 4)), Division((1, 4))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 5/8
                        c'8
                        c'4
                        c'4
                    } % measure
                }

        ..  container:: example

            Remainder less than or equal to ``1/8`` fused to the left:

            >>> division_maker = baca.SplitByDurationsDivisionCallback(
            ...     cyclic=True,
            ...     durations=[(1, 4)],
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=abjad.Duration(1, 8),
            ...     )

            >>> time_signatures = [(5, 8)]
            >>> division_lists = division_maker(time_signatures)
            >>> for division_list in division_lists:
            ...     division_list
            ...
            [Division((3, 8)), Division((1, 4))]

            >>> rhythm_maker = rhythmos.NoteRhythmMaker()
            >>> divisions = baca.sequence(division_lists).flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, time_signatures)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
                \new RhythmicStaff {
                    { % measure
                        \time 5/8
                        c'4.
                        c'4
                    } % measure
                }

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._remainder_fuse_threshold

    ### PUBLIC METHODS ###

    @staticmethod
    def show(music, divisions):
        r'''Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        '''
        return abjad.LilyPondFile.rhythm(
            music,
            divisions=divisions,
            )
