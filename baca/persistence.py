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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \clef "treble"
                            \once \override Staff.Clef.color = #(x11-color 'DarkViolet)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'violet)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \clef "treble"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \clef "alto"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \clef "treble"
                            \once \override Staff.Clef.color = #(x11-color 'green4)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'OliveDrab)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \clef "treble"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \clef "treble"
                            \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'DeepPink4)
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \clef "treble"
                            \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \override Staff.Clef.color = #(x11-color 'DeepPink4)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
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

..  container:: example

    Dynamics.

    ..  container:: example

        Explicit dynamics color blue:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \f
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even after a previous dynamic:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \p
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Reapplied dynamics color green:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'green4)
                            \f
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Redundant dynamics color pink:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \f
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'DeepPink1)
                            \f
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'DeepPink1)
                            \f
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Sforzando dynamics do not count as redundant:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \sfz
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \sfz
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \sfz
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        REGRESSION. Conventional and effort dynamics analyze
        nonredundantly:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \mf
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \tweak color #(x11-color 'blue)
                            \baca-effort-mf
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-default-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> # lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-default-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-default-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Explicit instruments color blue and redraw dull blue:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even after a previous instrument:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Reapplied instruments color green and redraw dull green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-reapplied-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-reapplied-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-reapplied-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...         map=baca.selectors.leaves((1, 2)),
        ...         ),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            ^ \baca-redundant-indicator-markup "(“Flute”)"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            ^ \baca-redundant-indicator-markup "(“Flute”)"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            ^ \baca-explicit-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            ^ \baca-redundant-indicator-markup "(“Flute”)"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 0, (11,)],
        ...         [2, 15, (11,)],
        ...         ),
        ...     )
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-redundant-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-redundant-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            ^ \baca-redundant-indicator-markup "(“Flute”)"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)
                            b'4.
                            ^ \baca-default-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'violet)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)
                            b'4.
                            ^ \baca-default-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'violet)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)
                            b'4.
                            ^ \baca-default-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'violet)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Explicit margin markup color blue and redraw dull blue:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'4.
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'4.
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'4.
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even after previous margin markup:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
                            \set Staff.instrumentName =
                            \markup { III+IV }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'4.
                            ^ \baca-explicit-indicator-markup "[“III+IV”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
                            \set Staff.instrumentName =
                            \markup { III+IV }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'4.
                            ^ \baca-explicit-indicator-markup "[“III+IV”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
                            \set Staff.instrumentName =
                            \markup { III+IV }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'4.
                            ^ \baca-explicit-indicator-markup "[“III+IV”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Reapplied margin markup color green and redraw dull green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            \set Staff.instrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                            b'4.
                            ^ \baca-reapplied-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            \set Staff.instrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                            b'4.
                            ^ \baca-reapplied-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            \set Staff.instrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                            b'4.
                            ^ \baca-reapplied-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...         map=baca.selectors.leaves((1, 2)),
        ...         ),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'2
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                            b'2
                            ^ \baca-redundant-indicator-markup "[“I+II”]"
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'2
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                            b'2
                            ^ \baca-redundant-indicator-markup "[“I+II”]"
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'2
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                            b'2
                            ^ \baca-redundant-indicator-markup "[“I+II”]"
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 0, (11,)],
        ...         [2, 15, (11,)],
        ...         ),
        ...     )
        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            \set Staff.instrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                            b'4.
                            ^ \baca-redundant-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> score = lilypond_file[abjad.Score]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            \set Staff.instrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                            b'4.
                            ^ \baca-redundant-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        >>> tags_ = ide.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            \set Staff.instrumentName =
                            \markup { I+II }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                            b'4.
                            ^ \baca-redundant-indicator-markup "[“I+II”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
        ...     margin_markups=margin_markups,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> maker(
        ...     'Music_Voice',
        ...     baca.tag(
        ...         ide.tags.NOT_PARTS,
        ...         baca.margin_markup(margin_markups['I+II']),
        ...         ),
        ...     baca.tag(
        ...         ide.tags.NOT_PARTS,
        ...         baca.margin_markup(margin_markups['III+IV']),
        ...         deactivate=True,
        ...         ),
        ...     baca.tag(
        ...         ide.tags.NOT_PARTS,
        ...         baca.margin_markup(margin_markups['III+IV']),
        ...         deactivate=True,
        ...         ),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> block = abjad.Block(name='layout')
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
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
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \set Staff.shortInstrumentName =
                            %@% \markup { III+IV }
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            b'2
                            ^ \baca-explicit-indicator-markup "[“I+II”]"
                            %@% ^ \baca-explicit-indicator-markup "[“III+IV”]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { I+II }
                            %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { III+IV }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'2
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #25
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even after a previous metronome mark:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \override TextSpanner.staff-padding = 4
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Reapplied metronome marks color green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \override TextSpanner.staff-padding = 4
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "90"
                        %@% \bacaStartTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "90" #'green4
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Redundant metronome marks color pink:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \override TextSpanner.staff-padding = 4
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

..  container:: example

    Persistent overrides.

    ..  container:: example

        Explicit persistent overrides work but do not color:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> override = ide.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> tag = "baca.bar_extent_persistent"
        >>> command = baca.IndicatorCommand(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 1
                            \startStaff
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
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

        Persistent overrides also appear in segment metadata:

        >>> string = abjad.storage(maker.persist['persistent_indicators'])
        >>> print(string)
        abjad.OrderedDict(
            [
                (
                    'Music_Staff',
                    [
                        ide.Momento(
                            context='Music_Voice',
                            edition=abjad.Tag('-PARTS'),
                            prototype='baca.BarExtent',
                            value=1,
                            ),
                        ide.Momento(
                            context='Music_Voice',
                            prototype='baca.StaffLines',
                            value=1,
                            ),
                        ide.Momento(
                            context='Music_Voice',
                            prototype='ide.PersistentOverride',
                            value=ide.PersistentOverride(
                                attribute='bar_extent',
                                context='Staff',
                                grob='BarLine',
                                value="#'(0 . 0)",
                                ),
                            ),
                        ],
                    ),
                (
                    'Score',
                    [
                        ide.Momento(
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
        ...     ide.Momento(
        ...         context='Music_Voice',
        ...         prototype='ide.PersistentOverride',
        ...         value=ide.PersistentOverride(
        ...             after=True,
        ...             attribute='bar_extent',
        ...             context='Staff',
        ...             grob='BarLine',
        ...             value="#'(0 . 0)",
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
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

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 24)),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> override = ide.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> tag = "baca.bar_extent_persistent"
        >>> command = baca.IndicatorCommand(
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
        ...     ide.Momento(
        ...         context='Music_Voice',
        ...         prototype='ide.PersistentOverride',
        ...         value=ide.PersistentOverride(
        ...             after=True,
        ...             attribute='bar_extent',
        ...             context='Staff',
        ...             grob='BarLine',
        ...             value="#'(0 . 0)",
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
                            \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
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

..  container:: example

    Staff lines.

    ..  container:: example

        Explicit staff lines color blue:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 5
                            \startStaff
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even after previous staff lines:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 1
                            \startStaff
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Reapplied staff lines color green:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 5
                            \startStaff
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.StaffSymbol.color = #(x11-color 'green4)
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Redundant staff lines color pink:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 5
                            \startStaff
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 5
                            \startStaff
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
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
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(-2 . 2)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 5
                            \startStaff
                            %@% \baca-not-yet-pitched-coloring
                            \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #25
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large
                        %@%     \upright
                        %@%         accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large
                            \upright
                                accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

        Even after a previous tempo trend:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \override TextSpanner.staff-padding = 4
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large
                        %@%     \upright
                        %@%         accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large
                            \upright
                                accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Reapplied tempo trends color green:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \override TextSpanner.staff-padding = 4
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large
                        %@%     \upright
                        %@%         accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'green4) \large
                            \upright
                                accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

    ..  container:: example

        Redundant tempo trends color pink:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large
                        %@%     \upright
                        %@%         accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large
                            \upright
                                accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large
                        %@%     \upright
                        %@%         accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'DeepPink1) \large
                            \upright
                                accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 4]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 4]
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

        Even at the beginning of a segment:

        >>> maker = baca.SegmentMaker(
        ...     breaks=breaks,
        ...     deactivate=[ide.tags.NOT_YET_PITCHED_COLORING],
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
        ...     ide.Momento(
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
                        \baca-new-spacing-section #1 #24
                        \override TextSpanner.staff-padding = 4
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #4 #'(8)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large
                        %@%     \upright
                        %@%         accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'DeepPink1) \large
                            \upright
                                accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
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
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            %@% \baca-not-yet-pitched-coloring
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 3]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
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

"""


def persistence():
    """
    Read module-level examples.
    """
    pass
