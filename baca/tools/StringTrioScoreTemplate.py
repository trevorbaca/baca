# -*- coding: utf-8 -*-
import abjad
from baca.tools.ScoreTemplate import ScoreTemplate


class StringTrioScoreTemplate(ScoreTemplate):
    r'''String trio score template.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.StringTrioScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin.viola.cello
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
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
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
                        \tag viola
                        \context ViolaMusicStaff = "Viola Music Staff" {
                            \clef "alto"
                            \context ViolaMusicVoice = "Viola Music Voice" {
                                R1 * 1/2
                                R1 * 3/8
                                R1 * 1/2
                                R1 * 3/8
                                \bar "|"
                            }
                        }
                        \tag cello
                        \context CelloMusicStaff = "Cello Music Staff" {
                            \clef "bass"
                            \context CelloMusicVoice = "Cello Music Voice" {
                                R1 * 1/2
                                R1 * 3/8
                                R1 * 1/2
                                R1 * 3/8
                                \bar "|"
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    voice_abbreviations = {
        'vn': 'Violin Music Voice',
        'va': 'Viola Music Voice',
        'vc': 'Cello Music Voice',
        }

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls string trio score template.

        Returns score.
        '''

        time_signature_context = self._make_time_signature_context()

        instrument_tags = (
            'violin',
            'viola',
            'cello',
            )
        tag_string = '.'.join(instrument_tags)
        tag_string = 'tag {}'.format(tag_string)
        tag_command = abjad.LilyPondCommand(
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
        abjad.attach(abjad.Clef('treble'), violin_music_staff)
        self._attach_tag('violin', violin_music_staff)

        viola_music_voice = abjad.scoretools.Voice(
            [], 
            context_name='ViolaMusicVoice',
            name=self.voice_abbreviations['va'],
            )
        viola_music_staff = abjad.scoretools.Staff(
            [viola_music_voice], 
            context_name='ViolaMusicStaff',
            name='Viola Music Staff',
            )
        abjad.attach(abjad.instrumenttools.Viola(), viola_music_staff)
        abjad.attach(abjad.Clef('alto'), viola_music_staff)
        self._attach_tag('viola', viola_music_staff)

        cello_music_voice = abjad.scoretools.Voice(
            [], 
            context_name='CelloMusicVoice',
            name=self.voice_abbreviations['vc'],
            )
        cello_music_staff = abjad.scoretools.Staff(
            [cello_music_voice], 
            context_name='CelloMusicStaff',
            name='Cello Music Staff',
            )
        abjad.attach(abjad.instrumenttools.Cello(), cello_music_staff)
        abjad.attach(abjad.Clef('bass'), cello_music_staff)
        self._attach_tag('cello', cello_music_staff)

        string_section_staff_group = abjad.scoretools.StaffGroup(
            [
                violin_music_staff, 
                viola_music_staff, 
                cello_music_staff,
                ], 
            context_name='StringSectionStaffGroup',
            name='String Section Staff Group',
            )

        music_context = abjad.scoretools.Context(
            [
                string_section_staff_group,
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
