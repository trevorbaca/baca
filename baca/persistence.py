r"""
Persistence.

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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_mmrests(time_signatures(), head="Music")
        >>> voice.extend(music)
        >>> _ = baca.clef(abjad.select.leaf(voice, 0), "treble")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'blue)
                                \set Staff.forceClef = ##t
                                c'1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                            }
                        >>
                        R1 * 3/8
                    }
                >>
            }

        Even after a previous clef:

        >>> def make_previous_metadata():
        ...     previous_metadata = {}
        ...     persistent_indicators = {}
        ...     persistent_indicators["Staff"] = [
        ...         baca.Memento(
        ...             context="Music",
        ...             prototype="abjad.Clef",
        ...             value="treble",
        ...         )
        ...     ]
        ...     previous_metadata["persistent_indicators"] = persistent_indicators
        ...     return previous_metadata

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_mmrests(time_signatures(), head="Music")
        >>> voice.extend(music)
        >>> previous_metadata = make_previous_metadata()
        >>> baca.section.reapply(voice, previous_metadata["persistent_indicators"])
        >>> _ = baca.clef(abjad.select.leaf(voice, 0), "alto")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "alto"
                                \once \override Staff.Clef.color = #(x11-color 'blue)
                                \set Staff.forceClef = ##t
                                c'1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                            }
                        >>
                        R1 * 3/8
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_mmrests(time_signatures(), head="Music")
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Clef",
        ...         value="treble",
        ...     )
        ... ]
        >>> baca.section.reapply(voice, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'green4)
                                \set Staff.forceClef = ##t
                                c'1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                            }
                        >>
                        R1 * 3/8
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_mmrests(time_signatures(), head="Music")
        >>> voice.extend(music)
        >>> _ = baca.clef(abjad.select.leaf(voice, 0), "treble")
        >>> _ = baca.clef(abjad.select.leaf(voice, 2), "treble")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'blue)
                                \set Staff.forceClef = ##t
                                c'1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                            }
                        >>
                        \clef "treble"
                        \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                        \set Staff.forceClef = ##t
                        R1 * 3/8
                        \override Staff.Clef.color = #(x11-color 'DeepPink4)
                        R1 * 3/8
                    }
                >>
            }

        Even at the beginning of a section:

        >>> def make_previous_metadata():
        ...     previous_metadata = {}
        ...     persistent_indicators = {}
        ...     persistent_indicators["Staff"] = [
        ...         baca.Memento(
        ...             context="Music",
        ...             prototype="abjad.Clef",
        ...             value="treble",
        ...         )
        ...     ]
        ...     previous_metadata["persistent_indicators"] = persistent_indicators
        ...     return baca.section.proxy(previous_metadata)

        >>> score = baca.docs.make_empty_score(1)
        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         1,
        ...         baca.system(measure=1, y_offset=0, distances=(11,)),
        ...         baca.system(measure=2, y_offset=15, distances=(11,)),
        ...     ),
        ... )
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_mmrests(time_signatures(), head="Music")
        >>> voice.extend(music)
        >>> previous_metadata = make_previous_metadata()
        >>> baca.section.reapply(voice, previous_metadata["persistent_indicators"])
        >>> _ = baca.clef(abjad.select.leaf(voice, 0), "treble")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                \clef "treble"
                                \once \override Staff.Clef.color = #(x11-color 'DeepPink1)
                                \set Staff.forceClef = ##t
                                c'1 * 3/8
                                \override Staff.Clef.color = #(x11-color 'DeepPink4)
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 3/8
                            }
                        >>
                        R1 * 3/8
                    }
                >>
            }

..  container:: example

    Dynamics.

    ..  container:: example

        Explicit dynamics color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier(fallback_duration=(1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "f")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \f
                        c'4.
                    }
                >>
            }

        Even after a previous dynamic:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "p")
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="f",
        ...     )
        ... ]
        >>> baca.section.reapply(score, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \p
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied dynamics color green:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="f",
        ...     )
        ... ]
        >>> baca.section.reapply(voice, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'green4)
                        \f
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant dynamics color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "f")
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 1), "f")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \f
                        c'4.
                        - \tweak color #(x11-color 'DeepPink1)
                        \f
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="f",
        ...     )
        ... ]
        >>> baca.section.reapply(voice, previous_persistent_indicators)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "f")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'DeepPink1)
                        \f
                        c'4.
                    }
                >>
            }

        Sforzando dynamics do not count as redundant:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "sfz")
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 1), "sfz")
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "sfz")
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Music"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="abjad.Dynamic",
        ...         value="sfz",
        ...     )
        ... ]
        >>> baca.section.reapply(score, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \sfz
                        c'4.
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Conventional and effort dynamics analyze nonredundantly:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 0), "mf")
        >>> _ = baca.dynamic(baca.select.pleaf(voice, 1), '"mf"')
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        - \tweak color #(x11-color 'blue)
                        \mf
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
        >>> manifests = {"abjad.Instrument": instruments}
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.instrument(abjad.select.leaf(voice, 0), "Flute", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        Even after a previous instrument:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="instruments",
        ...         value="Piccolo",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.instrument(abjad.select.leaf(voice, 0), "Flute", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        c'4.
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied instruments color green and redraw dull green:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="instruments",
        ...         value="Flute",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        ^ \baca-reapplied-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        c'4.
                        ^ \baca-reapplied-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        c'4.
                        ^ \baca-reapplied-instrument-markup "(“Flute”)"
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
        >>> time_signatures = baca.section.time_signatures([(4, 8), (4, 8), (4, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> manifests = {"abjad.Instrument": instruments}
        >>> _ = baca.instrument(voice[0], "Flute", manifests)
        >>> _ = baca.instrument(voice[1], "Flute", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'2
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'2
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        c'2
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        c'2
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'2
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        c'2
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        c'2
                        ^ \baca-explicit-instrument-markup "(“Flute”)"
                        c'2
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="instruments",
        ...         value="Flute",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.instrument(abjad.select.leaf(voice, 0), "Flute", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        c'4.
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.instrument_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        c'4.
                        ^ \baca-redundant-instrument-markup "(“Flute”)"
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
        >>> short_instrument_names["III+IV"] = abjad.ShortInstrumentName(
        ...     r"\markup III+IV")
        >>> manifests = {"abjad.ShortInstrumentName": short_instrument_names}
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.short_instrument_name(voice[0], "I+II", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        Even after previous short instrument name:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="short_instrument_names",
        ...         value="I+II",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.short_instrument_name(voice[0], "III+IV", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup III+IV
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup III+IV
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        \set Staff.shortInstrumentName = \markup III+IV
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup III+IV
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied short instrument names color green and redraw dull green:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="short_instrument_names",
        ...         value="I+II",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'green4)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)
                        \set Staff.shortInstrumentName = \markup I+II
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
        >>> time_signatures = baca.section.time_signatures([(4, 8), (4, 8), (4, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> manifests = {"abjad.ShortInstrumentName": short_instrument_names}
        >>> _ = baca.short_instrument_name(voice[0], "I+II", manifests)
        >>> _ = baca.short_instrument_name(voice[1], "I+II", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'2
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'2
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         manifest="short_instrument_names",
        ...         value="I+II",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.short_instrument_name(voice[0], "I+II", manifests)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        >>> score = lilypond_file["Score"]
        >>> text = abjad.lilypond(score)
        >>> text = abjad.tag.left_shift_tags(text)
        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.deactivate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
                        c'4.
                    }
                >>
            }

        >>> tags_ = baca.tags.short_instrument_name_color_tags()
        >>> match = lambda tags: bool(set(tags) & set(tags_))
        >>> text, count, skipped = abjad.activate(text, match)
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1)
                        c'4.
                        \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)
                        \set Staff.shortInstrumentName = \markup I+II
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
        >>> time_signatures = baca.section.time_signatures([(4, 8), (4, 8), (4, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.short_instrument_name(voice[0], "I+II", manifests)
        >>> wrappers = baca.short_instrument_name(voice[0], "III+IV", manifests)
        >>> for wrapper in wrappers:
        ...     wrapper.deactivate = True

        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \set Staff.shortInstrumentName = \markup I+II
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                        c'2
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                        \set Staff.shortInstrumentName = \markup I+II
                        \set Staff.shortInstrumentName = \markup III+IV
                        c'2
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
        >>> manifests = {"abjad.MetronomeMark": metronome_marks}

    ..  container:: example

        Explicit metronome marks color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     append_anchor_skip=True,
        ...     docs=True,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ... )
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.append_anchor_note(voice)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
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
                        c'4.
                        c'4.
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        c'1 * 1/4
                    }
                >>
            }

        Even after a previous metronome mark:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     append_anchor_skip=True,
        ...     docs=True,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ... )
        >>> _ = baca.text_spanner_staff_padding(score["Skips"][:-1], 4)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.append_anchor_note(voice)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         manifest="metronome_marks",
        ...         value="90",
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
                        \baca-new-spacing-section #1 #24
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
                        c'4.
                        c'4.
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        c'1 * 1/4
                    }
                >>
            }

    ..  container:: example

        Reapplied metronome marks color green:

        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         manifest="metronome_marks",
        ...         value="90",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     docs=True,
        ...     manifests={"abjad.MetronomeMark": metronome_marks},
        ...     previous_persistent_indicators=previous_persistent_indicators,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.text_spanner_staff_padding(score["Skips"], 4)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        \revert TextSpanner.staff-padding
                    }
                    \context Voice = "Music"
                    {
                        c'4.
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant metronome marks color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     append_anchor_skip=True,
        ...     docs=True,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ... )
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][2 - 1],
        ...     metronome_marks["112"],
        ... )
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.append_anchor_note(voice)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
                        - \abjad-invisible-line
                        - \baca-metronome-mark-spanner-colored-left-text 2 0 1 "112" #'DeepPink1
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
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
                        c'4.
                        c'4.
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        c'1 * 1/4
                    }
                >>
            }

        Even at the beginning of a section:

        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         manifest="metronome_marks",
        ...         value="112",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     append_anchor_skip=True,
        ...     docs=True,
        ...     manifests={"abjad.MetronomeMark": metronome_marks},
        ...     previous_persistent_indicators=previous_persistent_indicators,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     metronome_marks["112"],
        ... )
        >>> _ = baca.text_spanner_staff_padding(score["Skips"][:-1], 4)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.append_anchor_note(voice)
        >>> baca.section.reapply(voice, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \revert TextSpanner.staff-padding
                        \baca-new-spacing-section #1 #24
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
                        c'4.
                        c'4.
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        c'1 * 1/4
                    }
                >>
            }

..  container:: example

    Persistent overrides.

    ..  container:: example

        Explicit persistent overrides work but do not color:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> wrapper = abjad.attach(override, voice[0], wrapper=True)
        >>> _ = baca.staff_lines(voice[0], 1)
        >>> _ = baca.staff_position(voice, 0)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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

    ..  container:: example

        Reapplied persistent overrides work but do not color:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Music"] = [
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
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        \override Staff.BarLine.bar-extent = #'(0 . 0)
                        c'4.
                    }
                >>
            }

        Even at the beginning of a section:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> override = baca.PersistentOverride(
        ...     attribute="bar_extent",
        ...     context="Staff",
        ...     grob="BarLine",
        ...     value="#'(0 . 0)",
        ... )
        >>> abjad.attach(override, abjad.select.leaf(voice, 0))
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Music"] = [
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
        >>> baca.section.reapply(score, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        c'4.
                    }
                >>
            }

..  container:: example

    Staff lines.

    ..  container:: example

        Explicit staff lines color blue:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.staff_lines(voice[0], 5)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        c'4.
                        c'4.
                    }
                >>
            }

        Even after previous staff lines:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.staff_lines(voice[0], 1)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype='baca.StaffLines',
        ...         value=5,
        ...     )
        ... ]
        >>> baca.section.reapply(score, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 1
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        c'4.
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied staff lines color green:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="baca.StaffLines",
        ...         value=5,
        ...     )
        ... ]
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'green4)
                        c'4.
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant staff lines color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.staff_lines(voice[0], 5)
        >>> _ = baca.staff_lines(voice[1], 5)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                        c'4.
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Staff"] = [
        ...     baca.Memento(
        ...         context="Music",
        ...         prototype="baca.StaffLines",
        ...         value=5,
        ...     )
        ... ]
        >>> baca.section.reapply(voice, previous_persistent_indicators)
        >>> _ = baca.staff_lines(voice[0], 5)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        \override Staff.BarLine.bar-extent = #'(-2 . 2)
                        \stopStaff
                        \once \override Staff.StaffSymbol.line-count = 5
                        \startStaff
                        \once \override Staff.StaffSymbol.color = #(x11-color 'DeepPink1)
                        c'4.
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
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     append_anchor_skip=True,
        ...     docs=True,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ... )
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.append_anchor_note(voice)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score, manifests=manifests)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \baca-new-spacing-section #1 #24
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
                        c'4.
                        c'4.
                        \abjad-invisible-music-coloring
                        \once \override Accidental.stencil = ##f
                        \stopStaff
                        \once \override Staff.StaffSymbol.transparent = ##t
                        \startStaff
                        c'1 * 1/4
                    }
                >>
            }

        Even after a previous tempo trend:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ... )
        >>> _ = baca.text_spanner_staff_padding(score["Skips"], 4)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         prototype="baca.Ritardando",
        ...     )
        ... ]
        >>> baca.section.reapply(score, previous_persistent_indicators)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Reapplied tempo trends color green:

        >>> persist = {}
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         prototype="baca.Accelerando",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     docs=True,
        ...     previous_persistent_indicators=previous_persistent_indicators,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.text_spanner_staff_padding(score["Skips"], 4)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        c'4.
                    }
                >>
            }

    ..  container:: example

        Redundant tempo trends color pink:

        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8), (3, 8)])
        >>> baca.section.set_up_score(score, time_signatures(), docs=True)
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ... )
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][2 - 1],
        ...     baca.Accelerando(),
        ... )
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup \concat { \with-color #(x11-color 'blue) \large \upright accel. \hspace #0.5 }
                        \bacaStartTextSpanMM
                        \baca-new-spacing-section #1 #24
                        \noBreak
                        s1 * 3/8
                        \bacaStopTextSpanMM
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
                        c'4.
                        c'4.
                        c'4.
                    }
                >>
            }

        Even at the beginning of a section:

        >>> persist = {}
        >>> previous_persistent_indicators = {}
        >>> previous_persistent_indicators["Score"] = [
        ...     baca.Memento(
        ...         context="Skips",
        ...         prototype="baca.Accelerando",
        ...     )
        ... ]
        >>> score = baca.docs.make_empty_score(1)
        >>> time_signatures = baca.section.time_signatures([(3, 8), (3, 8)])
        >>> baca.section.set_up_score(
        ...     score,
        ...     time_signatures(),
        ...     docs=True,
        ...     previous_persistent_indicators=previous_persistent_indicators,
        ... )
        >>> baca.SpacingSpecifier((1, 24))(score)
        >>> baca.section.apply_breaks(score, breaks)
        >>> _ = baca.metronome_mark(
        ...     score["Skips"][1 - 1],
        ...     baca.Accelerando(),
        ... )
        >>> _ = baca.text_spanner_staff_padding(score["Skips"], 4)
        >>> voice = score["Music"]
        >>> music = baca.make_notes(time_signatures())
        >>> voice.extend(music)
        >>> baca.section.reapply(
        ...     voice,
        ...     previous_persistent_indicators,
        ...     manifests=manifests,
        ... )
        >>> _ = baca.section.remove_redundant_time_signatures(score)
        >>> baca.section.treat_untreated_persistent_wrappers(score)
        >>> baca.section.span_metronome_marks(score)
        >>> baca.section.style_anchor_skip(score)
        >>> baca.docs.remove_deactivated_wrappers(score)
        >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                        c'4.
                        c'4.
                    }
                >>
            }

"""


def dummy():
    """
    Read module-level examples.
    """
