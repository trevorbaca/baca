import abjad
import baca
from .Command import Command


class LabelCommand(Command):
    r"""
    Label command.

    ..  container:: example

        Labels pitch names:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                e'8
                                [
                                ^ \markup { E4 }
            <BLANKLINE>
                                d''8
                                ^ \markup { D5 }
            <BLANKLINE>
                                f'8
                                ^ \markup { F4 }
            <BLANKLINE>
                                e''8
                                ]
                                ^ \markup { E5 }
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                g'8
                                [
                                ^ \markup { G4 }
            <BLANKLINE>
                                f''8
                                ^ \markup { F5 }
            <BLANKLINE>
                                e'8
                                ]
                                ^ \markup { E4 }
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                d''8
                                [
                                ^ \markup { D5 }
            <BLANKLINE>
                                f'8
                                ^ \markup { F4 }
            <BLANKLINE>
                                e''8
                                ^ \markup { E5 }
            <BLANKLINE>
                                g'8
                                ]
                                ^ \markup { G4 }
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                f''8
                                [
                                ^ \markup { F5 }
            <BLANKLINE>
                                e'8
                                ^ \markup { E4 }
            <BLANKLINE>
                                d''8
                                ]
                                ^ \markup { D5 }
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Labels pitch names in tuplet 0:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.label(
        ...         abjad.label().with_pitches(locale='us'),
        ...         selector=baca.tuplet(0),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            ^ \markup { C4 }
                            d'16
                            ^ \markup { D4 }
                            bf'16
                            ]
                            ^ \markup { Bb4 }
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        expression=None,
        selector='baca.leaves()',
        ):
        Command.__init__(self, selector=selector)
        if expression is not None:
            assert isinstance(expression, abjad.Expression)
        self._expression = expression

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls command on `argument`.

        Returns none.
        """
        if argument is None:
            return
        if self.expression is None:
            return
        if self.selector:
            argument = self.selector(argument)
        self.expression(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def expression(self):
        """
        Gets expression.

        Defaults to none.

        Set to label expression or none.

        Returns label expression or none.
        """
        return self._expression
