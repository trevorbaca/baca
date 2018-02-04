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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context MusicStaff = "MusicStaff"
                    <<
                        \context MusicVoiceOne = "MusicVoiceOne"
                        {
            <BLANKLINE>
                            % [MusicVoiceOne measure 1]                                              %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoiceOne measure 2]                                              %! SM4
                            R1 * 3/8
            <BLANKLINE>
                            % [MusicVoiceOne measure 3]                                              %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoiceOne measure 4]                                              %! SM4
                            R1 * 3/8
            <BLANKLINE>
                        }
                        \context MusicVoiceTwo = "MusicVoiceTwo"
                        {
            <BLANKLINE>
                            % [MusicVoiceTwo measure 1]                                              %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoiceTwo measure 2]                                              %! SM4
                            R1 * 3/8
            <BLANKLINE>
                            % [MusicVoiceTwo measure 3]                                              %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoiceTwo measure 4]                                              %! SM4
                            R1 * 3/8
            <BLANKLINE>
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        r'''Calls two-voice staff score template.
        '''
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # MUSIC STAFF
        music_voice_1 = abjad.Voice(
            lilypond_type='MusicVoiceOne',
            name='MusicVoiceOne',
            )
        music_voice_2 = abjad.Voice(
            lilypond_type='MusicVoiceTwo',
            name='MusicVoiceTwo',
            )
        music_staff = abjad.Staff(
            [music_voice_1, music_voice_2],
            lilypond_type='MusicStaff',
            is_simultaneous=True,
            name='MusicStaff',
            )

        # MUSIC CONTEXT
        music_context = abjad.Context(
            [music_staff],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            )
        abjad.attach('two-voice', score, site='')
        return score
