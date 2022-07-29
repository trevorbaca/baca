r"""

>>> import pprint

..  container:: example

    Clefs.

    ..  container:: example

        Explicit clefs color blue and redraw dull blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.clef("treble", selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'blue)
                                %@% \override Staff.Clef.color = ##f
                                \set Staff.forceClef = ##t
                                b'1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            }
                        >>
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

        Even after a previous clef:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.clef("alto", selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "alto"
                                \once \override Staff.Clef.color = #(x11-color 'blue)
                                %@% \override Staff.Clef.color = ##f
                                \set Staff.forceClef = ##t
                                c'1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            }
                        >>
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    ..  container:: example

        Reapplied clefs color green and redraw dull green:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'green4)
                                %@% \override Staff.Clef.color = ##f
                                \set Staff.forceClef = ##t
                                b'1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            }
                        >>
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

    ..  container:: example

        Redundant clefs color pink and redraw dull pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=3, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.clef("treble", selector=lambda _: abjad.select.leaf(_, 0)),
        ...     baca.clef("treble", selector=lambda _: abjad.select.leaf(_, 1)),
        ... )
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'blue)
                                %@% \override Staff.Clef.color = ##f
                                \set Staff.forceClef = ##t
                                b'1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            }
                        >>
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

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ...     baca.clef("treble", selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                                %@% \override Staff.Clef.color = ##f
                                \set Staff.forceClef = ##t
                                b'1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            }
                        >>
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    }
                >>
            }

..  container:: example

    Dynamics.

    ..  container:: example

        Explicit dynamics color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.dynamic("f", selector=lambda _: baca.select.pleaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \f
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Even after a previous dynamic:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.dynamic("p", selector=lambda _: baca.select.pleaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="f",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \p
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied dynamics color green:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="f",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'green4)
                        \f
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant dynamics color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.dynamic("f", selector=lambda _: baca.select.pleaf(_, 0)),
        ...     baca.dynamic("f", selector=lambda _: abjad.select.leaf(_, 1)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \f
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'DeepPink1)
                        \f
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ...     baca.dynamic("f", selector=lambda _: baca.select.pleaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="f",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'DeepPink1)
                        \f
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Sforzando dynamics do not count as redundant:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.dynamic("sfz", selector=lambda _: baca.select.pleaf(_, 0)),
        ...     baca.dynamic("sfz", selector=lambda _: abjad.select.leaf(_, 1)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.dynamic("sfz", selector=lambda _: baca.select.pleaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="sfz",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Conventional and effort dynamics analyze nonredundantly:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.dynamic("mf", selector=lambda _: baca.select.pleaf(_, 0)),
        ...     baca.dynamic('"mf"', selector=lambda _: abjad.select.leaf(_, 1)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \mf
                        \baca-repeat-pitch-class-coloring
                        c'4.
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
        >>> instruments["Flute"] = abjad.Flute()
        >>> instruments["Piccolo"] = abjad.Piccolo()
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )

    ..  container:: example

        Explicit instruments color blue and redraw dull blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.instrument(
        ...         instruments["Flute"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     instruments=accumulator.instruments,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Even after a previous instrument:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.instrument(
        ...         instruments["Flute"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="instruments",
        ...         value="Piccolo",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     instruments=accumulator.instruments,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied instruments color green and redraw dull green:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="instruments",
        ...         value="Flute",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     instruments=accumulator.instruments,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-reapplied-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-reapplied-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-reapplied-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant instruments color pink and redraw dull pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=3, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.instrument(
        ...         instruments["Flute"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ...     baca.new(
        ...         baca.instrument(instruments["Flute"]),
        ...         map=lambda _: baca.select.leaves(_)[1:2],
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     instruments=accumulator.instruments,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'2
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'2
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'2
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'2
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'2
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'2
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'2
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'2
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'2
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     instruments=instruments,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ...     baca.instrument(
        ...         instruments["Flute"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="instruments",
        ...         value="Flute",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     instruments=accumulator.instruments,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

..  container:: example

    Short instrument names.

    ..  container:: example

        Short instrument names for examples:

        >>> short_instrument_names = {}
        >>> short_instrument_names["I+II"] = abjad.ShortInstrumentName(r"\markup I+II")
        >>> short_instrument_names["III+IV"] = abjad.ShortInstrumentName(r"\markup III+IV")
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )

    ..  container:: example

        Explicit short instrument names color blue and redraw dull blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.short_instrument_name(
        ...         short_instrument_names["I+II"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     first_section=True,
        ...     short_instrument_names=accumulator.short_instrument_names,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Even after previous short instrument name:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.short_instrument_name(
        ...         short_instrument_names["III+IV"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="short_instrument_names",
        ...         value="I+II",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     short_instrument_names=accumulator.short_instrument_names,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup III+IV
                        \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup III+IV
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup III+IV
                        \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup III+IV
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup III+IV
                        \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup III+IV
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied short instrument names color green and redraw dull green:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="short_instrument_names",
        ...         value="I+II",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     short_instrument_names=accumulator.short_instrument_names,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant short instrument names color pink and redraw dull pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=3, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.short_instrument_name(
        ...         short_instrument_names["I+II"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ...     baca.new(
        ...         baca.short_instrument_name(short_instrument_names["I+II"]),
        ...         map=lambda _: baca.select.leaves(_)[1:2],
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     first_section=True,
        ...     short_instrument_names=accumulator.short_instrument_names,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'2
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'2
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'2
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ...     baca.short_instrument_name(
        ...         short_instrument_names["I+II"],
        ...         selector=lambda _: abjad.select.leaf(_, 0),
        ...     ),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="short_instrument_names",
        ...         value="I+II",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     short_instrument_names=accumulator.short_instrument_names,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.deactivate(text, match)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count = abjad.activate(text, match)
        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file["score"].items[:] = lines
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> print(text)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.instrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Multiple short instrument names are allowed so long as only one is active:

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> accumulator = baca.CommandAccumulator(
        ...     short_instrument_names=short_instrument_names,
        ...     time_signatures=[(4, 8), (4, 8), (4, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.tag(
        ...         baca.tags.NOT_PARTS,
        ...         baca.short_instrument_name(
        ...             short_instrument_names["I+II"],
        ...             selector=lambda _: abjad.select.leaf(_, 0),
        ...         ),
        ...     ),
        ...     baca.tag(
        ...         baca.tags.NOT_PARTS,
        ...         baca.short_instrument_name(
        ...             short_instrument_names["III+IV"],
        ...             selector=lambda _: abjad.select.leaf(_, 0),
        ...         ),
        ...         deactivate=True,
        ...     ),
        ...     baca.tag(
        ...         baca.tags.NOT_PARTS,
        ...         baca.short_instrument_name(
        ...             short_instrument_names["III+IV"],
        ...             selector=lambda _: abjad.select.leaf(_, 0),
        ...         ),
        ...         deactivate=True,
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     first_section=True,
        ...     short_instrument_names=accumulator.short_instrument_names,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #0 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 4/8
                        s1 * 4/8
                        \baca-lbsd #15 #'(11)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \break
                        s1 * 4/8
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 4/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \set Staff.shortInstrumentName = \markup I+II
                        %@% \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        %@% \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        %@% \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup III+IV
                        \baca-repeat-pitch-class-coloring
                        c'2
                        \baca-repeat-pitch-class-coloring
                        c'2
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
        >>> metronome_marks["90"] = abjad.MetronomeMark((1, 4), 90)
        >>> metronome_marks["112"] = abjad.MetronomeMark((1, 4), 112)

    ..  container:: example

        Explicit metronome marks color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     append_anchor_skip=True,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 25),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ...     accumulator.manifests(),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.append_anchor_note(),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     append_anchor_skip=True,
        ...     metronome_marks=accumulator.metronome_marks,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue
                        \bacaStartTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-time-signature-transparent
                        \time 1/4
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        b'1 * 1/4
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                    }
                >>
            }

        Even after a previous metronome mark:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     append_anchor_skip=True,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ...     accumulator.manifests(),
        ... )
        >>> baca.text_spanner_staff_padding_function(score["Skips"][:-1], 4)
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.append_anchor_note(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         manifest="metronome_marks",
        ...         value="90",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     append_anchor_skip=True,
        ...     metronome_marks=accumulator.metronome_marks,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \override TextSpanner.staff-padding = 4
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue
                        \bacaStartTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-time-signature-transparent
                        \time 1/4
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        b'1 * 1/4
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                    }
                >>
            }

    ..  container:: example

        Reapplied metronome marks color green:

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]['Score'] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         manifest="metronome_marks",
        ...         value="90",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     previous_persist=persist,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )
        >>> baca.text_spanner_staff_padding_function(score["Skips"], 4)

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     metronome_marks=accumulator.metronome_marks,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \override TextSpanner.staff-padding = 4
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "90" #'green4
                        \bacaStartTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "90"
                        %@% \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant metronome marks color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     append_anchor_skip=True,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ...     accumulator.manifests(),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][2 - 1],
        ...     metronome_marks["112"],
        ...     accumulator.manifests(),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.append_anchor_note(),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     append_anchor_skip=True,
        ...     metronome_marks=accumulator.metronome_marks,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'blue
                        \bacaStartTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1
                        \bacaStartTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-time-signature-transparent
                        \time 1/4
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        b'1 * 1/4
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                    }
                >>
            }

        Even at the beginning of a section:

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         manifest="metronome_marks",
        ...         value="112",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     append_anchor_skip=True,
        ...     docs=True,
        ...     previous_persist=persist,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ...     accumulator.manifests(),
        ... )
        >>> baca.text_spanner_staff_padding_function(score["Skips"][:-1], 4)
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ...     baca.append_anchor_note(),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     append_anchor_skip=True,
        ...     metronome_marks=accumulator.metronome_marks,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \override TextSpanner.staff-padding = 4
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1
                        \bacaStartTextSpanMM
                        %@% - \abjad-invisible-line
                        %@% - \baca-metronome-mark-spanner-left-text 2 0 1 "112"
                        %@% \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-time-signature-transparent
                        \time 1/4
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        b'1 * 1/4
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                    }
                >>
            }

..  container:: example

    Persistent overrides.

    ..  container:: example

        Explicit persistent overrides work but do not color:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> tag = abjad.Tag("baca.bar_extent_persistent")
        >>> command = baca.IndicatorCommand(
        ...     indicators=[override],
        ...     selector=lambda _: abjad.select.leaf(_, 0),
        ...     tags=[tag],
        ... )

        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     command,
        ...     baca.staff_lines(1, selector=lambda _: abjad.select.leaf(_, 0)),
        ...     baca.staff_position(0),
        ... )

        >>> metadata, persist = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
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

        Persistent overrides also appear in section metadata:

        >>> dictionary = persist["persistent_indicators"]
        >>> dictionary
        {'Score': [baca.Memento(context='Skips', edition=None, manifest=None, prototype='abjad.TimeSignature', synthetic_offset=None, value='3/8')], 'Staff': [baca.Memento(context='Music', edition=None, manifest=None, prototype='baca.PersistentOverride', synthetic_offset=None, value=PersistentOverride(after=False, attribute='bar_extent', context='Staff', grob='BarLine', hide=False, value="#'(0 . 0)")), baca.Memento(context='Music', edition=None, manifest=None, prototype='baca.StaffLines', synthetic_offset=None, value=1), baca.Memento(context='Music', edition=Tag(string='-PARTS'), manifest=None, prototype='baca.BarExtent', synthetic_offset=None, value=1)]}

    ..  container:: example

        Reapplied persistent overrides work but do not color:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype='baca.PersistentOverride',
        ...         value=baca.PersistentOverride(
        ...             after=True,
        ...             attribute="bar_extent",
        ...             context="Staff",
        ...             grob="BarLine",
        ...             value="#'(0 . 0)",
        ...         ),
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> tag = abjad.Tag("baca.bar_extent_persistent")
        >>> command = baca.IndicatorCommand(
        ...     indicators=[override],
        ...     selector=lambda _: abjad.select.leaf(_, 0),
        ...     tags=[tag],
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     command,
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="baca.PersistentOverride",
        ...         value=baca.PersistentOverride(
        ...             after=True,
        ...             attribute="bar_extent",
        ...             context="Staff",
        ...             grob='BarLine',
        ...             value="#'(0 . 0)",
        ...         ),
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

..  container:: example

    Staff lines.

    ..  container:: example

        Explicit staff lines color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.staff_lines(5, selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Even after previous staff lines:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.staff_lines(1, selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied staff lines color green:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="baca.StaffLines",
        ...         value=5,
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'green4)
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant staff lines color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.staff_lines(5, selector=lambda _: abjad.select.leaf(_, 0)),
        ...     baca.staff_lines(5, selector=lambda _: abjad.select.leaf(_, 1)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                        c'4.
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ...     baca.staff_lines(5, selector=lambda _: abjad.select.leaf(_, 0)),
        ... )

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="baca.StaffLines",
        ...         value=5,
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \baca-time-signature-color #'blue
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
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
        >>> metronome_marks["90"] = abjad.MetronomeMark((1, 4), 90)
        >>> metronome_marks["112"] = abjad.MetronomeMark((1, 4), 112)

    ..  container:: example

        Explicit tempo trends color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     append_anchor_skip=True,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 25),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ...     accumulator.manifests(),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.append_anchor_note(),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     append_anchor_skip=True,
        ...     metronome_marks=accumulator.metronome_marks,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large \upright accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #25
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \noBreak
                        \baca-time-signature-transparent
                        \time 1/4
                        s1 * 1/4
                        \bacaStopTextSpanMM
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        %@% \abjad-invisible-music
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        b'1 * 1/4
                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                    }
                >>
            }

        Even after a previous tempo trend:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ...     )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ...     accumulator.manifests(),
        ... )
        >>> baca.text_spanner_staff_padding_function(score["Skips"], 4)
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         prototype="baca.Ritardando",
        ...     )
        ... ]
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \override TextSpanner.staff-padding = 4
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large \upright accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied tempo trends color green:

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         prototype="baca.Accelerando",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     previous_persist=persist,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )
        >>> baca.text_spanner_staff_padding_function(score["Skips"], 4)

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \override TextSpanner.staff-padding = 4
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large \upright accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'green4) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant tempo trends color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ...     accumulator.manifests(),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][2 - 1],
        ...     baca.Accelerando(),
        ...     accumulator.manifests(),
        ... )
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large \upright accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large \upright accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'DeepPink1) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

        Even at the beginning of a section:

        >>> metadata, persist = {}, {}
        >>> persist["persistent_indicators"] = {}
        >>> persist["persistent_indicators"]["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         prototype="baca.Accelerando",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(3, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ...     previous_persist=persist,
        ...     spacing=baca.SpacingSpecifier(
        ...         breaks=breaks,
        ...         fallback_duration=(1, 24),
        ...     ),
        ... )
        >>> baca.metronome_mark_function(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ...     accumulator.manifests(),
        ... )
        >>> baca.text_spanner_staff_padding_function(score["Skips"], 4)
        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.reapply_persistent_indicators(),
        ... )
        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     previous_metadata=metadata,
        ...     previous_persist=persist,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     treat_untreated_persistent_wrappers=True,
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
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
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \autoPageBreaksOff
                        \baca-lbsd #4 #'(8)
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        \override TextSpanner.staff-padding = 4
                        \baca-time-signature-color #'blue
                        \pageBreak
                        \time 3/8
                        s1 * 3/8
                        %@% - \abjad-dashed-line-with-arrow
                        %@% - \tweak bound-details.left.text \markup \concat { \large \upright accel. \hspace #0.5 }
                        %@% \bacaStartTextSpanMM
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'DeepPink1) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music"
                    {
                        \baca-repeat-pitch-class-coloring
                        c'4.
                        \baca-repeat-pitch-class-coloring
                        c'4.
                    }
                >>
            }

"""


def persistence():
    """
    Read module-level examples.
    """
    pass
