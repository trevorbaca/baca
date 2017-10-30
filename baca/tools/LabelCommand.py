import abjad
import baca
from .Command import Command


class LabelCommand(Command):
    r'''Label command.

    ..  container:: example

        Labels pitch names:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     )

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
                                e'8 [
                                    ^ \markup {
                                        \small
                                            E4
                                        }
                                d''8
                                    ^ \markup {
                                        \small
                                            D5
                                        }
                                f'8
                                    ^ \markup {
                                        \small
                                            F4
                                        }
                                e''8 ]
                                    ^ \markup {
                                        \small
                                            E5
                                        }
                            }
                            {
                                g'8 [
                                    ^ \markup {
                                        \small
                                            G4
                                        }
                                f''8
                                    ^ \markup {
                                        \small
                                            F5
                                        }
                                e'8 ]
                                    ^ \markup {
                                        \small
                                            E4
                                        }
                            }
                            {
                                d''8 [
                                    ^ \markup {
                                        \small
                                            D5
                                        }
                                f'8
                                    ^ \markup {
                                        \small
                                            F4
                                        }
                                e''8
                                    ^ \markup {
                                        \small
                                            E5
                                        }
                                g'8 ]
                                    ^ \markup {
                                        \small
                                            G4
                                        }
                            }
                            {
                                f''8 [
                                    ^ \markup {
                                        \small
                                            F5
                                        }
                                e'8
                                    ^ \markup {
                                        \small
                                            E4
                                        }
                                d''8 ]
                                    ^ \markup {
                                        \small
                                            D5
                                        }
                                \bar "|"
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
        ...         baca.select().tuplet(0),
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
                            c'16 [
                                ^ \markup {
                                    \small
                                        C4
                                    }
                            d'16
                                ^ \markup {
                                    \small
                                        D4
                                    }
                            bf'16 ]
                                ^ \markup {
                                    \small
                                        Bb4
                                    }
                        }
                        {
                            fs''16 [
                            e''16
                            ef''16
                            af''16
                            g''16 ]
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

    def __init__(
        self,
        expression=None,
        selector='baca.select().leaves().group()',
        ):
        Command.__init__(self, selector=selector)
        if expression is not None:
            assert isinstance(expression, abjad.Expression)
        self._expression = expression

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
        selections = self._select(music)
        if self.expression is None:
            return
        for selection in selections:
            self.expression(selection)

    ### PUBLIC PROPERTIES ###

    @property
    def expression(self):
        r'''Gets expression.

        Defaults to none.

        Set to label expression or none.

        Returns label expression or none.
        '''
        return self._expression
