import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class StringTrioScoreTemplate(ScoreTemplate):
    r'''String trio score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
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
                        \time 4/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context StringSectionStaffGroup = "String Section Staff Group"
                    <<
                        \tag Violin                                                                  %! ST4
                        \context ViolinMusicStaff = "ViolinMusicStaff"
                        {
                            \context ViolinMusicVoice = "ViolinMusicVoice"
                            {
            <BLANKLINE>
                                % [ViolinMusicVoice measure 1]                                       %! SM4
                                \set ViolinMusicStaff.instrumentName = \markup {                     %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Violin                                                       %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.shortInstrumentName = \markup {                %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Vn.                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.forceClef = ##t                                %! ST3:DEFAULT_CLEF:SM8
                                \clef "treble"                                                       %! ST3:DEFAULT_CLEF:SM8
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! ST1:DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! ST3:DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolinMusicStaff.Clef.color = ##f                          %! ST3:DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {                                                          %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                     %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        (Violin)                                                     %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                \set ViolinMusicStaff.instrumentName = \markup {                     %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Violin                                                       %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.shortInstrumentName = \markup {                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vn.                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! ST1:REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)         %! ST3:DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % [ViolinMusicVoice measure 2]                                       %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolinMusicVoice measure 3]                                       %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [ViolinMusicVoice measure 4]                                       %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                        \tag Viola                                                                   %! ST4
                        \context ViolaMusicStaff = "ViolaMusicStaff"
                        {
                            \context ViolaMusicVoice = "ViolaMusicVoice"
                            {
            <BLANKLINE>
                                % [ViolaMusicVoice measure 1]                                        %! SM4
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Viola                                                        %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Va.                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.forceClef = ##t                                 %! ST3:DEFAULT_CLEF:SM8
                                \clef "alto"                                                         %! ST3:DEFAULT_CLEF:SM8
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! ST1:DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! ST3:DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! ST3:DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {                                                          %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                     %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        (Viola)                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Viola                                                        %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Va.                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! ST1:REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! ST3:DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % [ViolaMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolaMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [ViolaMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                        \tag Cello                                                                   %! ST4
                        \context CelloMusicStaff = "CelloMusicStaff"
                        {
                            \context CelloMusicVoice = "CelloMusicVoice"
                            {
            <BLANKLINE>
                                % [CelloMusicVoice measure 1]                                        %! SM4
                                \set CelloMusicStaff.instrumentName = \markup {                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Cello                                                        %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Vc.                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.forceClef = ##t                                 %! ST3:DEFAULT_CLEF:SM8
                                \clef "bass"                                                         %! ST3:DEFAULT_CLEF:SM8
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! ST1:DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! ST3:DEFAULT_CLEF_COLOR:SM6
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! ST3:DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {                                                          %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                     %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        (Cello)                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                \set CelloMusicStaff.instrumentName = \markup {                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Cello                                                        %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vc.                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! ST1:REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! ST3:DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % [CelloMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [CelloMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [CelloMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Score:
        r'''Calls string trio score template.
        '''
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
            markup=baca.markup.instrument('Violin', hcenter_in=10),
            short_markup=baca.markup.short_instrument(
                'Vn.',
                hcenter_in=10,
                ),
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

        # VIOLA
        viola_music_voice = abjad.Voice(
            lilypond_type='ViolaMusicVoice',
            name='ViolaMusicVoice',
            )
        viola_music_staff = abjad.Staff(
            [viola_music_voice],
            lilypond_type='ViolaMusicStaff',
            name='ViolaMusicStaff',
            )
        abjad.annotate(
            viola_music_staff,
            'default_instrument',
            abjad.Viola(
                markup=baca.markup.instrument('Viola', hcenter_in=10),
                short_markup=baca.markup.short_instrument(
                    'Va.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            viola_music_staff,
            'default_clef',
            abjad.Clef('alto'),
            )
        self._attach_lilypond_tag('Viola', viola_music_staff)

        # CELLO
        cello_music_voice = abjad.Voice(
            lilypond_type='CelloMusicVoice',
            name='CelloMusicVoice',
            )
        cello_music_staff = abjad.Staff(
            [cello_music_voice],
            lilypond_type='CelloMusicStaff',
            name='CelloMusicStaff',
            )
        abjad.annotate(
            cello_music_staff,
            'default_instrument',
            abjad.Cello(
                markup=baca.markup.instrument('Cello', hcenter_in=10),
                short_markup=baca.markup.short_instrument(
                    'Vc.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            cello_music_staff,
            'default_clef',
            abjad.Clef('bass'),
            )
        self._attach_lilypond_tag('Cello', cello_music_staff)

        # SCORE
        string_section_staff_group = abjad.StaffGroup(
            [
                violin_music_staff,
                viola_music_staff,
                cello_music_staff,
                ],
            lilypond_type='StringSectionStaffGroup',
            name='String Section Staff Group',
            )
        music_context = abjad.Context(
            [string_section_staff_group],
            lilypond_type='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            )
        return score
