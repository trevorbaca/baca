import abjad
import baca
from .Command import Command


class ColorCommand(Command):
    r'''Color command.

    ..  container:: example

        With music-maker:

        Selects leaves by default:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.ColorCommand(),
            ...     baca.MusicRhythmSpecifier(
            ...         rhythm_maker=baca.MusicRhythmMaker(
            ...             talea=abjad.rhythmmakertools.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            c'8 ~ [
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            c'32
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'8
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            bf'8 ]
                        }
                        {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            fs''8 ~ [
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            fs''32
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e''8
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            ef''8
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            af''8 ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            af''32
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            g''8 ]
                        }
                        {
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            a'8 ~ [
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            a'32 ]
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
            ...     baca.even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.ColorCommand(),
            ...     )

        ::

            >>> result = segment_maker.run(is_doc_example=True)
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
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                e'8 [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                d''8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f'8
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''8 ]
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g'8 [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f''8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e'8 ]
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                d''8 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f'8
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g'8 ]
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f''8 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e'8
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns selector result for Selector docs.
        '''
        if not argument:
            return
        selector = self.selector or baca.select().leaves()
        result = selector(argument)
        if False:
            print(format(selector))
            print('---')
            print(argument)
            print('---')
            print(result)
            print('---')
        abjad.label(result).color_selections(selector=self.selector)
        return result
