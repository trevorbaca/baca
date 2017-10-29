import abjad
import baca
from .Command import Command


class RegisterCommand(Command):
    r"""Register command.

    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
            ...     baca.RegisterCommand(
            ...         registration=baca.Registration(
            ...             [('[A0, C8]', 15)],
            ...             ),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
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

        First stage only:

        ::

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
            ...     baca.RegisterCommand(
            ...         registration=baca.Registration(
            ...             [('[A0, C8]', 0)],
            ...             ),
            ...         selector=baca.select().tuplet(0),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
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
            ...         registration=baca.Registration(
            ...             [('[A0, C8]', 0)],
            ...             ),
            ...         selector=baca.select().tuplet(-1),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
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

    ..  container:: example

        With segment-maker:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
            ...     baca.even_runs(),
            ...     baca.RegisterCommand(
            ...         registration=baca.Registration(
            ...             [('[A0, C8]', 15)],
            ...             ),
            ...         ),
            ...     )

        ::

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
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

    __slots__ = (
        '_registration',
        )

    ### INITIALIZER ###

    def __init__(self, registration=None, selector=None):
        import baca
        Command.__init__(self, selector=selector)
        if registration is not None:
            prototype = baca.Registration
            assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        ..  container:: example

            Works with chords:

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Voice 1',
                ...     [{10, 12, 14}],
                ...     baca.RegisterCommand(
                ...         baca.Registration([('[A0, C8]', -6)]),
                ...         ),
                ...     )
                >>> lilypond_file = music_maker.show(contribution)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        selections = self._select(music)
        for selection in selections:
            plts = baca.select().plts()(selection)
            for plt in plts:
                for pleaf in plt:
                    if isinstance(pleaf, abjad.Note):
                        pitch = pleaf.written_pitch
                        pitches = self.registration([pitch])
                        pleaf.written_pitch = pitches[0]
                    elif isinstance(pleaf, abjad.Chord):
                        pitches = pleaf.written_pitches
                        pitches = self.registration(pitches)
                        pleaf.written_pitches = pitches
                    else:
                        raise TypeError(pleaf)
                    abjad.detach('not yet registered', pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def registration(self):
        r'''Gets registration.

        ..  container:: example

            ::

                >>> command = baca.RegisterCommand(
                ...     registration=baca.Registration(
                ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
                ...         ),
                ...     )

            ::

                >>> abjad.f(command.registration)
                baca.Registration(
                    components=[
                        baca.RegistrationComponent(
                            source_pitch_range=abjad.PitchRange('[A0, C4)'),
                            target_octave_start_pitch=abjad.NumberedPitch(15),
                            ),
                        baca.RegistrationComponent(
                            source_pitch_range=abjad.PitchRange('[C4, C8)'),
                            target_octave_start_pitch=abjad.NumberedPitch(27),
                            ),
                        ],
                    )

        Set to registration or none.

        Returns registration or none.
        '''
        return self._registration
