import abjad
import baca


class RegisterCommand(abjad.AbjadObject):
    r"""Register command.

    ::

        >>> import baca

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
            ...     baca.RegisterCommand(
            ...         registration=abjad.Registration(
            ...             [('[A0, C8]', 15)],
            ...             ),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf''16 [
                            c'''16
                            d'''16 ]
                        }
                        {
                            bf''16 [
                            c'''16
                            d'''16 ]
                        }
                        {
                            bf''16 [
                            c'''16
                            d'''16 ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
            ...     baca.even_runs(),
            ...     baca.RegisterCommand(
            ...         registration=abjad.Registration(
            ...             [('[A0, C8]', 15)],
            ...             ),
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
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                g''8 [
                                gqs''8
                                gs''8
                                gtqs''8 ]
                            }
                            {
                                aqf''8 [
                                af''8
                                atqf''8 ]
                            }
                            {
                                g''8 [
                                gqs''8
                                gs''8
                                gtqs''8 ]
                            }
                            {
                                aqf''8 [
                                af''8
                                atqf''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_pattern',
        '_registration',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, pattern=None, registration=None, selector=None):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        if registration is not None:
            prototype = abjad.Registration
            assert isinstance(registration, prototype), repr(registration)
        self._registration = registration
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        ..  container:: example

            Works with chords:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{10, 12, 14}],
                ...     baca.RegisterCommand(
                ...         registration=abjad.Registration(
                ...             [('[A0, C8]', -6)],
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                <bf c' d'>16
                            }
                        }
                    }
                >>

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if isinstance(argument, baca.ScopedSpecifier):
            selections = [argument]
        if isinstance(argument, abjad.Selection):
            selections = [argument]
        else:
            assert isinstance(argument, list), repr(argument)
            assert isinstance(argument[0], abjad.Selection), repr(argument)
            selections = argument
        pattern = self.pattern or abjad.index_all()
        selections = pattern.get_matching_items(selections)
        for selection in selections:
            for logical_tie in abjad.iterate(selection).by_logical_tie(
                pitched=True,
                with_grace_notes=True,
                ):
                for leaf in logical_tie:
                    if isinstance(leaf, abjad.Note):
                        written_pitch = leaf.written_pitch
                        written_pitches = self.registration([written_pitch])
                        leaf.written_pitch = written_pitches[0]
                    elif isinstance(leaf, abjad.Chord):
                        written_pitches = leaf.written_pitches
                        written_pitches = self.registration(written_pitches)
                        leaf.written_pitches = written_pitches
                    else:
                        raise TypeError(leaf)
                    abjad.detach('not yet registered', leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            First stage only:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
                ...     baca.RegisterCommand(
                ...         pattern=abjad.index_first(),
                ...         registration=abjad.Registration(
                ...             [('[A0, C8]', 0)],
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                bf'16 [
                                c'16
                                d'16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Last stage only:

            ::

                >>> music_maker = baca.MusicMaker()

            ::

                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
                ...     baca.RegisterCommand(
                ...         pattern=abjad.index_last(),
                ...         registration=abjad.Registration(
                ...             [('[A0, C8]', 0)],
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c'16
                                d'16 ]
                            }
                        }
                    }
                >>

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def registration(self):
        r'''Gets registration.

        ..  container:: example

            ::

                >>> command = baca.RegisterCommand(
                ...     registration=abjad.Registration(
                ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
                ...         ),
                ...     )

            ::

                >>> command.registration
                Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])

        Set to registration or none.

        Returns registration or none.
        '''
        return self._registration

    @property
    def selector(self):
        r'''Gets selector.

        Set to selector or none.
        '''
        return self._selector
