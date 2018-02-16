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
    def accelerandi(self) -> None:
        r'''Accelerandi.

        ..  container:: example

            >>> breaks = baca.breaks(baca.page([1, 0, (8,)]))
            >>> metronome_marks = abjad.MetronomeMarkDictionary()
            >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
            >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

        ..  container:: example

            Explicit accelerandi color blue and redraw dull blue:

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
            ...     baca.metronome_mark(abjad.Accelerando()),
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.arrow-width = 0.25                               %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =
                            \markup {
                                \large
                                    \upright
                                        accel.
                                \hspace
                                    #1
                                }                                                                        %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.arrow = ##f           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.arrow = ##t                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-fraction = 0.25                             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 1.5                                %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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

            Even after a previous ritardando:

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
            ...     baca.metronome_mark(abjad.Accelerando()),
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
            ...         value='abjad.Ritardando()',
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OC1
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.arrow-width = 0.25                               %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =
                            \markup {
                                \large
                                    \upright
                                        accel.
                                \hspace
                                    #1
                                }                                                                        %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.arrow = ##f           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.arrow = ##t                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-fraction = 0.25                             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 1.5                                %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                            ^ \markup {                                                                  %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                \large                                                                   %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                    \upright                                                             %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                        rit.                                                             %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                }                                                                        %! SM8:REAPPLIED_METRONOME_MARK:SM37
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \revert TextSpanner.staff-padding                                            %! OC2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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

            Reapplied accelerandi color green and redraw dull green:

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
            ...         value='abjad.Accelerando()',
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OC1
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            ^ \markup {                                                                  %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                \large                                                                   %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                    \upright                                                             %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                        accel.                                                           %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                }                                                                        %! SM8:REAPPLIED_METRONOME_MARK:SM37
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \revert TextSpanner.staff-padding                                            %! OC2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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

            Redundant accelerandi color pink and redraw dull pink:

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
            ...     baca.metronome_mark(abjad.Accelerando()),
            ...     baca.metronome_mark(abjad.Accelerando(), baca.leaf(1)),
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.arrow-width = 0.25                               %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =
                            \markup {
                                \large
                                    \upright
                                        accel.
                                \hspace
                                    #1
                                }                                                                        %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.arrow = ##f           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.arrow = ##t                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-fraction = 0.25                             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 1.5                                %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
            ...     baca.metronome_mark(abjad.Accelerando()),
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
            ...         value='abjad.Accelerando()',
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OC1
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.arrow-width = 0.25                               %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =
                            \markup {
                                \large
                                    \upright
                                        accel.
                                \hspace
                                    #1
                                }                                                                        %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.arrow = ##f           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.arrow = ##t                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-fraction = 0.25                             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 1.5                                %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                            ^ \markup {                                                                  %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                \large                                                                   %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                    \upright                                                             %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                        accel.                                                           %! SM8:REAPPLIED_METRONOME_MARK:SM37
                                }                                                                        %! SM8:REAPPLIED_METRONOME_MARK:SM37
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \revert TextSpanner.staff-padding                                            %! OC2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "treble"                                                           %! SM8:DEFAULT_CLEF:ST3
                                \once \override Staff.Clef.color = #(x11-color 'DarkViolet)              %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set Staff.forceClef = ##t                                               %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'violet)                        %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "treble"                                                           %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "alto"                                                             %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "treble"                                                           %! SM8:REAPPLIED_CLEF:SM37
                                \once \override Staff.Clef.color = #(x11-color 'green4)                  %! SM6:REAPPLIED_CLEF_COLOR:SM37
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:REAPPLIED_CLEF_COLOR_CANCELLATION:SM37
                                \set Staff.forceClef = ##t                                               %! SM8:REAPPLIED_CLEF:SM33:SM37
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)                     %! SM6:REAPPLIED_CLEF_REDRAW_COLOR:SM37
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "treble"                                                           %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \clef "treble"                                                           %! SM8:REDUNDANT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! SM6:REDUNDANT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:REDUNDANT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:REDUNDANT_CLEF:SM33:IC
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! SM6:REDUNDANT_CLEF_REDRAW_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \clef "treble"                                                           %! SM8:REDUNDANT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! SM6:REDUNDANT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:REDUNDANT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:REDUNDANT_CLEF:SM33:IC
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! SM6:REDUNDANT_CLEF_REDRAW_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                                c'4.
                                \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                                c'4.
                                \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'green4)           %! SM6:REAPPLIED_DYNAMIC_COLOR:SM37
                                c'4.
                                \f                                                                       %! SM8:REAPPLIED_DYNAMIC:SM37
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                                c'4.
                                \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:IC
                                c'4.
                                \f                                                                       %! SM8:REDUNDANT_DYNAMIC:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:IC
                                c'4.
                                \f                                                                       %! SM8:REDUNDANT_DYNAMIC:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                                c'4.
                                \sfz                                                                     %! SM8:EXPLICIT_DYNAMIC:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                                c'4.
                                \sfz                                                                     %! SM8:EXPLICIT_DYNAMIC:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                                c'4.
                                \sfz                                                                     %! SM8:EXPLICIT_DYNAMIC:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (“Flute”)                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                    %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%     \with-color                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%         #(x11-color 'DarkViolet) %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%         (“Flute”)                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%     }                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet) %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (“Flute”)                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    \with-color                                                          %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        #(x11-color 'green4)                                             %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        (“Flute”)                                                        %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    }                                                                    %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                  %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%     \with-color              %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%         #(x11-color 'green4) %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%         (“Flute”)            %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%     }                        %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                  %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    \with-color              %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        #(x11-color 'green4) %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        (“Flute”)            %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    }                        %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'2
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'2
                                ^ \markup {                                                              %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1)                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 4/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'2
                            %%% ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'2
                            %%% ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 4/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'2
                                ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'2
                                ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                c'4.
                                ^ \markup {                                                              %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1)                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                            %%% ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                c'4.
                                ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:DEFAULT_INSTRUMENT:ST1
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                c'4.
                                ^ \markup {                                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (“Flute”)                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                    %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override Staff.InstrumentName.color = #(x11-color 'violet)              %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:DEFAULT_INSTRUMENT:ST1
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                c'4.
                            %%% ^ \markup {                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%     \with-color                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%         #(x11-color 'DarkViolet) %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%         (“Flute”)                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%%     }                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            %%% \override Staff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:DEFAULT_INSTRUMENT:ST1
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                c'4.
                                ^ \markup {                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet) %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (“Flute”)                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override Staff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:EXPLICIT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'4.
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:EXPLICIT_INSTRUMENT:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'4.
                            %%% ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:EXPLICIT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'4.
                                ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:EXPLICIT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'4.
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:EXPLICIT_INSTRUMENT:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'4.
                            %%% ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:EXPLICIT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'4.
                                ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REAPPLIED_INSTRUMENT:SM37
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REAPPLIED_INSTRUMENT:SM37
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! SM6:REAPPLIED_INSTRUMENT_COLOR:SM37
                                c'4.
                                ^ \markup {                                                              %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    \with-color                                                          %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        #(x11-color 'green4)                                             %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        (“Flute”)                                                        %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    }                                                                    %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! SM6:REDRAWN_REAPPLIED_INSTRUMENT_COLOR:SM37
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_REAPPLIED_INSTRUMENT:SM34:SM37
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_REAPPLIED_INSTRUMENT:SM34:SM37
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REAPPLIED_INSTRUMENT:SM37
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REAPPLIED_INSTRUMENT:SM37
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! SM6:REAPPLIED_INSTRUMENT_COLOR:SM37
                                c'4.
                            %%% ^ \markup {                  %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%     \with-color              %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%         #(x11-color 'green4) %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%         (“Flute”)            %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%%     }                        %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                            %%% \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! SM6:REDRAWN_REAPPLIED_INSTRUMENT_COLOR:SM37
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_REAPPLIED_INSTRUMENT:SM34:SM37
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_REAPPLIED_INSTRUMENT:SM34:SM37
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REAPPLIED_INSTRUMENT:SM37
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REAPPLIED_INSTRUMENT:SM37
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! SM6:REAPPLIED_INSTRUMENT_COLOR:SM37
                                c'4.
                                ^ \markup {                  %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    \with-color              %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        #(x11-color 'green4) %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                        (“Flute”)            %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                    }                        %! SM11:REAPPLIED_INSTRUMENT_ALERT:SM37
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! SM6:REDRAWN_REAPPLIED_INSTRUMENT_COLOR:SM37
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_REAPPLIED_INSTRUMENT:SM34:SM37
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_REAPPLIED_INSTRUMENT:SM34:SM37
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:EXPLICIT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'2
                                ^ \markup {                                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDUNDANT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDUNDANT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                                c'2
                                ^ \markup {                                                              %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1)                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 4/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:EXPLICIT_INSTRUMENT:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'2
                            %%% ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDUNDANT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDUNDANT_INSTRUMENT:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                                c'2
                            %%% ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 4/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:EXPLICIT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:EXPLICIT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                c'2
                                ^ \markup {                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        (“Flute”)          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    }                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDUNDANT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDUNDANT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                                c'2
                                ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDUNDANT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDUNDANT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                                c'4.
                                ^ \markup {                                                              %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1)                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)                                                        %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                                                                    %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }                            %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. }                         %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
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
            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDUNDANT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDUNDANT_INSTRUMENT:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                                c'4.
                            %%% ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%         (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%%     }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.instrument_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDUNDANT_INSTRUMENT:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDUNDANT_INSTRUMENT:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                                c'4.
                                ^ \markup {                     %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    \with-color                 %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        #(x11-color 'DeepPink1) %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                        (“Flute”)               %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                    }                           %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                                \set Staff.instrumentName = \markup { Flute }    %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                                \set Staff.shortInstrumentName = \markup { Fl. } %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
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
    def margin_markups(self) -> None:
        r'''Margin markups.

        ..  container:: example

            Margin markup for examples:

            >>> margin_markups = abjad.OrderedDict()
            >>> margin_markups['I+II'] = abjad.MarginMarkup(
            ...     markup=abjad.Markup('I+II'),
            ...     short_markup=abjad.Markup('I+II'),
            ...     )
            >>> margin_markups['III+IV'] = abjad.MarginMarkup(
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
            ...     margin_markups['I+II'],
            ...     )
            >>> score_template.defaults.append(triple)
            >>> maker = baca.SegmentMaker(
            ...     breaks=breaks,
            ...     ignore_unpitched_notes=True,
            ...     margin_markups=margin_markups,
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:DEFAULT_MARGIN_MARKUP:+SCORE:+SEGMENT:ST2
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:DEFAULT_MARGIN_MARKUP:+SCORE:+SEGMENT:ST2
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! SM6:DEFAULT_MARGIN_MARKUP_COLOR:+SCORE:+SEGMENT:ST2
                                c'4.
                                ^ \markup {                                                              %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                    \with-color                                                          %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                        #(x11-color 'DarkViolet)                                         %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                        [“I+II”]                                                         %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                    }                                                                    %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                \override Staff.InstrumentName.color = #(x11-color 'violet)              %! SM6:REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:+SCORE:+SEGMENT:ST2
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:+SCORE:+SEGMENT:ST2
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:+SCORE:+SEGMENT:ST2
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
            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:DEFAULT_MARGIN_MARKUP:+SCORE:+SEGMENT:ST2
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:DEFAULT_MARGIN_MARKUP:+SCORE:+SEGMENT:ST2
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_MARGIN_MARKUP_COLOR:+SCORE:+SEGMENT:ST2
                                c'4.
                            %%% ^ \markup {                      %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                            %%%     \with-color                  %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                            %%%         #(x11-color 'DarkViolet) %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                            %%%         [“I+II”]                 %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                            %%%     }                            %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                            %%% \override Staff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:+SCORE:+SEGMENT:ST2
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:+SCORE:+SEGMENT:ST2
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:+SCORE:+SEGMENT:ST2
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:DEFAULT_MARGIN_MARKUP:+SCORE:+SEGMENT:ST2
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:DEFAULT_MARGIN_MARKUP:+SCORE:+SEGMENT:ST2
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_MARGIN_MARKUP_COLOR:+SCORE:+SEGMENT:ST2
                                c'4.
                                ^ \markup {                      %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                    \with-color                  %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                        #(x11-color 'DarkViolet) %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                        [“I+II”]                 %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                    }                            %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:+SCORE:+SEGMENT:ST2
                                \override Staff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:+SCORE:+SEGMENT:ST2
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:+SCORE:+SEGMENT:ST2
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:+SCORE:+SEGMENT:ST2
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
            ...     margin_markups=margin_markups,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markups['I+II']),
            ...     baca.make_notes(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> block = abjad.Block(name='layout')
            >>> block.indent = 0
            >>> lilypond_file.items.insert(0, block)
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
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                                ^ \markup {                                                              %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]                                                         %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
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
            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                            %%% ^ \markup {                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%         [“I+II”]           %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                                ^ \markup {                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]           %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    }                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
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
            ...     margin_markups=margin_markups,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markups['III+IV']),
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { III+IV }                           %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { III+IV }                      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                                ^ \markup {                                                              %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        [“III+IV”]                                                       %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { III+IV }                           %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { III+IV }                      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
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
            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { III+IV }      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { III+IV } %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                            %%% ^ \markup {                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%         [“III+IV”]         %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { III+IV }      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { III+IV } %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { III+IV }      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { III+IV } %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                                ^ \markup {                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        [“III+IV”]         %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    }                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { III+IV }      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { III+IV } %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
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
            ...     margin_markups=margin_markups,
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REAPPLIED_MARGIN_MARKUP:SM37
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REAPPLIED_MARGIN_MARKUP:SM37
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! SM6:REAPPLIED_MARGIN_MARKUP_COLOR:SM37
                                c'4.
                                ^ \markup {                                                              %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                    \with-color                                                          %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                        #(x11-color 'green4)                                             %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                        [“I+II”]                                                         %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                    }                                                                    %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! SM6:REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM37
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37
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
            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REAPPLIED_MARGIN_MARKUP:SM37
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REAPPLIED_MARGIN_MARKUP:SM37
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! SM6:REAPPLIED_MARGIN_MARKUP_COLOR:SM37
                                c'4.
                            %%% ^ \markup {                  %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                            %%%     \with-color              %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                            %%%         #(x11-color 'green4) %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                            %%%         [“I+II”]             %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                            %%%     }                        %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                            %%% \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! SM6:REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM37
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REAPPLIED_MARGIN_MARKUP:SM37
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REAPPLIED_MARGIN_MARKUP:SM37
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! SM6:REAPPLIED_MARGIN_MARKUP_COLOR:SM37
                                c'4.
                                ^ \markup {                  %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                    \with-color              %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                        #(x11-color 'green4) %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                        [“I+II”]             %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                    }                        %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! SM6:REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM37
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37
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
            ...     margin_markups=margin_markups,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markups['I+II']),
            ...     baca.map(
            ...         baca.margin_markup(margin_markups['I+II']),
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'2
                                ^ \markup {                                                              %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'blue)                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]                                                         %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    }                                                                    %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! SM6:REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                c'2
                                ^ \markup {                                                              %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                                                          %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'DeepPink1)                                          %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]                                                         %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    }                                                                    %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! SM6:REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
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
            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 4/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'2
                            %%% ^ \markup {                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%     \with-color            %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%         #(x11-color 'blue) %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%         [“I+II”]           %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%%     }                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                c'2
                            %%% ^ \markup {                     %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%     \with-color                 %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%         #(x11-color 'DeepPink1) %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%         [“I+II”]                %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%     }                           %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 3] %! SM4
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 4/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                c'2
                                ^ \markup {                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    \with-color            %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'blue) %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]           %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    }                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                c'2
                                ^ \markup {                     %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                 %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'DeepPink1) %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]                %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    }                           %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
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
            ...     margin_markups=margin_markups,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.margin_markup(margin_markups['I+II']),
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! SM6:REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                                ^ \markup {                                                              %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                                                          %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'DeepPink1)                                          %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]                                                         %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    }                                                                    %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! SM6:REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
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
            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.deactivate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                            %%% ^ \markup {                     %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%     \with-color                 %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%         #(x11-color 'DeepPink1) %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%         [“I+II”]                %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%%     }                           %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                <BLANKLINE>
                                % [MusicVoice measure 2] %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> tags_ = abjad.tags.margin_markup_color_tags()
            >>> match = lambda tags: bool(set(tags) & set(tags_))
            >>> text, count = abjad.activate(text, match)
            >>> lines = [_.strip('\n') for _ in text.split('\n')]
            >>> lilypond_file.score_block.items[:] = lines
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \autoPageBreaksOff %! BMM1:BREAK
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                         %! IC:BREAK
                            \time 3/8 %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar "" %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue) %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak %! IC:BREAK
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! SM4
                            \newSpacingSection                                               %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24) %! HSS1:SPACING
                            \noBreak %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                        %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break %! IC:BREAK
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f %! SM5
                            \bar "|"                                  %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1] %! SM4
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDUNDANT_MARGIN_MARKUP:IC
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                c'4.
                                ^ \markup {                     %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    \with-color                 %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        #(x11-color 'DeepPink1) %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                        [“I+II”]                %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                    }                           %! SM11:REDUNDANT_MARGIN_MARKUP_ALERT:IC
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! SM6:REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:IC
                                \set Staff.instrumentName = \markup { I+II }      %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
                                \set Staff.shortInstrumentName = \markup { I+II } %! SM8:REDRAWN_REDUNDANT_MARGIN_MARKUP:SM34:IC
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
            ...     margin_markups=margin_markups,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.tag(
            ...         '+SEGMENT',
            ...         baca.margin_markup(margin_markups['I+II']),
            ...         ),
            ...     baca.tag(
            ...         '+PARTS_VIOLIN',
            ...         baca.margin_markup(margin_markups['III+IV']),
            ...         deactivate=True,
            ...         ),
            ...     baca.tag(
            ...         '+PARTS_VIOLA',
            ...         baca.margin_markup(margin_markups['III+IV']),
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (11)))                              %! IC:BREAK
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 15) (alignment-distances . (11)))                             %! IC:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            \break                                                                       %! IC:BREAK
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:EXPLICIT_MARGIN_MARKUP:IC:+SEGMENT
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:EXPLICIT_MARGIN_MARKUP:IC:+SEGMENT
                            %@% \set Staff.instrumentName = \markup { III+IV }                           %! SM8:EXPLICIT_MARGIN_MARKUP:IC:+PARTS_VIOLIN
                            %@% \set Staff.shortInstrumentName = \markup { III+IV }                      %! SM8:EXPLICIT_MARGIN_MARKUP:IC:+PARTS_VIOLIN
                            %@% \set Staff.instrumentName = \markup { III+IV }                           %! SM8:EXPLICIT_MARGIN_MARKUP:IC:+PARTS_VIOLA
                            %@% \set Staff.shortInstrumentName = \markup { III+IV }                      %! SM8:EXPLICIT_MARGIN_MARKUP:IC:+PARTS_VIOLA
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC:+SEGMENT
                            %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC:+PARTS_VIOLIN
                            %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC:+PARTS_VIOLA
                                c'2
                                ^ \markup {
                                    \column
                                        {
                                            \line                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+SEGMENT
                                                {                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+SEGMENT
                                                    \with-color                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+SEGMENT
                                                        #(x11-color 'blue)                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+SEGMENT
                                                        [“I+II”]                                         %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+SEGMENT
                                                }                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+SEGMENT
                                        %@% \line                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLIN
                                        %@%     {                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLIN
                                        %@%         \with-color                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLIN
                                        %@%             #(x11-color 'blue)                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLIN
                                        %@%             [“III+IV”]                                       %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLIN
                                        %@%     }                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLIN
                                        %@% \line                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLA
                                        %@%     {                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLA
                                        %@%         \with-color                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLA
                                        %@%             #(x11-color 'blue)                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLA
                                        %@%             [“III+IV”]                                       %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLA
                                        %@%     }                                                        %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC:+PARTS_VIOLA
                                        }
                                    }
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC:+SEGMENT
                                \set Staff.instrumentName = \markup { I+II }                             %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC:+SEGMENT
                                \set Staff.shortInstrumentName = \markup { I+II }                        %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC:+SEGMENT
                            %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC:+PARTS_VIOLIN
                                \set Staff.instrumentName = \markup { III+IV }                           %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC:+PARTS_VIOLIN
                                \set Staff.shortInstrumentName = \markup { III+IV }                      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC:+PARTS_VIOLIN
                            %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC:+PARTS_VIOLA
                                \set Staff.instrumentName = \markup { III+IV }                           %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC:+PARTS_VIOLA
                                \set Staff.shortInstrumentName = \markup { III+IV }                      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC:+PARTS_VIOLA
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:EXPLICIT_METRONOME_MARK
                        %@% \markup {                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \fontsize                                                                %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         #-6                                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         \general-align                                                       %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             #Y                                                               %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             #DOWN                                                            %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             \note-by-number                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #2                                                           %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #0                                                           %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #1.5                                                         %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \upright                                                                 %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         {                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             =                                                                %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             112                                                              %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         }                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \hspace                                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         #1                                                                   %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     }                                                                        %! SM27:EXPLICIT_METRONOME_MARK %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                            \markup {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                \with-color                                                              %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    #(x11-color 'blue)                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \fontsize                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            #-6                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            \general-align                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #Y                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #DOWN                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                \note-by-number                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #2                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #0                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #1.5                                                 %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \upright                                                         %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            {                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                =                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                112                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            }                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \hspace                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            #1                                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                }                                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OC1
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:EXPLICIT_METRONOME_MARK
                        %@% \markup {                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \fontsize                                                                %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         #-6                                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         \general-align                                                       %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             #Y                                                               %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             #DOWN                                                            %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             \note-by-number                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #2                                                           %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #0                                                           %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #1.5                                                         %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \upright                                                                 %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         {                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             =                                                                %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             112                                                              %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         }                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \hspace                                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         #1                                                                   %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     }                                                                        %! SM27:EXPLICIT_METRONOME_MARK %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                            \markup {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                \with-color                                                              %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    #(x11-color 'blue)                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \fontsize                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            #-6                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            \general-align                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #Y                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #DOWN                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                \note-by-number                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #2                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #0                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #1.5                                                 %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \upright                                                         %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            {                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                =                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                112                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            }                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \hspace                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            #1                                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                }                                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \revert TextSpanner.staff-padding                                            %! OC2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OC1
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@% \markup {                                                                    %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%     \fontsize                                                                %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%         #-6                                                                  %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%         \general-align                                                       %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%             #Y                                                               %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%             #DOWN                                                            %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%             \note-by-number                                                  %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%                 #2                                                           %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%                 #0                                                           %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%                 #1.5                                                         %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%     \upright                                                                 %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%         {                                                                    %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%             =                                                                %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%             90                                                               %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%         }                                                                    %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%     \hspace                                                                  %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%         #1                                                                   %! SM27:REAPPLIED_METRONOME_MARK:SM36
                        %@%     }                                                                        %! SM27:REAPPLIED_METRONOME_MARK:SM36 %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =                        %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                            \markup {                                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                \with-color                                                              %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    #(x11-color 'green4)                                                 %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    {                                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                        \fontsize                                                        %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                            #-6                                                          %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                            \general-align                                               %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                #Y                                                       %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                #DOWN                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                \note-by-number                                          %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                    #2                                                   %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                    #0                                                   %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                    #1.5                                                 %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                        \upright                                                         %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                            {                                                            %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                =                                                        %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                                90                                                       %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                            }                                                            %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                        \hspace                                                          %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                            #1                                                           %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    }                                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                }                                                                        %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36 %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \revert TextSpanner.staff-padding                                            %! OC2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:EXPLICIT_METRONOME_MARK
                        %@% \markup {                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \fontsize                                                                %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         #-6                                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         \general-align                                                       %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             #Y                                                               %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             #DOWN                                                            %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             \note-by-number                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #2                                                           %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #0                                                           %! SM27:EXPLICIT_METRONOME_MARK
                        %@%                 #1.5                                                         %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \upright                                                                 %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         {                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             =                                                                %! SM27:EXPLICIT_METRONOME_MARK
                        %@%             112                                                              %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         }                                                                    %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     \hspace                                                                  %! SM27:EXPLICIT_METRONOME_MARK
                        %@%         #1                                                                   %! SM27:EXPLICIT_METRONOME_MARK
                        %@%     }                                                                        %! SM27:EXPLICIT_METRONOME_MARK %! SM29:METRONOME_MARK_SPANNER
                        %@% \once \override TextSpanner.bound-details.right.text =                       %! SM27:REDUNDANT_METRONOME_MARK
                        %@% \markup {                                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%     \concat                                                                  %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         {                                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             \hspace                                                          %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                 #-0.5                                                        %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             \line                                                            %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                 {                                                            %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                     \fontsize                                                %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                         #-6                                                  %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                         \general-align                                       %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                             #Y                                               %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                             #DOWN                                            %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                             \note-by-number                                  %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                                 #2                                           %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                                 #0                                           %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                                 #1.5                                         %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                     \upright                                                 %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                         {                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                             =                                                %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                             112                                              %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                         }                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                 }                                                            %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         }                                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%     }                                                                        %! SM27:REDUNDANT_METRONOME_MARK %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                            \markup {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                \with-color                                                              %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    #(x11-color 'blue)                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \fontsize                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            #-6                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            \general-align                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #Y                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #DOWN                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                \note-by-number                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #2                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #0                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    #1.5                                                 %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \upright                                                         %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            {                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                =                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                112                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            }                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        \hspace                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            #1                                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                }                                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.text =                       %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                            \markup {                                                                    %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                \with-color                                                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                    #(x11-color 'DeepPink1)                                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                    \concat                                                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                        {                                                                %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            \hspace                                                      %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                #-0.5                                                    %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            \line                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                {                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                    \fontsize                                            %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                        #-6                                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                        \general-align                                   %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                            #Y                                           %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                            #DOWN                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                            \note-by-number                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                                #2                                       %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                                #0                                       %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                                #1.5                                     %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                    \upright                                             %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                        {                                                %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                            =                                            %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                            112                                          %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                        }                                                %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                }                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                        }                                                                %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                }                                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OC1
                            \autoPageBreaksOff                                                           %! BMM1:BREAK
                            \noBreak                                                                     %! BMM2:BREAK
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! IC:BREAK
                            #'((Y-offset . 0) (alignment-distances . (8)))                               %! IC:BREAK
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:REDUNDANT_METRONOME_MARK
                        %@% \markup {                                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%     \fontsize                                                                %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         #-6                                                                  %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         \general-align                                                       %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             #Y                                                               %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             #DOWN                                                            %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             \note-by-number                                                  %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                 #2                                                           %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                 #0                                                           %! SM27:REDUNDANT_METRONOME_MARK
                        %@%                 #1.5                                                         %! SM27:REDUNDANT_METRONOME_MARK
                        %@%     \upright                                                                 %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         {                                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             =                                                                %! SM27:REDUNDANT_METRONOME_MARK
                        %@%             112                                                              %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         }                                                                    %! SM27:REDUNDANT_METRONOME_MARK
                        %@%     \hspace                                                                  %! SM27:REDUNDANT_METRONOME_MARK
                        %@%         #1                                                                   %! SM27:REDUNDANT_METRONOME_MARK
                        %@%     }                                                                        %! SM27:REDUNDANT_METRONOME_MARK %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                            \markup {                                                                    %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                \with-color                                                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                    #(x11-color 'DeepPink1)                                              %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                    {                                                                    %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                        \fontsize                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            #-6                                                          %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            \general-align                                               %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                #Y                                                       %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                #DOWN                                                    %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                \note-by-number                                          %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                    #2                                                   %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                    #0                                                   %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                    #1.5                                                 %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                        \upright                                                         %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            {                                                            %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                =                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                                112                                                      %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            }                                                            %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                        \hspace                                                          %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                            #1                                                           %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                    }                                                                    %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR
                                }                                                                        %! SM15:REDUNDANT_METRONOME_MARK_WITH_COLOR %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            \pageBreak                                                                   %! IC:BREAK
                            s1 * 3/8
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \noBreak                                                                     %! BMM2:BREAK
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \revert TextSpanner.staff-padding                                            %! OC2
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 5                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 1                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! SM8:REAPPLIED_STAFF_LINES:SM37
                                \once \override Staff.StaffSymbol.line-count = 5                         %! SM8:REAPPLIED_STAFF_LINES:SM37
                                \startStaff                                                              %! SM8:REAPPLIED_STAFF_LINES:SM37
                                \once \override Staff.StaffSymbol.color = #(x11-color 'green4)           %! SM6:REAPPLIED_STAFF_LINES_COLOR:SM37
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 5                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \stopStaff                                                               %! SM8:REDUNDANT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 5                         %! SM8:REDUNDANT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:REDUNDANT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_STAFF_LINES_COLOR:IC
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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \stopStaff                                                               %! SM8:REDUNDANT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 5                         %! SM8:REDUNDANT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:REDUNDANT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_STAFF_LINES_COLOR:IC
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
