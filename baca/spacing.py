r"""
Classes and functions for spacing.

..  container:: example

    Example 1. Break measure map basic example:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.StringTrioScoreTemplate(),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
    ...     breaks=baca.breaks(
    ...         baca.page(
    ...             baca.system(measure=1, y_offset=0, distances=(10, 20)),
    ...         ),
    ...     ),
    ... )

    >>> maker(
    ...     "Violin_Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitch("E4"),
    ... )
    >>> lilypond_file = maker.run(environment="docs")
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \autoPageBreaksOff
                    \noBreak
                    \baca-lbsd #0 #'(10 20)
                    \time 4/8
                    \baca-time-signature-color #'blue
                    \pageBreak
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \noBreak
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \noBreak
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \noBreak
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \noBreak
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 6]
                    \noBreak
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context StringSectionStaffGroup = "String_Section_Staff_Group"
                <<
        <BLANKLINE>
                    \tag Violin
                    \context ViolinMusicStaff = "Violin_Music_Staff"
                    {
        <BLANKLINE>
                        \context ViolinMusicVoice = "Violin_Music_Voice"
                        {
        <BLANKLINE>
                            % [Violin_Music_Voice measure 1]
                            \clef "treble"
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                            %@% \override ViolinMusicStaff.Clef.color = ##f
                            \set ViolinMusicStaff.forceClef = ##t
                            e'8
                            ^ \baca-default-indicator-markup "(Violin)"
                            [
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_even_divisions()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
                            ]
        <BLANKLINE>
                            % [Violin_Music_Voice measure 2]
                            e'8
                            [
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
                            ]
        <BLANKLINE>
                            % [Violin_Music_Voice measure 3]
                            e'8
                            [
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
                            ]
        <BLANKLINE>
                            % [Violin_Music_Voice measure 4]
                            e'8
                            [
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
                            ]
        <BLANKLINE>
                            % [Violin_Music_Voice measure 5]
                            e'8
                            [
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
        <BLANKLINE>
                            e'8
                            ]
                            <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                            <<
        <BLANKLINE>
                                \context Voice = "Violin_Music_Voice"
                                {
        <BLANKLINE>
                                    % [Violin_Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                                \context Voice = "Violin_Rest_Voice"
                                {
        <BLANKLINE>
                                    % [Violin_Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                            >>
        <BLANKLINE>
                        }
        <BLANKLINE>
                    }
        <BLANKLINE>
                    \tag Viola
                    \context ViolaMusicStaff = "Viola_Music_Staff"
                    {
        <BLANKLINE>
                        \context ViolaMusicVoice = "Viola_Music_Voice"
                        {
        <BLANKLINE>
                            % [Viola_Music_Voice measure 1]
                            \clef "alto"
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                            %@% \override ViolaMusicStaff.Clef.color = ##f
                            \set ViolaMusicStaff.forceClef = ##t
                            R1 * 4/8
                            ^ \baca-default-indicator-markup "(Viola)"
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)
        <BLANKLINE>
                            % [Viola_Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            % [Viola_Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
        <BLANKLINE>
                            % [Viola_Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            % [Viola_Music_Voice measure 5]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
        <BLANKLINE>
                            <<
        <BLANKLINE>
                                \context Voice = "Viola_Music_Voice"
                                {
        <BLANKLINE>
                                    % [Viola_Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                                \context Voice = "Viola_Rest_Voice"
                                {
        <BLANKLINE>
                                    % [Viola_Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                            >>
        <BLANKLINE>
                        }
        <BLANKLINE>
                    }
        <BLANKLINE>
                    \tag Cello
                    \context CelloMusicStaff = "Cello_Music_Staff"
                    {
        <BLANKLINE>
                        \context CelloMusicVoice = "Cello_Music_Voice"
                        {
        <BLANKLINE>
                            % [Cello_Music_Voice measure 1]
                            \clef "bass"
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet)
                            %@% \override CelloMusicStaff.Clef.color = ##f
                            \set CelloMusicStaff.forceClef = ##t
                            R1 * 4/8
                            ^ \baca-default-indicator-markup "(Cello)"
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)
        <BLANKLINE>
                            % [Cello_Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            % [Cello_Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
        <BLANKLINE>
                            % [Cello_Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
        <BLANKLINE>
                            % [Cello_Music_Voice measure 5]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
        <BLANKLINE>
                            <<
        <BLANKLINE>
                                \context Voice = "Cello_Music_Voice"
                                {
        <BLANKLINE>
                                    % [Cello_Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                                \context Voice = "Cello_Rest_Voice"
                                {
        <BLANKLINE>
                                    % [Cello_Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                                }
        <BLANKLINE>
                            >>
        <BLANKLINE>
                        }
        <BLANKLINE>
                    }
        <BLANKLINE>
                >>
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

..  container:: example

    Example 2. Spacing specifier used as null spacing command:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.SingleStaffScoreTemplate(),
    ...     spacing=baca.SpacingSpecifier(),
    ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> lilypond_file = maker.run(environment="docs")
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \baca-new-spacing-section #1 #8
                    \time 8/16
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \baca-new-spacing-section #1 #8
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \baca-new-spacing-section #1 #8
                    \time 2/4
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \baca-new-spacing-section #1 #8
                    \time 1/2
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \baca-new-spacing-section #1 #4
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context Staff = "Music_Staff"
                {
        <BLANKLINE>
                    \context Voice = "Music_Voice"
                    {
        <BLANKLINE>
                        % [Music_Voice measure 1]
                        e'8
                        [
                        - \abjad-dashed-line-with-hook
                        - \baca-text-spanner-left-text "make_even_divisions()"
                        - \tweak bound-details.right.padding 2.75
                        - \tweak color #darkcyan
                        - \tweak staff-padding 8
                        \bacaStartTextSpanRhythmAnnotation
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 2]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 3]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 4]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
                        <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                        <<
        <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
        <BLANKLINE>
                                % [Music_Voice measure 5]
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                \baca-not-yet-pitched-coloring
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                            \context Voice = "Rest_Voice"
                            {
        <BLANKLINE>
                                % [Rest_Voice measure 5]
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                        >>
        <BLANKLINE>
                    }
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

..  container:: example

    Example 3. Spacing specifier used for measurewise proportional spacing based on
    minimum duration per measure:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.SingleStaffScoreTemplate(),
    ...     spacing=baca.SpacingSpecifier(
    ...         multiplier=abjad.Multiplier(1),
    ...     ),
    ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> lilypond_file = maker.run(environment="docs")
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \baca-new-spacing-section #1 #8
                    \time 8/16
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \baca-new-spacing-section #1 #8
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \baca-new-spacing-section #1 #8
                    \time 2/4
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \baca-new-spacing-section #1 #8
                    \time 1/2
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \baca-new-spacing-section #1 #4
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context Staff = "Music_Staff"
                {
        <BLANKLINE>
                    \context Voice = "Music_Voice"
                    {
        <BLANKLINE>
                        % [Music_Voice measure 1]
                        e'8
                        [
                        - \abjad-dashed-line-with-hook
                        - \baca-text-spanner-left-text "make_even_divisions()"
                        - \tweak bound-details.right.padding 2.75
                        - \tweak color #darkcyan
                        - \tweak staff-padding 8
                        \bacaStartTextSpanRhythmAnnotation
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 2]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 3]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 4]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
                        <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                        <<
        <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
        <BLANKLINE>
                                % [Music_Voice measure 5]
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                \baca-not-yet-pitched-coloring
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                            \context Voice = "Rest_Voice"
                            {
        <BLANKLINE>
                                % [Rest_Voice measure 5]
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                        >>
        <BLANKLINE>
                    }
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

..  container:: example

    Example 4. Spacing specifier used for measurewise proportional spacing based on twice
    the minimum duration per measure:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.SingleStaffScoreTemplate(),
    ...     spacing=baca.SpacingSpecifier(
    ...         multiplier=abjad.Multiplier(2),
    ...     ),
    ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> lilypond_file = maker.run(environment="docs")
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \baca-new-spacing-section #1 #16
                    \time 8/16
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \baca-new-spacing-section #1 #16
                    \time 2/4
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \baca-new-spacing-section #1 #16
                    \time 1/2
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \baca-new-spacing-section #1 #4
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context Staff = "Music_Staff"
                {
        <BLANKLINE>
                    \context Voice = "Music_Voice"
                    {
        <BLANKLINE>
                        % [Music_Voice measure 1]
                        e'8
                        [
                        - \abjad-dashed-line-with-hook
                        - \baca-text-spanner-left-text "make_even_divisions()"
                        - \tweak bound-details.right.padding 2.75
                        - \tweak color #darkcyan
                        - \tweak staff-padding 8
                        \bacaStartTextSpanRhythmAnnotation
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 2]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 3]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 4]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
                        <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                        <<
        <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
        <BLANKLINE>
                                % [Music_Voice measure 5]
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                \baca-not-yet-pitched-coloring
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                            \context Voice = "Rest_Voice"
                            {
        <BLANKLINE>
                                % [Rest_Voice measure 5]
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                        >>
        <BLANKLINE>
                    }
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

..  container:: example

    Example 5. Spacing specifier used for measurewise proportional spacing based on twice
    the minimum duration per measure with minimum duration equal to an eighth note:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.SingleStaffScoreTemplate(),
    ...     spacing=baca.SpacingSpecifier(
    ...         multiplier=abjad.Multiplier(2),
    ...         minimum_duration=abjad.Duration(1, 8),
    ...     ),
    ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitches("E4 F4"),
    ... )

    >>> lilypond_file = maker.run(environment="docs")
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \baca-new-spacing-section #1 #16
                    \time 8/16
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \baca-new-spacing-section #1 #16
                    \time 2/4
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 4]
                    \baca-new-spacing-section #1 #16
                    \time 1/2
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 5]
                    \baca-new-spacing-section #1 #4
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context Staff = "Music_Staff"
                {
        <BLANKLINE>
                    \context Voice = "Music_Voice"
                    {
        <BLANKLINE>
                        % [Music_Voice measure 1]
                        e'8
                        [
                        - \abjad-dashed-line-with-hook
                        - \baca-text-spanner-left-text "make_even_divisions()"
                        - \tweak bound-details.right.padding 2.75
                        - \tweak color #darkcyan
                        - \tweak staff-padding 8
                        \bacaStartTextSpanRhythmAnnotation
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 2]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 3]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
        <BLANKLINE>
                        % [Music_Voice measure 4]
                        e'8
                        [
        <BLANKLINE>
                        f'8
        <BLANKLINE>
                        e'8
        <BLANKLINE>
                        f'8
                        ]
                        <> \bacaStopTextSpanRhythmAnnotation
        <BLANKLINE>
                        <<
        <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
        <BLANKLINE>
                                % [Music_Voice measure 5]
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                \baca-not-yet-pitched-coloring
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                            \context Voice = "Rest_Voice"
                            {
        <BLANKLINE>
                                % [Rest_Voice measure 5]
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                        >>
        <BLANKLINE>
                    }
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

..  container:: example

    Example 6. Spacing specifier works with accelerando and ritardando figures:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.SingleStaffScoreTemplate(),
    ...     spacing=baca.SpacingSpecifier(
    ...         minimum_duration=abjad.Duration(1, 8),
    ...     ),
    ...     time_signatures=[(4, 8), (3, 8)],
    ... )

    >>> maker(
    ...     "Music_Voice",
    ...     baca.pitches("E4 F4"),
    ...     baca.rhythm(
    ...         rmakers.accelerando([(1, 8), (1, 20), (1, 16)]),
    ...         rmakers.feather_beam(),
    ...         rmakers.duration_bracket(),
    ...     ),
    ... )

    >>> lilypond_file = maker.run(environment="docs")
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file[abjad.Score])
        >>> print(string)
        <BLANKLINE>
        \context Score = "Score"
        <<
        <BLANKLINE>
            \context GlobalContext = "Global_Context"
            <<
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"
                {
        <BLANKLINE>
                    % [Global_Skips measure 1]
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    \baca-time-signature-color #'blue
                    s1 * 1/2
        <BLANKLINE>
                    % [Global_Skips measure 2]
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    \baca-time-signature-color #'blue
                    s1 * 3/8
        <BLANKLINE>
                    % [Global_Skips measure 3]
                    \baca-new-spacing-section #1 #4
                    \time 1/4
                    \baca-time-signature-transparent
                    s1 * 1/4
                    \once \override Score.BarLine.transparent = ##t
                    \once \override Score.SpanBar.transparent = ##t
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
            \context MusicContext = "Music_Context"
            <<
        <BLANKLINE>
                \context Staff = "Music_Staff"
                {
        <BLANKLINE>
                    \context Voice = "Music_Voice"
                    {
        <BLANKLINE>
                        \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = 0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = 5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = 4
                                        \override TupletBracket.padding = 1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = 0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'2
                                    }
                                >>
                                \layout {
                                    indent = 0
                                    ragged-right = ##t
                                }
                            }
                        \times 1/1 {
        <BLANKLINE>
                            % [Music_Voice measure 1]
                            \once \override Beam.grow-direction = #right
                            e'16 * 63/32
                            %@% ^ \baca-duration-multiplier-markup #"63" #"32"
                            [
        <BLANKLINE>
                            f'16 * 115/64
                            %@% ^ \baca-duration-multiplier-markup #"115" #"64"
        <BLANKLINE>
                            e'16 * 91/64
                            %@% ^ \baca-duration-multiplier-markup #"91" #"64"
        <BLANKLINE>
                            f'16 * 35/32
                            %@% ^ \baca-duration-multiplier-markup #"35" #"32"
        <BLANKLINE>
                            e'16 * 29/32
                            %@% ^ \baca-duration-multiplier-markup #"29" #"32"
        <BLANKLINE>
                            f'16 * 13/16
                            %@% ^ \baca-duration-multiplier-markup #"13" #"16"
                            ]
        <BLANKLINE>
                        }
                        \revert TupletNumber.text
        <BLANKLINE>
                        \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = 0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = 5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = 4
                                        \override TupletBracket.padding = 1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = 0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'4.
                                    }
                                >>
                                \layout {
                                    indent = 0
                                    ragged-right = ##t
                                }
                            }
                        \times 1/1 {
        <BLANKLINE>
                            % [Music_Voice measure 2]
                            \once \override Beam.grow-direction = #right
                            e'16 * 117/64
                            %@% ^ \baca-duration-multiplier-markup #"117" #"64"
                            [
        <BLANKLINE>
                            f'16 * 99/64
                            %@% ^ \baca-duration-multiplier-markup #"99" #"64"
        <BLANKLINE>
                            e'16 * 69/64
                            %@% ^ \baca-duration-multiplier-markup #"69" #"64"
        <BLANKLINE>
                            f'16 * 13/16
                            %@% ^ \baca-duration-multiplier-markup #"13" #"16"
        <BLANKLINE>
                            e'16 * 47/64
                            %@% ^ \baca-duration-multiplier-markup #"47" #"64"
                            ]
        <BLANKLINE>
                        }
                        \revert TupletNumber.text
        <BLANKLINE>
                        <<
        <BLANKLINE>
                            \context Voice = "Music_Voice"
                            {
        <BLANKLINE>
                                % [Music_Voice measure 3]
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                \baca-not-yet-pitched-coloring
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                            \context Voice = "Rest_Voice"
                            {
        <BLANKLINE>
                                % [Rest_Voice measure 3]
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
        <BLANKLINE>
                            }
        <BLANKLINE>
                        >>
        <BLANKLINE>
                    }
        <BLANKLINE>
                }
        <BLANKLINE>
            >>
        <BLANKLINE>
        >>

    Minimum duration in each measure is taken from the **nonmultiplied**
    duration of each note.

..  container:: example exception

    Exception 1. Spacing specifier override method raises exception when measures is not
    int, pair or list:

    >>> spacing = baca.scorewide_spacing(
    ...     (1, 18, [4, 6]),
    ...     fallback_duration=(1, 20),
    ... )
    >>> spacing.override("all", (1, 16))
    Traceback (most recent call last):
        ...
    TypeError: measures must be int, pair or list (not 'all').

..  container:: example exception

    Exception 2. Breaks factory function raises exception on out-of-sequence page
    specifiers:

    >>> breaks = baca.breaks(
    ...     baca.page(
    ...         baca.system(measure=1, y_offset=20, distances=(15, 20, 20)),
    ...         baca.system(measure=13, y_offset=140, distances=(15, 20, 20)),
    ...         number=1,
    ...     ),
    ...     baca.page(
    ...         baca.system(measure=23, y_offset=20, distances=(15, 20, 20)),
    ...         number=9
    ...     ),
    ... )
    Traceback (most recent call last):
        ...
    Exception: page number (9) is not 2.

..  container:: example exception

    Exception 3. Spacing specifier raises exception when score contains too few measures:

    >>> maker = baca.SegmentMaker(
    ...     score_template=baca.StringTrioScoreTemplate(),
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
    ...     breaks=baca.breaks(
    ...         baca.page(
    ...             baca.system(measure=1, y_offset=0, distances=(10, 20)),
    ...         ),
    ...         baca.page(
    ...             baca.system(measure=11, y_offset=0, distances=(10, 20)),
    ...         ),
    ...     ),
    ... )
    >>> maker(
    ...     "Violin_Music_Voice",
    ...     baca.make_even_divisions(),
    ...     baca.pitch("E4"),
    ... )
    >>> lilypond_file = maker.run(environment="docs")
    Traceback (most recent call last):
        File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/doctest.py", line 1330, in __run
        compileflags, 1), test.globs)
        File "<doctest spacing.py[82]>", line 1, in <module>
        lilypond_file = maker.run(environment="docs")
        File "/Users/trevorbaca/baca/baca/segmentmaker.py", line 7390, in run
        self._apply_breaks()
        File "/Users/trevorbaca/baca/baca/segmentmaker.py", line 999, in _apply_breaks
        self.breaks(self.score['Global_Skips'])
        File "/Users/trevorbaca/baca/baca/spacing.py", line 319, in __call__
        raise Exception(message)
    Exception: score ends at measure 6 (not 11).

..  container:: example exception

    Exception 4. Page specifier factory function raises exception when system specifier
    Y-offsets overlap:

    >>> baca.page(
    ...     baca.system(measure=1, y_offset=60, distances=(20, 20)),
    ...     baca.system(measure=4, y_offset=60, distances=(20, 20)),
    ...     number=1,
    ... )
    Traceback (most recent call last):
        ...
    Exception: systems overlap at Y-offset 60.

"""
import collections
import pathlib

