# -*- coding: utf-8 -*-
import abjad
from baca.tools.ScoreTemplate import ScoreTemplate


class ViolinSoloScoreTemplate(ScoreTemplate):
    r'''Violin solo score template.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.**

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
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
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            R1 * 1/2
                            R1 * 3/8
                            R1 * 1/2
                            R1 * 3/8
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    voice_abbreviations = {
        'vn': 'Violin Music Voice',
        }

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls violin solo score template.

        Returns score.
        '''

        time_signature_context = self._make_time_signature_context()

        instrument_tags = (
            'violin',
            )
        tag_string = '.'.join(instrument_tags)
        tag_string = 'tag {}'.format(tag_string)
        tag_command = abjad.indicatortools.LilyPondCommand(
            tag_string,
            'before',
            )
        abjad.attach(tag_command, time_signature_context)

        violin_music_voice = abjad.scoretools.Voice(
            [], 
            context_name='ViolinMusicVoice',
            name=self.voice_abbreviations['vn'],
            )
        violin_music_staff = abjad.scoretools.Staff(
            [violin_music_voice], 
            context_name='ViolinMusicStaff',
            name='Violin Music Staff',
            )
        violin = abjad.instrumenttools.Violin()
        abjad.attach(violin, violin_music_staff)
        abjad.attach(abjad.indicatortools.Clef('treble'), violin_music_staff)
        self._attach_tag('violin', violin_music_staff)

        music_context = abjad.scoretools.Context(
            [
                violin_music_staff,
            ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='Music Context',
            )

        score = abjad.scoretools.Score(
            [
            time_signature_context,
            music_context,
            ],
            name='Score',
            )

        return score
