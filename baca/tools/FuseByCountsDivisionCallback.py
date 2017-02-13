# -*- coding: utf-8 -*-
import abjad
import baca


class FuseByCountsDivisionCallback(abjad.abctools.AbjadValueObject):
    r'''Fuse-by-counts division callback.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Fuses divisions together two at a time:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2],
            ...     )

        ::

            >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> divisions = division_maker(input_divisions)
            >>> divisions
            [Division((4, 8)), Division((8, 8)), Division((2, 4))]

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                c'2
                c'1
                c'2
            }

    ..  container:: example

        Fuses divisions together two at a time. Then splits resulting divisions
        by ``3/16`` durations:

        ::

            >>> division_maker = baca.tools.DivisionMaker()
            >>> division_maker = division_maker.fuse_by_counts(
            ...     counts=[2],
            ...     )
            >>> division_maker = division_maker.split_by_durations(
            ...     durations=[(3, 16)],
            ...     remainder=Right,
            ...     )

        ::

            >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> division_lists = division_maker(input_divisions)
            >>> for division_list in division_lists:
            ...     division_list
            [Division((3, 16)), Division((3, 16)), Division((1, 8))]
            [Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((1, 16))]
            [Division((3, 16)), Division((3, 16)), Division((1, 8))]

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
            >>> divisions = baca.Sequence(division_lists).flatten()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = division_maker.show(music, input_divisions)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                c'8.
                c'8.
                c'8
                c'8.
                c'8.
                c'8.
                c'8.
                c'8.
                c'16
                c'8.
                c'8.
                c'8
            }

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output.

    Treats input as time signatures. Glues input together into hypermeasures
    according to optional measure counts. Postprocesses resulting
    hypermeasures with optional secondary division-maker.

    Follows the two-step configure-once / call-repeatly pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Divisions'

    __slots__ = (
        '_cyclic',
        '_counts',
        '_secondary_division_maker',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=True,
        counts=None,
        secondary_division_maker=None,
        ):
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        counts = counts or ()
        if counts == abjad.Infinity:
            self._counts = counts
        else:
            assert abjad.mathtools.all_are_positive_integers(counts)
            self._counts = counts
        if secondary_division_maker is not None:
            prototype = (baca.tools.SplitByDurationsDivisionCallback,)
            assert isinstance(secondary_division_maker, prototype)
        self._secondary_division_maker = secondary_division_maker

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls fuse-by-counts division callback.

        ..  container:: example

            Returns divisions unfused:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts()

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [Division((2, 8)), Division((2, 8)), Division((4, 8)), Division((4, 8)), Division((2, 4))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 2/8
                        c'4
                    }
                    {
                        c'4
                    }
                    {
                        \time 4/8
                        c'2
                    }
                    {
                        c'2
                    }
                    {
                        \time 2/4
                        c'2
                    }
                }

        ..  container:: example

            Fuses divisions two at a time:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [Division((4, 8)), Division((8, 8)), Division((2, 4))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'2
                    c'1
                    c'2
                }

        ..  container:: example

            Fuses divisions two at a time. Then splits fused divisions by
            ``3/16`` durations.

            Remainders to the right:
            
            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(3, 16)],
                ...     remainder=Right,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((3, 16)), Division((3, 16)), Division((1, 8))]
                [Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((1, 16))]
                [Division((3, 16)), Division((3, 16)), Division((1, 8))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'8.
                    c'8.
                    c'8
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'16
                    c'8.
                    c'8.
                    c'8
                }

            Remainders to the left:
            
            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(3, 16)],
                ...     remainder=Left,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((1, 8)), Division((3, 16)), Division((3, 16))]
                [Division((1, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16))]
                [Division((1, 8)), Division((3, 16)), Division((3, 16))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'8
                    c'8.
                    c'8.
                    c'16
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8
                    c'8.
                    c'8.
                }

        ..  container:: example

            Fuses all divisions:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=abjad.Infinity,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = division_maker(input_divisions)
                >>> divisions
                [Division((16, 8))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'\breve
                }

        ..  container:: example

            Fuses all divisions. Then splits fused divisions by ``3/8``
            durations:

            Remainder at right:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=abjad.Infinity,
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(3, 16)],
                ...     remainder=Right,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((1, 8))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8
                }

            Remainder at left:

            ::

                >>> division_maker = baca.tools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=abjad.Infinity,
                ...     )
                >>> division_maker = division_maker.split_by_durations(
                ...     durations=[(3, 16)],
                ...     remainder=Left,
                ...     )

            ::

                >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list
                [Division((1, 8)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16)), Division((3, 16))]

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker()
                >>> divisions = baca.Sequence(division_lists).flatten()
                >>> music = rhythm_maker(divisions)
                >>> lilypond_file = division_maker.show(music, input_divisions)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    c'8
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                    c'8.
                }

        ..  container:: example

            Empty input:

            ::

                >>> input_divisions = []
                >>> division_lists = division_maker(input_divisions)
                >>> for division_list in division_lists:
                ...     division_list

            Works with start offset:

            ::

                >>> callback = baca.tools.FuseByCountsDivisionCallback(
                ...     counts=abjad.Infinity,
                ...     )

            ::

                >>> divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
                >>> divisions = [baca.tools.Division(_) for _ in divisions]
                >>> divisions[0] = abjad.new(
                ...     divisions[0],
                ...     start_offset=abjad.Offset(1, 4),
                ...     )
                >>> divisions
                [Division((0, 1), start_offset=Offset(1, 4)), Division((2, 8)), Division((4, 8)), Division((4, 8)), Division((2, 4))]

            ::

                >>> callback(divisions)
                [Division((14, 8), start_offset=Offset(1, 4))]

        Returns list of division lists.
        '''
        divisions = divisions or ()
        start_offset = None
        if divisions:
            start_offset = divisions[0].start_offset
        if not divisions:
            pass
        elif self.counts == abjad.Infinity:
            divisions = [sum(divisions)]
        elif self.counts:
            parts = baca.Sequence(divisions).partition_by_counts(
                self.counts,
                cyclic=self.cyclic,
                overhang=True,
                )
            divisions = [sum(_) for _ in parts]
        divisions = [baca.tools.Division(_) for _ in divisions]
        if self.secondary_division_maker is None:
            divisions, start_offset = baca.tools.DivisionMaker._to_divisions(
                divisions,
                start_offset,
                )
            return divisions
        division_lists = []
        for division in divisions:
            if self.secondary_division_maker is not None:
                division_list = self.secondary_division_maker([division])[0]
            else:
                division_list = [division]
            division_list = [
                baca.tools.Division(_) for _ in division_list]
            division_lists.append(division_list)
        division_lists, start_offset = baca.tools.DivisionMaker._to_divisions(
            division_lists, 
            start_offset=start_offset,
            )
        return division_lists

    ### PRIVATE METHODS ###

    def _coerce_divisions(self, divisions):
        divisions_ = []
        for division in divisions:
            if hasattr(division, 'time_signature'):
                argument = division.time_signature.pair
            elif hasattr(division, 'duration'):
                argument = division.duration
            else:
                argument = division
            division_ = baca.tools.Division(argument)
            divisions_.append(division_)
        return divisions_

    def _get_storage_format_specification(self):
        agent = abjad.systemtools.StorageFormatAgent(self)
        keyword_argument_names = agent.signature_keyword_names
        keyword_argument_names = list(keyword_argument_names)
        if self.cyclic == True:
            keyword_argument_names.remove('cyclic')
        if not self.counts:
            keyword_argument_names.remove('counts')
        return abjad.systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets measure counts of hypermeasure division-maker.

        Set to (possibly empty) list or tuple of positive integers.

        Or set to infinity.
        '''
        return self._counts

    @property
    def cyclic(self):
        r'''Is true when hypermeasure division-maker treats measure 
        counts cyclically. Otherwise false.

        Set to true or false.
        '''
        return self._cyclic

    @property
    def secondary_division_maker(self):
        r'''Gets hypermeasure postprocessor of hypermeasure division-maker.

        Returns division-maker or none.
        '''
        return self._secondary_division_maker
