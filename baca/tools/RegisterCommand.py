import abjad
import baca
from .Command import Command


class RegisterCommand(Command):
    r"""Register command.

    ..  container:: example

        With music-maker:

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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf''16
                            [
                            c'''16
                            d'''16
                            ]
                        }
                        {
                            bf''16
                            [
                            c'''16
                            d'''16
                            ]
                        }
                        {
                            bf''16
                            [
                            c'''16
                            d'''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        First stage only:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 0)],
        ...             ),
        ...         selector=baca.tuplet(0),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf'16
                            [
                            c'16
                            d'16
                            ]
                        }
                        {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                        {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        Last stage only:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 0)],
        ...             ),
        ...         selector=baca.tuplet(-1),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                        {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                        {
                            bf'16
                            [
                            c'16
                            d'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
        ...     baca.make_even_runs(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 15)],
        ...             ),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 1                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \bar ""                                                                      %! EMPTY_START_BAR:SM2
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {                                                                  %! STAGE_NUMBER_MARKUP:SM3
                            \fontsize                                                                %! STAGE_NUMBER_MARKUP:SM3
                                #-3                                                                  %! STAGE_NUMBER_MARKUP:SM3
                                \with-color                                                          %! STAGE_NUMBER_MARKUP:SM3
                                    #(x11-color 'DarkCyan)                                           %! STAGE_NUMBER_MARKUP:SM3
                                    [1]                                                              %! STAGE_NUMBER_MARKUP:SM3
                            }                                                                        %! STAGE_NUMBER_MARKUP:SM3
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                g''8
                                [
            <BLANKLINE>
                                gqs''8
            <BLANKLINE>
                                gs''8
            <BLANKLINE>
                                gtqs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                aqf''8
                                [
            <BLANKLINE>
                                af''8
            <BLANKLINE>
                                atqf''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                g''8
                                [
            <BLANKLINE>
                                gqs''8
            <BLANKLINE>
                                gs''8
            <BLANKLINE>
                                gtqs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                aqf''8
                                [
            <BLANKLINE>
                                af''8
            <BLANKLINE>
                                atqf''8
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Works with chords:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{10, 12, 14}],
        ...     baca.RegisterCommand(
        ...         baca.Registration([('[A0, C8]', -6)]),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_registration',
        )

    ### INITIALIZER ###

    def __init__(self, registration=None, selector='baca.plts()'):
        import baca
        Command.__init__(self, selector=selector)
        if registration is not None:
            prototype = baca.Registration
            assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.registration is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for plt in baca.select(argument).plts():
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

            >>> command = baca.RegisterCommand(
            ...     registration=baca.Registration(
            ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
            ...         ),
            ...     )

            >>> abjad.f(command.registration, strict=89)
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