import abjad

from . import classes as _classes
from . import commandclasses as _commandclasses
from . import indicators as _indicators
from . import path as _path
from . import scoping as _scoping
from . import selectors as _selectors
from . import tags as _tags

### CLASSES ###


class BreakMeasureMap:
    """
    Break measure map.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_bol_measure_numbers",
        "_commands",
        "_deactivate",
        "_page_count",
        "_partial_score",
        "_tags",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        commands=None,
        deactivate=False,
        page_count=None,
        partial_score=None,
        tags=None,
    ):
        tags = _scoping.Command._preprocess_tags(tags)
        assert _scoping.Command._validate_tags(tags), repr(tags)
        if _tags.BREAK not in tags:
            tags.append(_tags.BREAK)
        self._tags = tags
        self._bol_measure_numbers = []
        self._deactivate = deactivate
        if page_count is not None:
            assert isinstance(page_count, int), repr(page_count)
        self._page_count = page_count
        if partial_score is not None:
            assert isinstance(partial_score, int), repr(partial_score)
        self._partial_score = partial_score
        if commands is not None:
            commands_ = abjad.OrderedDict()
            for measure_number, list_ in commands.items():
                commands_[measure_number] = []
                for command in list_:
                    command_ = abjad.new(
                        command, deactivate=self.deactivate, tags=self.tags
                    )
                    commands_[measure_number].append(command_)
            commands = commands_
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, context=None):
        """
        Calls break measure map on ``context``.
        """
        if context is None:
            return
        skips = _classes.Selection(context).skips()
        measure_count = self.partial_score or len(skips)
        final_measure_number = self.first_measure_number + measure_count - 1
        literal = abjad.LilyPondLiteral(r"\autoPageBreaksOff", "before")
        abjad.attach(
            literal,
            skips[0],
            deactivate=self.deactivate,
            tag=self.tag.append(abjad.Tag("baca.BreakMeasureMap.__call__(1)")),
        )
        for skip in skips[:measure_count]:
            if not abjad.get.has_indicator(skip, LBSD):
                literal = abjad.LilyPondLiteral(r"\noBreak", "before")
                abjad.attach(
                    literal,
                    skip,
                    deactivate=self.deactivate,
                    tag=self.tag.append(abjad.Tag("baca.BreakMeasureMap.__call__(2)")),
                )
        assert self.commands is not None
        for measure_number, commands in self.commands.items():
            if final_measure_number < measure_number:
                message = f"score ends at measure {final_measure_number}"
                message += f" (not {measure_number})."
                raise Exception(message)
            for command in commands:
                command(context)

    ### PUBLIC PROPERTIES ###

    @property
    def bol_measure_numbers(self):
        """
        Gets beginning-of-line measure numbers.

        Populated during ``baca.breaks()`` initialization.
        """
        return self._bol_measure_numbers

    @property
    def commands(self):
        """
        Gets commands.
        """
        return self._commands

    @property
    def deactivate(self):
        """
        Is true when tags should write deactivated.
        """
        return self._deactivate

    @property
    def first_measure_number(self):
        """
        Gets first measure number.
        """
        return self.bol_measure_numbers[0]

    @property
    def page_count(self):
        """
        Gets page count.
        """
        return self._page_count

    @property
    def partial_score(self):
        """
        Gets number of measures in partial score.

        Set to a positive integer to cap total measures generated.

        Leave set to none to render all measures in score.
        """
        return self._partial_score

    @property
    def tag(self):
        """
        Gets tag.
        """
        if self.tags:
            words = [str(_) for _ in self.tags]
            string = ":".join(words)
            return abjad.Tag(string)
        else:
            return abjad.Tag()

    @property
    def tags(self):
        """
        Gets tags.
        """
        assert _scoping.Command._validate_tags(self._tags), repr(self._tags)
        return self._tags[:]


class SpacingSpecifier:
    """
    Spacing specifier.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_breaks",
        "_fermata_measure_numbers",
        "_fermata_measure_duration",
        "_fermata_start_offsets",
        "_first_measure_number",
        "_measure_count",
        "_measures",
        "_minimum_duration",
        "_multiplier",
        "_overriden_fermata_measures",
        "_phantom",
    )

    _magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        breaks=None,
        fermata_measure_numbers=None,
        fermata_measure_duration=(1, 4),
        first_measure_number=None,
        measure_count=None,
        measures=None,
        minimum_duration=None,
        multiplier=None,
        phantom=False,
    ):
        if breaks is not None:
            assert isinstance(breaks, BreakMeasureMap), repr(breaks)
        self._breaks = breaks
        if fermata_measure_numbers is not None:
            assert isinstance(fermata_measure_numbers, collections.abc.Iterable)
            assert all(isinstance(_, int) for _ in fermata_measure_numbers)
        self._fermata_measure_numbers = fermata_measure_numbers or []
        duration_ = None
        if fermata_measure_duration is not None:
            duration_ = abjad.Duration(fermata_measure_duration)
        self._fermata_measure_duration = duration_
        self._fermata_start_offsets = []
        if first_measure_number is not None:
            assert isinstance(first_measure_number, int)
            assert 1 <= first_measure_number
        self._first_measure_number = first_measure_number
        if measure_count is not None:
            assert isinstance(measure_count, int)
            assert 0 <= measure_count
        self._measure_count = measure_count
        if minimum_duration is not None:
            minimum_duration = abjad.Duration(minimum_duration)
        self._minimum_duration = minimum_duration
        if multiplier is not None:
            multiplier = abjad.Multiplier(multiplier)
        self._multiplier = multiplier
        if measures is not None:
            assert isinstance(measures, abjad.OrderedDict), repr(measures)
        else:
            measures = abjad.OrderedDict()
        self._measures = measures
        self._overriden_fermata_measures = []
        assert isinstance(phantom, bool), repr(phantom)
        self._phantom = phantom

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None):
        """
        Calls spacing specifier on ``segment_maker``.
        """
        score = segment_maker.score
        skips = _classes.Selection(score["Global_Skips"]).skips()
        programmatic = True
        if self.measures and len(self.measures) == len(skips):
            programmatic = False
        if programmatic:
            leaves = abjad.iterate(score).leaves(grace=False)
            method = self._get_minimum_durations_by_measure
            minimum_durations_by_measure = method(skips, leaves)
        else:
            minimum_durations_by_measure = []
        string = "_fermata_start_offsets"
        self._fermata_start_offsets = getattr(segment_maker, string, [])
        first_measure_number = self.first_measure_number or 1
        total = len(skips)
        for measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + measure_index
            duration, eol_adjusted, duration_ = self._calculate_duration(
                measure_index,
                measure_number,
                skip,
                minimum_durations_by_measure,
            )
            if measure_index == total - 1:
                duration = abjad.Duration(1, 4)
            spacing_section = _indicators.SpacingSection(duration=duration)
            tag = _tags.SPACING_COMMAND
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(1)")),
            )
            string_ = self._make_annotation(duration, eol_adjusted, duration_)
            if measure_index < total - 1:
                tag = _tags.SPACING
                string = r"- \baca-start-spm-left-only"
                string += f' "{string_}"'
                start_text_span = abjad.StartTextSpan(
                    command=r"\bacaStartTextSpanSPM", left_text=string
                )
                abjad.attach(
                    start_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(2)")),
                )
            if 0 < measure_index:
                tag = _tags.SPACING
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSPM")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(abjad.Tag("baca.SpacingSpecifier.__call__(3)")),
                )

    ### PRIVATE METHODS ###

    def _calculate_duration(
        self, measure_index, measure_number, skip, minimum_durations_by_measure
    ):
        if (
            self._is_fermata_measure(measure_number, skip)
            and measure_number in self._overriden_fermata_measures
        ):
            duration = self.measures[measure_number]
            duration = abjad.NonreducedFraction(duration)
        elif self.fermata_measure_duration is not None and self._is_fermata_measure(
            measure_number, skip
        ):
            duration = self.fermata_measure_duration
        elif self.measures and measure_number in self.measures:
            duration = self.measures[measure_number]
            duration = abjad.NonreducedFraction(duration)
        else:
            duration = minimum_durations_by_measure[measure_index]
            if self.minimum_duration is not None:
                if self.minimum_duration < duration:
                    duration = self.minimum_duration
            if self.multiplier is not None:
                duration = duration / self.multiplier
        eol_adjusted, duration_ = False, None
        if measure_number in self.eol_measure_numbers:
            duration_ = duration
            duration *= self._magic_lilypond_eol_adjustment
            eol_adjusted = True
        return duration, eol_adjusted, duration_

    def _coerce_measure_number(self, measure_number, force_local=False):
        if measure_number == 0:
            raise Exception("zero-valued measure number not allowed.")
        if force_local is True:
            measure_number = self.first_measure_number + measure_number - 1
        if measure_number < 0:
            measure_number = self.final_measure_number - abs(measure_number) + 1
        if measure_number < self.first_measure_number:
            measure_number += self.first_measure_number - 1
        if self.final_measure_number < measure_number:
            raise Exception(
                f"measure number {measure_number} greater than"
                f" last measure number ({self.final_measure_number})."
            )
        return measure_number

    def _get_minimum_durations_by_measure(self, skips, leaves):
        measure_timespans = []
        durations_by_measure = []
        for skip in skips:
            measure_timespan = abjad.get.timespan(skip)
            measure_timespans.append(measure_timespan)
            durations_by_measure.append([])
        leaf_timespans = set()
        leaf_count = 0
        for leaf in leaves:
            leaf_timespan = abjad.get.timespan(leaf)
            leaf_duration = leaf_timespan.duration
            if leaf.multiplier is not None:
                leaf_duration = leaf_duration / leaf.multiplier
            pair = (leaf_timespan, leaf_duration)
            leaf_timespans.add(pair)
            leaf_count += 1
        measure_index = 0
        measure_timespan = measure_timespans[measure_index]
        leaf_timespans = list(leaf_timespans)
        leaf_timespans.sort(key=lambda _: _[0].start_offset)
        start_offset = 0
        for pair in leaf_timespans:
            leaf_timespan, leaf_duration = pair
            assert start_offset <= leaf_timespan.start_offset
            start_offset = leaf_timespan.start_offset
            if leaf_timespan.starts_during_timespan(measure_timespan):
                durations_by_measure[measure_index].append(leaf_duration)
            else:
                measure_index += 1
                if len(measure_timespans) <= measure_index:
                    continue
                measure_timespan = measure_timespans[measure_index]
                assert leaf_timespan.starts_during_timespan(measure_timespan)
                durations_by_measure[measure_index].append(leaf_duration)
        minimum_durations_by_measure = [min(_) for _ in durations_by_measure]
        return minimum_durations_by_measure

    def _is_fermata_measure(self, measure_number, skip):
        if (
            self.fermata_measure_numbers
            and measure_number in self.fermata_measure_numbers
        ):
            return True
        measure_timespan = abjad.get.timespan(skip)
        return measure_timespan.start_offset in self._fermata_start_offsets

    def _make_annotation(self, duration, eol_adjusted, duration_):
        if eol_adjusted:
            multiplier = self._magic_lilypond_eol_adjustment
            string = f"[[{duration_!s} * {multiplier!s}]]"
        else:
            string = f"[{duration!s}]"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def bol_measure_numbers(self):
        """
        Gets beginning-of-line measure numbers.
        """
        bol_measure_numbers = []
        if self.breaks and self.breaks.bol_measure_numbers:
            first_breaks_measure_number = self.breaks.bol_measure_numbers[0]
            assert isinstance(self.first_measure_number, int)
            for bol_measure_number in self.breaks.bol_measure_numbers:
                offset = bol_measure_number - first_breaks_measure_number
                bol_measure_number = self.first_measure_number + offset
                bol_measure_numbers.append(bol_measure_number)
        return bol_measure_numbers

    @property
    def breaks(self):
        """
        Gets break measure map.
        """
        return self._breaks

    @property
    def eol_measure_numbers(self):
        """
        Gets end-of-line measure numbers.
        """
        eol_measure_numbers = []
        for bol_measure_number in self.bol_measure_numbers[1:]:
            eol_measure_number = bol_measure_number - 1
            eol_measure_numbers.append(eol_measure_number)
        return eol_measure_numbers

    @property
    def fermata_measure_duration(self):
        """
        Gets fermata measure duration.

        Sets fermata measures to exactly this duration when set; ignores minimum duration
        and multiplier.
        """
        return self._fermata_measure_duration

    @property
    def fermata_measure_numbers(self):
        """
        Gets fermata measure numbers.
        """
        return self._fermata_measure_numbers

    @property
    def final_measure_number(self):
        """
        Gets final measure number.

        Gives none when first measure number is not defined.

        Gives none when measure count is not defined.
        """
        if self.first_measure_number is not None and self.measure_count is not None:
            return self.first_measure_number + self.measure_count - 1
        else:
            return None

    @property
    def first_measure_number(self):
        """
        Gets first measure number.
        """
        return self._first_measure_number

    @property
    def magic_lilypond_eol_adjustment(self):
        """
        Gets magic LilyPond EOL adjustment.

        Optically determined to correct LilyPond end-of-line spacing bug.

        Class property.
        """
        return self._magic_lilypond_eol_adjustment

    @property
    def measure_count(self):
        """
        Gets measure count.
        """
        return self._measure_count

    @property
    def measures(self):
        """
        Gets measure overrides.
        """
        return self._measures

    @property
    def minimum_duration(self):
        """
        Gets minimum duration.

        Defaults to none and interprets none equal to ``1/8``.
        """
        return self._minimum_duration

    @property
    def multiplier(self):
        """
        Gets multiplier.
        """
        return self._multiplier

    @property
    def phantom(self):
        """
        Is true when segment concludes with phantom measure.
        """
        return self._phantom

    ### PUBLIC METHODS ###

    def override(
        self,
        measures,
        pair,
        *,
        fermata=False,
        force_local=False,
    ):
        r"""
        Overrides ``measures`` with spacing ``pair``.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         baca.system(measure=1, y_offset=15, distances=(10, 20)),
            ...     ),
            ... )
            >>> spacing = baca.scorewide_spacing(
            ...     (1, 5, []),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ... )

            >>> string = abjad.storage(spacing.measures)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        1,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        2,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        3,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        4,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        5,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    ]
                )

            >>> spacing.override((1, -1), (1, 24))
            >>> string = abjad.storage(spacing.measures)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        1,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        2,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        3,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        4,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        5,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with measure number:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override(1, (1, 24))
            >>> string = abjad.storage(spacing.measures)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        1,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        2,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        3,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        4,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        5,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    ]
                )

            Works with range of measure numbers:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override((1, 3), (1, 24))
            >>> string = abjad.storage(spacing.measures)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        1,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        2,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        3,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        4,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        5,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    ]
                )

            Works with list of measure numbers:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override([1, 3, 5], (1, 24))
            >>> string = abjad.storage(spacing.measures)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        1,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        2,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        3,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        4,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        5,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with negative indices:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override([-3, -1], (1, 24))
            >>> string = abjad.storage(spacing.measures)
            >>> print(string)
            abjad.OrderedDict(
                [
                    (
                        1,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        2,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        3,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        4,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        5,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

        """
        measures_ = []
        duration = abjad.NonreducedFraction(pair)
        if isinstance(measures, int):
            number = self._coerce_measure_number(measures, force_local=force_local)
            self.measures[number] = duration
            measures_.append(number)
        elif isinstance(measures, tuple):
            assert len(measures) == 2, repr(measures)
            start_measure, stop_measure = measures
            start_measure = self._coerce_measure_number(
                start_measure, force_local=force_local
            )
            stop_measure = self._coerce_measure_number(
                stop_measure, force_local=force_local
            )
            for number in range(start_measure, stop_measure + 1):
                self.measures[number] = duration
                measures_.append(number)
        elif isinstance(measures, list):
            for measure in measures:
                number = self._coerce_measure_number(measure, force_local=force_local)
                self.measures[number] = duration
                measures_.append(number)
        else:
            raise TypeError(f"measures must be int, pair or list (not {measures!r}).")
        if fermata:
            self._overriden_fermata_measures.extend(measures_)


