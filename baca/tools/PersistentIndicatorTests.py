import abjad


class PersistentIndicatorTests(abjad.AbjadObject):
    r'''Persistent indicator tests.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(2) Makers'

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def clefs(self) -> None:
        r'''Clefs.

        ..  container:: example

            Default clefs color purple and redraw dull purple:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> score_template = baca.SingleStaffScoreTemplate()
            >>> triple = ('MusicStaff', 'default_clef', abjad.Clef('treble'))
            >>> score_template.defaults.append(triple)
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     score_template=score_template,
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! DEFAULT_CLEF:SM8
                                \clef "treble"                                                           %! DEFAULT_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'DarkViolet)              %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'violet)                        %! DEFAULT_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Explicit clefs color blue and redraw dull blue:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.clef('treble'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:SM8
                                \clef "treble"                                                           %! EXPLICIT_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after a previous clef:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.clef('alto'),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Clef',
            ...         value='treble',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:SM8
                                \clef "alto"                                                             %! EXPLICIT_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied clefs color green and redraw dull green:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Clef',
            ...         value='treble',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)

            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! REAPPLIED_CLEF:SM8
                                \clef "treble"                                                           %! REAPPLIED_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'green4)                  %! REAPPLIED_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! REAPPLIED_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)                     %! REAPPLIED_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant clefs color pink and redraw dull pink:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [3, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.clef('treble', baca.leaf(0)),
            ...     baca.clef('treble', baca.leaf(1)),
            ...     )
            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)

            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:SM8
                                \clef "treble"                                                           %! EXPLICIT_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! REDUNDANT_CLEF:SM8
                                \clef "treble"                                                           %! REDUNDANT_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! REDUNDANT_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! REDUNDANT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! REDUNDANT_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.clef('treble'),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Clef',
            ...         value='treble',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)

            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.forceClef = ##t                                               %! REDUNDANT_CLEF:SM8
                                \clef "treble"                                                           %! REDUNDANT_CLEF:SM8
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! REDUNDANT_CLEF_COLOR:SM6
                            %@% \override Staff.Clef.color = ##f                                         %! REDUNDANT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! REDUNDANT_CLEF_REDRAW_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Returns none.
        '''
        pass

    @property
    def dynamics(self) -> None:
        r'''Dynamics.

        ..  container:: example

            Explicit dynamics color blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.dynamic('f'),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:SM6
                                c'4.
                                \f                                                                       %! EXPLICIT_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after a previous dynamic:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.dynamic('p'),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicVoice'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Dynamic',
            ...         value='f',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:SM6
                                c'4.
                                \p                                                                       %! EXPLICIT_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied dynamics color green:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicVoice'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Dynamic',
            ...         value='f',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'green4)           %! REAPPLIED_DYNAMIC_COLOR:SM6
                                c'4.
                                \f                                                                       %! REAPPLIED_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant dynamics color pink:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.dynamic('f'),
            ...     baca.dynamic('f', baca.leaf(1)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:SM6
                                c'4.
                                \f                                                                       %! EXPLICIT_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! REDUNDANT_DYNAMIC_COLOR:SM6
                                c'4.
                                \f                                                                       %! REDUNDANT_DYNAMIC:SM8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.dynamic('f'),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicVoice'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Dynamic',
            ...         value='f',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! REDUNDANT_DYNAMIC_COLOR:SM6
                                c'4.
                                \f                                                                       %! REDUNDANT_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Sforzando dynamics do not count as redundant:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.dynamic('sfz'),
            ...     baca.dynamic('sfz', baca.leaf(1)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:SM6
                                c'4.
                                \sfz                                                                     %! EXPLICIT_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:SM6
                                c'4.
                                \sfz                                                                     %! EXPLICIT_DYNAMIC:SM8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.dynamic('sfz'),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicVoice'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Dynamic',
            ...         value='sfz',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:SM6
                                c'4.
                                \sfz                                                                     %! EXPLICIT_DYNAMIC:SM8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        pass

    @property
    def hidden_instruments(self) -> None:
        r'''Hidden instruments.

        Hidden instruments provide an alert.
        
        Alerts are realized as markup formatted between round parentheses.
        
        Alerts do not redraw.

        ..  container:: example

            Example instruments:

            >>> instruments = abjad.InstrumentDictionary()
            >>> instruments['Flute'] = abjad.Flute(hide=True)
            >>> instruments['Piccolo'] = abjad.Piccolo(hide=True)
            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )

        ..  container:: example

            With ``hide`` set to true, default instrument alerts color purple:

            >>> score_template = baca.SingleStaffScoreTemplate()
            >>> triple = (
            ...     'MusicStaff', 'default_instrument', instruments['Flute'],
            ...     )
            >>> score_template.defaults.append(triple)
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=score_template,
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                         %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! DEFAULT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                      %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color                  %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)                %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%     }                            %! DEFAULT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                      %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                  %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                            %! DEFAULT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            With ``hide`` set to true, explicit instrument alerts color blue:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     }                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after a previous instrument:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Instrument',
            ...         value='Piccolo',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     }                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            With ``hide`` set to true, reapplied instrument alerts color green:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Instrument',
            ...         value='Flute',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'green4)                                             %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                  %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%     \with-color              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'green4) %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)            %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%     }                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                  %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    \with-color              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'green4) %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        (“Flute”)            %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    }                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            With ``hide`` set to true, redundant instrument alerts color pink:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [3, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.map(
            ...         baca.instrument(instruments['Flute']),
            ...         baca.leaves()[1],
            ...         ),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'2
                                ^ \markup {                                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'2
                                ^ \markup {                                                              %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1)                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'2
                            %%% ^ \markup {                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     }                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'2
                            %%% ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'2
                                ^ \markup {                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'2
                                ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Instrument',
            ...         value='Flute',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1)                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)                                                        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         (“Flute”)               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        (“Flute”)               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        pass

    @property
    def instruments(self) -> None:
        r'''Instruments.

        ..  container:: example

            Example instruments:

            >>> instruments = abjad.InstrumentDictionary()
            >>> instruments['Flute'] = abjad.Flute()
            >>> instruments['Piccolo'] = abjad.Piccolo()
            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )

        ..  container:: example

            Default instruments color purple and redraw dull purple:

            >>> score_template = baca.SingleStaffScoreTemplate()
            >>> triple = ('MusicStaff', 'default_instrument', abjad.Flute())
            >>> score_template.defaults.append(triple)
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=score_template,
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! DEFAULT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! DEFAULT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! DEFAULT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                         %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        {                                                                %! DEFAULT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! DEFAULT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! DEFAULT_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                {                                                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                        )                                                %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                }                                                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        }                                                                %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! DEFAULT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'violet)              %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! DEFAULT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! DEFAULT_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                      %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color                  %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%         {                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter             %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”         %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter             %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                 Flute            %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%             \concat              %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                 {                %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter     %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.      %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter     %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                         )        %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%                 }                %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%         }                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                            %%%     }                            %! DEFAULT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! DEFAULT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! DEFAULT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                      %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                  %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        {                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                                            \vcenter             %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                (“Flute”         %! DEFAULT_INSTRUMENT_ALERT:SM11
                                            \vcenter             %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                Flute            %! DEFAULT_INSTRUMENT_ALERT:SM11
                                            \concat              %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                {                %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                    \vcenter     %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                        Fl.      %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                    \vcenter     %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                        )        %! DEFAULT_INSTRUMENT_ALERT:SM11
                                                }                %! DEFAULT_INSTRUMENT_ALERT:SM11
                                        }                        %! DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                            %! DEFAULT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Explicit instruments color blue and redraw dull blue:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! EXPLICIT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        {                                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                {                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        )                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                }                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        }                                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! EXPLICIT_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'blue)   %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         {                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 Flute        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \concat          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 {            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                         )    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 }            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         }                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     }                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! EXPLICIT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)   %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        {                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                (“Flute”     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                Flute        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \concat          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                {            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        Fl.  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        )    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                }            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        }                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after a previous instrument:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Instrument',
            ...         value='Piccolo',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! EXPLICIT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        {                                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                {                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        )                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                }                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        }                                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! EXPLICIT_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'blue)   %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         {                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 Flute        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \concat          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 {            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                         )    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 }            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         }                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     }                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! EXPLICIT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)   %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        {                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                (“Flute”     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                Flute        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \concat          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                {            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        Fl.  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        )    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                }            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        }                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied instruments color green and redraw dull green:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Instrument',
            ...         value='Flute',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! REAPPLIED_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REAPPLIED_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! REAPPLIED_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'green4)                                             %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        {                                                                %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                {                                                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                        )                                                %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                }                                                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        }                                                                %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_REAPPLIED_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_REAPPLIED_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! REDRAWN_REAPPLIED_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! REAPPLIED_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REAPPLIED_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! REAPPLIED_INSTRUMENT_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                  %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%     \with-color              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'green4) %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%         {                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”     %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                 Flute        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%             \concat          %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                 {            %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.  %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                         )    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%                 }            %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%         }                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                            %%%     }                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_REAPPLIED_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_REAPPLIED_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! REDRAWN_REAPPLIED_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! REAPPLIED_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REAPPLIED_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! REAPPLIED_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                  %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    \with-color              %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'green4) %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        {                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                (“Flute”     %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                Flute        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                            \concat          %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                {            %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                        Fl.  %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                        )    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                                }            %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                        }                    %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                    }                        %! REAPPLIED_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_REAPPLIED_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_REAPPLIED_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! REDRAWN_REAPPLIED_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant instruments color pink and redraw dull pink:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [3, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.map(
            ...         baca.instrument(instruments['Flute']),
            ...         baca.leaves()[1],
            ...         ),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! EXPLICIT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'2
                                ^ \markup {                                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        {                                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                {                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        )                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                }                                                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        }                                                                %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDUNDANT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_INSTRUMENT_COLOR:SM6
                                c'2
                                ^ \markup {                                                              %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1)                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        {                                                                %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                {                                                        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        )                                                %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                }                                                        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        }                                                                %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! EXPLICIT_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'2
                            %%% ^ \markup {                  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'blue)   %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         {                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 Flute        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%             \concat          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 {            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                         )    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%                 }            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%         }                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                            %%%     }                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDUNDANT_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_COLOR:SM6
                                c'2
                            %%% ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         {                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 Flute           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%             \concat             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 {               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                         )       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 }               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         }                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! EXPLICIT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:SM6
                                c'2
                                ^ \markup {                  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    \with-color              %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'blue)   %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        {                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                (“Flute”     %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \vcenter         %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                Flute        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                            \concat          %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                {            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        Fl.  %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                    \vcenter %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                        )    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                                }            %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                        }                    %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                    }                        %! EXPLICIT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_EXPLICIT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDUNDANT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_COLOR:SM6
                                c'2
                                ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        {                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                (“Flute”        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                Flute           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \concat             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                {               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        Fl.     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        )       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                }               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        }                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.Instrument',
            ...         value='Flute',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDUNDANT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1)                                          %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        {                                                                %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                (“Flute”                                                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                Flute                                                    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \concat                                                      %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                {                                                        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        Fl.                                              %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        )                                                %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                }                                                        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        }                                                                %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                                                                    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }                            %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDUNDANT_INSTRUMENT:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         {                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 (“Flute”        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 Flute           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%             \concat             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 {               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                         Fl.     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                         )       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%                 }               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%         }                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                            %%%     }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDUNDANT_INSTRUMENT:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_COLOR:SM6
                                c'4.
                                ^ \markup {                     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    \with-color                 %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DeepPink1) %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        {                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                (“Flute”        %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \vcenter            %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                Flute           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                            \concat             %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                {               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        Fl.     %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                        )       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                                }               %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                        }                       %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                    }                           %! REDUNDANT_INSTRUMENT_ALERT:SM11
                                \set Staff.instrumentName = \markup { Flute }    %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \set Staff.shortInstrumentName = \markup { Fl. } %! REDRAWN_REDUNDANT_INSTRUMENT:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_INSTRUMENT_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        pass

    @property
    def margin_markup(self) -> None:
        r'''Margin markup.

        ..  container:: example

            Margin markup for examples:

            >>> margin_markup = abjad.OrderedDict()
            >>> margin_markup['I+II'] = abjad.MarginMarkup(
            ...     markup=abjad.Markup('I+II'),
            ...     short_markup=abjad.Markup('I+II'),
            ...     )
            >>> margin_markup['III+IV'] = abjad.MarginMarkup(
            ...     markup=abjad.Markup('III+IV'),
            ...     short_markup=abjad.Markup('III+IV'),
            ...     )
            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )

        ..  container:: example

            Default margin markup color purple and redraw dull purple:

            >>> score_template = baca.SingleStaffScoreTemplate()
            >>> triple = (
            ...     'MusicStaff',
            ...     'default_margin_markup',
            ...     margin_markup['I+II'],
            ...     )
            >>> score_template.defaults.append(triple)
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=score_template,
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! DEFAULT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! DEFAULT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! DEFAULT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                         %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”                                                  %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                I+II                                                     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II                                             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }                             %! REDRAWN_DEFAULT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDRAWN_DEFAULT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'violet)              %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! DEFAULT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! DEFAULT_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                      %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color                  %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'DarkViolet) %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“I+II”          %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 I+II             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat              %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         I+II     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                            %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_DEFAULT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_DEFAULT_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! DEFAULT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! DEFAULT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                      %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                  %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'DarkViolet) %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                        {                        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”          %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                I+II             %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                            \concat              %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                {                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter     %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                        ]        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                                }                %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                        }                        %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                    }                            %! DEFAULT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_DEFAULT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_DEFAULT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Explicit margin markup color blue and redraw dull blue:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markup['I+II']),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”                                                  %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                I+II                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }                             %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! EXPLICIT_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                  %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'blue)   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“I+II”      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 I+II         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         I+II %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                  %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'blue)   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        {                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                I+II         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \concat          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        ]    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    }                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after previous margin markup:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markup['III+IV']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.MarginMarkup',
            ...         value='I+II',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { III+IV }                           %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { III+IV }                      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                [“III+IV”                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                III+IV                                                   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        III+IV                                           %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { III+IV }                           %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { III+IV }                      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { III+IV }      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { III+IV } %! EXPLICIT_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'blue)     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter           %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“III+IV”      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter           %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 III+IV         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         III+IV %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { III+IV }      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { III+IV } %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { III+IV }      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { III+IV } %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'blue)     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        {                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter           %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                [“III+IV”      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter           %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                III+IV         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \concat            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        III+IV %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        ]      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    }                          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { III+IV }      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { III+IV } %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied margin markup color green and redraw dull green:

            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.MarginMarkup',
            ...         value='I+II',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! REAPPLIED_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REAPPLIED_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! REAPPLIED_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'green4)                                             %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”                                                  %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                I+II                                                     %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                        I+II                                             %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }                             %! REDRAWN_REAPPLIED_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDRAWN_REAPPLIED_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! REAPPLIED_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REAPPLIED_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! REAPPLIED_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                  %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color              %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'green4) %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter         %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“I+II”      %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter         %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                 I+II         %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat          %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {            %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                         I+II %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }            %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                        %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_REAPPLIED_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_REAPPLIED_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! REAPPLIED_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REAPPLIED_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! REAPPLIED_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                  %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                    \with-color              %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'green4) %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                        {                    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter         %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”      %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter         %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                I+II         %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                            \concat          %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                {            %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                        I+II %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                        ]    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                                }            %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                        }                    %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                    }                        %! REAPPLIED_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_REAPPLIED_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_REAPPLIED_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant margin markup color pink and redraw dull pink:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [3, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markup['I+II']),
            ...     baca.map(
            ...         baca.margin_markup(margin_markup['I+II']),
            ...         baca.leaves()[1],
            ...         ),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                                ^ \markup {                                                              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'blue)                                               %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”                                                  %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                I+II                                                     %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }                             %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDUNDANT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                                ^ \markup {                                                              %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'DeepPink1)                                          %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”                                                  %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                I+II                                                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II                                             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }                             %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! EXPLICIT_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                            %%% ^ \markup {                  %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'blue)   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“I+II”      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 I+II         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         I+II %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDUNDANT_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                            %%% ^ \markup {                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color                 %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“I+II”         %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 I+II            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         I+II    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                           %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                                ^ \markup {                  %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color              %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'blue)   %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        {                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”      %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                I+II         %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                            \concat          %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        ]    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }            %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }                    %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                    }                        %! EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDUNDANT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                                ^ \markup {                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                 %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        {                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”         %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                I+II            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \concat             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                {               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        ]       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                }               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        }                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    }                           %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markup['I+II']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.MarginMarkup',
            ...         value='I+II',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDUNDANT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                                                              %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                                                          %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'DeepPink1)                                          %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        {                                                                %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”                                                  %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter                                                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                I+II                                                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \concat                                                      %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II                                             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter                                             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        ]                                                %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        }                                                                %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    }                                                                    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }                             %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDUNDANT_MARGIN_MARKUP:SM8
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                            %%% ^ \markup {                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%     \with-color                 %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%         #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%         {                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 [“I+II”         %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 I+II            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%             \concat             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 {               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         I+II    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                     \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                         ]       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%                 }               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%         }                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                            %%%     }                           %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = baca.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \autoPageBreaksOff %! BREAK:BMM1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! BREAK:IC
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar "" %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak %! BREAK:IC
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! SPACING:HSS1
                            \noBreak %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break %! BREAK:IC
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDUNDANT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                                c'4.
                                ^ \markup {                     %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    \with-color                 %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        {                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                [“I+II”         %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \vcenter            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                I+II            %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                            \concat             %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                {               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        I+II    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                    \vcenter    %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                        ]       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                                }               %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                        }                       %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                    }                           %! REDUNDANT_MARGIN_MARKUP_ALERT:SM11
                                \set Staff.instrumentName = \markup { I+II }      %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II } %! REDRAWN_REDUNDANT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Multiple margin markup are allowed so long as only one is active:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 0, (11,)],
            ...         [2, 15, (11,)],
            ...         ),
            ...     )
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markup=margin_markup,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.tag(
            ...         '+SEGMENT',
            ...         baca.margin_markup(margin_markup['I+II']),
            ...         ),
            ...     baca.tag(
            ...         '+PARTS_VIOLIN',
            ...         baca.margin_markup(margin_markup['III+IV']),
            ...         deactivate=True,
            ...         ),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! BREAK:IC
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! BREAK:IC
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            \break                                                                       %! BREAK:IC
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! +SEGMENT:EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! +SEGMENT:EXPLICIT_MARGIN_MARKUP:SM8
                            %@% \set Staff.instrumentName = \markup { III+IV }                           %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP:SM8
                            %@% \set Staff.shortInstrumentName = \markup { III+IV }                      %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP:SM8
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                            %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                                c'2
                                ^ \markup {
                                    \column
                                        {
                                            \line                                                        %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                {                                                        %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                    \with-color                                          %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        #(x11-color 'blue)                               %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        {                                                %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                            \vcenter                                     %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                [“I+II”                                  %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                            \vcenter                                     %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                I+II                                     %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                            \concat                                      %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                {                                        %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                    \vcenter                             %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                        I+II                             %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                    \vcenter                             %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                        ]                                %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                                }                                        %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                        }                                                %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                                }                                                        %! +SEGMENT:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@% \line                                                        %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%     {                                                        %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%         \with-color                                          %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%             #(x11-color 'blue)                               %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%             {                                                %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                 \vcenter                                     %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                     [“III+IV”                                %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                 \vcenter                                     %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                     III+IV                                   %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                 \concat                                      %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                     {                                        %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                         \vcenter                             %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                             III+IV                           %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                         \vcenter                             %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                             ]                                %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%                     }                                        %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%             }                                                %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        %@%     }                                                        %! +PARTS_VIOLIN:EXPLICIT_MARGIN_MARKUP_ALERT:SM11
                                        }
                                    }
                                \set Staff.instrumentName = \markup { I+II }                             %! +SEGMENT:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! +SEGMENT:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                            %@% \set Staff.instrumentName = \markup { III+IV }                           %! +PARTS_VIOLIN:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                            %@% \set Staff.shortInstrumentName = \markup { III+IV }                      %! +PARTS_VIOLIN:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM8
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! +SEGMENT:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                            %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! +PARTS_VIOLIN:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:SM6
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return None

    @property
    def metronome_marks(self) -> None:
        r'''Metronome marks.

        ..  container:: example

            >>> breaks = baca.breaks(baca.page([1, 0, (8,)]))
            >>> metronome_marks = abjad.MetronomeMarkDictionary()
            >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
            >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

        ..  container:: example

            Explicit metronome marks color blue and redraw dull blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 25)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('GlobalSkips', 1),
            ...     baca.metronome_mark('112'),
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! BREAK:IC
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK:SM27
                        %@% \markup {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \fontsize                                                                %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         #-6                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         \general-align                                                       %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             #Y                                                               %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             #DOWN                                                            %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             \note-by-number                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #2                                                           %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #0                                                           %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #1.5                                                         %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \upright                                                                 %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             =                                                                %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             112                                                              %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \hspace                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         #1                                                                   %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:SM27 %! SM29
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = \markup {
                                \null
                                }                                                                        %! SM29
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            \markup {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                \with-color                                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    #(x11-color 'blue)                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \fontsize                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #-6                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            \general-align                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #Y                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #DOWN                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                \note-by-number                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #2                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #0                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #1.5                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \upright                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                =                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                112                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            }                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #1                                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.dash-period = 0                                  %! SM29
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after a previous metronome mark:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('GlobalSkips', 1),
            ...     baca.metronome_mark('112'),
            ...     baca.text_spanner_staff_padding(4),
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         prototype='abjad.MetronomeMark',
            ...         value='90',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \override TextSpanner.staff-padding = #4                                     %! OC
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! BREAK:IC
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK:SM27
                        %@% \markup {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \fontsize                                                                %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         #-6                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         \general-align                                                       %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             #Y                                                               %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             #DOWN                                                            %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             \note-by-number                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #2                                                           %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #0                                                           %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #1.5                                                         %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \upright                                                                 %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             =                                                                %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             112                                                              %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \hspace                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         #1                                                                   %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:SM27 %! SM29
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = \markup {
                                \null
                                }                                                                        %! SM29
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            \markup {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                \with-color                                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    #(x11-color 'blue)                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \fontsize                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #-6                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            \general-align                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #Y                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #DOWN                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                \note-by-number                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #2                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #0                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #1.5                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \upright                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                =                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                112                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            }                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #1                                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.dash-period = 0                                  %! SM29
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29
                            \revert TextSpanner.staff-padding                                            %! OC
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied metronome marks color green and redraw dull green:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )
            >>> maker(
            ...     baca.scope('GlobalSkips', 1),
            ...     baca.text_spanner_staff_padding(4),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         prototype='abjad.MetronomeMark',
            ...         value='90',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \override TextSpanner.staff-padding = #4                                     %! OC
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! BREAK:IC
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! REAPPLIED_METRONOME_MARK:SM27
                        %@% \markup {                                                                    %! REAPPLIED_METRONOME_MARK:SM27
                        %@%     \fontsize                                                                %! REAPPLIED_METRONOME_MARK:SM27
                        %@%         #-6                                                                  %! REAPPLIED_METRONOME_MARK:SM27
                        %@%         \general-align                                                       %! REAPPLIED_METRONOME_MARK:SM27
                        %@%             #Y                                                               %! REAPPLIED_METRONOME_MARK:SM27
                        %@%             #DOWN                                                            %! REAPPLIED_METRONOME_MARK:SM27
                        %@%             \note-by-number                                                  %! REAPPLIED_METRONOME_MARK:SM27
                        %@%                 #2                                                           %! REAPPLIED_METRONOME_MARK:SM27
                        %@%                 #0                                                           %! REAPPLIED_METRONOME_MARK:SM27
                        %@%                 #1.5                                                         %! REAPPLIED_METRONOME_MARK:SM27
                        %@%     \upright                                                                 %! REAPPLIED_METRONOME_MARK:SM27
                        %@%         {                                                                    %! REAPPLIED_METRONOME_MARK:SM27
                        %@%             =                                                                %! REAPPLIED_METRONOME_MARK:SM27
                        %@%             90                                                               %! REAPPLIED_METRONOME_MARK:SM27
                        %@%         }                                                                    %! REAPPLIED_METRONOME_MARK:SM27
                        %@%     \hspace                                                                  %! REAPPLIED_METRONOME_MARK:SM27
                        %@%         #1                                                                   %! REAPPLIED_METRONOME_MARK:SM27
                        %@%     }                                                                        %! REAPPLIED_METRONOME_MARK:SM27 %! SM29
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = \markup {
                                \null
                                }                                                                        %! SM29
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.bound-details.left.text =                        %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                            \markup {                                                                    %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                \with-color                                                              %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                    #(x11-color 'green4)                                                 %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                    {                                                                    %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                        \fontsize                                                        %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                            #-6                                                          %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                            \general-align                                               %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                #Y                                                       %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                #DOWN                                                    %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                \note-by-number                                          %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                    #2                                                   %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                    #0                                                   %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                    #1.5                                                 %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                        \upright                                                         %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                            {                                                            %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                =                                                        %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                                90                                                       %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                            }                                                            %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                        \hspace                                                          %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                            #1                                                           %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                    }                                                                    %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                        %! REAPPLIED_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.dash-period = 0                                  %! SM29
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29
                            \revert TextSpanner.staff-padding                                            %! OC
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant metronome marks color pink and redraw dull pink:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('GlobalSkips', 1),
            ...     baca.metronome_mark('112'),
            ...     baca.metronome_mark('112', baca.leaf(1)),
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! BREAK:IC
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK:SM27
                        %@% \markup {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \fontsize                                                                %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         #-6                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         \general-align                                                       %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             #Y                                                               %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             #DOWN                                                            %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             \note-by-number                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #2                                                           %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #0                                                           %! EXPLICIT_METRONOME_MARK:SM27
                        %@%                 #1.5                                                         %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \upright                                                                 %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             =                                                                %! EXPLICIT_METRONOME_MARK:SM27
                        %@%             112                                                              %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     \hspace                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                        %@%         #1                                                                   %! EXPLICIT_METRONOME_MARK:SM27
                        %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:SM27 %! SM29
                        %@% \once \override TextSpanner.bound-details.right.text =                       %! REDUNDANT_METRONOME_MARK:SM27
                        %@% \markup {                                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%     \concat                                                                  %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         {                                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             \hspace                                                          %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                 #-0.5                                                        %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             \line                                                            %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                 {                                                            %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                     \fontsize                                                %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                         #-6                                                  %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                         \general-align                                       %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                             #Y                                               %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                             #DOWN                                            %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                             \note-by-number                                  %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                                 #2                                           %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                                 #0                                           %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                                 #1.5                                         %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                     \upright                                                 %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                         {                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                             =                                                %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                             112                                              %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                         }                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                 }                                                            %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         }                                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%     }                                                                        %! REDUNDANT_METRONOME_MARK:SM27 %! SM29
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = \markup {
                                \null
                                }                                                                        %! SM29
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            \markup {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                \with-color                                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    #(x11-color 'blue)                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \fontsize                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #-6                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            \general-align                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #Y                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #DOWN                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                \note-by-number                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #2                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #0                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #1.5                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \upright                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                =                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                112                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            }                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #1                                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.bound-details.right.text =                       %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                            \markup {                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                \with-color                                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                    #(x11-color 'DeepPink1)                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                    \concat                                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                        {                                                                %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            \hspace                                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                #-0.5                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            \line                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                {                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                    \fontsize                                            %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                        #-6                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                        \general-align                                   %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                            #Y                                           %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                            #DOWN                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                            \note-by-number                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                                #2                                       %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                                #0                                       %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                                #1.5                                     %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                    \upright                                             %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                        {                                                %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                            =                                            %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                            112                                          %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                        }                                                %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                }                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                        }                                                                %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                            \once \override TextSpanner.dash-period = 0                                  %! SM29
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override TextSpanner.bound-details.left-broken.text = \markup {
                                \null
                                }                                                                        %! SM29
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('GlobalSkips', 1),
            ...     baca.metronome_mark('112'),
            ...     baca.text_spanner_staff_padding(4),
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         prototype='abjad.MetronomeMark',
            ...         value='112',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \override TextSpanner.staff-padding = #4                                     %! OC
                            \autoPageBreaksOff                                                           %! BREAK:BMM1
                            \noBreak                                                                     %! BREAK:BMM2
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! BREAK:IC
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! REDUNDANT_METRONOME_MARK:SM27
                        %@% \markup {                                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%     \fontsize                                                                %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         #-6                                                                  %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         \general-align                                                       %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             #Y                                                               %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             #DOWN                                                            %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             \note-by-number                                                  %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                 #2                                                           %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                 #0                                                           %! REDUNDANT_METRONOME_MARK:SM27
                        %@%                 #1.5                                                         %! REDUNDANT_METRONOME_MARK:SM27
                        %@%     \upright                                                                 %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         {                                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             =                                                                %! REDUNDANT_METRONOME_MARK:SM27
                        %@%             112                                                              %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         }                                                                    %! REDUNDANT_METRONOME_MARK:SM27
                        %@%     \hspace                                                                  %! REDUNDANT_METRONOME_MARK:SM27
                        %@%         #1                                                                   %! REDUNDANT_METRONOME_MARK:SM27
                        %@%     }                                                                        %! REDUNDANT_METRONOME_MARK:SM27 %! SM29
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                            \once \override TextSpanner.bound-details.left-broken.text = \markup {
                                \null
                                }                                                                        %! SM29
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.bound-details.left.text =                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                            \markup {                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                \with-color                                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                    #(x11-color 'DeepPink1)                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                    {                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                        \fontsize                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            #-6                                                          %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            \general-align                                               %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                #Y                                                       %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                #DOWN                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                \note-by-number                                          %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #2                                                   %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #0                                                   %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                    #1.5                                                 %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                        \upright                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            {                                                            %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                =                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                                112                                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            }                                                            %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                        \hspace                                                          %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                            #1                                                           %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                    }                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                            \once \override TextSpanner.dash-period = 0                                  %! SM29
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            \pageBreak                                                                   %! BREAK:IC
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \noBreak                                                                     %! BREAK:BMM2
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29
                            \revert TextSpanner.staff-padding                                            %! OC
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        pass

    @property
    def staff_lines(self) -> None:
        r'''Staff lines.

        ..  container:: example

            Explicit staff lines color blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.staff_lines(5),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override MusicStaff.StaffSymbol.line-count = 5                    %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:SM8
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after previous staff lines:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.staff_lines(1),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='baca.StaffLines',
            ...         value=5,
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override MusicStaff.StaffSymbol.line-count = 1                    %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:SM8
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied staff lines color green:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='baca.StaffLines',
            ...         value=5,
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! REAPPLIED_STAFF_LINES:SM8
                                \once \override MusicStaff.StaffSymbol.line-count = 5                    %! REAPPLIED_STAFF_LINES:SM8
                                \startStaff                                                              %! REAPPLIED_STAFF_LINES:SM8
                                \once \override Staff.StaffSymbol.color = #(x11-color 'green4)           %! REAPPLIED_STAFF_LINES_COLOR:SM6
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant staff lines color pink:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.staff_lines(5),
            ...     baca.staff_lines(5, baca.leaf(1)),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override MusicStaff.StaffSymbol.line-count = 5                    %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:SM8
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \stopStaff                                                               %! REDUNDANT_STAFF_LINES:SM8
                                \once \override MusicStaff.StaffSymbol.line-count = 5                    %! REDUNDANT_STAFF_LINES:SM8
                                \startStaff                                                              %! REDUNDANT_STAFF_LINES:SM8
                                \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! REDUNDANT_STAFF_LINES_COLOR:SM6
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_notes(),
            ...     baca.staff_lines(5),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='baca.StaffLines',
            ...         value=5,
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     )
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                            \bar ""                                                                      %! +SEGMENT:EMPTY_START_BAR:SM2
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! SPACING:HSS1
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! SPACING:HSS1
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! REDUNDANT_TIME_SIGNATURE_COLOR:SM6
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! REDUNDANT_STAFF_LINES:SM8
                                \once \override MusicStaff.StaffSymbol.line-count = 5                    %! REDUNDANT_STAFF_LINES:SM8
                                \startStaff                                                              %! REDUNDANT_STAFF_LINES:SM8
                                \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! REDUNDANT_STAFF_LINES_COLOR:SM6
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        pass
