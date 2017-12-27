import abjad
import baca
from .Command import Command


class LabelCommand(Command):
    r'''Label command.

    ..  container:: example

        Labels pitch names:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=True)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar ""        %%! EMPTY_START_BAR:1
                        s1 * 1/2
                        - \markup {                               %%! STAGE_NUMBER_MARKUP:2
                            \fontsize                             %%! STAGE_NUMBER_MARKUP:2
                                #-3                               %%! STAGE_NUMBER_MARKUP:2
                                \with-color                       %%! STAGE_NUMBER_MARKUP:2
                                    #(x11-color 'DarkCyan)        %%! STAGE_NUMBER_MARKUP:2
                                    [1]                           %%! STAGE_NUMBER_MARKUP:2
                            }                                     %%! STAGE_NUMBER_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                e'8
                                [
                                ^ \markup {
                                    \small
                                        E4
                                    }
            <BLANKLINE>
                                d''8
                                ^ \markup {
                                    \small
                                        D5
                                    }
            <BLANKLINE>
                                f'8
                                ^ \markup {
                                    \small
                                        F4
                                    }
            <BLANKLINE>
                                e''8
                                ]
                                ^ \markup {
                                    \small
                                        E5
                                    }
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                g'8
                                [
                                ^ \markup {
                                    \small
                                        G4
                                    }
            <BLANKLINE>
                                f''8
                                ^ \markup {
                                    \small
                                        F5
                                    }
            <BLANKLINE>
                                e'8
                                ]
                                ^ \markup {
                                    \small
                                        E4
                                    }
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                d''8
                                [
                                ^ \markup {
                                    \small
                                        D5
                                    }
            <BLANKLINE>
                                f'8
                                ^ \markup {
                                    \small
                                        F4
                                    }
            <BLANKLINE>
                                e''8
                                ^ \markup {
                                    \small
                                        E5
                                    }
            <BLANKLINE>
                                g'8
                                ]
                                ^ \markup {
                                    \small
                                        G4
                                    }
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                f''8
                                [
                                ^ \markup {
                                    \small
                                        F5
                                    }
            <BLANKLINE>
                                e'8
                                ^ \markup {
                                    \small
                                        E4
                                    }
            <BLANKLINE>
                                d''8
                                ]
                                ^ \markup {
                                    \small
                                        D5
                                    }
                                \bar "|"
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
        ...         baca.tuplet(0),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=True)
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'16
                            [
                            ^ \markup {
                                \small
                                    C4
                                }
                            d'16
                            ^ \markup {
                                \small
                                    D4
                                }
                            bf'16
                            ]
                            ^ \markup {
                                \small
                                    Bb4
                                }
                        }
                        {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        {
                            a'16
                        }
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(self, expression=None, selector='baca.leaves()'):
        Command.__init__(self, selector=selector)
        if expression is not None:
            assert isinstance(expression, abjad.Expression)
        self._expression = expression

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
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
        r'''Gets expression.

        Defaults to none.

        Set to label expression or none.

        Returns label expression or none.
        '''
        return self._expression
