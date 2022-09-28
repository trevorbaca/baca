r"""
overrides.py examples.

..  container:: example

    Overrides bar line transparency before measure 1:

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> def make_rhythm(divisions):
    ...     nested_music = rmakers.talea(divisions, [1, 1, 1, -1], 8)
    ...     voice = rmakers.wrap_in_time_signature_staff(nested_music, divisions)
    ...     rmakers.beam(voice)
    ...     rmakers.extract_trivial(voice)
    ...     music = abjad.mutate.eject_contents(voice)
    ...     return music

    >>> music = make_rhythm(measures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.bar_line_transparent(
    ...         abjad.select.group_by_measure(voice)[1]
    ... )
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    e'8
                    [
                    d''8
                    f'8
                    ]
                    r8
                    \override Score.BarLine.transparent = ##t
                    e''8
                    [
                    g'8
                    f''8
                    ]
                    \revert Score.BarLine.transparent
                    r8
                    e'8
                    [
                    d''8
                    f'8
                    ]
                    r8
                    e''8
                    [
                    g'8
                    ]
                }
            >>
        }

..  container:: example

    Overrides beam positions:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     treatments=[-1],
    ... )
    >>> _ = baca.stem_up(baca.select.pleaves(container))
    >>> rmakers.beam(container)
    >>> _ = baca.beam_positions(container, 6)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 4)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \times 4/5
                {
                    \override Beam.positions = #'(6 . 6)
                    \override TupletBracket.staff-padding = 4
                    \time 3/4
                    r8
                    \override Stem.direction = #up
                    c'16
                    [
                    d'16
                    bf'16
                    ]
                }
                \times 4/5
                {
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert Stem.direction
                    r4
                    \revert Beam.positions
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides dynamic line spanner staff padding on all leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.dls_staff_padding(container, 4)
    >>> for tuplet in baca.select.tuplets(container):
    ...     _ = baca.hairpin(
    ...         baca.select.tleaves(tuplet),
    ...         "p < f",
    ...         remove_length_1_spanner_start=True,
    ...     )

    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override DynamicLineSpanner.staff-padding = 4
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    \p
                    [
                    \<
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    \f
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    \p
                    [
                    \<
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    \f
                    ]
                }
                \times 4/5
                {
                    a'16
                    \p
                    r4
                    \revert DynamicLineSpanner.staff-padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Up-overrides dynamic line spanner direction on all leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.dls_up(container)
    >>> for tuplet in baca.select.tuplets(container):
    ...     _ = baca.hairpin(
    ...         baca.select.tleaves(tuplet),
    ...         "p < f",
    ...         remove_length_1_spanner_start=True,
    ...     )

    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override DynamicLineSpanner.direction = #up
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    \p
                    [
                    \<
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    \f
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    \p
                    [
                    \<
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    \f
                    ]
                }
                \times 4/5
                {
                    a'16
                    \p
                    r4
                    \revert DynamicLineSpanner.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>


..  container:: example

    Overrides dynamic text extra offset on pitched leaf 0:

    >>> def selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = baca.select.phead(result, 0)
    ...     return result

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.dynamic(baca.select.pleaf(container, 0), "p")
    >>> _ = baca.dynamic(selector(container), "f")
    >>> _ = baca.dynamic_text_extra_offset(
    ...     baca.select.pleaf(container, 0), (-3, 0))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \once \override DynamicText.extra-offset = #'(-3 . 0)
                    c'16
                    \p
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    \f
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    REGRESSION. Coerces X11 color names:

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> voice = score["Music"]
    >>> music = baca.make_mmrests(measures(), head="Music")
    >>> score["Music"].extend(music)
    >>> _ = baca.mmrest_color(
    ...     baca.select.mmrests(voice)[1:],
    ...     "#(x11-color 'DarkOrchid)",
    ... )
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
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
                            b'1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                    >>
                    \override MultiMeasureRest.color = #(x11-color 'DarkOrchid)
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    R1 * 4/8
                    %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    \revert MultiMeasureRest.color
                }
            >>
        }

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> voice = score["Music"]
    >>> music = baca.make_mmrests(measures(), head="Music")
    >>> score["Music"].extend(music)
    >>> _ = baca.markup(
    ...     baca.select.mmrest(voice, 2),
    ...     r"\baca-boxed-markup still",
    ... )
    >>> _ = baca.mmrest_text_color(baca.select.mmrests(voice)[1:], "#red")
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
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
                            b'1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                    >>
                    \override MultiMeasureRestText.color = #red
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    \revert MultiMeasureRestText.color
                }
            >>
        }

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> voice = score["Music"]
    >>> music = baca.make_mmrests(measures(), head="Music")
    >>> score["Music"].extend(music)
    >>> _ = baca.markup(
    ...     baca.select.mmrest(voice, 2),
    ...     r"\baca-boxed-markup still",
    ... )
    >>> _ = baca.mmrest_text_extra_offset(
    ...     baca.select.mmrests(voice)[1:], (0, 2))
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
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
                            b'1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                    >>
                    \override MultiMeasureRestText.extra-offset = #'(0 . 2)
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    \revert MultiMeasureRestText.extra-offset
                }
            >>
        }

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> voice = score["Music"]
    >>> music = baca.make_mmrests(measures(), head="Music")
    >>> score["Music"].extend(music)
    >>> _ = baca.markup(
    ...     baca.select.mmrest(voice, 2),
    ...     r"\baca-boxed-markup still",
    ... )
    >>> _ = baca.mmrest_text_padding(baca.select.mmrests(voice)[1:], 2)
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
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
                            b'1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                    >>
                    \override MultiMeasureRestText.padding = 2
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    \revert MultiMeasureRestText.padding
                }
            >>
        }

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> voice = score["Music"]
    >>> music = baca.make_mmrests(measures(), head="Music")
    >>> score["Music"].extend(music)
    >>> _ = baca.markup(
    ...     baca.select.mmrest(voice, 2),
    ...     r"\baca-boxed-markup still",
    ... )
    >>> _ = baca.mmrest_text_parent_center(baca.select.mmrests(voice)[1:])
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
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
                            b'1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                    >>
                    \override MultiMeasureRestText.parent-alignment-X = 0
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    \revert MultiMeasureRestText.parent-alignment-X
                }
            >>
        }

..  container:: example

    >>> score = baca.docs.make_empty_score(1)
    >>> measures = baca.measures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> first_measure_number = baca.section.set_up_score(
    ...     score,
    ...     measures(),
    ...     docs=True,
    ... )
    >>> voice = score["Music"]
    >>> music = baca.make_mmrests(measures(), head="Music")
    >>> score["Music"].extend(music)
    >>> _ = baca.markup(
    ...     baca.select.mmrest(voice, 2),
    ...     r"\baca-boxed-markup still",
    ... )
    >>> _ = baca.mmrest_text_staff_padding(baca.select.mmrests(voice)[1:], 2)
    >>> _, _ = baca.section.postprocess_score(
    ...     score,
    ...     measures(),
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
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
                            b'1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        }
                    >>
                    \override MultiMeasureRestText.staff-padding = 2
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                    R1 * 3/8
                    %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                    \revert MultiMeasureRestText.staff-padding
                }
            >>
        }

..  container:: example

    Overrides note-head style on all pitched leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.note_head_style_cross(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \override NoteHead.style = #'cross
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert NoteHead.style
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides note-head style on all PLTs:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.note_head_style_harmonic(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \override NoteHead.style = #'harmonic
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert NoteHead.style
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides repeat tie direction on pitched leaves:

    >>> container = baca.figure(
    ...     [[11, 11, 12], [11, 11, 11], [11]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> for qrun in baca.select.qruns(container):
    ...     _ = baca.repeat_tie(qrun[1:])

    >>> pleaves = baca.select.pleaves(container)
    >>> _ = baca.repeat_tie_down(pleaves)
    >>> _ = baca.stem_up(pleaves)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 5/4
                    r8
                    \override RepeatTie.direction = #down
                    \override Stem.direction = #up
                    b'16
                    [
                    b'16
                    ]
                    \repeatTie
                    c''4
                    ~
                    c''16
                    \repeatTie
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/8
                {
                    b'16
                    [
                    b'16
                    ]
                    \repeatTie
                    b'4
                    \repeatTie
                    ~
                    b'16
                    \repeatTie
                    r16
                }
                \times 4/5
                {
                    b'16
                    \revert RepeatTie.direction
                    \revert Stem.direction
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides repeat tie direction on all leaves:

    >>> container = baca.figure(
    ...     [[11, 11, 12], [11, 11, 11], [11]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> for qrun in baca.select.qruns(container):
    ...     _ = baca.repeat_tie(qrun[1:])

    >>> pleaves = baca.select.pleaves(container)
    >>> _ = baca.repeat_tie_up(pleaves)
    >>> _ = baca.stem_down(pleaves)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 5/4
                    r8
                    \override RepeatTie.direction = #up
                    \override Stem.direction = #down
                    b'16
                    [
                    b'16
                    ]
                    \repeatTie
                    c''4
                    ~
                    c''16
                    \repeatTie
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/8
                {
                    b'16
                    [
                    b'16
                    ]
                    \repeatTie
                    b'4
                    \repeatTie
                    ~
                    b'16
                    \repeatTie
                    r16
                }
                \times 4/5
                {
                    b'16
                    \revert RepeatTie.direction
                    \revert Stem.direction
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Down-overrides direction of rests:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.rest_down(abjad.select.rests(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Rest.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert Rest.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides rest position:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.rest_staff_position(container, -6)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Rest.staff-position = -6
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert Rest.staff-position
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Makes rests transparent:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.rest_transparent(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Rest.transparent = ##t
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert Rest.transparent
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Up-overrides rest direction:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.rest_up(abjad.select.rests(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Rest.direction = #up
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert Rest.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides script color on all leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.accent(baca.select.pheads(container))
    >>> _ = baca.script_color(container, "#red")
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Script.color = #red
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    - \accent
                    [
                    d'16
                    - \accent
                    ]
                    bf'4
                    - \accent
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \accent
                    [
                    e''16
                    - \accent
                    ]
                    ef''4
                    - \accent
                    ~
                    ef''16
                    r16
                    af''16
                    - \accent
                    [
                    g''16
                    - \accent
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \accent
                    r4
                    \revert Script.color
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Down-overrides script direction on all leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.accent(baca.select.pheads(container))
    >>> _ = baca.script_down(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Script.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    - \accent
                    [
                    d'16
                    - \accent
                    ]
                    bf'4
                    - \accent
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \accent
                    [
                    e''16
                    - \accent
                    ]
                    ef''4
                    - \accent
                    ~
                    ef''16
                    r16
                    af''16
                    - \accent
                    [
                    g''16
                    - \accent
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \accent
                    r4
                    \revert Script.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides script extra offset on leaf 1:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.accent(baca.select.pheads(container))
    >>> _ = baca.script_extra_offset(abjad.select.leaf(container, 1), (-1.5, 0))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \once \override Script.extra-offset = #'(-1.5 . 0)
                    c'16
                    - \accent
                    [
                    d'16
                    - \accent
                    ]
                    bf'4
                    - \accent
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \accent
                    [
                    e''16
                    - \accent
                    ]
                    ef''4
                    - \accent
                    ~
                    ef''16
                    r16
                    af''16
                    - \accent
                    [
                    g''16
                    - \accent
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \accent
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Up-overrides script direction on all leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.accent(baca.select.pheads(container))
    >>> _ = baca.script_up(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Script.direction = #up
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    - \accent
                    [
                    d'16
                    - \accent
                    ]
                    bf'4
                    - \accent
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \accent
                    [
                    e''16
                    - \accent
                    ]
                    ef''4
                    - \accent
                    ~
                    ef''16
                    r16
                    af''16
                    - \accent
                    [
                    g''16
                    - \accent
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \accent
                    r4
                    \revert Script.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides slur direction:

    >>> def selector(argument):
    ...     selection = abjad.select.tuplets(argument)
    ...     items = [baca.select.tleaves(_) for _ in selection]
    ...     selection = abjad.select.nontrivial(items)
    ...     return selection
    ...
    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> for item in selector(container):
    ...     _ = baca.slur(item)

    >>> _ = baca.slur_down(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Slur.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    (
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    )
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    (
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    )
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert Slur.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Up-overrides slur direction on leaves:

    >>> def selector(argument):
    ...     selection = abjad.select.tuplets(argument)
    ...     items = [baca.select.tleaves(_) for _ in selection]
    ...     selection = abjad.select.nontrivial(items)
    ...     return selection
    ...

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> for item in selector(container):
    ...     _ = baca.slur(item)

    >>> _ = baca.slur_up(container)
    >>> _ = baca.stem_down(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> _ = baca.tuplet_bracket_down(container)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Slur.direction = #up
                    \override TupletBracket.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \override Stem.direction = #down
                    c'16
                    [
                    (
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    )
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    (
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    )
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert Stem.direction
                    r4
                    \revert Slur.direction
                    \revert TupletBracket.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides stem color on pitched leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.stem_color(baca.select.pleaves(container), "#red")
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \override Stem.color = #red
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert Stem.color
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Down-overrides stem direction pitched leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.stem_down(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \override Stem.direction = #down
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert Stem.direction
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Up-overrides stem direction on pitched leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.stem_up(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \override Stem.direction = #up
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \revert Stem.direction
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides sustain pedal staff padding:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> for tuplet in baca.select.tuplets(container):
    ...     _ = baca.sustain_pedal(tuplet)

    >>> _ = baca.sustain_pedal_staff_padding(container, 4)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Staff.SustainPedalLineSpanner.staff-padding = 4
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    \sustainOn
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                    \sustainOff
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    \sustainOn
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    \sustainOff
                    ]
                }
                \times 4/5
                {
                    a'16
                    \sustainOn
                    r4
                    \sustainOff
                    \revert Staff.SustainPedalLineSpanner.staff-padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides text script color on all leaves:

    >>> def selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = baca.select.phead(result, 0)
    ...     return result
    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.markup(baca.select.pleaf(container, 0), r'\markup "più mosso"')
    >>> _ = baca.markup(selector(container), r'\markup "lo stesso tempo"')
    >>> _ = baca.text_script_color(container, "#red")
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TextScript.color = #red
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    ^ \markup "più mosso"
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    ^ \markup "lo stesso tempo"
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TextScript.color
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Down-overrides text script direction on leaves:

    >>> def selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = baca.select.phead(result, 0)
    ...     return result
    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.markup(baca.select.pleaf(container, 0), r'\markup "più mosso"')
    >>> _ = baca.markup(selector(container), r'\markup "lo stesso tempo"')
    >>> _ = baca.text_script_down(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TextScript.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    ^ \markup "più mosso"
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    ^ \markup "lo stesso tempo"
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TextScript.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides text script padding on leaves:

    >>> def selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = baca.select.phead(result, 0)
    ...     return result
    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.markup(baca.select.pleaf(container, 0), r'\markup "più mosso"')
    >>> _ = baca.markup(selector(container), r'\markup "lo stesso tempo"')
    >>> _ = baca.text_script_padding(container, 4)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TextScript.padding = 4
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    ^ \markup "più mosso"
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    ^ \markup "lo stesso tempo"
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TextScript.padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides text script staff padding on leaves:

    >>> def selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = baca.select.phead(result, 0)
    ...     return result
    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.markup(baca.select.pleaf(container, 0), r'\markup "più mosso"')
    >>> _ = baca.markup(selector(container), r'\markup "lo stesso tempo"')
    >>> _ = baca.text_script_staff_padding(container, n=4)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TextScript.staff-padding = 4
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    ^ \markup "più mosso"
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    ^ \markup "lo stesso tempo"
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TextScript.staff-padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>



..  container:: example

    Up-overrides text script direction on leaves:

    >>> def selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = baca.select.phead(result, 0)
    ...     return result
    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.markup(baca.select.pleaf(container, 0), r'\markup "più mosso"')
    >>> _ = baca.markup(selector(container), r'\markup "lo stesso tempo"')
    >>> _ = baca.text_script_up(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TextScript.direction = #up
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    ^ \markup "più mosso"
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    ^ \markup "lo stesso tempo"
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TextScript.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides text spanner staff padding on all trimmed leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.text_spanner_staff_padding(container, 6)
    >>> _ = baca.text_script_staff_padding(container, 6)
    >>> _ = baca.text_spanner(baca.select.tleaves(container), "pont. => ord.")
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(
    ...     selection, includes=["baca.ily"]
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TextScript.staff-padding = 6
                    \override TextSpanner.staff-padding = 6
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \abjad-dashed-line-with-arrow
                    - \baca-text-spanner-left-text "pont."
                    - \baca-text-spanner-right-text "ord."
                    \startTextSpan
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    \stopTextSpan
                    r4
                    \revert TextScript.staff-padding
                    \revert TextSpanner.staff-padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides tie direction on pitched leaves:

    >>> container = baca.figure(
    ...     [[11, 11, 12], [11, 11, 11], [11]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.stem_up(baca.select.pleaves(container))
    >>> _ = baca.tie(baca.select.pleaf(container, 0))
    >>> _ = baca.tie_down(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 5/4
                    r8
                    \override Stem.direction = #up
                    \override Tie.direction = #down
                    b'16
                    [
                    ~
                    b'16
                    ]
                    c''4
                    ~
                    c''16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/8
                {
                    b'16
                    [
                    b'16
                    ]
                    b'4
                    ~
                    b'16
                    r16
                }
                \times 4/5
                {
                    b'16
                    \revert Stem.direction
                    \revert Tie.direction
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides tie direction on pitched leaves:

    >>> container = baca.figure(
    ...     [[11, 11, 12], [11, 11, 11], [11]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.stem_down(baca.select.pleaves(container))
    >>> _ = baca.tie_up(baca.select.pleaves(container))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 5/4
                    r8
                    \override Stem.direction = #down
                    \override Tie.direction = #up
                    b'16
                    [
                    b'16
                    ]
                    c''4
                    ~
                    c''16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/8
                {
                    b'16
                    [
                    b'16
                    ]
                    b'4
                    ~
                    b'16
                    r16
                }
                \times 4/5
                {
                    b'16
                    \revert Stem.direction
                    \revert Tie.direction
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides time signature extra offset on leaf 0:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.time_signature_extra_offset(
    ...     abjad.select.rest(container, 0), (-6, 0))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Makes all time signatures transparent:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.time_signature_transparent(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Score.TimeSignature.transparent = ##t
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert Score.TimeSignature.transparent
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides tuplet bracket direction on leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> _ = baca.tuplet_bracket_down(container)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides tuplet bracket extra offset on leaf 0:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.tuplet_bracket_extra_offset(
    ...     abjad.select.leaf(container, 0), (-1, 0))
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \once \override TupletBracket.extra-offset = #'(-1 . 0)
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides tuplet bracket staff padding on leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Override tuplet bracket direction on leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> _ = baca.tuplet_bracket_up(container)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Overrides tuplet number extra offset on leaf 0:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam(container)
    >>> _ = baca.tuplet_bracket_staff_padding(container, 2)
    >>> _ = baca.tuplet_number_extra_offset(
    ...     abjad.select.leaf(container, 0), (-1, 0))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \once \override TupletNumber.extra-offset = #'(-1 . 0)
                    \override TupletBracket.staff-padding = 2
                    \time 11/8
                    r8
                    c'16
                    [
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    af''16
                    [
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

"""


def dummy():
    """
    Read module-level examples.
    """