class LBSD:
    """
    Line-break system details.
    """

    ### CLASS VARIABLES ###

    _override = r"\overrideProperty"
    _override += " Score.NonMusicalPaperColumn.line-break-system-details"

    ### INITIALIZER ###

    def __init__(self, *, y_offset=None, alignment_distances=None):
        self.y_offset = y_offset
        if alignment_distances is not None:
            assert isinstance(alignment_distances, collections.abc.Iterable)
            alignment_distances = tuple(alignment_distances)
        self.alignment_distances = alignment_distances

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        alignment_distances = " ".join(str(_) for _ in self.alignment_distances)
        string = rf"\baca-lbsd #{self.y_offset} #'({alignment_distances})"
        bundle.before.commands.append(string)
        return bundle


class PageSpecifier:
    """
    Page specifier.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        number=None,
        systems=None,
    ):
        if number is not None:
            assert isinstance(number, int), repr(number)
            assert 1 <= number, repr(number)
        self.number = number
        if systems is not None:
            y_offsets: list = []
            for system in systems:
                if isinstance(system, SystemSpecifier):
                    y_offset = system.y_offset
                elif isinstance(system, list):
                    y_offset = system[1]
                if y_offset in y_offsets:
                    raise Exception(f"systems overlap at Y-offset {y_offset}.")
                else:
                    y_offsets.append(y_offset)
        self.systems = systems


class SystemSpecifier:
    """
    System specifier.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        measure,
        y_offset,
        distances,
    ):
        assert isinstance(measure, int), repr(measure)
        self.measure = measure
        assert isinstance(y_offset, (int, float)), repr(y_offset)
        self.y_offset = y_offset
        assert isinstance(distances, collections.abc.Iterable), repr(distances)
        for distance in distances:
            assert isinstance(distance, (int, float)), repr(distance)
        distances = list(distances)
        self.distances = distances


