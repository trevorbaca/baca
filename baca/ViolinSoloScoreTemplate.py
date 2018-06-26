import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class ViolinSoloScoreTemplate(ScoreTemplate):
    r"""
    Violin solo score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
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
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \tag Violin                                                                      %! ST4
                    \context ViolinMusicStaff = "ViolinMusicStaff"
                    {
                        \context ViolinMusicVoice = "ViolinMusicVoice"
                        {
            <BLANKLINE>
                            % [ViolinMusicVoice measure 1]                                           %! SM4
                            \clef "treble"                                                           %! SM8:DEFAULT_CLEF:ST3
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet)   %! SM6:DEFAULT_CLEF_COLOR:ST3
                        %@% \override ViolinMusicStaff.Clef.color = ##f                              %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                            \set ViolinMusicStaff.forceClef = ##t                                    %! SM8:DEFAULT_CLEF:SM33:ST3
                            R1 * 1/2
                            ^ \markup {                                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \with-color                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    #(x11-color 'DarkViolet)                                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    (Violin)                                                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                }                                                                    %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)             %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
            <BLANKLINE>
                            % [ViolinMusicVoice measure 2]                                           %! SM4
                            R1 * 3/8
            <BLANKLINE>
                            % [ViolinMusicVoice measure 3]                                           %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % [ViolinMusicVoice measure 4]                                           %! SM4
                            R1 * 3/8
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        """
        Calls violin solo score template.
        """
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # VIOLIN
        violin_music_voice = abjad.Voice(
            lilypond_type='ViolinMusicVoice',
            name='ViolinMusicVoice',
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            lilypond_type='ViolinMusicStaff',
            name='ViolinMusicStaff',
            )
        violin = abjad.Violin(
            markup=baca.markups.instrument('Violin'),
            short_markup=baca.markups.short_instrument('Vn.'),
            )
        abjad.annotate(
            violin_music_staff,
            'default_instrument',
            violin,
            )
        abjad.annotate(
            violin_music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        self._attach_lilypond_tag('Violin', violin_music_staff)

        # MUSIC ONTEXT
        music_context = abjad.Context(
            [violin_music_staff],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            )
        return score
