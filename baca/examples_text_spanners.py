r"""
Examples: text spanners.

..  container:: example

    1-piece spanners.

    Dashed line with arrow:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(voice, "pont. => ord.")
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(voice, "pont. =| ord.")
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(voice, "pont. -> ord.")
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(voice, "pont. -| ord.")
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(voice, "pont. || ord.")
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    Invisible line with null markup:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(voice, r"pont. || \markup \null")
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
                    [
                    - \baca-invisible-line
                    - \baca-text-spanner-left-text "pont."
                    - \baca-text-spanner-right-markup \markup \null
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
    ...     baca.text_spanner(
    ...         voice,
    ...         "A || B",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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
                    - \baca-invisible-line
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
                    - \baca-invisible-line
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(
    ...         voice,
    ...         "A -> B ->",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(
    ...         voice,
    ...         "A || B",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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
                    - \baca-invisible-line
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
                    - \baca-invisible-line
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(
    ...         voice,
    ...         "A -> B ->",
    ...         bookend=True,
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     score["Music"].extend("{ c2 c4. c2 c4. }")
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "C4 D4 E4 F4")
    ...     baca.text_spanner(
    ...         voice,
    ...         "P -> T ->",
    ...         (abjad.Tweak(r"- \tweak color #red"), 0),
    ...         (abjad.Tweak(r"- \tweak color #blue"), 1),
    ...         (abjad.Tweak(r"- \tweak color #green"), 2),
    ...         (abjad.Tweak(r"- \tweak color #purple"), 3),
    ...         final_piece_spanner=False,
    ...         pieces=baca.select.plts(voice),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                        - \tweak staff-padding 8
                        ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(
    ...             baca.select.rmleaves(voice, 2),
    ...             r"\baca-damp-markup =|",
    ...             bookend=False,
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_even_divisions(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    ...     baca.text_spanner(
    ...         voice,
    ...         "A -| B -|",
    ...         pieces=baca.select.cmgroups(voice, [1]),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     baca.override.dls_staff_padding(voice, 5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     music = baca.make_notes(time_signatures())
    ...     score["Music"].extend(music)
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "C4 D4 E4 F4 G4 A4")
    ...     baca.text_spanner(
    ...         voice,
    ...         "P -> T -> P",
    ...         pieces=baca.select.plts(voice),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
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
                    - \tweak staff-padding 8
                    ^ \markup \transparent A
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
                    - \baca-invisible-line
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(1)
    ...     time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 12))(score)
    ...     score["Music"].extend("{ c2 c4. c2 c4 ~ c8 }")
    ...     voice = score["Music"]
    ...     baca.pitches(voice, "C4 D4 E4 F4")
    ...     baca.text_spanner(
    ...         voice,
    ...         "P -> T ->",
    ...         final_piece_spanner=False,
    ...         pieces=baca.select.plts(voice),
    ...     )
    ...     baca.override.text_spanner_staff_padding(voice, 4.5)
    ...     strut = abjad.Markup(r"\markup \transparent A")
    ...     bundle = abjad.bundle(strut, r"- \tweak staff-padding 8")
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     abjad.attach(bundle, leaf, direction=abjad.UP)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(lilypond_file["Score"])
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
                        - \tweak staff-padding 8
                        ^ \markup \transparent A
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
