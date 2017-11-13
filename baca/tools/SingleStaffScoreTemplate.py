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

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "Global Context" <<
                    \context GlobalSkips = "Global Skips" {
                        % measure 1
                        \time 4/8
                        s1 * 1/2
                        % measure 2
                        \time 3/8
                        s1 * 3/8
                        % measure 3
                        \time 4/8
                        s1 * 1/2
                        % measure 4
                        \time 3/8
                        s1 * 3/8
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context Staff = "Music Staff" {
                        \context Voice = "Music Voice" {
                            % measure 1
                            \clef "treble"
                            R1 * 1/2
                            % measure 2
                            R1 * 3/8
                            % measure 3
                            R1 * 1/2
                            % measure 4
                            R1 * 3/8
                            \bar "|"
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
        time_signature_context = self._make_time_signature_context()
        # 
        music_voice = abjad.Voice(
            [],
            name='Music Voice',
            )
        music_staff = abjad.Staff(
            [music_voice],
            name='Music Staff',
            )
        abjad.annotate(
            music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        # SCORE
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
        return score
