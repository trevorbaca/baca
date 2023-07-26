r"""
Examples: piecewise.

..  container:: example

    Conventional dynamics:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(voice, "p < f", bookend=-1)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \p
                    [
                    \<
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \f
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Effort dynamic al niente:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.hairpin(voice, '"ff" >o niente')
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \baca-effort-ff
                    [
                    - \tweak circled-tip ##t
                    - \tweak to-barline ##t
                    \>
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \!
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Effort dynamic dal niente:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.hairpin(voice, 'niente o< "ff"')
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \!
                    [
                    - \tweak circled-tip ##t
                    \<
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \baca-effort-ff
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Effort dynamic constante:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.hairpin(voice, '"p" -- f')
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \baca-effort-p
                    [
                    - \tweak stencil #constante-hairpin
                    \<
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \f
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Effort dynamics crescendo subito, decrescendo subito:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.hairpin(baca.select.leaves(voice)[:7], '"mp" <| "f"')
    >>> _ = baca.hairpin(baca.select.leaves(voice)[7:], '"mf" |> "p"')
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \baca-effort-mp
                    [
                    - \tweak stencil #abjad-flared-hairpin
                    \<
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    \baca-effort-f
                    ]
                    d''8
                    \baca-effort-mf
                    [
                    - \tweak stencil #abjad-flared-hairpin
                    \>
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \baca-effort-p
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Piece selector groups leaves by time_signatures:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(
    ...         voice,
    ...         "p f",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     ),
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \p
                    [
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    \f
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    \p
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    \f
                    [
                    e'8
                    d''8
                    \p
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

    With hairpins:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(
    ...         voice,
    ...         "p < f >",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \p
                    [
                    \<
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    \f
                    [
                    \>
                    f''8
                    e'8
                    ]
                    d''8
                    \p
                    [
                    \<
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    \f
                    [
                    \>
                    e'8
                    d''8
                    \p
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

    Bookends each piece:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(
    ...         voice,
    ...         "p f",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \p
                    [
                    d''8
                    f'8
                    e''8
                    \f
                    ]
                    g'8
                    \f
                    [
                    f''8
                    e'8
                    \p
                    ]
                    d''8
                    \p
                    [
                    f'8
                    e''8
                    g'8
                    \f
                    ]
                    f''8
                    \f
                    [
                    e'8
                    d''8
                    \p
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

    With hairpins:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(
    ...         voice,
    ...         "p -- f >",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \p
                    [
                    - \tweak stencil #constante-hairpin
                    \<
                    d''8
                    f'8
                    e''8
                    \f
                    ]
                    g'8
                    \f
                    [
                    \>
                    f''8
                    e'8
                    \p
                    ]
                    d''8
                    \p
                    [
                    - \tweak stencil #constante-hairpin
                    \<
                    f'8
                    e''8
                    g'8
                    \f
                    ]
                    f''8
                    \f
                    [
                    \>
                    e'8
                    d''8
                    \p
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    REGRESSION. Works with lone dynamic:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.hairpin(voice, "f", bookend=False)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    \f
                    [
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    REGRESSION. Works with lone hairpin:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.hairpin(voice, "< !")
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    [
                    \<
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \!
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    REGRESSION. Works with to-barline tweak:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.parse("{ c2 r4. c2 r4. }")
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "C4 D4")
    >>> _ = baca.hairpin(
    ...         baca.select.leaves(voice)[:2],
    ...         "p -- niente",
    ...         abjad.Tweak(r"- \tweak to-barline ##t"),
    ...     )
    >>> _ = baca.hairpin(
    ...         baca.select.leaves(voice)[2:],
    ...         "f -- niente",
    ...         abjad.Tweak(r"- \tweak to-barline ##t"),
    ...     )
    >>> _ = baca.dls_staff_padding(voice, 4)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {
                        \override DynamicLineSpanner.staff-padding = 4
                        c'2
                        \p
                        - \tweak stencil #constante-hairpin
                        - \tweak to-barline ##t
                        \<
                        r4.
                        \!
                        d'2
                        \f
                        - \tweak stencil #constante-hairpin
                        - \tweak to-barline ##t
                        \<
                        r4.
                        \!
                        \revert DynamicLineSpanner.staff-padding
                    }
                }
            >>
        }

..  container:: example

    Works with interposed niente dynamics:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(
    ...         voice,
    ...         "mf niente o< p",
    ...         bookend=False,
    ...         pieces=baca.select.mgroups(voice, [1, 2, 1]),
    ...     )
    >>> _ = baca.dls_staff_padding(voice, 4)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 4
                    e'8
                    \mf
                    [
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    \!
                    [
                    - \tweak circled-tip ##t
                    \<
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    \p
                    [
                    e'8
                    d''8
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Works with parenthesized dynamics:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.hairpin(voice, "(mp) < mf")
    >>> _ = baca.dls_staff_padding(voice, 4)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 4
                    e'8
                    \baca-mp-parenthesized
                    [
                    \<
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \mf
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Text spanner examples.

    1-piece spanners.

    Dashed line with arrow:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(voice, "pont. => ord.")
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-dashed-line-with-arrow
                    - \baca-text-spanner-left-text "pont."
                    - \baca-text-spanner-right-text "ord."
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    Dashed line with hook:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(voice, "pont. =| ord.")
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-dashed-line-with-hook
                    - \baca-text-spanner-left-text "pont."
                    - \tweak bound-details.right.text \markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75 \general-align #Y #1 \upright ord. }
                    - \tweak bound-details.right.padding 1.25
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    Solid line with arrow:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(voice, "pont. -> ord.")
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "pont."
                    - \baca-text-spanner-right-text "ord."
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    Solid line with hook:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(voice, "pont. -| ord.")
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-solid-line-with-hook
                    - \baca-text-spanner-left-text "pont."
                    - \tweak bound-details.right.text \markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75 \general-align #Y #1 \upright ord. }
                    - \tweak bound-details.right.padding 1.25
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    Invisible lines:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(voice, "pont. || ord.")
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-invisible-line
                    - \baca-text-spanner-left-text "pont."
                    - \baca-text-spanner-right-text "ord."
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Piece selector groups leaves by time_signatures:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "A || B",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-invisible-line
                    - \baca-text-spanner-left-text "A"
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    \stopTextSpan
                    [
                    - invisible-line
                    - \baca-text-spanner-left-text "B"
                    \startTextSpan
                    f''8
                    e'8
                    ]
                    d''8
                    \stopTextSpan
                    [
                    - \baca-invisible-line
                    - \baca-text-spanner-left-text "A"
                    \startTextSpan
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    \stopTextSpan
                    [
                    - invisible-line
                    - \baca-text-spanner-left-text "B"
                    - \baca-text-spanner-right-text "A"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert DynamicLineSpanner.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    With spanners:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "A -> B ->",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "A"
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    \stopTextSpan
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "B"
                    \startTextSpan
                    f''8
                    e'8
                    ]
                    d''8
                    \stopTextSpan
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "A"
                    \startTextSpan
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    \stopTextSpan
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "B"
                    - \baca-text-spanner-right-text "A"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert DynamicLineSpanner.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    Bookends each piece:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "A || B",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-invisible-line
                    - \baca-text-spanner-left-text "A"
                    - \baca-text-spanner-right-text "B"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    \stopTextSpan
                    ]
                    g'8
                    [
                    - invisible-line
                    - \baca-text-spanner-left-text "B"
                    - \baca-text-spanner-right-text "A"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    f''8
                    e'8
                    \stopTextSpan
                    ]
                    d''8
                    [
                    - \baca-invisible-line
                    - \baca-text-spanner-left-text "A"
                    - \baca-text-spanner-right-text "B"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    f'8
                    e''8
                    g'8
                    \stopTextSpan
                    ]
                    f''8
                    [
                    - invisible-line
                    - \baca-text-spanner-left-text "B"
                    - \baca-text-spanner-right-text "A"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert DynamicLineSpanner.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

    With spanners:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "A -> B ->",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "A"
                    - \baca-text-spanner-right-text "B"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    \stopTextSpan
                    ]
                    g'8
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "B"
                    - \baca-text-spanner-right-text "A"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    f''8
                    e'8
                    \stopTextSpan
                    ]
                    d''8
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "A"
                    - \baca-text-spanner-right-text "B"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    f'8
                    e''8
                    g'8
                    \stopTextSpan
                    ]
                    f''8
                    [
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "B"
                    - \baca-text-spanner-right-text "A"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert DynamicLineSpanner.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Indexes tweaks. No purple appears because tweakable indicators appear on pieces
    0, 1, 2 but piece 3 carries only a stop text span:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.parse("{ c2 c4. c2 c4. }")
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "C4 D4 E4 F4")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "P -> T ->",
    ...         (abjad.Tweak(r"- \tweak color #red"), 0),
    ...         (abjad.Tweak(r"- \tweak color #blue"), 1),
    ...         (abjad.Tweak(r"- \tweak color #green"), 2),
    ...         (abjad.Tweak(r"- \tweak color #purple"), 3),
    ...         final_piece_spanner=False,
    ...         pieces=baca.select.plts(voice),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {
                        \override TextSpanner.staff-padding = 4.5
                        c'2
                        - \baca-solid-line-with-arrow
                        - \baca-text-spanner-left-text "P"
                        - \tweak color #red
                        \startTextSpan
                        d'4.
                        \stopTextSpan
                        - \baca-solid-line-with-arrow
                        - \baca-text-spanner-left-text "T"
                        - \tweak color #blue
                        \startTextSpan
                        e'2
                        \stopTextSpan
                        - \baca-solid-line-with-arrow
                        - \baca-text-spanner-left-text "P"
                        - \baca-text-spanner-right-text "T"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        - \tweak color #green
                        \startTextSpan
                        f'4.
                        \stopTextSpan
                        \revert TextSpanner.staff-padding
                    }
                }
            >>
        }

..  container:: example

    REGRESSION. Handles backslashed markup correctly:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(
    ...         baca.select.rmleaves(voice, 2),
    ...         r"\baca-damp-markup =|",
    ...         bookend=False,
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-dashed-line-with-hook
                    - \baca-text-spanner-left-markup \baca-damp-markup
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    \stopTextSpan
                    [
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    ]
                    \revert DynamicLineSpanner.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    REGRESSION. Kerns bookended hooks:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "A -| B -|",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> _ = baca.dls_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    \override TextSpanner.staff-padding = 4.5
                    e'8
                    [
                    - \baca-solid-line-with-hook
                    - \baca-text-spanner-left-text "A"
                    \startTextSpan
                    d''8
                    f'8
                    e''8
                    ]
                    g'8
                    \stopTextSpan
                    [
                    - \baca-solid-line-with-hook
                    - \baca-text-spanner-left-text "B"
                    \startTextSpan
                    f''8
                    e'8
                    ]
                    d''8
                    \stopTextSpan
                    [
                    - \baca-solid-line-with-hook
                    - \baca-text-spanner-left-text "A"
                    \startTextSpan
                    f'8
                    e''8
                    g'8
                    ]
                    f''8
                    \stopTextSpan
                    [
                    - \baca-solid-line-with-hook
                    - \baca-text-spanner-left-text "B"
                    - \tweak bound-details.right.text \markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75 \general-align #Y #1 \upright A }
                    - \tweak bound-details.right.padding 1.25
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    e'8
                    d''8
                    \stopTextSpan
                    ]
                    \revert DynamicLineSpanner.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    REGRESSION. Backsteals left text from length-1 final piece:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "C4 D4 E4 F4 G4 A4")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "P -> T -> P",
    ...         pieces=baca.select.plts(voice),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override TextSpanner.staff-padding = 4.5
                    c'2
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "P"
                    \startTextSpan
                    d'4.
                    \stopTextSpan
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "T"
                    \startTextSpan
                    e'2
                    \stopTextSpan
                    - invisible-line
                    - \baca-text-spanner-left-text "P"
                    \startTextSpan
                    f'4.
                    \stopTextSpan
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "P"
                    \startTextSpan
                    g'2
                    \stopTextSpan
                    - \baca-solid-line-with-arrow
                    - \baca-text-spanner-left-text "T"
                    - \baca-text-spanner-right-text "P"
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    \startTextSpan
                    a'4.
                    \stopTextSpan
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    REGRESSION. Backsteals left text from spannerless final piece:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.parse("{ c2 c4. c2 c4 ~ c8 }")
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "C4 D4 E4 F4")
    >>> _ = baca.text_spanner(
    ...         voice,
    ...         "P -> T ->",
    ...         final_piece_spanner=False,
    ...         pieces=baca.select.plts(voice),
    ...     )
    >>> _ = baca.text_spanner_staff_padding(voice, 4.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
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
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    {
                        \override TextSpanner.staff-padding = 4.5
                        c'2
                        - \baca-solid-line-with-arrow
                        - \baca-text-spanner-left-text "P"
                        \startTextSpan
                        d'4.
                        \stopTextSpan
                        - \baca-solid-line-with-arrow
                        - \baca-text-spanner-left-text "T"
                        \startTextSpan
                        e'2
                        \stopTextSpan
                        - \baca-solid-line-with-arrow
                        - \baca-text-spanner-left-text "P"
                        - \baca-text-spanner-right-text "T"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'4
                        \stopTextSpan
                        ~
                        f'8
                        \revert TextSpanner.staff-padding
                    }
                }
            >>
        }

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
