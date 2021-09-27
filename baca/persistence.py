r"""
..  container:: example

    Clefs.

    ..  container:: example

        Default clefs color purple and redraw dull purple:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     indicator_defaults=[
        ...         ("Music_Staff", "default_clef", abjad.Clef("treble"))
        ...     ],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'DarkViolet)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'violet)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    ..  container:: example

        Explicit clefs color blue and redraw dull blue:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.clef("treble"),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'blue)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

        Even after a previous clef:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.clef("alto"),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \clef "alto"
                        \once \override Staff.Clef.color = #(x11-color 'blue)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    ..  container:: example

        Reapplied clefs color green and redraw dull green:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'green4)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'OliveDrab)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    ..  container:: example

        Redundant clefs color pink and redraw dull pink:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=3, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
        ... )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.clef("treble", selector=baca.selectors.leaf(0)),
        ...     baca.clef("treble", selector=baca.selectors.leaf(1)),
        ... )
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'blue)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'DeepPink4)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.clef("treble"),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                        %@% \override Staff.Clef.color = ##f
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \override Staff.Clef.color = #(x11-color 'DeepPink4)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

..  container:: example

    Dynamics.

    ..  container:: example

        Explicit dynamics color blue:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.dynamic('f'),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \f
                        b'4.
                    }
                >>
            }

        Even after a previous dynamic:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.dynamic('p'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Voice"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='abjad.Dynamic',
        ...         value='f',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \p
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied dynamics color green:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Voice"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='abjad.Dynamic',
        ...         value='f',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'green4)
                        \f
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Redundant dynamics color pink:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.dynamic('f'),
        ...     baca.dynamic('f', selector=baca.selectors.leaf(1)),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \f
                        b'4.
                        - \tweak color #(x11-color 'DeepPink1)
                        \f
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.dynamic('f'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Voice"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='abjad.Dynamic',
        ...         value='f',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'DeepPink1)
                        \f
                        b'4.
                    }
                >>
            }

        Sforzando dynamics do not count as redundant:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.dynamic('sfz'),
        ...     baca.dynamic('sfz', selector=baca.selectors.leaf(1)),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.dynamic('sfz'),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Voice"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='abjad.Dynamic',
        ...         value='sfz',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                        b'4.
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Conventional and effort dynamics analyze nonredundantly:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.dynamic('mf'),
        ...     baca.dynamic('"mf"', selector=baca.selectors.leaf(1)),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \mf
                        b'4.
                        - \tweak color #(x11-color 'blue)
                        \baca-effort-mf
                    }
                >>
            }

..  container:: example

    Instruments.

    ..  container:: example

        Example instruments:

        >>> instruments = {}
        >>> instruments['Flute'] = abjad.Flute()
        >>> instruments['Piccolo'] = abjad.Piccolo()
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )

    ..  container:: example

        Default instruments color purple and redraw dull purple:

        >>> score_template = baca.make_empty_score_maker(1)
        >>> triple = ("Music_Staff", 'default_instrument', abjad.Flute())
        >>> commands = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     score_template=score_template,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ... )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     instruments=commands.instruments,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     indicator_defaults=[triple],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-default-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> # lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-default-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-default-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Explicit instruments color blue and redraw dull blue:

        >>> commands = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.instrument(instruments['Flute']),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     instruments=commands.instruments,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        Even after a previous instrument:

        >>> commands = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.instrument(instruments['Flute']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         manifest='instruments',
        ...         value='Piccolo',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     instruments=commands.instruments,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied instruments color green and redraw dull green:

        >>> commands = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         manifest='instruments',
        ...         value='Flute',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     instruments=commands.instruments,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-reapplied-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-reapplied-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-reapplied-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Redundant instruments color pink and redraw dull pink:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=3, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.instrument(instruments['Flute']),
        ...     baca.new(
        ...         baca.instrument(instruments['Flute']),
        ...         map=baca.selectors.leaves((1, 2)),
        ...         ),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     instruments=commands.instruments,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'2
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'2
                        ^ \baca-redundant-indicator-markup "(“Flute”)"
                        b'2
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'2
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'2
                        ^ \baca-redundant-indicator-markup "(“Flute”)"
                        b'2
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'2
                        ^ \baca-explicit-indicator-markup "(“Flute”)"
                        b'2
                        ^ \baca-redundant-indicator-markup "(“Flute”)"
                        b'2
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.instrument(instruments['Flute']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         manifest='instruments',
        ...         value='Flute',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     instruments=commands.instruments,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-redundant-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-redundant-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        ^ \baca-redundant-indicator-markup "(“Flute”)"
                        b'4.
                    }
                >>
            }

..  container:: example

    Margin markups.

    ..  container:: example

        Margin markup for examples:

        >>> margin_markups = {}
        >>> margin_markups['I+II'] = abjad.MarginMarkup(
        ...     markup=abjad.Markup('I+II'),
        ...     )
        >>> margin_markups['III+IV'] = abjad.MarginMarkup(
        ...     markup=abjad.Markup('III+IV'),
        ...     )
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )

    ..  container:: example

        Default margin markup color purple and redraw dull purple:

        >>> score_template = baca.make_empty_score_maker(1)
        >>> triple = (
        ...     "Music_Staff",
        ...     'default_margin_markup',
        ...     margin_markups['I+II'],
        ...     )
        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=score_template,
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     indicator_defaults=[triple],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)
                        b'4.
                        ^ \baca-default-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'violet)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)
                        b'4.
                        ^ \baca-default-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'violet)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet)
                        b'4.
                        ^ \baca-default-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'violet)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Explicit margin markup color blue and redraw dull blue:

        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.margin_markup(margin_markups['I+II']),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'4.
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'4.
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'4.
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        Even after previous margin markup:

        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.margin_markup(margin_markups['III+IV']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         manifest='margin_markups',
        ...         value='I+II',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        \set Staff.instrumentName =
                        \markup { III+IV }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'4.
                        ^ \baca-explicit-indicator-markup "[“III+IV”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        \set Staff.instrumentName =
                        \markup { III+IV }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'4.
                        ^ \baca-explicit-indicator-markup "[“III+IV”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        \set Staff.instrumentName =
                        \markup { III+IV }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'4.
                        ^ \baca-explicit-indicator-markup "[“III+IV”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied margin markup color green and redraw dull green:

        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         manifest='margin_markups',
        ...         value='I+II',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.instrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        b'4.
                        ^ \baca-reapplied-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.instrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        b'4.
                        ^ \baca-reapplied-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.instrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        b'4.
                        ^ \baca-reapplied-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Redundant margin markup color pink and redraw dull pink:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=3, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.margin_markup(margin_markups['I+II']),
        ...     baca.new(
        ...         baca.margin_markup(margin_markups['I+II']),
        ...         map=baca.selectors.leaves((1, 2)),
        ...         ),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'2
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        b'2
                        ^ \baca-redundant-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'2
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'2
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        b'2
                        ^ \baca-redundant-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'2
                    }
                >>
            }

        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'2
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        b'2
                        ^ \baca-redundant-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'2
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.margin_markup(margin_markups['I+II']),
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         manifest='margin_markups',
        ...         value='I+II',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.instrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        b'4.
                        ^ \baca-redundant-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.lilypondformat.left_shift_tags(text)
        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.lilypondformat.left_shift_tags(text, 89)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.instrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        b'4.
                        ^ \baca-redundant-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.margin_markup_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file.score_block.items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        \set Staff.instrumentName =
                        \markup { I+II }
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        b'4.
                        ^ \baca-redundant-indicator-markup "[“I+II”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Multiple margin markup are allowed so long as only one is active:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> commands = baca.CommandAccumulator(
        ...     margin_markups=margin_markups,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.tag(
        ...         baca.tags.NOT_PARTS,
        ...         baca.margin_markup(margin_markups['I+II']),
        ...         ),
        ...     baca.tag(
        ...         baca.tags.NOT_PARTS,
        ...         baca.margin_markup(margin_markups['III+IV']),
        ...         deactivate=True,
        ...         ),
        ...     baca.tag(
        ...         baca.tags.NOT_PARTS,
        ...         baca.margin_markup(margin_markups['III+IV']),
        ...         deactivate=True,
        ...         ),
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     margin_markups=commands.margin_markups,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \autoPageBreaksOff
                        \noBreak
                        \baca-lbsd #0 #'(11)
                        \time 4/8
                        \baca-time-signature-color #'blue
                        \pageBreak
                        s1 * 1/2
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-lbsd #15 #'(11)
                        \break
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        s1 * 1/2
                    }
                    \context Voice = "Music_Voice"
                    {
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        %@% \set Staff.shortInstrumentName =
                        %@% \markup { III+IV }
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        b'2
                        ^ \baca-explicit-indicator-markup "[“I+II”]"
                        %@% ^ \baca-explicit-indicator-markup "[“III+IV”]"
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { I+II }
                        %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName =
                        \markup { III+IV }
                        b'2
                        b'2
                    }
                >>
            }

..  container:: example

    Metronome marks.

    ..  container:: example

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=4, distances=(8,)),
        ...     ),
        ... )
        >>> metronome_marks = {}
        >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
        >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

    ..  container:: example

        Explicit metronome marks color blue:

        >>> commands = baca.CommandAccumulator(
        ...     append_phantom_measure=True,
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark('112'),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     append_phantom_measure=commands.append_phantom_measure,
        ...     metronome_marks=commands.metronome_marks,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 25),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                        <<
                            \context Voice = "Music_Voice"
                            {
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                            \context Voice = "Rest_Voice"
                            {
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                        >>
                    }
                >>
            }

        Even after a previous metronome mark:

        >>> commands = baca.CommandAccumulator(
        ...     append_phantom_measure=True,
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark('112'),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Global_Skips",
        ...         manifest='metronome_marks',
        ...         value='90',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     append_phantom_measure=commands.append_phantom_measure,
        ...     metronome_marks=commands.metronome_marks,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                        <<
                            \context Voice = "Music_Voice"
                            {
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                            \context Voice = "Rest_Voice"
                            {
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                        >>
                    }
                >>
            }

    ..  container:: example

        Reapplied metronome marks color green:

        >>> commands = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.text_spanner_staff_padding(4),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Global_Skips",
        ...         manifest='metronome_marks',
        ...         value='90',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     metronome_marks=commands.metronome_marks,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Redundant metronome marks color pink:

        >>> commands = baca.CommandAccumulator(
        ...     append_phantom_measure=True,
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark('112'),
        ...     baca.metronome_mark('112', selector=baca.selectors.leaf(1)),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     append_phantom_measure=commands.append_phantom_measure,
        ...     metronome_marks=commands.metronome_marks,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                        <<
                            \context Voice = "Music_Voice"
                            {
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                            \context Voice = "Rest_Voice"
                            {
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                        >>
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> commands = baca.CommandAccumulator(
        ...     append_phantom_measure=True,
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark('112'),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Global_Skips",
        ...         manifest='metronome_marks',
        ...         value='112',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     append_phantom_measure=commands.append_phantom_measure,
        ...     metronome_marks=commands.metronome_marks,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                        <<
                            \context Voice = "Music_Voice"
                            {
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                            \context Voice = "Rest_Voice"
                            {
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                        >>
                    }
                >>
            }

..  container:: example

    Persistent overrides.

    ..  container:: example

        Explicit persistent overrides work but do not color:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> tag = "baca.bar_extent_persistent"
        >>> command = baca.IndicatorCommand(
        ...     indicators=[override], selector=baca.selectors.leaf(0), tags=[tag]
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     command,
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_position(0),
        ...     )

        >>> lilypond_file, metadata, persist = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     return_metadata=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        b'4.
                        b'4.
                    }
                >>
            }

        Persistent overrides also appear in segment metadata:

        >>> dictionary = persist["persistent_indicators"]
        >>> string = abjad.storage(dictionary)
        >>> print(string)
        dict(
            {
                'Music_Staff': [
                    baca.Memento(
                        context='Music_Voice',
                        edition=abjad.Tag('-PARTS'),
                        prototype='baca.BarExtent',
                        value=1,
                        ),
                    baca.Memento(
                        context='Music_Voice',
                        prototype='baca.PersistentOverride',
                        value=baca.PersistentOverride(
                            attribute='bar_extent',
                            context='Staff',
                            grob='BarLine',
                            value="#'(0 . 0)",
                            ),
                        ),
                    baca.Memento(
                        context='Music_Voice',
                        prototype='baca.StaffLines',
                        value=1,
                        ),
                    ],
                'Score': [
                    baca.Memento(
                        context='Global_Skips',
                        prototype='abjad.TimeSignature',
                        value='3/8',
                        ),
                    ],
                }
            )

    ..  container:: example

        Reapplied persistent overrides work but do not color:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Voice"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='baca.PersistentOverride',
        ...         value=baca.PersistentOverride(
        ...             after=True,
        ...             attribute='bar_extent',
        ...             context='Staff',
        ...             grob='BarLine',
        ...             value="#'(0 . 0)",
        ...             ),
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        b'4.
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> tag = "baca.bar_extent_persistent"
        >>> command = baca.IndicatorCommand(
        ...     indicators=[override], selector=baca.selectors.leaf(0), tags=[tag]
        ... )
        >>> commands(
        ...     "Music_Voice",
        ...     command,
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Voice"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='baca.PersistentOverride',
        ...         value=baca.PersistentOverride(
        ...             after=True,
        ...             attribute='bar_extent',
        ...             context='Staff',
        ...             grob='BarLine',
        ...             value="#'(0 . 0)",
        ...             ),
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        b'4.
                        b'4.
                    }
                >>
            }

..  container:: example

    Staff lines.

    ..  container:: example

        Explicit staff lines color blue:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.staff_lines(5),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        b'4.
                        b'4.
                    }
                >>
            }

        Even after previous staff lines:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        b'4.
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied staff lines color green:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'green4)
                        b'4.
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Redundant staff lines color pink:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.staff_lines(5),
        ...     baca.staff_lines(5, selector=baca.selectors.leaf(1)),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        b'4.
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                        b'4.
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> commands = baca.CommandAccumulator(
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.staff_lines(5),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music_Staff"] = [
        ...     baca.Memento(
        ...         context="Music_Voice",
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \bar ""
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                        b'4.
                        b'4.
                    }
                >>
            }

..  container:: example

    Tempo trends.

    ..  container:: example

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=4, distances=(8,)),
        ...     ),
        ... )
        >>> metronome_marks = {}
        >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
        >>> metronome_marks['112'] = abjad.MetronomeMark((1, 4), 112)

    ..  container:: example

        Explicit tempo trends color blue:

        >>> commands = baca.CommandAccumulator(
        ...     append_phantom_measure=True,
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     append_phantom_measure=commands.append_phantom_measure,
        ...     metronome_marks=commands.metronome_marks,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 25),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                        <<
                            \context Voice = "Music_Voice"
                            {
                                \abjad-invisible-music-coloring
                                %@% \abjad-invisible-music
                                b'1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                            \context Voice = "Rest_Voice"
                            {
                                \once \override Score.TimeSignature.X-extent = ##f
                                \once \override MultiMeasureRest.transparent = ##t
                                \stopStaff
                                \once \override Staff.StaffSymbol.transparent = ##t
                                \startStaff
                                R1 * 1/4
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                            }
                        >>
                    }
                >>
            }

        Even after a previous tempo trend:

        >>> commands = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Global_Skips",
        ...         prototype='baca.Ritardando',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied tempo trends color green:

        >>> commands = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.text_spanner_staff_padding(4),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Global_Skips",
        ...         prototype='baca.Accelerando',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                    }
                >>
            }

    ..  container:: example

        Redundant tempo trends color pink:

        >>> commands = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     baca.metronome_mark(
        ...         baca.Accelerando(),
        ...         selector=baca.selectors.leaf(1),
        ...         ),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     includes=["baca.ily"],
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                        b'4.
                    }
                >>
            }

        Even at the beginning of a segment:

        >>> commands = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> commands(
        ...     "Global_Skips",
        ...     baca.metronome_mark(baca.Accelerando()),
        ...     baca.text_spanner_staff_padding(4),
        ...     )
        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Global_Skips",
        ...         prototype='baca.Accelerando',
        ...         )
        ...     ]
        >>> lilypond_file = baca.interpret_commands(
        ...     commands.commands,
        ...     commands.score_template,
        ...     commands.time_signatures,
        ...     commands.voice_metadata,
        ...     environment="docs",
        ...     first_segment=False,
        ...     includes=["baca.ily"],
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ...     treat_untreated_persistent_wrappers=True,
        ...     )
        >>> block = abjad.Block(name="layout")
        >>> block.indent = 0
        >>> lilypond_file.items.insert(0, block)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
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
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music_Voice"
                    {
                        b'4.
                        b'4.
                    }
                >>
            }

"""


def persistence():
    """
    Read module-level examples.
    """
    pass
