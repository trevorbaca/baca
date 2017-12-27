import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class SingleStaffScoreTemplate(ScoreTemplate):
    r'''Single-staff score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
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
            <BLANKLINE>
                            %%% MusicVoice [measure 1] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoice [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% MusicVoice [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoice [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''

        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # MUSIC VOICE, MUSIC STAFF
        music_voice = abjad.Voice(name='MusicVoice')
        music_staff = abjad.Staff(
            [music_voice],
            name='MusicStaff',
            )

#        abjad.annotate(
#            music_staff,
#            'default_clef',
#            abjad.Clef('treble'),
#            )

        # MUSIC CONTEXT
        music_context = abjad.Context(
            [music_staff],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            )

        self._attach_calltime_defaults(score)

        return score
