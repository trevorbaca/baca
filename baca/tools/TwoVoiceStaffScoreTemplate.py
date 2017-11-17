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
                \context GlobalContext = "Global Context" <<
                    \context GlobalSkips = "Global Skips" {
            <BLANKLINE>
                        %%% Global Skips [measure 1] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% Global Skips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% Global Skips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% Global Skips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context MusicStaff = "Music Staff" <<
                        \context MusicVoiceOne = "Music Voice 1" {
            <BLANKLINE>
                            %%% Music Voice 1 [measure 1] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% Music Voice 1 [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% Music Voice 1 [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% Music Voice 1 [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                        \context MusicVoiceTwo = "Music Voice 2" {
            <BLANKLINE>
                            %%% Music Voice 2 [measure 1] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% Music Voice 2 [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% Music Voice 2 [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% Music Voice 2 [measure 4] %%%
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
            name='Music Voice 1',
            )
        music_voice_2 = abjad.Voice(
            [],
            context_name='MusicVoiceTwo',
            name='Music Voice 2',
            )
        music_staff = abjad.Staff([
            music_voice_1,
            music_voice_2,
            ],
            context_name='MusicStaff',
            is_simultaneous=True,
            name='Music Staff',
            )

        music_context = abjad.Context([
            music_staff,
            ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='Music Context',
            )

        score = abjad.Score([
            global_context,
            music_context,
            ],
            name='Score',
            )

        abjad.attach('two-voice', score)
        return score
