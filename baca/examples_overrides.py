r"""
Examples: overrides.

..  container:: example

    Overrides bar line transparency:

    >>> def make_rhythm(time_signatures):
    ...     durations = [_.duration for _ in time_signatures]
    ...     nested_music = rmakers.talea(durations, [1, 1, 1, -1], 8)
    ...     voice = rmakers.wrap_in_time_signature_staff(nested_music, time_signatures)
    ...     rmakers.beam(voice)
    ...     rmakers.extract_trivial(voice)
    ...     music = abjad.mutate.eject_contents(voice)
    ...     return music

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     music = make_rhythm(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.bar_line_transparent(
    ...             abjad.select.group_by_measure(voice)[1]
    ...     )
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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

    >>> def make_score():
    ...     collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     tuplets = [baca.prolate(_, "5:4") for _ in tuplets]
    ...     tuplets[0].insert(0, "r8")
    ...     tuplets[-1].append("r4")
    ...     pleaves = baca.select.pleaves(tuplets)
    ...     baca.stem_up(pleaves)
    ...     rmakers.beam(tuplets)
    ...     baca.beam_positions(tuplets, 6)
    ...     baca.tuplet_bracket_staff_padding(tuplets, 4)
    ...     score = baca.docs.make_single_staff_score(tuplets)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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

    Overrides dynamic line spanner staff padding:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     score = baca.docs.make_single_staff_score([container], voice=True)
    ...     baca.hairpin(container, "p < f")
    ...     baca.dls_staff_padding(container, 4)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \override DynamicLineSpanner.staff-padding = 4
                        \time 3/4
                        c'4
                        \p
                        \<
                        d'4
                        e'4
                        \f
                        \revert DynamicLineSpanner.staff-padding
                    }
                }
            }
        >>

..  container:: example

    Up-overrides dynamic line spanner direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     score = baca.docs.make_single_staff_score([container], voice=True)
    ...     baca.hairpin(container, "p < f")
    ...     baca.dls_staff_padding(container, 4)
    ...     baca.dls_up(container)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \override DynamicLineSpanner.direction = #up
                        \override DynamicLineSpanner.staff-padding = 4
                        \time 3/4
                        c'4
                        \p
                        \<
                        d'4
                        e'4
                        \f
                        \revert DynamicLineSpanner.direction
                        \revert DynamicLineSpanner.staff-padding
                    }
                }
            }
        >>

..  container:: example

    Overrides dynamic text extra offset:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     score = baca.docs.make_single_staff_score([container], voice=True)
    ...     baca.dynamic(container[0], "f")
    ...     baca.dls_staff_padding(container, 4)
    ...     baca.dynamic_text_extra_offset(container[0], (3, 0))
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \once \override DynamicText.extra-offset = #'(3 . 0)
                        \override DynamicLineSpanner.staff-padding = 4
                        \time 3/4
                        c'4
                        \f
                        d'4
                        e'4
                        \revert DynamicLineSpanner.staff-padding
                    }
                }
            }
        >>

..  container:: example

    REGRESSION. Coerces X11 color names:

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     voice = score["Music"]
    ...     music = baca.make_mmrests(time_signatures(), head="Music")
    ...     score["Music"].extend(music)
    ...     baca.mmrest_color(
    ...         baca.select.mmrests(voice)[1:],
    ...         "#(x11-color 'DarkOrchid)",
    ...     )
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                            \abjad-invisible-music-coloring
                            \once \override Accidental.stencil = ##f
                            \once \override NoteColumn.ignore-collision = ##t
                            c'1 * 4/8
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                        }
                    >>
                    \override MultiMeasureRest.color = #(x11-color 'DarkOrchid)
                    R1 * 3/8
                    R1 * 4/8
                    R1 * 3/8
                    \revert MultiMeasureRest.color
                }
            >>
        }

..  container:: example

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     voice = score["Music"]
    ...     music = baca.make_mmrests(time_signatures(), head="Music")
    ...     score["Music"].extend(music)
    ...     baca.markup(
    ...         baca.select.mmrest(voice, 2),
    ...         r"\baca-boxed-markup still",
    ...     )
    ...     baca.mmrest_text_color(baca.select.mmrests(voice)[1:], "#red")
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                            \abjad-invisible-music-coloring
                            \once \override Accidental.stencil = ##f
                            \once \override NoteColumn.ignore-collision = ##t
                            c'1 * 4/8
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                        }
                    >>
                    \override MultiMeasureRestText.color = #red
                    R1 * 3/8
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    R1 * 3/8
                    \revert MultiMeasureRestText.color
                }
            >>
        }

..  container:: example

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     voice = score["Music"]
    ...     music = baca.make_mmrests(time_signatures(), head="Music")
    ...     score["Music"].extend(music)
    ...     baca.markup(
    ...         baca.select.mmrest(voice, 2),
    ...         r"\baca-boxed-markup still",
    ...     )
    ...     baca.mmrest_text_extra_offset(
    ...         baca.select.mmrests(voice)[1:], (0, 2)
    ...     )
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                            \abjad-invisible-music-coloring
                            \once \override Accidental.stencil = ##f
                            \once \override NoteColumn.ignore-collision = ##t
                            c'1 * 4/8
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                        }
                    >>
                    \override MultiMeasureRestText.extra-offset = #'(0 . 2)
                    R1 * 3/8
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    R1 * 3/8
                    \revert MultiMeasureRestText.extra-offset
                }
            >>
        }

..  container:: example

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     voice = score["Music"]
    ...     music = baca.make_mmrests(time_signatures(), head="Music")
    ...     score["Music"].extend(music)
    ...     baca.markup(
    ...         baca.select.mmrest(voice, 2),
    ...         r"\baca-boxed-markup still",
    ...     )
    ...     baca.mmrest_text_padding(baca.select.mmrests(voice)[1:], 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                            \abjad-invisible-music-coloring
                            \once \override Accidental.stencil = ##f
                            \once \override NoteColumn.ignore-collision = ##t
                            c'1 * 4/8
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                        }
                    >>
                    \override MultiMeasureRestText.padding = 2
                    R1 * 3/8
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    R1 * 3/8
                    \revert MultiMeasureRestText.padding
                }
            >>
        }

..  container:: example

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     voice = score["Music"]
    ...     music = baca.make_mmrests(time_signatures(), head="Music")
    ...     score["Music"].extend(music)
    ...     baca.markup(
    ...         baca.select.mmrest(voice, 2),
    ...         r"\baca-boxed-markup still",
    ...     )
    ...     baca.mmrest_text_parent_center(baca.select.mmrests(voice)[1:])
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                            \abjad-invisible-music-coloring
                            \once \override Accidental.stencil = ##f
                            \once \override NoteColumn.ignore-collision = ##t
                            c'1 * 4/8
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                        }
                    >>
                    \override MultiMeasureRestText.parent-alignment-X = 0
                    R1 * 3/8
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    R1 * 3/8
                    \revert MultiMeasureRestText.parent-alignment-X
                }
            >>
        }

..  container:: example

    >>> def make_score():
    ...     score = baca.docs.make_empty_score(1)
    ...     pairs = [(4, 8), (3, 8), (4, 8), (3, 8)]
    ...     time_signatures = baca.section.wrap(pairs)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     voice = score["Music"]
    ...     music = baca.make_mmrests(time_signatures(), head="Music")
    ...     score["Music"].extend(music)
    ...     baca.markup(
    ...         baca.select.mmrest(voice, 2),
    ...         r"\baca-boxed-markup still",
    ...     )
    ...     baca.mmrest_text_staff_padding(baca.select.mmrests(voice)[1:], 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
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
                            \abjad-invisible-music-coloring
                            \once \override Accidental.stencil = ##f
                            \once \override NoteColumn.ignore-collision = ##t
                            c'1 * 4/8
                        }
                        \context Voice = "Rests"
                        {
                            R1 * 4/8
                        }
                    >>
                    \override MultiMeasureRestText.staff-padding = 2
                    R1 * 3/8
                    R1 * 4/8
                    ^ \baca-boxed-markup still
                    R1 * 3/8
                    \revert MultiMeasureRestText.staff-padding
                }
            >>
        }

..  container:: example

    Overrides note-head style:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.note_head_style_cross(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override NoteHead.style = #'cross
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    \revert NoteHead.style
                }
            }
        >>

..  container:: example

    Down-overrides repeat tie direction:

    >>> def make_score():
    ...     voice = abjad.Voice(r"c'4 c' c'", name="Voice")
    ...     baca.repeat_tie(voice[1:])
    ...     baca.repeat_tie_down(voice)
    ...     baca.stem_up(voice)
    ...     score = baca.docs.make_single_staff_score([voice])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    \override RepeatTie.direction = #down
                    \override Stem.direction = #up
                    \time 3/4
                    c'4
                    c'4
                    \repeatTie
                    c'4
                    \repeatTie
                    \revert RepeatTie.direction
                    \revert Stem.direction
                }
            }
        >>

..  container:: example

    Up-overrides repeat tie direction:

    >>> def make_score():
    ...     voice = abjad.Voice(r"c'4 c' c'", name="Voice")
    ...     baca.repeat_tie(voice[1:])
    ...     baca.repeat_tie_down(voice)
    ...     baca.stem_down(voice)
    ...     score = baca.docs.make_single_staff_score([voice])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    \override RepeatTie.direction = #down
                    \override Stem.direction = #down
                    \time 3/4
                    c'4
                    c'4
                    \repeatTie
                    c'4
                    \repeatTie
                    \revert RepeatTie.direction
                    \revert Stem.direction
                }
            }
        >>

..  container:: example

    Down-overrides direction of rests:

    >>> def make_score():
    ...     container = abjad.Container("r8 d'4 e' r8")
    ...     baca.rest_down(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Rest.direction = #down
                    \time 3/4
                    r8
                    d'4
                    e'4
                    r8
                    \revert Rest.direction
                }
            }
        >>

..  container:: example

    Overrides rest position:

    >>> def make_score():
    ...     container = abjad.Container("r8 d'4 e' r8")
    ...     baca.rest_staff_position(container, -6)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Rest.staff-position = -6
                    \time 3/4
                    r8
                    d'4
                    e'4
                    r8
                    \revert Rest.staff-position
                }
            }
        >>

..  container:: example

    Makes rests transparent:

    >>> def make_score():
    ...     container = abjad.Container("r8 d'4 e' r8")
    ...     baca.rest_transparent(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Rest.transparent = ##t
                    \time 3/4
                    r8
                    d'4
                    e'4
                    r8
                    \revert Rest.transparent
                }
            }
        >>

..  container:: example

    Up-overrides rest direction:

    >>> def make_score():
    ...     container = abjad.Container("r8 d'4 e' r8")
    ...     baca.rest_up(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Rest.direction = #up
                    \time 3/4
                    r8
                    d'4
                    e'4
                    r8
                    \revert Rest.direction
                }
            }
        >>

..  container:: example

    Overrides script color:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.accent(container)
    ...     baca.script_color(container, "#red")
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Script.color = #red
                    \time 3/4
                    c'4
                    - \accent
                    d'4
                    - \accent
                    e'4
                    - \accent
                    \revert Script.color
                }
            }
        >>

..  container:: example

    Down-overrides script direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.accent(container)
    ...     baca.script_down(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Script.direction = #down
                    \time 3/4
                    c'4
                    - \accent
                    d'4
                    - \accent
                    e'4
                    - \accent
                    \revert Script.direction
                }
            }
        >>

..  container:: example

    Overrides script extra offset:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.accent(container)
    ...     baca.script_extra_offset(container, (-1.5, 0))
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Script.extra-offset = #'(-1.5 . 0)
                    \time 3/4
                    c'4
                    - \accent
                    d'4
                    - \accent
                    e'4
                    - \accent
                    \revert Script.extra-offset
                }
            }
        >>

..  container:: example

    Up-overrides script direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.accent(container)
    ...     baca.script_up(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Script.direction = #up
                    \time 3/4
                    c'4
                    - \accent
                    d'4
                    - \accent
                    e'4
                    - \accent
                    \revert Script.direction
                }
            }
        >>

..  container:: example

    Down-overrides slur direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.slur(container)
    ...     baca.slur_down([container])
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Slur.direction = #down
                    \time 3/4
                    c'4
                    (
                    d'4
                    e'4
                    )
                    \revert Slur.direction
                }
            }
        >>

..  container:: example

    Up-overrides slur direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.slur(container)
    ...     baca.slur_up([container])
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Slur.direction = #up
                    \time 3/4
                    c'4
                    (
                    d'4
                    e'4
                    )
                    \revert Slur.direction
                }
            }
        >>

..  container:: example

    Overrides stem color:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.stem_color(container, "#red")
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Stem.color = #red
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    \revert Stem.color
                }
            }
        >>

..  container:: example

    Down-overrides stem direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.stem_down(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Stem.direction = #down
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    \revert Stem.direction
                }
            }
        >>

..  container:: example

    Up-overrides stem direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.stem_up(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Stem.direction = #up
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    \revert Stem.direction
                }
            }
        >>

..  container:: example

    Overrides sustain pedal staff padding:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.sustain_pedal(container)
    ...     baca.sustain_pedal_staff_padding(container, 5)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Staff.SustainPedalLineSpanner.staff-padding = 5
                    \time 3/4
                    c'4
                    \sustainOn
                    d'4
                    e'4
                    \sustainOff
                    \revert Staff.SustainPedalLineSpanner.staff-padding
                }
            }
        >>

..  container:: example

    Overrides text script color:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.markup(container[0], r'\markup "più mosso"')
    ...     baca.text_script_color(container, "#red")
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override TextScript.color = #red
                    \time 3/4
                    c'4
                    ^ \markup "più mosso"
                    d'4
                    e'4
                    \revert TextScript.color
                }
            }
        >>

..  container:: example

    Down-overrides text script direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.markup(container[0], r'\markup "più mosso"')
    ...     baca.text_script_down(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override TextScript.direction = #down
                    \time 3/4
                    c'4
                    ^ \markup "più mosso"
                    d'4
                    e'4
                    \revert TextScript.direction
                }
            }
        >>

..  container:: example

    Overrides text script padding:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.markup(container[0], r'\markup "più mosso"')
    ...     baca.text_script_padding(container, 4)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override TextScript.padding = 4
                    \time 3/4
                    c'4
                    ^ \markup "più mosso"
                    d'4
                    e'4
                    \revert TextScript.padding
                }
            }
        >>

..  container:: example

    Overrides text script staff padding:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.markup(container[0], r'\markup "più mosso"')
    ...     baca.text_script_staff_padding(container, n=4)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override TextScript.staff-padding = 4
                    \time 3/4
                    c'4
                    ^ \markup "più mosso"
                    d'4
                    e'4
                    \revert TextScript.staff-padding
                }
            }
        >>

..  container:: example

    Up-overrides text script direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.markup(container[0], r'\markup "più mosso"')
    ...     baca.text_script_up(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override TextScript.direction = #up
                    \time 3/4
                    c'4
                    ^ \markup "più mosso"
                    d'4
                    e'4
                    \revert TextScript.direction
                }
            }
        >>

..  container:: example

    Overrides text spanner staff padding:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.text_spanner_staff_padding(container, 6)
    ...     baca.text_script_staff_padding(container, 6)
    ...     baca.text_spanner(container, "pont. => ord.")
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override TextScript.staff-padding = 6
                    \override TextSpanner.staff-padding = 6
                    \time 3/4
                    c'4
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \abjad-dashed-line-with-arrow
                    - \baca-text-spanner-left-text "pont."
                    - \baca-text-spanner-right-text "ord."
                    \startTextSpan
                    d'4
                    e'4
                    \stopTextSpan
                    \revert TextScript.staff-padding
                    \revert TextSpanner.staff-padding
                }
            }
        >>

..  container:: example

    Down-overrides tie direction:

    >>> def make_score():
    ...     container = abjad.Container("c''4 ~ c'' ~ c''")
    ...     baca.stem_up(container)
    ...     baca.tie_down(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Stem.direction = #up
                    \override Tie.direction = #down
                    \time 3/4
                    c''4
                    ~
                    c''4
                    ~
                    c''4
                    \revert Stem.direction
                    \revert Tie.direction
                }
            }
        >>

..  container:: example

    Up-overrides tie direction:

    >>> def make_score():
    ...     container = abjad.Container("c'4 ~ c' ~ c'")
    ...     baca.stem_down(container)
    ...     baca.tie_up(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Stem.direction = #down
                    \override Tie.direction = #up
                    \time 3/4
                    c'4
                    ~
                    c'4
                    ~
                    c'4
                    \revert Stem.direction
                    \revert Tie.direction
                }
            }
        >>

..  container:: example

    Overrides time signature extra offset:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.time_signature_extra_offset(container[0], (-6, 0))
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)
                    \time 3/4
                    c'4
                    d'4
                    e'4
                }
            }
        >>

..  container:: example

    Makes all time signatures transparent:

    >>> def make_score():
    ...     container = abjad.Container("c'4 d' e'")
    ...     baca.time_signature_transparent(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \override Score.TimeSignature.transparent = ##t
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    \revert Score.TimeSignature.transparent
                }
            }
        >>

..  container:: example

    Down-overrides tuplet bracket direction:

    >>> def make_score():
    ...     container = abjad.Container(r"\times 2/3 { c'4 d' e' }")
    ...     baca.tuplet_bracket_staff_padding(container, 2)
    ...     baca.tuplet_bracket_down(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \times 2/3
                    {
                        \override TupletBracket.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 1/2
                        c'4
                        d'4
                        e'4
                        \revert TupletBracket.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            }
        >>

..  container:: example

    Up-overrides tuplet bracket direction:

    >>> def make_score():
    ...     container = abjad.Container(r"\times 2/3 { c'4 d' e' }")
    ...     baca.tuplet_bracket_staff_padding(container, 2)
    ...     baca.tuplet_bracket_up(container)
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \times 2/3
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \time 1/2
                        c'4
                        d'4
                        e'4
                        \revert TupletBracket.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            }
        >>

..  container:: example

    Overrides tuplet number extra offset:

    >>> def make_score():
    ...     container = abjad.Container(r"\times 2/3 { c'4 d' e' }")
    ...     baca.tuplet_bracket_staff_padding(container, 2)
    ...     baca.tuplet_number_extra_offset(container, (-1, 0))
    ...     score = baca.docs.make_single_staff_score([container])
    ...     return score

    >>> score = make_score()
    >>> lilypond_file = baca.docs.lilypond_file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                {
                    \times 2/3
                    {
                        \override TupletBracket.staff-padding = 2
                        \override TupletNumber.extra-offset = #'(-1 . 0)
                        \time 1/2
                        c'4
                        d'4
                        e'4
                        \revert TupletBracket.staff-padding
                        \revert TupletNumber.extra-offset
                    }
                }
            }
        >>

"""


def sphinx():
    """
    Makes Sphinx read this module.
    """
    pass