### FUNCTIONS ###


def breaks(
    *page_specifiers,
    partial_score=None,
):
    r"""
    Makes break measure map.

    Set ``partial_score`` when rendering only the first measures of a score; leave
    ``partial_score`` set to none when rendering a complete score.
    """
    commands = abjad.OrderedDict()
    page_count = len(page_specifiers)
    if not page_specifiers:
        return BreakMeasureMap(
            commands=commands, page_count=0, partial_score=partial_score
        )
    first_system = page_specifiers[0].systems[0]
    assert isinstance(first_system, SystemSpecifier), repr(first_system)
    first_measure_number = first_system.measure
    assert first_measure_number == 1, repr(first_measure_number)
    bol_measure_numbers = []
    for i, page_specifier in enumerate(page_specifiers):
        page_number = i + 1
        if page_specifier.number is not None:
            if page_specifier.number != page_number:
                message = f"page number ({page_specifier.number})"
                message += f" is not {page_number}."
                raise Exception(message)
        for j, system in enumerate(page_specifier.systems):
            if hasattr(system, "measure"):
                measure_number = system.measure
            else:
                measure_number = system[0]
            bol_measure_numbers.append(measure_number)
            skip_index = measure_number - first_measure_number
            if hasattr(system, "y_offset"):
                y_offset = system.y_offset
            else:
                y_offset = system[1]
            if hasattr(system, "distances"):
                alignment_distances = system.distances
            else:
                alignment_distances = system[2]
            assert 0 <= skip_index
            selector = _selectors.skip(skip_index)
            if j == 0:
                break_ = abjad.LilyPondLiteral(r"\pageBreak")
            else:
                break_ = abjad.LilyPondLiteral(r"\break")
            command = _commandclasses.IndicatorCommand(
                indicators=[break_], selector=selector
            )
            alignment_distances = _classes.Sequence(alignment_distances)
            alignment_distances = alignment_distances.flatten()
            lbsd = LBSD(alignment_distances=alignment_distances, y_offset=y_offset)
            lbsd_command = _commandclasses.IndicatorCommand(
                indicators=[lbsd], selector=selector
            )
            commands[measure_number] = [command, lbsd_command]
    breaks = BreakMeasureMap(
        commands=commands,
        page_count=page_count,
        partial_score=partial_score,
    )
    breaks._bol_measure_numbers.extend(bol_measure_numbers)
    return breaks


