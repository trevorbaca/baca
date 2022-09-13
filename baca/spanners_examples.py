r"""
spanners.py examples

..  container:: example

    Beams everything and sets beam direction down:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier(fallback_duration=(1, 12))(score)

    >>> music = baca.make_even_divisions_function(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "C4")
    >>> _ = baca.beam(voice, direction=abjad.DOWN)

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
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
                    c'8
                    _ [
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    ]
                }
            >>
        }

..  container:: example

    Attaches ottava indicators to trimmed leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.ottava(baca.select.tleaves(container))
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
                    \ottava 1
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
                    \ottava 0
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches ottava bassa indicators to trimmed leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.ottava_bassa(baca.select.tleaves(container))
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
                    \ottava -1
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
                    \ottava 0
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches slur to trimmed leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.slur(baca.select.tleaves(container))
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
                    )
                    r4
                    \revert Slur.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Pedals leaves:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.sustain_pedal(container)
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
                    \sustainOff
                    \revert Staff.SustainPedalLineSpanner.staff-padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches trill spanner to trimmed leaves (leaked to the right):

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.trill_spanner(baca.select.tleaves(container, rleak=True))
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
                    \startTrillSpan
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
                    \stopTrillSpan
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches trill to trimmed leaves (leaked to the right) in every
    run:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> for run in baca.select.runs(container):
    ...     run = baca.select.rleak(run)
    ...     _ = baca.trill_spanner(run)

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
                    \startTrillSpan
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                    \stopTrillSpan
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    \startTrillSpan
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    \stopTrillSpan
                    af''16
                    [
                    \startTrillSpan
                    g''16
                    ]
                }
                \times 4/5
                {
                    a'16
                    r4
                    \stopTrillSpan
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Tweaks trill spanner:

    >>> container = baca.figure(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.trill_spanner(
    ...     baca.select.tleaves(container, rleak=True),
    ...     abjad.Tweak(r"- \tweak color #red"),
    ...     alteration="M2",
    ... )
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
                    \pitchedTrill
                    c'16
                    [
                    - \tweak color #red
                    \startTrillSpan d'
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
                    \stopTrillSpan
                    \revert TupletBracket.staff-padding
                }
            }
        >>

"""


def dummy():
    """
    Read module-level examples.
    """
