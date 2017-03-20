# -*- coding: utf-8 -*-
import abjad
from baca.tools.ScoreTemplate import ScoreTemplate


class TwoVoiceStaffScoreTemplate(ScoreTemplate):
    r'''Two-voice staff score template.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.TwoVoiceStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
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
                    \context MusicStaff = "Music Staff" <<
                        \context MusicVoiceOne = "Music Voice 1" {
                            R1 * 1/2
                            R1 * 3/8
                            R1 * 1/2
                            R1 * 3/8
                            \bar "|"
                        }
                        \context MusicVoiceTwo = "Music Voice 2" {
                            R1 * 1/2
                            R1 * 3/8
                            R1 * 1/2
                            R1 * 3/8
                            \bar "|"
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    voice_abbreviations = {
        'v1': 'Music Voice 1',
        'v2': 'Music Voice 2',
        }

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls two-voice staff score template.

        Returns score.
        '''

        time_signature_context = self._make_time_signature_context()

        music_voice_1 = abjad.Voice(
            [], 
            context_name='MusicVoiceOne',
            name=self.voice_abbreviations['v1'],
            )
        music_voice_2 = abjad.Voice(
            [], 
            context_name='MusicVoiceTwo',
            name=self.voice_abbreviations['v2'],
            )
        music_staff = abjad.Staff(
            [music_voice_1, music_voice_2], 
            context_name='MusicStaff',
            is_simultaneous=True,
            name='Music Staff',
            )

        music_context = abjad.Context(
            [
                music_staff,
            ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='Music Context',
            )

        score = abjad.Score(
            [
            time_signature_context,
            music_context,
            ],
            name='Score',
            )

        abjad.attach('two-voice', score)
        return score
