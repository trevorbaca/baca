import abjad


class PersistentIndicatorTests(abjad.AbjadObject):
    """
    Persistent indicator tests.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Classes'

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def clefs(self) -> None:
        r"""
        Clefs.

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
            ...     spacing=baca.minimum_duration((1, 24)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \clef "treble"                                                           %! DEFAULT_CLEF:_set_status_tag:ScoreTemplate(3)
                                \once \override Staff.Clef.color = #(x11-color 'DarkViolet)              %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):ScoreTemplate(3)
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'violet)                        %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \clef "treble"                                                           %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \clef "alto"                                                             %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \clef "treble"                                                           %! REAPPLIED_CLEF:_set_status_tag:_reapply_persistent_indicators(3)
                                \once \override Staff.Clef.color = #(x11-color 'green4)                  %! REAPPLIED_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! REAPPLIED_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! REAPPLIED_CLEF:_set_status_tag:_treat_persistent_wrapper(2):_reapply_persistent_indicators(3)
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)                     %! REAPPLIED_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.clef('treble', selector=baca.leaf(0)),
            ...     baca.clef('treble', selector=baca.leaf(1)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \clef "treble"                                                           %! EXPLICIT_CLEF:_set_status_tag:IndicatorCommand
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \clef "treble"                                                           %! REDUNDANT_CLEF:_set_status_tag:IndicatorCommand
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! REDUNDANT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! REDUNDANT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! REDUNDANT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! REDUNDANT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \clef "treble"                                                           %! REDUNDANT_CLEF:_set_status_tag:IndicatorCommand
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! REDUNDANT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override Staff.Clef.color = ##f                                         %! REDUNDANT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set Staff.forceClef = ##t                                               %! REDUNDANT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):IndicatorCommand
                                R1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! REDUNDANT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        Returns none.
        """
        pass

    @property
    def dynamics(self) -> None:
        r"""
        Dynamics.

        ..  container:: example

            Explicit dynamics color blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'green4)           %! REAPPLIED_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \f                                                                       %! REAPPLIED_DYNAMIC:_set_status_tag:_reapply_persistent_indicators(3)
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.dynamic('f'),
            ...     baca.dynamic('f', selector=baca.leaf(1)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! REDUNDANT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \f                                                                       %! REDUNDANT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! REDUNDANT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \f                                                                       %! REDUNDANT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.dynamic('sfz'),
            ...     baca.dynamic('sfz', selector=baca.leaf(1)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \sfz                                                                     %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \sfz                                                                     %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \sfz                                                                     %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            REGRESSION. Conventional and effort dynamics analyze
            nonredundantly:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.dynamic('mf'),
            ...     baca.dynamic('"mf"', selector=baca.leaf(1)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \mf                                                                      %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! EXPLICIT_DYNAMIC_COLOR:_attach_color_literal(2)
                                c'4.
                                \baca_effort_mf                                                          %! EXPLICIT_DYNAMIC:_set_status_tag:IndicatorCommand
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        pass

    @property
    def instruments(self) -> None:
        r"""
        Instruments.

        ..  container:: example

            Example instruments:

            >>> instruments = abjad.OrderedDict()
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-default-indicator-markup "(“Flute”)"                     %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                            %%% ^ \markup \baca-default-indicator-markup "(“Flute”)" %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-default-indicator-markup "(“Flute”)" %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "(“Flute”)"                    %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                            %%% ^ \markup \baca-explicit-indicator-markup "(“Flute”)" %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "(“Flute”)" %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         manifest='instruments',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "(“Flute”)"                    %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                            %%% ^ \markup \baca-explicit-indicator-markup "(“Flute”)" %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "(“Flute”)" %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         manifest='instruments',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-reapplied-indicator-markup "(“Flute”)"                   %! REAPPLIED_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                            %%% ^ \markup \baca-reapplied-indicator-markup "(“Flute”)" %! REAPPLIED_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-reapplied-indicator-markup "(“Flute”)" %! REAPPLIED_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.instrument(instruments['Flute']),
            ...     baca.map(
            ...         baca.leaves()[1],
            ...         baca.instrument(instruments['Flute']),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'2
                                ^ \markup \baca-explicit-indicator-markup "(“Flute”)"                    %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'2
                                ^ \markup \baca-redundant-indicator-markup "(“Flute”)"                   %! REDUNDANT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'2
                            %%% ^ \markup \baca-explicit-indicator-markup "(“Flute”)" %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
                                c'2
                            %%% ^ \markup \baca-redundant-indicator-markup "(“Flute”)" %! REDUNDANT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 3] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'2
                                ^ \markup \baca-explicit-indicator-markup "(“Flute”)" %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
                                c'2
                                ^ \markup \baca-redundant-indicator-markup "(“Flute”)" %! REDUNDANT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 3] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.instrument(instruments['Flute']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         manifest='instruments',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-redundant-indicator-markup "(“Flute”)"                   %! REDUNDANT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                            %%% ^ \markup \baca-redundant-indicator-markup "(“Flute”)" %! REDUNDANT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                c'4.
                                ^ \markup \baca-redundant-indicator-markup "(“Flute”)" %! REDUNDANT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        pass

    @property
    def margin_markups(self) -> None:
        r"""
        Margin markups.

        ..  container:: example

            Margin markup for examples:

            >>> margin_markups = abjad.OrderedDict()
            >>> margin_markups['I+II'] = abjad.MarginMarkup(
            ...     markup=abjad.Markup('I+II'),
            ...     )
            >>> margin_markups['III+IV'] = abjad.MarginMarkup(
            ...     markup=abjad.Markup('III+IV'),
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! DEFAULT_MARGIN_MARKUP:_set_status_tag:ScoreTemplate(2):-PARTS
                                \markup { I+II }                                                         %! DEFAULT_MARGIN_MARKUP:_set_status_tag:ScoreTemplate(2):-PARTS
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! DEFAULT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-default-indicator-markup "[“I+II”]"                      %! DEFAULT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'violet)              %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):ScoreTemplate(2):-PARTS
                                \markup { I+II }                                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):ScoreTemplate(2):-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! DEFAULT_MARGIN_MARKUP:_set_status_tag:ScoreTemplate(2):-PARTS
                                \markup { I+II }                 %! DEFAULT_MARGIN_MARKUP:_set_status_tag:ScoreTemplate(2):-PARTS
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                            %%% ^ \markup \baca-default-indicator-markup "[“I+II”]" %! DEFAULT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_DEFAULT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):ScoreTemplate(2):-PARTS
                                \markup { I+II }                 %! REDRAWN_DEFAULT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):ScoreTemplate(2):-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! DEFAULT_MARGIN_MARKUP:_set_status_tag:ScoreTemplate(2):-PARTS
                                \markup { I+II }                 %! DEFAULT_MARGIN_MARKUP:_set_status_tag:ScoreTemplate(2):-PARTS
                                \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-default-indicator-markup "[“I+II”]" %! DEFAULT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_DEFAULT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):ScoreTemplate(2):-PARTS
                                \markup { I+II }                 %! REDRAWN_DEFAULT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):ScoreTemplate(2):-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "[“I+II”]"                     %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                            %%% ^ \markup \baca-explicit-indicator-markup "[“I+II”]" %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "[“I+II”]" %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.margin_markup(margin_markups['III+IV']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         manifest='margin_markups',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { III+IV }                                                       %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "[“III+IV”]"                   %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { III+IV }                                                       %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { III+IV }               %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                            %%% ^ \markup \baca-explicit-indicator-markup "[“III+IV”]" %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { III+IV }               %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { III+IV }               %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-explicit-indicator-markup "[“III+IV”]" %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { III+IV }               %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         manifest='margin_markups',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! REAPPLIED_MARGIN_MARKUP:_set_status_tag:_reapply_persistent_indicators(3):-PARTS
                                \markup { I+II }                                                         %! REAPPLIED_MARGIN_MARKUP:_set_status_tag:_reapply_persistent_indicators(3):-PARTS
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! REAPPLIED_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-reapplied-indicator-markup "[“I+II”]"                    %! REAPPLIED_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):_reapply_persistent_indicators(3):-PARTS
                                \markup { I+II }                                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):_reapply_persistent_indicators(3):-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! REAPPLIED_MARGIN_MARKUP:_set_status_tag:_reapply_persistent_indicators(3):-PARTS
                                \markup { I+II }                 %! REAPPLIED_MARGIN_MARKUP:_set_status_tag:_reapply_persistent_indicators(3):-PARTS
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! REAPPLIED_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                            %%% ^ \markup \baca-reapplied-indicator-markup "[“I+II”]" %! REAPPLIED_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_REAPPLIED_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):_reapply_persistent_indicators(3):-PARTS
                                \markup { I+II }                 %! REDRAWN_REAPPLIED_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):_reapply_persistent_indicators(3):-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! REAPPLIED_MARGIN_MARKUP:_set_status_tag:_reapply_persistent_indicators(3):-PARTS
                                \markup { I+II }                 %! REAPPLIED_MARGIN_MARKUP:_set_status_tag:_reapply_persistent_indicators(3):-PARTS
                                \once \override Staff.InstrumentName.color = #(x11-color 'green4) %! REAPPLIED_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-reapplied-indicator-markup "[“I+II”]" %! REAPPLIED_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'OliveDrab) %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_REAPPLIED_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):_reapply_persistent_indicators(3):-PARTS
                                \markup { I+II }                 %! REDRAWN_REAPPLIED_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):_reapply_persistent_indicators(3):-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.margin_markup(margin_markups['I+II']),
            ...     baca.map(
            ...         baca.leaves()[1],
            ...         baca.margin_markup(margin_markups['I+II']),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                                ^ \markup \baca-explicit-indicator-markup "[“I+II”]"                     %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                                ^ \markup \baca-redundant-indicator-markup "[“I+II”]"                    %! REDUNDANT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                            %%% ^ \markup \baca-explicit-indicator-markup "[“I+II”]" %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                            %%% ^ \markup \baca-redundant-indicator-markup "[“I+II”]" %! REDUNDANT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 3] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 4/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 1/2 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                                ^ \markup \baca-explicit-indicator-markup "[“I+II”]" %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                                ^ \markup \baca-redundant-indicator-markup "[“I+II”]" %! REDUNDANT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 3] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.margin_markup(margin_markups['I+II']),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         manifest='margin_markups',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-redundant-indicator-markup "[“I+II”]"                    %! REDUNDANT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> score = lilypond_file[abjad.Score]
            >>> text = format(score, 'lilypond')
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                            %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                            %%% ^ \markup \baca-redundant-indicator-markup "[“I+II”]" %! REDUNDANT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
                            % [GlobalSkips measure 1] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff %! BreakMeasureMap(1):BREAK
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11) %! IndicatorCommand:BREAK
                            \time 3/8 %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar "" %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue" %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2] %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24 %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11) %! IndicatorCommand:BREAK
                            \break %! IndicatorCommand:BREAK
                            s1 * 3/8 %! _make_global_skips(1)
                            \baca_bar_line_visible %! _attach_final_bar_line
                            \bar "|"               %! _attach_final_bar_line
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
                                % [MusicVoice measure 1] %! _comment_measure_numbers
                                \set Staff.shortInstrumentName = %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \markup { I+II }                 %! REDUNDANT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand
                                \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'4.
                                ^ \markup \baca-redundant-indicator-markup "[“I+II”]" %! REDUNDANT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepPink4) %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName = %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                                \markup { I+II }                 %! REDRAWN_REDUNDANT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand
                <BLANKLINE>
                                % [MusicVoice measure 2] %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.tag(
            ...         '-PARTS',
            ...         baca.margin_markup(margin_markups['I+II']),
            ...         ),
            ...     baca.tag(
            ...         '-PARTS',
            ...         baca.margin_markup(margin_markups['III+IV']),
            ...         deactivate=True,
            ...         ),
            ...     baca.tag(
            ...         '-PARTS',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #0 #'(11)                                                         %! IndicatorCommand:BREAK
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #15 #'(11)                                                        %! IndicatorCommand:BREAK
                            \break                                                                       %! IndicatorCommand:BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand:-PARTS
                                \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand:-PARTS
                            %@% \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand:-PARTS
                            %@% \markup { III+IV }                                                       %! EXPLICIT_MARGIN_MARKUP:_set_status_tag:IndicatorCommand:-PARTS
                                \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                            %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                c'2
                                ^ \markup \baca-explicit-indicator-markup "[“I+II”]"                     %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                            %@% ^ \markup \baca-explicit-indicator-markup "[“III+IV”]"                   %! EXPLICIT_MARGIN_MARKUP_ALERT:_attach_latent_indicator_alert
                                \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand:-PARTS
                                \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand:-PARTS
                            %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:_attach_color_literal(2)
                                \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand:-PARTS
                                \markup { III+IV }                                                       %! REDRAWN_EXPLICIT_MARGIN_MARKUP:_set_status_tag:_treat_persistent_wrapper(3):IndicatorCommand:-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                                c'2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return None

    @property
    def metronome_marks(self) -> None:
        r"""
        Metronome marks.

        ..  container:: example

            >>> breaks = baca.breaks(baca.page([1, 4, (8,)]))
            >>> metronome_marks = abjad.OrderedDict()
            >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
            >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

        ..  container:: example

            Explicit metronome marks color blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 25)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark('112'),
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_invisible_line                                                      %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \abjad-metronome-mark-markup #2 #0 #1 #"112"                     %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_invisible_line                                                      %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'blue)                                           %! _attach_metronome_marks(3)
                                            \abjad-metronome-mark-markup #2 #0 #1 #"112"                 %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark('112'),
            ...     baca.text_spanner_staff_padding(4),
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         manifest='metronome_marks',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OverrideCommand(1)
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_invisible_line                                                      %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \abjad-metronome-mark-markup #2 #0 #1 #"112"                     %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_invisible_line                                                      %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'blue)                                           %! _attach_metronome_marks(3)
                                            \abjad-metronome-mark-markup #2 #0 #1 #"112"                 %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \revert TextSpanner.staff-padding                                            %! OverrideCommand(2)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied metronome marks color green:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.text_spanner_staff_padding(4),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         manifest='metronome_marks',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OverrideCommand(1)
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_invisible_line                                                      %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \abjad-metronome-mark-markup #2 #0 #1 #"90"                      %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_invisible_line                                                      %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'green4)                                         %! _attach_metronome_marks(3)
                                            \abjad-metronome-mark-markup #2 #0 #1 #"90"                  %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \revert TextSpanner.staff-padding                                            %! OverrideCommand(2)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant metronome marks color pink:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark('112'),
            ...     baca.metronome_mark('112', selector=baca.leaf(1)),
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_invisible_line                                                      %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \abjad-metronome-mark-markup #2 #0 #1 #"112"                     %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.right.text \markup {                                  %! _attach_metronome_marks(2)
                        %@%     \abjad-metronome-mark-markup #2 #0 #1 #"112"                             %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_invisible_line                                                      %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'blue)                                           %! _attach_metronome_marks(3)
                                            \abjad-metronome-mark-markup #2 #0 #1 #"112"                 %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            - \tweak bound-details.right.text \markup {                                  %! _attach_metronome_marks(3)
                                \with-color                                                              %! _attach_metronome_marks(3)
                                    #(x11-color 'DeepPink1)                                              %! _attach_metronome_marks(3)
                                    \abjad-metronome-mark-markup #2 #0 #1 #"112"                         %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark('112'),
            ...     baca.text_spanner_staff_padding(4),
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         manifest='metronome_marks',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OverrideCommand(1)
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_invisible_line                                                      %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \abjad-metronome-mark-markup #2 #0 #1 #"112"                     %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_invisible_line                                                      %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'DeepPink1)                                      %! _attach_metronome_marks(3)
                                            \abjad-metronome-mark-markup #2 #0 #1 #"112"                 %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \revert TextSpanner.staff-padding                                            %! OverrideCommand(2)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        pass

    @property
    def persistent_overrides(self) -> None:
        r"""
        Persistent overrides.

        ..  container:: example

            Explicit persistent overrides work but do not color:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.bar_extent_persistent((0, 0)),
            ...     baca.make_notes(),
            ...     baca.staff_lines(1),
            ...     baca.staff_position(0),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_PERSISTENT_OVERRIDE:_set_status_tag:IndicatorCommand
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                                b'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                b'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Persistent overrides also appear in segment metadata:

            >>> abjad.f(maker.metadata['persistent_indicators'])
            abjad.OrderedDict(
                [
                    (
                        'MusicStaff',
                        [
                            abjad.Momento(
                                context='MusicVoice',
                                prototype='abjad.PersistentOverride',
                                value=abjad.PersistentOverride(
                                    after=True,
                                    attribute='bar_extent',
                                    context='Staff',
                                    grob='bar_line',
                                    value=(0, 0),
                                    ),
                                ),
                            abjad.Momento(
                                context='MusicVoice',
                                prototype='baca.StaffLines',
                                value=1,
                                ),
                            ],
                        ),
                    (
                        'Score',
                        [
                            abjad.Momento(
                                context='GlobalSkips',
                                prototype='abjad.TimeSignature',
                                value='3/8',
                                ),
                            ],
                        ),
                    ]
                )


        ..  container:: example

            Reapplied persistent overrides work but do not color:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicVoice'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.PersistentOverride',
            ...         value=abjad.PersistentOverride(
            ...             after=True,
            ...             attribute='bar_extent',
            ...             context='Staff',
            ...             grob='bar_line',
            ...             value=(0, 0),
            ...             ),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! REAPPLIED_PERSISTENT_OVERRIDE:_set_status_tag:_reapply_persistent_indicators(3)
                                \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Redundant persistent overrides work but currently provide no
            warning:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.bar_extent_persistent((0, 0)),
            ...     baca.bar_extent_persistent((0, 0), selector=baca.leaf(1)),
            ...     baca.make_notes(),
            ...     baca.staff_lines(1),
            ...     baca.staff_position(0),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_PERSISTENT_OVERRIDE:_set_status_tag:IndicatorCommand
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                                b'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! REDUNDANT_PERSISTENT_OVERRIDE:_set_status_tag:IndicatorCommand
                                b'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even at the beginning of a segment:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.bar_extent_persistent((0, 0)),
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicVoice'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
            ...         prototype='abjad.PersistentOverride',
            ...         value=abjad.PersistentOverride(
            ...             after=True,
            ...             attribute='bar_extent',
            ...             context='Staff',
            ...             grob='bar_line',
            ...             value=(0, 0),
            ...             ),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! REDUNDANT_PERSISTENT_OVERRIDE:_set_status_tag:IndicatorCommand
                                \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \baca_unpitched_music_warning                                            %! _color_unpitched_notes
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        pass

    @property
    def staff_lines(self) -> None:
        r"""
        Staff lines.

        ..  container:: example

            Explicit staff lines color blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 5                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \stopStaff                                                               %! REAPPLIED_STAFF_LINES:_set_status_tag:_reapply_persistent_indicators(3)
                                \once \override Staff.StaffSymbol.line-count = 5                         %! REAPPLIED_STAFF_LINES:_set_status_tag:_reapply_persistent_indicators(3)
                                \startStaff                                                              %! REAPPLIED_STAFF_LINES:_set_status_tag:_reapply_persistent_indicators(3)
                                \once \override Staff.StaffSymbol.color = #(x11-color 'green4)           %! REAPPLIED_STAFF_LINES_COLOR:_attach_color_literal(2)
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.staff_lines(5),
            ...     baca.staff_lines(5, selector=baca.leaf(1)),
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \stopStaff                                                               %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 5                         %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! EXPLICIT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:_attach_color_literal(2)
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                \stopStaff                                                               %! REDUNDANT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 5                         %! REDUNDANT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! REDUNDANT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! REDUNDANT_STAFF_LINES_COLOR:_attach_color_literal(2)
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                \stopStaff                                                               %! REDUNDANT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.line-count = 5                         %! REDUNDANT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \startStaff                                                              %! REDUNDANT_STAFF_LINES:_set_status_tag:IndicatorCommand
                                \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! REDUNDANT_STAFF_LINES_COLOR:_attach_color_literal(2)
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        pass

    @property
    def tempo_trends(self) -> None:
        r"""
        Tempo trends.

        ..  container:: example

            >>> breaks = baca.breaks(baca.page([1, 4, (8,)]))
            >>> metronome_marks = abjad.OrderedDict()
            >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
            >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

        ..  container:: example

            Explicit tempo trends color blue:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 25)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark(baca.Accelerando()),
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \large                                                           %! _attach_metronome_marks(2)
                        %@%                 \upright                                                     %! _attach_metronome_marks(2)
                        %@%                     accel.                                                   %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'blue)                                           %! _attach_metronome_marks(3)
                                            \large                                                       %! _attach_metronome_marks(3)
                                                \upright                                                 %! _attach_metronome_marks(3)
                                                    accel.                                               %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Even after a previous tempo trend:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark(baca.Accelerando()),
            ...     baca.text_spanner_staff_padding(4),
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         prototype='baca.Ritardando',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OverrideCommand(1)
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \large                                                           %! _attach_metronome_marks(2)
                        %@%                 \upright                                                     %! _attach_metronome_marks(2)
                        %@%                     accel.                                                   %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'blue)                                           %! _attach_metronome_marks(3)
                                            \large                                                       %! _attach_metronome_marks(3)
                                                \upright                                                 %! _attach_metronome_marks(3)
                                                    accel.                                               %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \revert TextSpanner.staff-padding                                            %! OverrideCommand(2)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Reapplied tempo trends color green:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.text_spanner_staff_padding(4),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         prototype='baca.Accelerando',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OverrideCommand(1)
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \large                                                           %! _attach_metronome_marks(2)
                        %@%                 \upright                                                     %! _attach_metronome_marks(2)
                        %@%                     accel.                                                   %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'green4)                                         %! _attach_metronome_marks(3)
                                            \large                                                       %! _attach_metronome_marks(3)
                                                \upright                                                 %! _attach_metronome_marks(3)
                                                    accel.                                               %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \revert TextSpanner.staff-padding                                            %! OverrideCommand(2)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>
                
        ..  container:: example

            Redundant tempo trends color pink:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     breaks=breaks,
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark(baca.Accelerando()),
            ...     baca.metronome_mark(
            ...         baca.Accelerando(),
            ...         selector=baca.leaf(1),
            ...         ),
            ...     )
            >>> maker(
            ...     'MusicVoice',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \large                                                           %! _attach_metronome_marks(2)
                        %@%                 \upright                                                     %! _attach_metronome_marks(2)
                        %@%                     accel.                                                   %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'blue)                                           %! _attach_metronome_marks(3)
                                            \large                                                       %! _attach_metronome_marks(3)
                                                \upright                                                 %! _attach_metronome_marks(3)
                                                    accel.                                               %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(1)
                        %@% - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \large                                                           %! _attach_metronome_marks(2)
                        %@%                 \upright                                                     %! _attach_metronome_marks(2)
                        %@%                     accel.                                                   %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'DeepPink1)                                      %! _attach_metronome_marks(3)
                                            \large                                                       %! _attach_metronome_marks(3)
                                                \upright                                                 %! _attach_metronome_marks(3)
                                                    accel.                                               %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
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
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=[(3, 8), (3, 8)],
            ...     )
            >>> maker(
            ...     'GlobalSkips',
            ...     baca.metronome_mark(baca.Accelerando()),
            ...     baca.text_spanner_staff_padding(4),
            ...     )
            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     )

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['Score'] = [
            ...     abjad.Momento(
            ...         context='GlobalSkips',
            ...         prototype='baca.Accelerando',
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
                            % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \override TextSpanner.staff-padding = #4                                     %! OverrideCommand(1)
                            \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            \baca_lbsd #4 #'(8)                                                          %! IndicatorCommand:BREAK
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca_time_signature_color "blue"                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            \pageBreak                                                                   %! IndicatorCommand:BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                        %@% - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(2)
                        %@% - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(2)
                        %@%     \concat                                                                  %! _attach_metronome_marks(2)
                        %@%         {                                                                    %! _attach_metronome_marks(2)
                        %@%             \large                                                           %! _attach_metronome_marks(2)
                        %@%                 \upright                                                     %! _attach_metronome_marks(2)
                        %@%                     accel.                                                   %! _attach_metronome_marks(2)
                        %@%             \hspace                                                          %! _attach_metronome_marks(2)
                        %@%                 #0.5                                                         %! _attach_metronome_marks(2)
                        %@%         }                                                                    %! _attach_metronome_marks(2)
                        %@%     }                                                                        %! _attach_metronome_marks(2)
                        %@% \startTextSpan                                                               %! _attach_metronome_marks(2)
                            - \abjad_dashed_line_with_arrow                                              %! _attach_metronome_marks(3)
                            - \tweak bound-details.left.text \markup {                                   %! _attach_metronome_marks(3)
                                \concat                                                                  %! _attach_metronome_marks(3)
                                    {                                                                    %! _attach_metronome_marks(3)
                                        \with-color                                                      %! _attach_metronome_marks(3)
                                            #(x11-color 'DeepPink1)                                      %! _attach_metronome_marks(3)
                                            \large                                                       %! _attach_metronome_marks(3)
                                                \upright                                                 %! _attach_metronome_marks(3)
                                                    accel.                                               %! _attach_metronome_marks(3)
                                        \hspace                                                          %! _attach_metronome_marks(3)
                                            #0.5                                                         %! _attach_metronome_marks(3)
                                    }                                                                    %! _attach_metronome_marks(3)
                                }                                                                        %! _attach_metronome_marks(3)
                            \startTextSpan                                                               %! _attach_metronome_marks(3)
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                            \baca_new_spacing_section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING
                            \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \stopTextSpan                                                                %! _attach_metronome_marks(4)
                            \revert TextSpanner.staff-padding                                            %! OverrideCommand(2)
                            \baca_bar_line_visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
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
                                % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        pass
