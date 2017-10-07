import abjad
import baca
from .Command import Command


class GlissandoCommand(Command):
    r'''Glissando command.

    ..  container:: example

        Selects all logical ties:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'Violin Music Voice',
            ...     baca.select_stages(1),
            ...     baca.even_runs(),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.GlissandoCommand()
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
                                e'8 \glissando [
                                d''8 \glissando
                                f'8 \glissando
                                e''8 ] \glissando
                            }
                            {
                                g'8 \glissando [
                                f''8 \glissando
                                e'8 ] \glissando
                            }
                            {
                                d''8 \glissando [
                                f'8 \glissando
                                e''8 \glissando
                                g'8 ] \glissando
                            }
                            {
                                f''8 \glissando [
                                e'8 \glissando
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Selects first and last pitched logical ties:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'Violin Music Voice',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.even_runs(),
            ...     baca.GlissandoCommand(baca.select_plts(stop=2)),
            ...     baca.GlissandoCommand(baca.select_plts(start=-2)),
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
                                e'8 \glissando [
                                d''8
                                f'8
                                e''8 ]
                            }
                            {
                                g'8 [
                                f''8
                                e'8 ]
                            }
                            {
                                d''8 [
                                f'8
                                e''8
                                g'8 ]
                            }
                            {
                                f''8 [
                                e'8 \glissando
                                d''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Selects first stage with music-maker:

        ::

            >>> music_maker = baca.MusicMaker()

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.GlissandoCommand(baca.select_tuplet(0)),
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
                            c'16 \glissando [
                            d'16 \glissando
                            bf'16 ]
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

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, selector=None):
        if selector is not None:
            assert isinstance(selector, abjad.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        selector = baca.select_plts()
        plts = selector(argument)
        for i, plt in enumerate(plts):
            if i + 1 < len(plts):
                self._attach_glissando(plt)

    ### PRIVATE METHODS ###

    def _attach_glissando(self, logical_tie):
        note_or_chord = (abjad.Note, abjad.Chord)
        last_leaf = logical_tie.tail
        if not isinstance(last_leaf, note_or_chord):
            return
        next_leaf = abjad.inspect(last_leaf).get_leaf(1)
        if not isinstance(next_leaf, note_or_chord):
            return
        leaves = abjad.select([last_leaf, next_leaf])
        abjad.attach(abjad.Glissando(), leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
