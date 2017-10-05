import abjad
import baca
import itertools


class ColorFingeringCommand(abjad.AbjadObject):
    r'''Color fingering command.

    ..  container:: example

        Initializes with number lists:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'Violin Music Voice',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4', allow_repeat_pitches=True),
            ...     baca.messiaen_notes(),
            ...     baca.ColorFingeringCommand(
            ...         number_lists=([0, 1, 2, 1],),
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            e'2
                            e'4.
                                ^ \markup {
                                    \override
                                        #'(circle-padding . 0.25)
                                        \circle
                                            \finger
                                                1
                                    }
                            e'2
                                ^ \markup {
                                    \override
                                        #'(circle-padding . 0.25)
                                        \circle
                                            \finger
                                                2
                                    }
                            e'4.
                                ^ \markup {
                                    \override
                                        #'(circle-padding . 0.25)
                                        \circle
                                            \finger
                                                1
                                    }
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_by_pitch_run',
        '_deposit_annotations',
        '_number_lists',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        by_pitch_run=None,
        deposit_annotations=None,
        number_lists=None,
        selector=None,
        ):
        self._by_pitch_run = by_pitch_run
        if deposit_annotations is not None:
            deposit_annotations = tuple(deposit_annotations)
        self._deposit_annotations = deposit_annotations
        if number_lists is not None:
            number_lists = tuple(number_lists)
            for number_list in number_lists:
                assert abjad.mathtools.all_are_nonnegative_integers(
                    number_list)
        self._number_lists = number_lists
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector


    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        selector = self.selector or baca.select_plts()
        selections = selector(argument)
        assert len(selections) == 1, repr(selections)
        logical_ties = selections[0]
        if self.number_lists is None:
            return
        number_lists = abjad.CyclicTuple(self.number_lists)
        if not self.by_pitch_run:
            assert len(self.number_lists) == 1
            number_list = self.number_lists[0]
            number_list = abjad.CyclicTuple(number_list)
            for i, logical_tie in enumerate(logical_ties):
                number = number_list[i]
                if not number == 0:
                    fingering = abjad.ColorFingering(number)
                    abjad.attach(fingering, logical_tie.head)
                self._attach_deposit_annotations(logical_tie.head)
        else:
            number_list_index = 0
            pairs = itertools.groupby(
                logical_ties,
                lambda _: _.head.written_pitch,
                )
            for key, values in pairs:
                values = list(values)
                if len(values) == 1 and not self.by_pitch_run:
                    continue
                number_list = number_lists[number_list_index]
                number_list = abjad.CyclicTuple(number_list)
                for i, logical_tie in enumerate(values):
                    number = number_list[i]
                    if not number == 0:
                        fingering = abjad.ColorFingering(number)
                        abjad.attach(fingering, logical_tie.head)
                    self._attach_deposit_annotations(logical_tie.head)
                number_list_index += 1

    ### PRIVATE METHODS ###

    def _attach_deposit_annotations(self, note):
        if not self.deposit_annotations:
            return
        for annotation_name in self.deposit_annotations:
            annotation = {annotation_name: True}
            abjad.attach(annotation, note)

    ### PUBLIC PROPERTIES ###

    @property
    def by_pitch_run(self):
        r'''Is true when fingerings attach by pitch run. Is false when
        fingerings attach to every note.

        ..  container:: example

            Attaches color fingerings to every note:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'Violin Music Voice',
                ...     baca.select_stages(1),
                ...     baca.pitches('C4 D4 E4 F4'),
                ...     baca.messiaen_notes(),
                ...     baca.ColorFingeringCommand(
                ...         number_lists=([0, 1, 2, 1],),
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 4/8
                                R1 * 1/2
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                            {
                                \time 4/8
                                R1 * 1/2
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                            }
                            {
                                \time 3/8
                                s1 * 3/8
                            }
                            {
                                \time 4/8
                                s1 * 1/2
                            }
                            {
                                \time 3/8
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                c'2
                                d'4.
                                    ^ \markup {
                                        \override
                                            #'(circle-padding . 0.25)
                                            \circle
                                                \finger
                                                    1
                                        }
                                e'2
                                    ^ \markup {
                                        \override
                                            #'(circle-padding . 0.25)
                                            \circle
                                                \finger
                                                    2
                                        }
                                f'4.
                                    ^ \markup {
                                        \override
                                            #'(circle-padding . 0.25)
                                            \circle
                                                \finger
                                                    1
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        ..  container:: example

            Attaches color fingerings by pitch run:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'Violin Music Voice',
                ...     baca.select_stages(1),
                ...     baca.pitches(
                ...         'C4 D4 D4 D4 E4 F4 F4',
                ...         allow_repeat_pitches=True,
                ...         ),
                ...     baca.even_runs(),
                ...     baca.ColorFingeringCommand(
                ...         by_pitch_run=True,
                ...         number_lists=([1, 2, 1],),
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 4/8
                                R1 * 1/2
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                            {
                                \time 4/8
                                R1 * 1/2
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                            }
                            {
                                \time 3/8
                                s1 * 3/8
                            }
                            {
                                \time 4/8
                                s1 * 1/2
                            }
                            {
                                \time 3/8
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    c'8 [
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    d'8
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    d'8
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        2
                                            }
                                    d'8 ]
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                }
                                {
                                    e'8 [
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    f'8
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    f'8 ]
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        2
                                            }
                                }
                                {
                                    c'8 [
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    d'8
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    d'8
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        2
                                            }
                                    d'8 ]
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                }
                                {
                                    e'8 [
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    f'8
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        1
                                            }
                                    f'8 ]
                                        ^ \markup {
                                            \override
                                                #'(circle-padding . 0.25)
                                                \circle
                                                    \finger
                                                        2
                                            }
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._by_pitch_run

    @property
    def deposit_annotations(self):
        r'''Gets deposit annotations of command.

        These will be attached to every note affected at call time.

        Set to annotations or none.
        '''
        return self._deposit_annotations

    @property
    def number_lists(self):
        r'''Gets number lists of color fingering command.

        ..  container:: example

            ::

                >>> command = baca.ColorFingeringCommand(
                ...     number_lists=(
                ...         [0, 1, 2, 1],
                ...         ),
                ...     )

            ::

                >>> command.number_lists
                ([0, 1, 2, 1],)

        Set to nested list of nonnegative integers or none.
        '''
        return self._number_lists

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
