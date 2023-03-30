r"""
rhythm.py examples.

..  container:: example

    Displaced quarter notes:

    >>> time_signatures = 5 * [abjad.TimeSignature((1, 4))]
    >>> container = baca.make_rhythm([-1, 4, 4, 4, 4, -3], 16, time_signatures)
    >>> components = abjad.mutate.eject_contents(container)
    >>> staff = abjad.Staff(components)
    >>> leaf = abjad.select.leaf(staff, 0)
    >>> abjad.attach(time_signatures[0], leaf)
    >>> abjad.show(staff) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            \time 1/4
            r16
            c'8.
            ~
            c'16
            [
            c'8.
            ]
            ~
            c'16
            [
            c'8.
            ]
            ~
            c'16
            [
            c'8.
            ]
            ~
            c'16
            r8.
        }


..  container:: example

    Displaced accelerandi, ritardandi:

    >>> time_signatures = 5 * [abjad.TimeSignature((1, 4))]
    >>> duration = abjad.Duration(1, 4)
    >>> container = baca.make_rhythm([
    ...     -1,
    ...     baca.make_accelerando([1, 1, 1, 1, 1], 16, duration),
    ...     baca.make_accelerando([1, 1, 1, 1, 1], 16, duration, exponent=1.625),
    ...     4,
    ...     baca.make_accelerando([1, 1, 1, 1, 1], 16, duration, exponent=1.625),
    ...     -3
    ...     ],
    ...     16,
    ...     time_signatures
    ... )
    >>> components = abjad.mutate.eject_contents(container)
    >>> staff = abjad.Staff(components, lilypond_type="RhythmicStaff")
    >>> leaf = abjad.select.leaf(staff, 0)
    >>> abjad.attach(time_signatures[0], leaf)
    >>> score = abjad.Score([staff])
    >>> abjad.override(score).TupletBracket.bracket_visibility = True
    >>> abjad.override(score).TupletBracket.padding = 2
    >>> abjad.setting(score).autoBeaming = False
    >>> abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 24)"
    >>> abjad.setting(score).tupletFullLength = True
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 24)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \time 1/4
                r16
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #right
                    c'16 * 7488/5120
                    [
                    c'16 * 4032/5120
                    c'16 * 3328/5120
                    c'16 * 2944/5120
                    c'16 * 2688/5120
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #left
                    c'16 * 1472/5120
                    [
                    c'16 * 3136/5120
                    c'16 * 4288/5120
                    c'16 * 5312/5120
                    c'16 * 6272/5120
                    ]
                }
                \revert TupletNumber.text
                c'8.
                ~
                c'16
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #left
                    c'16 * 1472/5120
                    [
                    c'16 * 3136/5120
                    c'16 * 4288/5120
                    c'16 * 5312/5120
                    c'16 * 6272/5120
                    ]
                }
                \revert TupletNumber.text
                r8.
            }
        >>

..  container:: example

    Ritardando with grace notes:

    >>> duration = abjad.Duration(1, 4)
    >>> tuplet = baca.make_accelerando(
    ...     [
    ...         1, 1,
    ...         baca.GraceSpecifier([1], 1),
    ...         baca.GraceSpecifier([1, 1], 1),
    ...         baca.GraceSpecifier([1, 1, 1], 1),
    ...     ],
    ...     16, duration, exponent=1.625
    ... )
    >>> staff = abjad.Staff([tuplet], lilypond_type="RhythmicStaff")
    >>> abjad.override(staff).TupletBracket.padding = 2
    >>> score = abjad.Score([staff])
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new RhythmicStaff
            \with
            {
                \override TupletBracket.padding = 2
            }
            {
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #left
                    c'16 * 1472/5120
                    [
                    c'16 * 3136/5120
                    \slashedGrace {
                        c'16
                        (
                    }
                    c'16 * 4288/5120
                    )
                    \grace {
                        \slash
                        c'16
                        [
                        (
                        c'16
                        ]
                    }
                    c'16 * 5312/5120
                    )
                    \grace {
                        \slash
                        c'16
                        [
                        (
                        c'16
                        c'16
                        ]
                    }
                    c'16 * 6272/5120
                    )
                    ]
                }
                \revert TupletNumber.text
            }
        >>

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
