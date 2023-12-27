r"""
Examples: hairpins.

..  container:: example

    Conventional dynamics:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(voice, "p < f")
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    ...     baca.hairpin(voice, '"ff" >o niente')
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    ...     baca.hairpin(voice, 'niente o< "ff"')
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    ...     baca.hairpin(voice, '"p" -- f')
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    Effort dynamics crescendo subito, diminuendo subito:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    ...     baca.hairpin(abjad.select.leaves(voice)[:7], '"mp" <| "f"')
    ...     baca.hairpin(abjad.select.leaves(voice)[7:], '"mf" |> "p"')
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    Piece selector groups leaves by time signatures:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(
    ...         voice,
    ...         "p f",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     ),
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(
    ...         voice,
    ...         "p < f >",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(
    ...         voice,
    ...         "p f",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(
    ...         voice,
    ...         "p -- f >",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    ...     baca.hairpin(voice, "f", bookend=False)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    ...     baca.hairpin(voice, "< !")
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     score["Music"].extend("{ c2 r4. c2 r4. }")
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "C4 D4")
    ...     baca.hairpin(
    ...         abjad.select.leaves(voice)[:2],
    ...         "p -- niente",
    ...         abjad.Tweak(r"- \tweak to-barline ##t"),
    ...     )
    ...     baca.hairpin(
    ...         abjad.select.leaves(voice)[2:],
    ...         "f -- niente",
    ...         abjad.Tweak(r"- \tweak to-barline ##t"),
    ...     )
    ...     baca.override.dls_staff_padding(voice, 4)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(
    ...         voice,
    ...         "mf niente o< p",
    ...         bookend=False,
    ...         pieces=baca.select.mgroups(voice, [1, 2, 1]),
    ...     )
    ...     baca.override.dls_staff_padding(voice, 4)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.hairpin(voice, "(mp) < mf")
    ...     baca.override.dls_staff_padding(voice, 4)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
