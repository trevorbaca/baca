r"""
articulations.py examples.

..  container:: example

    **COLOR FINGERINGS.**

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> baca.interpret.set_up_score(
    ...     score,
    ...     accumulator,
    ...     accumulator.manifests(),
    ...     accumulator.time_signatures,
    ...     docs=True,
    ... )
    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> accumulator(
    ...     "Music",
    ...     baca.pitch("E4"),
    ...     baca.color_fingerings(numbers=[0, 1, 2, 1]),
    ... )
    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     accumulator.manifests(),
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

    **STOP-ON-STRING.** Attaches stop-on-string to pitched head -1:

    >>> stack = baca.stack(
    ...     baca.figure(
    ...         [1, 1, 5, -1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         restart_talea=True,
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.stop_on_string(
    ...         selector=lambda _: baca.select.pleaf(_, -1),
    ...     ),
    ...     baca.tuplet_bracket_staff_padding(2),
    ... )
    >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
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
                    - \baca-stop-on-string
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