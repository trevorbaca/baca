r"""
..  container:: example

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
        >>> triple = ('Music_Staff', 'default_clef', abjad.Clef('treble'))
        >>> score_template.defaults.append(triple)
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "treble"                                                           %! DEFAULT_CLEF:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(3)
                            \once \override Staff.Clef.color = #(x11-color 'DarkViolet)              %! DEFAULT_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! DEFAULT_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! DEFAULT_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults(3)
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'violet)                        %! DEFAULT_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

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
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('treble'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "treble"                                                           %! EXPLICIT_CLEF:baca.SegmentMaker._set_status_tag():baca.clef():baca.IndicatorCommand._call()
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):baca.clef():baca.IndicatorCommand._call()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after a previous clef:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 0, (11,)],
        ...         [2, 15, (11,)],
        ...         ),
        ...     )
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('alto'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Clef',
        ...         value='treble',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "alto"                                                             %! EXPLICIT_CLEF:baca.SegmentMaker._set_status_tag():baca.clef():baca.IndicatorCommand._call()
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):baca.clef():baca.IndicatorCommand._call()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

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
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Clef',
        ...         value='treble',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)

        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "treble"                                                           %! REAPPLIED_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3)
                            \once \override Staff.Clef.color = #(x11-color 'green4)                  %! REAPPLIED_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! REAPPLIED_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! REAPPLIED_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._reapply_persistent_indicators(3)
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'OliveDrab)                     %! REAPPLIED_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

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
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "treble"                                                           %! EXPLICIT_CLEF:baca.SegmentMaker._set_status_tag():baca.clef():baca.IndicatorCommand._call()
                            \once \override Staff.Clef.color = #(x11-color 'blue)                    %! EXPLICIT_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! EXPLICIT_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! EXPLICIT_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):baca.clef():baca.IndicatorCommand._call()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! EXPLICIT_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "treble"                                                           %! REDUNDANT_CLEF:baca.SegmentMaker._set_status_tag():baca.clef():baca.IndicatorCommand._call()
                            \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! REDUNDANT_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! REDUNDANT_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! REDUNDANT_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):baca.clef():baca.IndicatorCommand._call()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! REDUNDANT_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 0, (11,)],
        ...         [2, 15, (11,)],
        ...         ),
        ...     )
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('treble'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Clef',
        ...         value='treble',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)

        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "treble"                                                           %! REDUNDANT_CLEF:baca.SegmentMaker._set_status_tag():baca.clef():baca.IndicatorCommand._call()
                            \once \override Staff.Clef.color = #(x11-color 'DeepPink1)               %! REDUNDANT_CLEF_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \override Staff.Clef.color = ##f                                         %! REDUNDANT_CLEF_COLOR_CANCELLATION:baca.SegmentMaker._attach_color_literal(1)
                            \set Staff.forceClef = ##t                                               %! REDUNDANT_CLEF:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(2):baca.clef():baca.IndicatorCommand._call()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
                            \override Staff.Clef.color = #(x11-color 'DeepPink4)                     %! REDUNDANT_CLEF_REDRAW_COLOR:baca.SegmentMaker._attach_color_literal(2)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                             %! DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

    Dynamics.

    ..  container:: example

        Explicit dynamics color blue:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after a previous dynamic:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.dynamic('p'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Voice'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Dynamic',
        ...         value='f',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Reapplied dynamics color green:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Voice'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Dynamic',
        ...         value='f',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'green4)                                      %! REAPPLIED_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! REAPPLIED_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Redundant dynamics color pink:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'DeepPink1)                                   %! REDUNDANT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! REDUNDANT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.dynamic('f'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Voice'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Dynamic',
        ...         value='f',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'DeepPink1)                                   %! REDUNDANT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! REDUNDANT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Sforzando dynamics do not count as redundant:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \sfz                                                                     %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \sfz                                                                     %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.dynamic('sfz'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Voice'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='abjad.Dynamic',
        ...         value='sfz',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \sfz                                                                     %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        REGRESSION. Conventional and effort dynamics analyze
        nonredundantly:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \mf                                                                      %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-mf                                                          %! EXPLICIT_DYNAMIC:baca.SegmentMaker._set_status_tag():baca.dynamic():baca.IndicatorCommand._call()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

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
        >>> triple = ('Music_Staff', 'default_instrument', abjad.Flute())
        >>> score_template.defaults.append(triple)
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     instruments=instruments,
        ...     score_template=score_template,
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-default-indicator-markup "(“Flute”)"                             %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-default-indicator-markup "(“Flute”)"                             %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-default-indicator-markup "(“Flute”)"                             %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Explicit instruments color blue and redraw dull blue:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     instruments=instruments,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                %@% \baca-not-yet-pitched-coloring                                                   %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                %@% \baca-not-yet-pitched-coloring                                                   %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after a previous instrument:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     instruments=instruments,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.instrument(instruments['Flute']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         manifest='instruments',
        ...         value='Piccolo',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Reapplied instruments color green and redraw dull green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     instruments=instruments,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         manifest='instruments',
        ...         value='Flute',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-reapplied-indicator-markup "(“Flute”)"                           %! REAPPLIED_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-reapplied-indicator-markup "(“Flute”)"                           %! REAPPLIED_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                %@% \baca-not-yet-pitched-coloring                                                   %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-reapplied-indicator-markup "(“Flute”)"                           %! REAPPLIED_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                %@% \baca-not-yet-pitched-coloring                                                   %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

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
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     instruments=instruments,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.instrument(instruments['Flute']),
        ...     baca.new(
        ...         baca.instrument(instruments['Flute']),
        ...         map=baca.leaves()[1],
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "(“Flute”)"                           %! REDUNDANT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                        %%% ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                        %%% ^ \baca-redundant-indicator-markup "(“Flute”)"                           %! REDUNDANT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "(“Flute”)"                            %! EXPLICIT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "(“Flute”)"                           %! REDUNDANT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 0, (11,)],
        ...         [2, 15, (11,)],
        ...         ),
        ...     )
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     instruments=instruments,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.instrument(instruments['Flute']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         manifest='instruments',
        ...         value='Flute',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "(“Flute”)"                           %! REDUNDANT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-redundant-indicator-markup "(“Flute”)"                           %! REDUNDANT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "(“Flute”)"                           %! REDUNDANT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

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
        ...     'Music_Staff',
        ...     'default_margin_markup',
        ...     margin_markups['I+II'],
        ...     )
        >>> score_template.defaults.append(triple)
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=score_template,
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \markup { I+II }                                                         %! DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! DEFAULT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-default-indicator-markup "[“I+II”]"                              %! DEFAULT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'violet)              %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \markup { I+II }                                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):abjad.ScoreTemplate.attach_defaults(2):-PARTS
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \markup { I+II }                                                         %! DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(2):-PARTS
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! DEFAULT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-default-indicator-markup "[“I+II”]"                              %! DEFAULT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'violet)              %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \markup { I+II }                                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):abjad.ScoreTemplate.attach_defaults(2):-PARTS
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \markup { I+II }                                                         %! DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)    %! DEFAULT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-default-indicator-markup "[“I+II”]"                              %! DEFAULT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'violet)              %! REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):abjad.ScoreTemplate.attach_defaults(2):-PARTS
                            \markup { I+II }                                                         %! REDRAWN_DEFAULT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):abjad.ScoreTemplate.attach_defaults(2):-PARTS
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Explicit margin markup color blue and redraw dull blue:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after previous margin markup:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.margin_markup(margin_markups['III+IV']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         manifest='margin_markups',
        ...         value='I+II',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { III+IV }                                                       %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“III+IV”]"                           %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { III+IV }                                                       %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-explicit-indicator-markup "[“III+IV”]"                           %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { III+IV }                                                       %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“III+IV”]"                           %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Reapplied margin markup color green and redraw dull green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         manifest='margin_markups',
        ...         value='I+II',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \markup { I+II }                                                         %! REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { I+II }                                                         %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! REAPPLIED_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-reapplied-indicator-markup "[“I+II”]"                            %! REAPPLIED_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \markup { I+II }                                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \markup { I+II }                                                         %! REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { I+II }                                                         %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! REAPPLIED_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-reapplied-indicator-markup "[“I+II”]"                            %! REAPPLIED_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \markup { I+II }                                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \markup { I+II }                                                         %! REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { I+II }                                                         %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \once \override Staff.InstrumentName.color = #(x11-color 'green4)        %! REAPPLIED_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-reapplied-indicator-markup "[“I+II”]"                            %! REAPPLIED_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)           %! REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
                            \markup { I+II }                                                         %! REDRAWN_REAPPLIED_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.SegmentMaker._reapply_persistent_indicators(3):-PARTS
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

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
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.margin_markup(margin_markups['I+II']),
        ...     baca.new(
        ...         baca.margin_markup(margin_markups['I+II']),
        ...         map=baca.leaves()[1],
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "[“I+II”]"                            %! REDUNDANT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                        %%% ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                        %%% ^ \baca-redundant-indicator-markup "[“I+II”]"                            %! REDUNDANT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "[“I+II”]"                            %! REDUNDANT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 0, (11,)],
        ...         [2, 15, (11,)],
        ...         ),
        ...     )
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.margin_markup(margin_markups['I+II']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         manifest='margin_markups',
        ...         value='I+II',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { I+II }                                                         %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "[“I+II”]"                            %! REDUNDANT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> score = lilypond_file[abjad.Score]
        >>> text = format(score, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { I+II }                                                         %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                        %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                        %%% ^ \baca-redundant-indicator-markup "[“I+II”]"                            %! REDUNDANT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        >>> tags_ = abjad.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():baca.IndicatorCommand._call()
                            \set Staff.instrumentName =                                              %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \markup { I+II }                                                         %! baca.SegmentMaker._clone_segment_initial_short_instrument_name()
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)     %! REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            ^ \baca-redundant-indicator-markup "[“I+II”]"                            %! REDUNDANT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)           %! REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_REDUNDANT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                    %@% \baca-not-yet-pitched-coloring                                               %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

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
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.tag(
        ...         abjad.Tag('-PARTS'),
        ...         baca.margin_markup(margin_markups['I+II']),
        ...         ),
        ...     baca.tag(
        ...         abjad.Tag('-PARTS'),
        ...         baca.margin_markup(margin_markups['III+IV']),
        ...         deactivate=True,
        ...         ),
        ...     baca.tag(
        ...         abjad.Tag('-PARTS'),
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(11)                                                         %! BREAK:baca.IndicatorCommand._call()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #15 #'(11)                                                        %! BREAK:baca.IndicatorCommand._call()
                        \break                                                                       %! BREAK:baca.IndicatorCommand._call()
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                        %@% \set Staff.shortInstrumentName =                                         %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                        %@% \markup { III+IV }                                                       %! EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
                            ^ \baca-explicit-indicator-markup "[“I+II”]"                             %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %@% ^ \baca-explicit-indicator-markup "[“III+IV”]"                           %! EXPLICIT_MARGIN_MARKUP_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                            \markup { I+II }                                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                        %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            \set Staff.shortInstrumentName =                                         %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
                            \markup { III+IV }                                                       %! REDRAWN_EXPLICIT_MARGIN_MARKUP:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._treat_persistent_wrapper(3):baca.margin_markup():-PARTS:baca.IndicatorCommand._call()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'2                                                                      %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

    Metronome marks.

    ..  container:: example

        >>> breaks = baca.breaks(baca.page([1, 4, (8,)]))
        >>> metronome_marks = abjad.OrderedDict()
        >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
        >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

    ..  container:: example

        Explicit metronome marks color blue:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 25)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark('112'),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-invisible-line                                                      %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-invisible-line                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after a previous metronome mark:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark('112'),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Score'] = [
        ...     abjad.Momento(
        ...         context='Global_Skips',
        ...         manifest='metronome_marks',
        ...         value='90',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \override TextSpanner.staff-padding = #4                                     %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-invisible-line                                                      %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-invisible-line                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Reapplied metronome marks color green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.text_spanner_staff_padding(4),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Score'] = [
        ...     abjad.Momento(
        ...         context='Global_Skips',
        ...         manifest='metronome_marks',
        ...         value='90',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \override TextSpanner.staff-padding = #4                                     %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-invisible-line                                                      %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "90"                          %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-invisible-line                                                      %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "90" #'green4         %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Redundant metronome marks color pink:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark('112'),
        ...     baca.metronome_mark('112', selector=baca.leaf(1)),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-invisible-line                                                      %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-invisible-line                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \bacaStopTextSpanMM                                                          %! baca.SegmentMaker._attach_metronome_marks(1)
                    %@% - \abjad-invisible-line                                                      %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-invisible-line                                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1     %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark('112'),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Score'] = [
        ...     abjad.Momento(
        ...         context='Global_Skips',
        ...         manifest='metronome_marks',
        ...         value='112',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \override TextSpanner.staff-padding = #4                                     %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-invisible-line                                                      %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-invisible-line                                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1     %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

    Persistent overrides.

    ..  container:: example

        Explicit persistent overrides work but do not color:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> override = abjad.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="bar_line",
        ...     value=(0, 0),
        ... )
        >>> tag = "baca.bar_extent_persistent"
        >>> command = IndicatorCommand(
        ...     indicators=[override], selector=baca.leaf(0), tags=[tag]
        ... )

        >>> maker(
        ...     'Music_Voice',
        ...     command,
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_PERSISTENT_OVERRIDE:baca.SegmentMaker._set_status_tag():baca.bar_extent_persistent:baca.IndicatorCommand._call()
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_BAR_EXTENT:baca.SegmentMaker._set_status_tag():-PARTS:baca.IndicatorCommand._call()
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Persistent overrides also appear in segment metadata:

        >>> abjad.f(maker.persist['persistent_indicators'])
        abjad.OrderedDict(
            [
                (
                    'Music_Staff',
                    [
                        abjad.Momento(
                            context='Music_Voice',
                            edition=abjad.Tag('-PARTS'),
                            prototype='baca.BarExtent',
                            value=1,
                            ),
                        abjad.Momento(
                            context='Music_Voice',
                            prototype='abjad.PersistentOverride',
                            value=abjad.PersistentOverride(
                                attribute='bar_extent',
                                context='Staff',
                                grob='bar_line',
                                value=(0, 0),
                                ),
                            ),
                        abjad.Momento(
                            context='Music_Voice',
                            prototype='baca.StaffLines',
                            value=1,
                            ),
                        ],
                    ),
                (
                    'Score',
                    [
                        abjad.Momento(
                            context='Global_Skips',
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
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Voice'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
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
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! REAPPLIED_PERSISTENT_OVERRIDE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> override = abjad.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="bar_line",
        ...     value=(0, 0),
        ... )
        >>> tag = "baca.bar_extent_persistent"
        >>> command = IndicatorCommand(
        ...     indicators=[override], selector=baca.leaf(0), tags=[tag]
        ... )
        >>> maker(
        ...     'Music_Voice',
        ...     command,
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Voice'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
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
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! REDUNDANT_PERSISTENT_OVERRIDE:baca.SegmentMaker._set_status_tag():baca.bar_extent_persistent:baca.IndicatorCommand._call()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

    Staff lines.

    ..  container:: example

        Explicit staff lines color blue:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)                          %! EXPLICIT_BAR_EXTENT:baca.SegmentMaker._set_status_tag():-PARTS:baca.IndicatorCommand._call()
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.line-count = 5                         %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after previous staff lines:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! EXPLICIT_BAR_EXTENT:baca.SegmentMaker._set_status_tag():-PARTS:baca.IndicatorCommand._call()
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.line-count = 1                         %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Reapplied staff lines color green:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \stopStaff                                                               %! REAPPLIED_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3)
                            \once \override Staff.StaffSymbol.line-count = 5                         %! REAPPLIED_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3)
                            \startStaff                                                              %! REAPPLIED_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(3)
                            \once \override Staff.StaffSymbol.color = #(x11-color 'green4)           %! REAPPLIED_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Redundant staff lines color pink:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
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
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)                          %! EXPLICIT_BAR_EXTENT:baca.SegmentMaker._set_status_tag():-PARTS:baca.IndicatorCommand._call()
                            \stopStaff                                                               %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.line-count = 5                         %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \startStaff                                                              %! EXPLICIT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! EXPLICIT_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)                          %! REDUNDANT_BAR_EXTENT:baca.SegmentMaker._set_status_tag():-PARTS:baca.IndicatorCommand._call()
                            \stopStaff                                                               %! REDUNDANT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.line-count = 5                         %! REDUNDANT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \startStaff                                                              %! REDUNDANT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! REDUNDANT_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.staff_lines(5),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Music_Staff'] = [
        ...     abjad.Momento(
        ...         context='Music_Voice',
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)                          %! EXPLICIT_BAR_EXTENT:baca.SegmentMaker._set_status_tag():-PARTS:baca.IndicatorCommand._call()
                            \stopStaff                                                               %! REDUNDANT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.line-count = 5                         %! REDUNDANT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \startStaff                                                              %! REDUNDANT_STAFF_LINES:baca.SegmentMaker._set_status_tag():baca.staff_lines():baca.IndicatorCommand._call()
                            \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)        %! REDUNDANT_STAFF_LINES_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

..  container:: example

    Tempo trends.

    ..  container:: example

        >>> breaks = baca.breaks(baca.page([1, 4, (8,)]))
        >>> metronome_marks = abjad.OrderedDict()
        >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
        >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

    ..  container:: example

        Explicit tempo trends color blue:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 25)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-dashed-line-with-arrow                                              %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \tweak bound-details.left.text \markup {                                   %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     \concat                                                                  %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \large                                                           %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 \upright                                                     %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                     accel.                                                   %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \hspace                                                          %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 #0.5                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-dashed-line-with-arrow                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \tweak bound-details.left.text \markup {                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            \concat                                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \with-color                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #(x11-color 'blue)                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        \large                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                            \upright                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                                accel.                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #0.5                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #25                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even after a previous tempo trend:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Score'] = [
        ...     abjad.Momento(
        ...         context='Global_Skips',
        ...         prototype='baca.Ritardando',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \override TextSpanner.staff-padding = #4                                     %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-dashed-line-with-arrow                                              %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \tweak bound-details.left.text \markup {                                   %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     \concat                                                                  %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \large                                                           %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 \upright                                                     %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                     accel.                                                   %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \hspace                                                          %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 #0.5                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-dashed-line-with-arrow                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \tweak bound-details.left.text \markup {                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            \concat                                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \with-color                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #(x11-color 'blue)                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        \large                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                            \upright                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                                accel.                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #0.5                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    ..  container:: example

        Reapplied tempo trends color green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.text_spanner_staff_padding(4),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Score'] = [
        ...     abjad.Momento(
        ...         context='Global_Skips',
        ...         prototype='baca.Accelerando',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \override TextSpanner.staff-padding = #4                                     %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-dashed-line-with-arrow                                              %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \tweak bound-details.left.text \markup {                                   %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     \concat                                                                  %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         {                                                                    %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \large                                                           %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 \upright                                                     %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                     accel.                                                   %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \hspace                                                          %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 #0.5                                                         %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         }                                                                    %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     }                                                                        %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! REAPPLIED_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._reapply_persistent_indicators(2):baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-dashed-line-with-arrow                                              %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \tweak bound-details.left.text \markup {                                   %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            \concat                                                                  %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                {                                                                    %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \with-color                                                      %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #(x11-color 'green4)                                         %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        \large                                                       %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                            \upright                                                 %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                                accel.                                               %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \hspace                                                          %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #0.5                                                         %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                }                                                                    %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            }                                                                        %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! REAPPLIED_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            
    ..  container:: example

        Redundant tempo trends color pink:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     baca.metronome_mark(
        ...         baca.Accelerando(),
        ...         selector=baca.leaf(1),
        ...         ),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-dashed-line-with-arrow                                              %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \tweak bound-details.left.text \markup {                                   %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     \concat                                                                  %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \large                                                           %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 \upright                                                     %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                     accel.                                                   %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \hspace                                                          %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 #0.5                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-dashed-line-with-arrow                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \tweak bound-details.left.text \markup {                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            \concat                                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \with-color                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #(x11-color 'blue)                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        \large                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                            \upright                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                                accel.                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #0.5                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \bacaStopTextSpanMM                                                          %! baca.SegmentMaker._attach_metronome_marks(1)
                    %@% - \abjad-dashed-line-with-arrow                                              %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \tweak bound-details.left.text \markup {                                   %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     \concat                                                                  %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         {                                                                    %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \large                                                           %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 \upright                                                     %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                     accel.                                                   %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \hspace                                                          %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 #0.5                                                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         }                                                                    %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     }                                                                        %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-dashed-line-with-arrow                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \tweak bound-details.left.text \markup {                                   %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            \concat                                                                  %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                {                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \with-color                                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #(x11-color 'DeepPink1)                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        \large                                                       %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                            \upright                                                 %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                                accel.                                               %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \hspace                                                          %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #0.5                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                }                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            }                                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 4]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 4]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[abjad.tags.NOT_YET_PITCHED],
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'Global_Skips',
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist['persistent_indicators'] = {}
        >>> persist['persistent_indicators']['Score'] = [
        ...     abjad.Momento(
        ...         context='Global_Skips',
        ...         prototype='baca.Accelerando',
        ...         )
        ...     ]
        >>> metadata['segment_number'] = 1
        >>> lilypond_file = maker.run(
        ...     environment='docs',
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     )
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \override TextSpanner.staff-padding = #4                                     %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #4 #'(8)                                                          %! BREAK:baca.IndicatorCommand._call()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(2)
                        \bar ""                                                                      %! baca.SegmentMaker._make_global_skips(4):+SEGMENT:EMPTY_START_BAR
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:baca.IndicatorCommand._call()
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                    %@% - \abjad-dashed-line-with-arrow                                              %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% - \tweak bound-details.left.text \markup {                                   %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     \concat                                                                  %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         {                                                                    %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \large                                                           %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 \upright                                                     %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                     accel.                                                   %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%             \hspace                                                          %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%                 #0.5                                                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%         }                                                                    %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@%     }                                                                        %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                    %@% \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._attach_metronome_marks(2)
                        - \abjad-dashed-line-with-arrow                                              %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        - \tweak bound-details.left.text \markup {                                   %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            \concat                                                                  %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                {                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \with-color                                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #(x11-color 'DeepPink1)                                      %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        \large                                                       %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                            \upright                                                 %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                                accel.                                               %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                    \hspace                                                          %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                        #0.5                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                                }                                                                    %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                            }                                                                        %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
                        \bacaStartTextSpanMM                                                         %! REDUNDANT_METRONOME_MARK_WITH_COLOR:baca.SegmentMaker._attach_metronome_marks(3)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \noBreak                                                                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):BreakMeasureMap(2):BREAK
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._set_status_tag():baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \bacaStopTextSpanMM                                                          %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):SEGMENT_FINAL_STOP_MM_SPANNER:baca.SegmentMaker._attach_metronome_marks(4)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \baca-not-yet-pitched-coloring                                           %! NOT_YET_PITCHED:baca.SegmentMaker._color_not_yet_pitched()
                            b'4.                                                                     %! baca.make_notes()
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 3]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 3]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):DURATION_MULTIPLIER:baca.SegmentMaker._label_duration_multipliers()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

"""


def persistence():
    """
    Read module-level examples.
    """
    pass
