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
                    \context StringSectionStaffGroup = "String Section Staff Group"
                    <<
                        \tag Violin                                                                  %! ST4
                        \context ViolinMusicStaff = "ViolinMusicStaff"
                        {
                            \context ViolinMusicVoice = "ViolinMusicVoice"
                            {
            <BLANKLINE>
                                % [ViolinMusicVoice measure 1]                                       %! SM4
                                \set ViolinMusicStaff.instrumentName = \markup {                     %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Violin                                                       %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set ViolinMusicStaff.shortInstrumentName = \markup {                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Vn.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "treble"                                                       %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolinMusicStaff.Clef.color = ##f                          %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolinMusicStaff.forceClef = ##t                                %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 1/2
                                ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Violin)                                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set ViolinMusicStaff.instrumentName = \markup {                     %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Violin                                                       %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set ViolinMusicStaff.shortInstrumentName = \markup {                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Vn.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)         %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
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
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Viola                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Va.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 1/2
                                ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Viola                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Va.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
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
                                \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Cello                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Vc.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "bass"                                                         %! SM8:DEFAULT_CLEF:ST3
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set CelloMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 1/2
                                ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Cello)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Cello                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Vc.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
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

    _part_manifest = abjad.PartManifest(
        abjad.Part(section='Violin', abbreviation='VN'),
        abjad.Part(section='Viola', abbreviation='VA'),
        abjad.Part(section='Cello', abbreviation='VC'),
        )

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
