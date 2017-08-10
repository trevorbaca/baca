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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin.viola.cello
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
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
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

        violin_music_voice = abjad.Voice(
            [],
            context_name='ViolinMusicVoice',
            name=self.voice_abbreviations['vn'],
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            context_name='ViolinMusicStaff',
            name='Violin Music Staff',
            )
        violin = abjad.instrumenttools.Violin()
#        abjad.annotate(
#            violin_music_staff,
#            'default_instrument',
#            violin,
#            )
#        abjad.annotate(
#            violin_music_staff,
#            'default_clef',
#            abjad.Clef('treble'),
#            )
        self._attach_tag('violin', violin_music_staff)

        viola_music_voice = abjad.Voice(
            [],
            context_name='ViolaMusicVoice',
            name=self.voice_abbreviations['va'],
            )
        viola_music_staff = abjad.Staff(
            [viola_music_voice],
            context_name='ViolaMusicStaff',
            name='Viola Music Staff',
            )
#        abjad.annotate(
#            viola_music_staff,
#            'default_instrument',
#            abjad.instrumenttools.Viola(),
#            )
#        abjad.annotate(
#            viola_music_staff,
#            'default_clef',
#            abjad.Clef('alto'),
#            )
        self._attach_tag('viola', viola_music_staff)

        cello_music_voice = abjad.Voice(
            [],
            context_name='CelloMusicVoice',
            name=self.voice_abbreviations['vc'],
            )
        cello_music_staff = abjad.Staff(
            [cello_music_voice],
            context_name='CelloMusicStaff',
            name='Cello Music Staff',
            )
#        abjad.annotate(
#            cello_music_staff,
#            'default_instrument',
#            abjad.instrumenttools.Cello(),
#            )
#        abjad.annotate(
#            cello_music_staff,
#            'default_clef',
#            abjad.Clef('bass'),
#            )
        self._attach_tag('cello', cello_music_staff)

        string_section_staff_group = abjad.StaffGroup(
            [
                violin_music_staff,
                viola_music_staff,
                cello_music_staff,
                ],
            context_name='StringSectionStaffGroup',
            name='String Section Staff Group',
            )

        music_context = abjad.Context(
            [
                string_section_staff_group,
            ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='Music Context',
            )

        score = abjad.Score([
            time_signature_context,
            music_context,
            ],
            name='Score',
            )

        return score
