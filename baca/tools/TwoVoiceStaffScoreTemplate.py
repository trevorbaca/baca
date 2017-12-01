import abjad
from baca.tools.ScoreTemplate import ScoreTemplate


class TwoVoiceStaffScoreTemplate(ScoreTemplate):
    r'''Two-voice staff score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        s1 * 1/2
                            - \markup { %! STAGE_NUMBER_MARKUP:2
                                \fontsize %! STAGE_NUMBER_MARKUP:2
                                    #-3 %! STAGE_NUMBER_MARKUP:2
                                    \with-color %! STAGE_NUMBER_MARKUP:2
                                        #(x11-color 'DarkCyan) %! STAGE_NUMBER_MARKUP:2
                                        [1] %! STAGE_NUMBER_MARKUP:2
                                } %! STAGE_NUMBER_MARKUP:2
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
                    \context MusicStaff = "MusicStaff" <<
                        \context MusicVoiceOne = "MusicVoiceOne" {
            <BLANKLINE>
                            %%% MusicVoiceOne [measure 1] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoiceOne [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% MusicVoiceOne [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoiceOne [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                        \context MusicVoiceTwo = "MusicVoiceTwo" {
            <BLANKLINE>
                            %%% MusicVoiceTwo [measure 1] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoiceTwo [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% MusicVoiceTwo [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoiceTwo [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls two-voice staff score template.

        Returns score.
        '''

        global_context = self._make_global_context()

        music_voice_1 = abjad.Voice(
            [],
            context_name='MusicVoiceOne',
            name='MusicVoiceOne',
            )
        music_voice_2 = abjad.Voice(
            [],
            context_name='MusicVoiceTwo',
            name='MusicVoiceTwo',
            )
        music_staff = abjad.Staff([
            music_voice_1,
            music_voice_2,
            ],
            context_name='MusicStaff',
            is_simultaneous=True,
            name='MusicStaff',
            )

        music_context = abjad.Context([
            music_staff,
            ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

        score = abjad.Score([
            global_context,
            music_context,
            ],
            name='Score',
            )

        abjad.attach('two-voice', score)
        return score
