# -*- coding: utf-8 -*-
import abjad
import baca


class DivisionMaker(abjad.abctools.AbjadValueObject):
    r'''Division-maker.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Splits every division by ``1/4`` with remainder at right:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
            [Division((1, 4)), Division((1, 8))]
            [Division((1, 4)), Division((1, 4)), Division((1, 8))]


        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> divisions = baca.Sequence(division_lists).flatten()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                {
                    \time 7/8
                    c'4
                    c'4
                    c'4
                    c'8
                }
                {
                    \time 3/8
                    c'4
                    c'8
                }
                {
                    \time 5/8
                    c'4
                    c'4
                    c'8
                }
            }

    ..  container:: example

        Fuses divisions:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=abjad.Infinity,
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = division_maker(input_divisions)
            >>> divisions
            [Division((15, 8))]


        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                c'1...
            }

        Fuses divisions and then splits by ``1/4`` with remainder on right:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=abjad.Infinity,
            ...     )
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(1, 4)],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> divisions = baca.Sequence(division_lists).flatten()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP


        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'8
            }

    ..  container:: example

        Splits every division by ``3/8``:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 8)],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [Division((3, 8)), Division((3, 8)), Division((1, 8))]
            [Division((3, 8))]
            [Division((3, 8)), Division((2, 8))]

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> divisions = baca.Sequence(division_lists).flatten()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                {
                    \time 7/8
                    c'4.
                    c'4.
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
                {
                    \time 5/8
                    c'4.
                    c'4
                }
            }

        Splits every division by ``3/8`` and then fuses flattened divisions
        into differently sized groups:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 8)],
            ...     )
            >>> division_maker = division_maker.flatten()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2, 3, 1],
            ...     )

        ::

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = division_maker(input_divisions)
            >>> divisions
            [Division((6, 8)), Division((7, 8)), Division((2, 8))]

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                c'2.
                c'2..
                c'4
            }

    ..  container:: example

        Splits every division by ``3/8`` and then fuses flattened divisions
        into differently sized groups. Works with start offset:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 8)],
            ...     )
            >>> division_maker = division_maker.flatten()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2, 3, 1],
            ...     )

        ::

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [baca.tools.Division(_) for _ in divisions]
            >>> divisions[0]._start_offset = abjad.Offset(1, 4)
            >>> divisions = division_maker(divisions)
            >>> for division in divisions:
            ...     division
            Division((6, 8), start_offset=Offset(1, 4))
            Division((7, 8), start_offset=Offset(1, 1))
            Division((2, 8), start_offset=Offset(15, 8))

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                c'2.
                c'2..
                c'4
            }

    Division-makers object-model a sequence of partially evaluated functions 
    taken together in functional composition.

    Usage follows the two-step configure-once / call-repeatedly pattern shown 
    here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Divisions'

    __slots__ = (
        '_callbacks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        callbacks=None,
        ):
        callbacks = callbacks or ()
        if callbacks:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Makes divisions from `argument`.

        Pass in `argument` as either a list of divisions or as a list of division
        lists.

        Returns either a list of divisions or a list of division lists.
        '''
        argument = argument or []
        argument, start_offset = self._to_divisions(argument)
        for callback in self.callbacks:
            argument = callback(argument)
        result, start_offset = self._to_divisions(argument)
        return result

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = abjad.new(self)
        result._callbacks = callbacks
        return result

    @staticmethod
    def _is_flat_list(argument):
        if isinstance(argument, list):
            if not(argument):
                return True
            elif not isinstance(argument[0], list):
                return True
        return False

    @staticmethod
    def _to_divisions(argument, start_offset=None):
        if isinstance(argument, baca.tools.Division):
            result = baca.tools.Division(argument)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif isinstance(argument, abjad.mathtools.NonreducedFraction):
            result = baca.tools.Division(argument.pair)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif hasattr(argument, 'pair'):
            result = baca.tools.Division(argument.pair)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif isinstance(argument, tuple):
            result = baca.tools.Division(argument)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif isinstance(argument, (list, abjad.sequencetools.Sequence)):
            result = []
            for element in argument:
                new_element, start_offset = DivisionMaker._to_divisions(
                    element,
                    start_offset=start_offset,
                    )
                result.append(new_element)
            result = type(argument)(result)
        else:
            raise TypeError(repr(argument))
        return result, start_offset

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets division-maker callbacks.

        ..  container:: example

            No callbacks:

            ::

                >>> division_maker = baca.tools.DivisionMaker()

            ::

                >>> division_maker.callbacks
                ()

        ..  container:: example

            One callback:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> division_maker.callbacks
                (SplitByDurationsDivisionCallback(compound_meter_multiplier=Multiplier(1, 1), cyclic=True, durations=(Division((1, 4)),), pattern_rotation_index=0, remainder=Right),)

        Returns tuple of zero or more callbacks.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def append_callback(self, callback):
        r'''Configures division-maker with arbitrary `callback`.

        Returns new division-maker.
        '''
        return self._append_callback(callback)

    def flatten(self, depth=-1):
        r'''Flattens division lists.

        Returns new division-maker.
        '''
        callback = baca.tools.FlattenDivisionCallback(depth=depth)
        return self._append_callback(callback)

    def fuse_by_counts(
        self,
        cyclic=True,
        counts=None,
        ):
        r'''Fuses divisions (or division lists) by `counts`.

        ..  container:: example

            Fuses every two divisions together:
 
            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )

            ::

                >>> input_divisions = [(7, 8), (7, 8), (7, 16)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [Division((14, 8)), Division((7, 16))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'1..
                    c'4..
                }

        '''
        callback = baca.tools.FuseByCountsDivisionCallback(
            cyclic=cyclic,
            counts=counts,
            )
        return self._append_callback(callback)

    def partition_by_counts(
        self,
        counts=None,
        fuse_assignable_total_duration=False,
        append_remainder=False,
        remainder_direction=Right,
        ):
        r'''Partitions divisions (or division lists) by `counts`.

        ..  container:: example

            Partitions divisions into pairs with remainder at right:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> for item in division_maker(divisions):
                ...     item
                ...
                Sequence([Division((1, 8)), Division((1, 8))])
                Sequence([Division((1, 4)), Division((1, 4))])
                [Division((1, 16))]

            Partitions divisions into pairs with remainder appended at right:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> for item in division_maker(divisions):
                ...     item
                ...
                Sequence([Division((1, 8)), Division((1, 8))])
                Sequence([Division((1, 4)), Division((1, 4)), Division((1, 16))])

            Partitions divisions into pairs with remainder at left:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> for item in division_maker(divisions):
                ...     item
                ...
                [Division((1, 8))]
                Sequence([Division((1, 8)), Division((1, 4))])
                Sequence([Division((1, 4)), Division((1, 16))])

            Partitions divisions into pairs with remainder appeneded at left:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> divisions = [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)]
                >>> for item in division_maker(divisions):
                ...     item
                ...
                Sequence([Division((1, 8)), Division((1, 8)), Division((1, 4))])
                Sequence([Division((1, 4)), Division((1, 16))])

            These examples show how the class partitions a flat list of
            divisions. Output equal to one nested division list.

        ..  container:: example

            Partitions division lists into pairs with remainders at right:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                ...
                [Sequence([Division((1, 8)), Division((1, 8))]), [Division((1, 4))]]
                [Sequence([Division((1, 8)), Division((1, 8))]), Sequence([Division((1, 4)), Division((1, 4))]), [Division((1, 16))]]

            Partitions division lists into pairs with remainders appended at
            right:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                ...
                [Sequence([Division((1, 8)), Division((1, 8)), Division((1, 4))])]
                [Sequence([Division((1, 8)), Division((1, 8))]), Sequence([Division((1, 4)), Division((1, 4)), Division((1, 16))])]

            Partitions division lists into pairs with remainders at left:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                ...
                [[Division((1, 8))], Sequence([Division((1, 8)), Division((1, 4))])]
                [[Division((1, 8))], Sequence([Division((1, 8)), Division((1, 4))]), Sequence([Division((1, 4)), Division((1, 16))])]

            Partitions division lists into pairs with remainders appended at
            left:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.partition_by_counts(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> division_lists = [
                ...     [(1, 8), (1, 8), (1, 4)],
                ...     [(1, 8), (1, 8), (1, 4), (1, 4), (1, 16)],
                ...     ]
                >>> partitioned_division_lists = division_maker(division_lists)
                >>> for partitioned_division_list in partitioned_division_lists:
                ...     partitioned_division_list
                ...
                [Sequence([Division((1, 8)), Division((1, 8)), Division((1, 4))])]
                [Sequence([Division((1, 8)), Division((1, 8)), Division((1, 4))]), Sequence([Division((1, 4)), Division((1, 16))])]

            These examples show how the class automatically maps over multiple
            input division lists. Output equal to arbitrarily many nested
            division lists.

        Returns new division-maker.
        '''
        callback = baca.tools.PartitionDivisionCallback(
            counts=counts,
            fuse_assignable_total_duration=fuse_assignable_total_duration,
            append_remainder=append_remainder,
            remainder_direction=remainder_direction,
            )
        return self._append_callback(callback)

    @staticmethod
    def show(music, divisions):
        r'''Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        '''
        return abjad.rhythmmakertools.make_lilypond_file(
            music,
            divisions=divisions,
            )
        
    def split_by_durations(
        self,
        compound_meter_multiplier=abjad.durationtools.Multiplier(1),
        cyclic=True,
        durations=(),
        pattern_rotation_index=0,
        remainder=Right,
        remainder_fuse_threshold=None,
        ):
        r'''Splits divisions by durations.

        ..  container:: example

            Makes quarter-valued divisions with remainder at right:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(1, 4)],
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
                [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))]
                [Division((1, 4)), Division((3, 16))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                    {
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                    {
                        \time 7/16
                        c'4
                        c'8.
                    }
                }

        ..  container:: example

            Makes quarter-valued divisions with remainder at left:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(1, 4)],
                ...     remainder=Left,
                ...     )

            ::

                >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
                >>> division_lists = division_maker(time_signatures)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((1, 8)), Division((1, 4)), Division((1, 4)), Division((1, 4))]
                [Division((1, 8)), Division((1, 4)), Division((1, 4)), Division((1, 4))]
                [Division((3, 16)), Division((1, 4))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/8
                        c'8
                        c'4
                        c'4
                        c'4
                    }
                    {
                        c'8
                        c'4
                        c'4
                        c'4
                    }
                    {
                        \time 7/16
                        c'8.
                        c'4
                    }
                }

        Returns new division-maker.
        '''
        callback = baca.tools.SplitByDurationsDivisionCallback(
            compound_meter_multiplier=compound_meter_multiplier,
            cyclic=cyclic,
            durations=durations,
            pattern_rotation_index=pattern_rotation_index,
            remainder=remainder,
            remainder_fuse_threshold=remainder_fuse_threshold,
            )
        return self._append_callback(callback)

    def split_by_rounded_ratios(
        self,
        ratios=None,
        ):
        r'''Splits divisions by rounded ratios.

        ..  container:: example

            Makes divisions with ``2:1`` ratios:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.split_by_rounded_ratios(
                ...     ratios=[abjad.Ratio([2, 1])],
                ...     )

            ::

                >>> input_divisions = [(5, 8), (6, 8)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((3, 8)), Division((2, 8))]
                [Division((4, 8)), Division((2, 8))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4.
                        c'4
                    }
                    {
                        \time 6/8
                        c'2
                        c'4
                    }
                }


        ..  container:: example

            Makes divisions with alternating ``2:1`` and ``1:1:1`` ratios:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.split_by_rounded_ratios(
                ...     ratios=[
                ...         abjad.Ratio([2, 1]),
                ...         abjad.Ratio([1, 1, 1]),
                ...         ],
                ...     )

            ::

                >>> input_divisions = [(5, 8), (6, 8)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((3, 8)), Division((2, 8))]
                [Division((2, 8)), Division((2, 8)), Division((2, 8))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4.
                        c'4
                    }
                    {
                        \time 6/8
                        c'4
                        c'4
                        c'4
                    }
                }

        Returns new division-maker.
        '''
        callback = baca.tools.SplitByRoundedRatiosDivisionCallback(
            ratios=ratios,
            )
        return self._append_callback(callback)