def minimum_duration(duration):
    """
    Makes spacing specifier with ``duration`` minimum width.
    """
    return SpacingSpecifier(minimum_duration=duration)


def page(*systems, number=None):
    """
    Makes page specifier.
    """
    systems_ = []
    for system in systems:
        assert isinstance(system, SystemSpecifier), repr(system)
        systems_.append(system)
    return PageSpecifier(number=number, systems=systems_)


def scorewide_spacing(
    path,
    *,
    fallback_duration,
    breaks=None,
    fermata_measure_duration=(1, 4),
):
    r"""
    Makes scorewide spacing.

    Uses ``path`` for first measure number, measure count, and fermata measure numbers
    metadata; triple may be passed directly for tests.

    Uses ``fallback_duration`` spacing for measures without override.

    Uses ``breaks`` measure map for beginning-of-line and end-of-line measure numbers.

    Uses ``fermata_measure_duration`` spacing for measures found in fermata measure
    numbers path metadata.

    ..  container:: example

        >>> spacing = baca.scorewide_spacing(
        ...     (1, 18, [4, 6]),
        ...     breaks=baca.breaks(
        ...         baca.page(
        ...             baca.system(measure=1, y_offset=15, distances=(10, 20)),
        ...             baca.system(measure=9, y_offset=115, distances=(10, 20)),
        ...         ),
        ...     ),
        ...     fallback_duration=(1, 20),
        ... )

        >>> spacing.bol_measure_numbers
        [1, 9]

        >>> spacing.eol_measure_numbers
        [8]

        >>> spacing.fermata_measure_numbers
        [4, 6]

        >>> spacing.first_measure_number
        1

        >>> spacing.final_measure_number
        18

        >>> spacing.measure_count
        18

        >>> len(spacing.measures)
        18

    """
    if isinstance(path, tuple):
        assert len(path) == 3, repr(path)
        first_measure_number, measure_count, fermata_measure_numbers = path
    else:
        path = pathlib.Path(path)
        tuple_ = _path.get_measure_profile_metadata(path)
        first_measure_number = tuple_[0]
        measure_count = tuple_[1]
        fermata_measure_numbers = tuple_[2] or []
        first_measure_number = first_measure_number or 1
        fermata_measure_numbers = [
            _ - (first_measure_number - 1) for _ in fermata_measure_numbers
        ]
    first_measure_number = 1
    fallback_fraction = abjad.NonreducedFraction(fallback_duration)
    measures = abjad.OrderedDict()
    final_measure_number = first_measure_number + measure_count - 1
    for n in range(first_measure_number, final_measure_number + 1):
        measures[n] = fallback_fraction
    specifier = SpacingSpecifier(
        breaks=breaks,
        fermata_measure_duration=fermata_measure_duration,
        fermata_measure_numbers=fermata_measure_numbers,
        first_measure_number=first_measure_number,
        measure_count=measure_count,
        measures=measures,
    )
    return specifier


def system(*, measure, y_offset, distances):
    """
    Makes system specifier.
    """
    distances = _classes.Sequence(distances).flatten(depth=-1)
    return SystemSpecifier(measure=measure, y_offset=y_offset, distances=distances)
