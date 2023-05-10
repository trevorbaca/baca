r"""
Examples: commands.

..  container:: example

    Bow contact points. Tweaks LilyPond ``TextSpanner`` grob:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 16))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.bcps(
    ...     voice,
    ...     [(1, 5), (2, 5)],
    ...     abjad.Tweak(r"- \tweak color #red"),
    ...     abjad.Tweak(r"- \tweak staff-padding 2.5"),
    ... )
    >>> _ = baca.pitches(voice, "E4 F4")
    >>> _ = baca.script_staff_padding(voice, 5)
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    Style LilyPond ``Script`` grob with overrides (instead of tweaks).

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Script.staff-padding = 5
                    e'8
                    - \downbow
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    ]
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    ]
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    ]
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    - \baca-bcp-spanner-right-text #2 #5
                    \bacaStartTextSpanBCP
                    f'8
                    \bacaStopTextSpanBCP
                    ]
                    \revert Script.staff-padding
                }
            >>
        }

..  container:: example

    PATTERN. Define chunkwise spanners like this:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 16))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.bcps(voice[:7], bcps=[(1, 5), (2, 5)])
    >>> _ = baca.bcps(voice[7:], bcps=[(3, 5), (4, 5)])
    >>> _ = baca.pitches(voice, "E4 F4")
    >>> _ = baca.script_staff_padding(voice, 5.5)
    >>> _ = baca.text_spanner_staff_padding(voice, 2.5)
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Script.staff-padding = 5.5
                    \override TextSpanner.staff-padding = 2.5
                    e'8
                    - \downbow
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    ]
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    - \baca-bcp-spanner-right-text #1 #5
                    \bacaStartTextSpanBCP
                    e'8
                    \bacaStopTextSpanBCP
                    ]
                    f'8
                    - \downbow
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #3 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #4 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #3 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    ]
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #4 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #3 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #4 #5
                    - \baca-bcp-spanner-right-text #3 #5
                    \bacaStartTextSpanBCP
                    f'8
                    \bacaStopTextSpanBCP
                    ]
                    \revert Script.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    **COLOR FINGERINGS.**

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "E4")
    >>> _ = baca.color_fingerings(voice, numbers=[0, 1, 2, 1])
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    e'2
                    e'4.
                    ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                    e'2
                    ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }
                    e'4.
                    ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                }
            >>
        }

..  container:: example

    Effort dynamics:

    >>> note = abjad.Note("c'4")
    >>> lilypond_file = abjad.illustrators.components([note], includes=["baca.ily"])
    >>> _ = baca.dynamic(note, '"f"')
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    \time 1/4
                    c'4
                    \baca-effort-f
                }
            }
        }

..  container:: example

    Works with hairpins:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 13))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> pleaf = baca.select.pleaf(voice, 0)
    >>> _ = baca.dynamic(pleaf, "p")
    >>> _ = baca.dynamic(pleaf, "<")
    >>> _ = baca.dynamic(baca.select.pleaf(voice, -1), "!")
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
                    \baca-new-spacing-section #1 #13
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #13
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #13
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #13
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

    Works with tweaks:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.dynamic(
    ...     baca.select.pleaf(voice, 0),
    ...     "p",
    ...     abjad.Tweak(r"- \tweak extra-offset #'(-4 . 0)"),
    ... )
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
                    - \tweak extra-offset #'(-4 . 0)
                    \p
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

    Force accidentals. Inverts edition-specific tags:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_notes(time_signatures(), repeat_ties=True)
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 F4")
    >>> baca.force_accidental(
    ...     baca.select.pleaves(voice)[:2], tag=baca.tags.NOT_PARTS
    ... )
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
                    e'2
                    %@% e'!2
                    f'4.
                    %@% f'!4.
                    e'2
                    f'4.
                }
            >>
        }

..  container:: example

    Attaches short instrument name.

    >>> short_instrument_names = {}
    >>> markup = abjad.Markup(r"\markup Fl.")
    >>> short_instrument_names["Fl."] = abjad.ShortInstrumentName(markup)
    >>> manifests = {"abjad.ShortInstrumentName": short_instrument_names}
    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_notes(time_signatures(), repeat_ties=True)
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.short_instrument_name(voice[0], "Fl.", manifests)
    >>> _ = baca.pitches(voice, "E4 F4")
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
                    \set Staff.shortInstrumentName = \markup Fl.
                    e'2
                    f'4.
                    e'2
                    f'4.
                }
            >>
        }

..  container:: example

    Single-line staff with percussion clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef(voice[0], "percussion")
    >>> _ = baca.staff_lines(voice[0], 1)
    >>> _ = baca.staff_positions(voice, [-2, -1, 0, 1, 2])
    >>> _ = baca.section.remove_redundant_time_signatures(score)
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(0 . 0)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 1
                    \startStaff
                    \clef "percussion"
                    a4.
                    b4.
                    c'4.
                    d'4.
                    e'4.
                }
            >>
        }


    Single-line staff with bass clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef(voice[0], "bass")
    >>> _ = baca.staff_lines(voice[0], 1)
    >>> _ = baca.staff_positions(voice, [-2, -1, 0, 1, 2])
    >>> _ = baca.section.remove_redundant_time_signatures(score)
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(0 . 0)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 1
                    \startStaff
                    \clef "bass"
                    b,4.
                    c4.
                    d4.
                    e4.
                    f4.
                }
            >>
        }

..  container:: example

    Two-line staff with percussion clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef(voice[0], "percussion")
    >>> _ = baca.staff_lines(voice[0], 2)
    >>> _ = baca.staff_positions(voice, [-2, -1, 0, 1, 2])
    >>> _ = baca.section.remove_redundant_time_signatures(score)
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 2
                    \startStaff
                    \clef "percussion"
                    a4.
                    b4.
                    c'4.
                    d'4.
                    e'4.
                }
            >>
        }

    Two-line staff with bass clef; clef set before staff positions:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef(voice[0], "bass")
    >>> _ = baca.staff_lines(voice[0], 2)
    >>> _ = baca.staff_positions(voice, [-2, -1, 0, 1, 2])
    >>> _ = baca.section.remove_redundant_time_signatures(score)
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 2
                    \startStaff
                    \clef "bass"
                    b,4.
                    c4.
                    d4.
                    e4.
                    f4.
                }
            >>
        }

    Two-line staff with bass clef; staff positions set before clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.staff_lines(voice[0], 2)
    >>> _ = baca.staff_positions(voice, [-2, -1, 0, 1, 2])
    >>> _ = baca.clef(voice[0], "bass")
    >>> _ = baca.section.remove_redundant_time_signatures(score)
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 2
                    \startStaff
                    \clef "bass"
                    g'4.
                    a'4.
                    b'4.
                    c''4.
                    d''4.
                }
            >>
        }

..  container:: example

    Colors leaves:

    >>> container = abjad.Container("c'4 d' e'")
    >>> baca.color(container)
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \abjad-color-music #'red
                        \time 3/4
                        c'4
                        \abjad-color-music #'blue
                        d'4
                        \abjad-color-music #'red
                        e'4
                    }
                }
            }
        }

..  container:: example

    Attaches cross-staff command to last two pitched leaves:

    >>> score = baca.docs.make_empty_score(1, 1)
    >>> time_signatures = baca.section.wrap([(4, 4)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = abjad.Container("e'4 f' g' a'")[:]
    >>> score["Music.1"].extend(music)
    >>> music = abjad.Container("c'4 d' e' f'")[:]
    >>> score["Music.2"].extend(music)
    >>> _ = baca.cross_staff(baca.select.pleaves(score["Music.2"])[-2:])
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context StaffGroup = "StaffGroup"
            <<
                \context Staff = "Staff.1"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/4
                        s1 * 4/4
                    }
                    \context Voice = "Music.1"
                    {
                        e'4
                        f'4
                        g'4
                        a'4
                    }
                >>
                \context Staff = "Staff.2"
                {
                    \context Voice = "Music.2"
                    {
                        c'4
                        d'4
                        \crossStaff
                        e'4
                        \crossStaff
                        f'4
                    }
                }
            >>
        }

..  container:: example

    Makes finger pressure transition glissando.

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "C5")
    >>> notes = abjad.select.notes(voice)
    >>> _ = baca.note_head_style_harmonic(notes[0])
    >>> _ = baca.note_head_style_harmonic(notes[2])
    >>> baca.finger_pressure_transition(notes[:2])
    >>> baca.finger_pressure_transition(notes[2:])
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    \once \override NoteHead.style = #'harmonic
                    c''2
                    - \tweak arrow-length 2
                    - \tweak arrow-width 0.5
                    - \tweak bound-details.right.arrow ##t
                    - \tweak thickness 3
                    \glissando
                    c''4.
                    \once \override NoteHead.style = #'harmonic
                    c''2
                    - \tweak arrow-length 2
                    - \tweak arrow-width 0.5
                    - \tweak bound-details.right.arrow ##t
                    - \tweak thickness 3
                    \glissando
                    c''4.
                }
            >>
        }

..  container:: example

    Glissando works with tweaks:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> baca.glissando(
    ...     voice,
    ...     abjad.Tweak(r"- \tweak color #red"),
    ... )
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    - \tweak color #red
                    \glissando
                    d''8
                    - \tweak color #red
                    \glissando
                    f'8
                    - \tweak color #red
                    \glissando
                    e''8
                    ]
                    - \tweak color #red
                    \glissando
                    g'8
                    [
                    - \tweak color #red
                    \glissando
                    f''8
                    - \tweak color #red
                    \glissando
                    e'8
                    ]
                    - \tweak color #red
                    \glissando
                    d''8
                    [
                    - \tweak color #red
                    \glissando
                    f'8
                    - \tweak color #red
                    \glissando
                    e''8
                    - \tweak color #red
                    \glissando
                    g'8
                    ]
                    - \tweak color #red
                    \glissando
                    f''8
                    [
                    - \tweak color #red
                    \glissando
                    e'8
                    - \tweak color #red
                    \glissando
                    d''8
                    ]
                }
            >>
        }

..  container:: example

    Glissando works with indexed tweaks:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches(voice, "E4 D5 F4 E5 G4 F5")
    >>> baca.glissando(
    ...     voice,
    ...     (abjad.Tweak(r"- \tweak color #red"), 0),
    ...     (abjad.Tweak(r"- \tweak color #red"), -1),
    ... )
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    - \tweak color #red
                    \glissando
                    d''8
                    \glissando
                    f'8
                    \glissando
                    e''8
                    ]
                    \glissando
                    g'8
                    [
                    \glissando
                    f''8
                    \glissando
                    e'8
                    ]
                    \glissando
                    d''8
                    [
                    \glissando
                    f'8
                    \glissando
                    e''8
                    \glissando
                    g'8
                    ]
                    \glissando
                    f''8
                    [
                    \glissando
                    e'8
                    - \tweak color #red
                    \glissando
                    d''8
                    ]
                }
            >>
        }

..  container:: example

    Attaches ``\baca-invisible-music`` literal to middle leaves:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "C5")
    >>> _ = baca.invisible_music(baca.select.leaves(voice)[1:-1])
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    c''2
                    \abjad-invisible-music-coloring
                    c''4.
                    \abjad-invisible-music-coloring
                    c''2
                    c''4.
                }
            >>
        }

..  container:: example

    Labels pitch names:

    >>> container = abjad.Container("c'4 d' e'")
    >>> abjad.label.with_pitches(container, locale="us")
    >>> lilypond_file = abjad.illustrators.components([container])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        c'4
                        ^ \markup { C4 }
                        d'4
                        ^ \markup { D4 }
                        e'4
                        ^ \markup { E4 }
                    }
                }
            }
        }

..  container:: example

    Assigns parts.

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> music = baca.make_notes(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.assign_part(voice, baca.parts.PartAssignment("Music"))
    >>> _ = baca.pitch(voice, "E4")
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

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
                {   %*% PartAssignment('Music')
                    e'2
                    e'4.
                    e'2
                    e'4.
                }   %*% PartAssignment('Music')
            }
        >>
    }

..  container:: example

    **STOP-ON-STRING.**

    >>> container = abjad.Container("c'4 d' e'")
    >>> _ = baca.stop_on_string(container[0])
    >>> lilypond_file = abjad.illustrators.components([container], includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    {
                        \time 3/4
                        c'4
                        - \baca-stop-on-string
                        d'4
                        e'4
                    }
                }
            }
        }

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
