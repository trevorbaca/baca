r"""
Articulations.

..  container:: example

    **ACCENT.** Attaches accent to pitched head 0:

    >>> stack = baca.stack(
    ...     baca.figure(
    ...         [1, 1, 5, -1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         restart_talea=True,
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.accent(),
    ...     baca.tuplet_bracket_staff_padding(2),
    ... )
    >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
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
                    - \accent
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

    **ALTERNATE BOW STROKES.** Attaches alternate bow strokes to pitched heads
    (down-bow first):

    >>> stack = baca.stack(
    ...     baca.figure(
    ...         [1, 1, 5, -1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         restart_talea=True,
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.alternate_bow_strokes(downbow_first=True),
    ...     baca.tuplet_bracket_staff_padding(2),
    ... )
    >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
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
                    - \downbow
                    [
                    d'16
                    - \upbow
                    ]
                    bf'4
                    - \downbow
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \upbow
                    [
                    e''16
                    - \downbow
                    ]
                    ef''4
                    - \upbow
                    ~
                    ef''16
                    r16
                    af''16
                    - \downbow
                    [
                    g''16
                    - \upbow
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \downbow
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

    Attaches alternate bow strokes to pitched heads (up-bow first):

    >>> stack = baca.stack(
    ...     baca.figure(
    ...         [1, 1, 5, -1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         restart_talea=True,
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.alternate_bow_strokes(downbow_first=False),
    ...     baca.tuplet_bracket_staff_padding(6),
    ... )
    >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
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
                    \override TupletBracket.staff-padding = 6
                    \time 11/8
                    r8
                    c'16
                    - \upbow
                    [
                    d'16
                    - \downbow
                    ]
                    bf'4
                    - \upbow
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \downbow
                    [
                    e''16
                    - \upbow
                    ]
                    ef''4
                    - \downbow
                    ~
                    ef''16
                    r16
                    af''16
                    - \upbow
                    [
                    g''16
                    - \downbow
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \upbow
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

    Attaches alternate full bow strokes to pitched heads:

    >>> stack = baca.stack(
    ...     baca.figure(
    ...         [1, 1, 5, -1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         restart_talea=True,
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.alternate_bow_strokes(full=True),
    ...     baca.tuplet_bracket_staff_padding(6),
    ... )
    >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
    >>> lilypond_file = abjad.illustrators.selection(selection, includes=["baca.ily"])
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
                    \override TupletBracket.staff-padding = 6
                    \time 11/8
                    r8
                    c'16
                    - \baca-full-downbow
                    [
                    d'16
                    - \baca-full-upbow
                    ]
                    bf'4
                    - \baca-full-downbow
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    - \baca-full-upbow
                    [
                    e''16
                    - \baca-full-downbow
                    ]
                    ef''4
                    - \baca-full-upbow
                    ~
                    ef''16
                    r16
                    af''16
                    - \baca-full-downbow
                    [
                    g''16
                    - \baca-full-upbow
                    ]
                }
                \times 4/5
                {
                    a'16
                    - \baca-full-downbow
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    **STACCATO.** Attaches staccato to pitched head 0:

    >>> stack = baca.stack(
    ...     baca.figure(
    ...         [1, 1, 5, -1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         restart_talea=True,
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.staccato(),
    ...     baca.tuplet_bracket_staff_padding(2),
    ... )
    >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
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
                    - \staccato
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
    Makes Sphinx read this module.
    """
    pass
