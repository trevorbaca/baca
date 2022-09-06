r"""
figures.py examples.

..  container:: example

    LMR. Left counts equal to a single 1:

    >>> lmr = baca.lmr(
    ...     left_counts=[1],
    ...     left_cyclic=False,
    ...     left_length=3,
    ...     right_length=2,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1]
    [2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1]
    [2, 3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4]
    [5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5]
    [6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5, 6]
    [7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5, 6, 7]
    [8, 9]

..  container:: example

    Left counts all equal to 1:

    >>> lmr = baca.lmr(
    ...     left_counts=[1],
    ...     left_cyclic=True,
    ...     left_length=3,
    ...     right_length=2,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1]
    [2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1]
    [2]
    [3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1]
    [2]
    [3]
    [4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1]
    [2]
    [3]
    [4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1]
    [2]
    [3]
    [4]
    [5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1]
    [2]
    [3]
    [4, 5]
    [6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1]
    [2]
    [3]
    [4, 5, 6]
    [7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1]
    [2]
    [3]
    [4, 5, 6, 7]
    [8, 9]

..  container:: example

    Left length equal to 2:

    >>> lmr = baca.lmr(
    ...     left_length=2,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1, 2]
    [3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2]
    [3, 4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7, 8, 9]

..  container:: example

    Cyclic middle counts equal to [2]:

    >>> lmr = baca.lmr(
    ...     middle_counts=[2],
    ...     middle_cyclic=True,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1, 2]
    [3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2]
    [3, 4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5, 6]
    [7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5, 6]
    [7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5, 6]
    [7, 8]
    [9]

    Odd parity produces length-1 part at right.

..  container:: example

    Reversed cyclic middle counts equal to [2]:

    >>> lmr = baca.lmr(
    ...     middle_counts=[2],
    ...     middle_cyclic=True,
    ...     middle_reversed=True,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1]
    [2, 3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2]
    [3, 4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5]
    [6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5, 6]
    [7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5]
    [6, 7]
    [8, 9]

    Odd parity produces length-1 part at left.

..  container:: example

    Priority to the left:

    >>> lmr = baca.lmr(
    ...     left_length=2,
    ...     right_length=1,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1, 2]
    [3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2]
    [3]
    [4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5]
    [6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6]
    [7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7]
    [8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7, 8]
    [9]

..  container:: example

    Priority to the right:

    >>> lmr = baca.lmr(
    ...     left_length=2,
    ...     priority=abjad.RIGHT,
    ...     right_length=1,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1]
    [2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1, 2]
    [3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2]
    [3]
    [4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1, 2]
    [3, 4]
    [5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5]
    [6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6]
    [7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7]
    [8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1, 2]
    [3, 4, 5, 6, 7, 8]
    [9]

..  container:: example

    Right length equal to 2:

    >>> lmr = baca.lmr(
    ...     right_length=2,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1]
    [2, 3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2]
    [3, 4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1, 2, 3]
    [4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2, 3, 4]
    [5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1, 2, 3, 4, 5]
    [6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2, 3, 4, 5, 6]
    [7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1, 2, 3, 4, 5, 6, 7]
    [8, 9]

..  container:: example

    Right length equal to 2 and left counts equal to [1]:

    >>> lmr = baca.lmr(
    ...     left_counts=[1],
    ...     left_cyclic=False,
    ...     right_length=2,
    ... )

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts = lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1]
    [2, 3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1]
    [2]
    [3, 4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1]
    [2, 3]
    [4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1]
    [2, 3, 4]
    [5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1]
    [2, 3, 4, 5]
    [6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1]
    [2, 3, 4, 5, 6]
    [7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1]
    [2, 3, 4, 5, 6, 7]
    [8, 9]

..  container:: example

    Default LMR:

    >>> lmr = baca.lmr()

    >>> parts = lmr([1])
    >>> for part in parts: part
    [1]

    >>> parts =lmr([1, 2])
    >>> for part in parts: part
    [1, 2]

    >>> parts = lmr([1, 2, 3])
    >>> for part in parts: part
    [1, 2, 3]

    >>> parts = lmr([1, 2, 3, 4])
    >>> for part in parts: part
    [1, 2, 3, 4]

    >>> parts = lmr([1, 2, 3, 4, 5])
    >>> for part in parts: part
    [1, 2, 3, 4, 5]

    >>> parts = lmr([1, 2, 3, 4, 5, 6])
    >>> for part in parts: part
    [1, 2, 3, 4, 5, 6]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7])
    >>> for part in parts: part
    [1, 2, 3, 4, 5, 6, 7]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8])
    >>> for part in parts: part
    [1, 2, 3, 4, 5, 6, 7, 8]

    >>> parts = lmr([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> for part in parts: part
    [1, 2, 3, 4, 5, 6, 7, 8, 9]


..  container:: example

    Sixteenth-note acciaccaturas by default:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 8, acciaccatura=True)
    >>> rmakers.beam_function(abjad.select.leaves(container, grace=False))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        ]
                    }
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                        [
                        bf'16
                        fs''16
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        c'16
                        d'16
                        ]
                    }
                    bf'8
                }
            }
        >>

..  container:: example

    Eighth-note acciaccaturas:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> specifier = baca.Acciaccatura([abjad.Duration(1, 8)])
    >>> container = baca.figure_function(collections, [1], 8, acciaccatura=specifier)
    >>> rmakers.beam_function(abjad.select.leaves(container, grace=False))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'8
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''8
                        [
                        e''8
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''8
                        [
                        g''8
                        a'8
                        ]
                    }
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'8
                        [
                        bf'8
                        fs''8
                        e''8
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''8
                        [
                        g''8
                        a'8
                        c'8
                        d'8
                        ]
                    }
                    bf'8
                }
            }
        >>

..  container:: example

    As many acciaccaturas as possible per collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 8, acciaccatura=True)
    >>> rmakers.beam_function(abjad.select.leaves(container, grace=False))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        ]
                    }
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                        [
                        bf'16
                        fs''16
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        c'16
                        d'16
                        ]
                    }
                    bf'8
                }
            }
        >>

..  container:: example

    At most two acciaccaturas at the beginning of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections,
    ...     [1],
    ...     8,
    ...     acciaccatura=baca.lmr(
    ...         left_length=3,
    ...         right_counts=[1],
    ...         right_cyclic=True,
    ...     ),
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 3/2
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        ]
                    }
                    a'8
                    [
                    c'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                        [
                        bf'16
                        ]
                    }
                    fs''8
                    [
                    e''8
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        ]
                    }
                    a'8
                    [
                    c'8
                    d'8
                    bf'8
                    ]
                }
            }
        >>

..  container:: example

    At most two acciaccaturas at the end of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections,
    ...     [1],
    ...     8,
    ...     acciaccatura=baca.lmr(
    ...         right_length=3,
    ...         left_counts=[1],
    ...         left_cyclic=True,
    ...     ),
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/2
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    af''8
                    [
                    \acciaccatura {
                        g''16
                        [
                        a'16
                        ]
                    }
                    c'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    d'8
                    [
                    bf'8
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    af''8
                    [
                    g''8
                    a'8
                    \acciaccatura {
                        c'16
                        [
                        d'16
                        ]
                    }
                    bf'8
                    ]
                }
            }
        >>

..  container:: example

    At most two acciaccaturas at the beginning of every collection and then at
    most two acciaccaturas at the end of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections,
    ...     [1],
    ...     8,
    ...     acciaccatura=baca.lmr(
    ...         left_length=3,
    ...         middle_counts=[1],
    ...         middle_cyclic=True,
    ...         right_length=3,
    ...     ),
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 9/8
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        ]
                    }
                    a'8
                    [
                    c'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                        [
                        bf'16
                        ]
                    }
                    fs''8
                    [
                    \acciaccatura {
                        e''16
                    }
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        ]
                    }
                    a'8
                    [
                    \acciaccatura {
                        c'16
                        [
                        d'16
                        ]
                    }
                    bf'8
                    ]
                }
            }
        >>

..  container:: example

    As many acciaccaturas as possible in the middle of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections, [1], 8, acciaccatura=baca.lmr(left_length=1)
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 11/8
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    d'8
                    [
                    bf'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''8
                    [
                    \acciaccatura {
                        e''16
                    }
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    af''8
                    [
                    \acciaccatura {
                        g''16
                        [
                        a'16
                        ]
                    }
                    c'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    d'8
                    [
                    \acciaccatura {
                        bf'16
                        [
                        fs''16
                        e''16
                        ]
                    }
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    af''8
                    [
                    \acciaccatura {
                        g''16
                        [
                        a'16
                        c'16
                        d'16
                        ]
                    }
                    bf'8
                    ]
                }
            }
        >>

..  container:: example

    Without state manifest:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    c'16
                    [
                    d'16
                    bf'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    g''16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'8
                }
            }
        >>

..  container:: example

    As many acciaccaturas as possible per collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 8, acciaccatura=True)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        ]
                    }
                    c'8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                        [
                        bf'16
                        fs''16
                        e''16
                        ]
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        c'16
                        d'16
                        ]
                    }
                    bf'8
                }
            }
        >>

..  container:: example

    Graced quarters:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 4, acciaccatura=True)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/2
                    c'4
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                    }
                    bf'4
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        fs''16
                        [
                        e''16
                        ]
                    }
                    ef''4
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        ]
                    }
                    c'4
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        d'16
                        [
                        bf'16
                        fs''16
                        e''16
                        ]
                    }
                    ef''4
                }
                \scaleDurations #'(1 . 1)
                {
                    \acciaccatura {
                        af''16
                        [
                        g''16
                        a'16
                        c'16
                        d'16
                        ]
                    }
                    bf'4
                }
            }
        >>

..  container:: example

    Spells nonassignable durations with monontonically decreasing durations by
    default:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> container =  baca.figure_function(collections, [4, 4, 5], 32)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 39/32
                    c'8
                    [
                    d'8
                    bf'8
                    ~
                    bf'32
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''8
                    [
                    e''8
                    ef''8
                    ~
                    ef''32
                    af''8
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'8
                    [
                    ~
                    a'32
                    ]
                }
            }
        >>

..  container:: example

    Spells nonassignable durations with monontonically increasing durations:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> container = baca.figure_function(
    ...     collections,
    ...     [4, 4, 5],
    ...     32,
    ...     spelling=rmakers.Spelling(increase_monotonic=True),
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 39/32
                    c'8
                    [
                    d'8
                    bf'32
                    ~
                    bf'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''8
                    [
                    e''8
                    ef''32
                    ~
                    ef''8
                    af''8
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'32
                    [
                    ~
                    a'8
                    ]
                }
            }
        >>

..  container:: example

    Sixteenths and eighths:

    >>> collections = [[0, 2, 10, 8]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 5/16
                    c'16
                    [
                    d'16
                    bf'8
                    af'16
                    ]
                }
            }
        >>

    >>> collections = [[18, 16, 15, 20, 19]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 3/8
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    g''16
                    ]
                }
            }
        >>

    >>> collections = [[9]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 1/16
                    a'16
                }
            }
        >>

    >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 13/16
                    c'16
                    [
                    d'16
                    bf'8
                    af'16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''16
                    [
                    e''8
                    ef''16
                    af''16
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'16
                }
            }
        >>

..  container:: example

    Works with rests:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> container = baca.figure_function(collections, [3, -1, 2, 2], 16)
    >>> rmakers.beam_function(
    ...     rmakers.nongrace_leaves_in_each_tuplet_function(container),
    ...     beam_rests=True,
    ...     stemlet_length=1.5,
    ... )
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
                \scaleDurations #'(1 . 1)
                {
                    \override Staff.Stem.stemlet-length = 1.5
                    \time 3/2
                    c'8.
                    [
                    r16
                    d'8
                    \revert Staff.Stem.stemlet-length
                    bf'8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    \override Staff.Stem.stemlet-length = 1.5
                    fs''8.
                    [
                    r16
                    e''8
                    ef''8
                    af''8.
                    r16
                    \revert Staff.Stem.stemlet-length
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'8
                }
            }
        >>

..  container:: example

    Works with large counts:

    >>> collections = [[0, 2]]
    >>> container = baca.figure_function([[0, 2]], [29], 64)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> rmakers.force_repeat_tie()(container)
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
                \scaleDurations #'(1 . 1)
                {
                    \time 29/32
                    c'4..
                    c'64
                    \repeatTie
                    d'4..
                    d'64
                    \repeatTie
                }
            }
        >>

..  container:: example

    One extra count per division:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16, treatments=[1])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \times 5/4
                {
                    \time 15/16
                    c'16
                    [
                    d'16
                    bf'8
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/6
                {
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    g''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2
                {
                    a'8
                }
            }
        >>

..  container:: example

    One missing count per division:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> container = baca.figure_function(collections, [1, 1, 2], 16, treatments=[-1])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \times 3/4
                {
                    \time 5/8
                    c'16
                    [
                    d'16
                    bf'8
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/6
                {
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    g''16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'8
                }
            }
        >>

..  container:: example

    Accelerandi:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 16, treatments=["accel"])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 21/16
                    c'16
                }
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'8
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    d'16 * 1328/1024
                    [
                    bf'16 * 720/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'8.
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    fs''16 * 1552/1024
                    [
                    e''16 * 832/1024
                    ef''16 * 688/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    af''16 * 1728/1024
                    [
                    g''16 * 928/1024
                    a'16 * 768/1024
                    c'16 * 672/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    d'16 * 1872/1024
                    [
                    bf'16 * 1008/1024
                    fs''16 * 832/1024
                    e''16 * 736/1024
                    ef''16 * 672/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4.
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    af''16 * 2000/1024
                    [
                    g''16 * 1088/1024
                    a'16 * 896/1024
                    c'16 * 784/1024
                    d'16 * 720/1024
                    bf'16 * 656/1024
                    ]
                }
                \revert TupletNumber.text
            }
        >>

..  container:: example

    Ritardandi:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 16, treatments=["rit"])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \scaleDurations #'(1 . 1)
                {
                    \time 21/16
                    c'16
                }
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'8
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    d'16 * 656/1024
                    [
                    bf'16 * 1392/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'8.
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    fs''16 * 512/1024
                    [
                    e''16 * 1072/1024
                    ef''16 * 1488/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    af''16 * 432/1024
                    [
                    g''16 * 896/1024
                    a'16 * 1232/1024
                    c'16 * 1536/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    d'16 * 368/1024
                    [
                    bf'16 * 784/1024
                    fs''16 * 1072/1024
                    e''16 * 1328/1024
                    ef''16 * 1568/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4.
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    af''16 * 336/1024
                    [
                    g''16 * 704/1024
                    a'16 * 960/1024
                    c'16 * 1184/1024
                    d'16 * 1392/1024
                    bf'16 * 1568/1024
                    ]
                }
                \revert TupletNumber.text
            }
        >>

..  container:: example

    Accelerandi followed by ritardandi:

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0, 2],
    ...     [10, 18, 16, 15, 20],
    ...     [19, 9, 0, 2, 10, 18],
    ... ]
    >>> container = baca.figure_function(
    ...     collections, [1], 16, treatments=["accel", "rit"]
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    \time 11/8
                    c'16 * 1872/1024
                    [
                    d'16 * 1008/1024
                    bf'16 * 832/1024
                    fs''16 * 736/1024
                    e''16 * 672/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4.
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    ef''16 * 336/1024
                    [
                    af''16 * 704/1024
                    g''16 * 960/1024
                    a'16 * 1184/1024
                    c'16 * 1392/1024
                    d'16 * 1568/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    bf'16 * 1872/1024
                    [
                    fs''16 * 1008/1024
                    e''16 * 832/1024
                    ef''16 * 736/1024
                    af''16 * 672/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4.
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    g''16 * 336/1024
                    [
                    a'16 * 704/1024
                    c'16 * 960/1024
                    d'16 * 1184/1024
                    bf'16 * 1392/1024
                    fs''16 * 1568/1024
                    ]
                }
                \revert TupletNumber.text
            }
        >>

..  container:: example

    Mixed accelerandi, ritardandi and prolation:

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2],
    ...     [10, 18, 16, 15, 20],
    ...     [19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections, [1], 16, treatments=["accel", -2, "rit"])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    \time 13/8
                    c'16 * 1872/1024
                    [
                    d'16 * 1008/1024
                    bf'16 * 832/1024
                    fs''16 * 736/1024
                    e''16 * 672/1024
                    ]
                }
                \revert TupletNumber.text
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5
                {
                    ef''16
                    [
                    af''16
                    g''16
                    a'16
                    c'16
                    ]
                }
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    d'16 * 368/1024
                    [
                    bf'16 * 784/1024
                    fs''16 * 1072/1024
                    e''16 * 1328/1024
                    ef''16 * 1568/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #right
                    af''16 * 1872/1024
                    [
                    g''16 * 1008/1024
                    a'16 * 832/1024
                    c'16 * 736/1024
                    d'16 * 672/1024
                    ]
                }
                \revert TupletNumber.text
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5
                {
                    bf'16
                    [
                    fs''16
                    e''16
                    ef''16
                    af''16
                    ]
                }
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \score
                    {
                        \context Score = "Score"
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = 0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \context RhythmicStaff = "Rhythmic_Staff"
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = 5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = 4
                                \override TupletBracket.padding = 1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = 0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout
                        {
                            indent = 0
                            ragged-right = ##t
                        }
                    }
                \scaleDurations #'(1 . 1)
                {
                    \once \override Beam.grow-direction = #left
                    g''16 * 368/1024
                    [
                    a'16 * 784/1024
                    c'16 * 1072/1024
                    d'16 * 1328/1024
                    bf'16 * 1568/1024
                    ]
                }
                \revert TupletNumber.text
            }
        >>

..  container:: example

    Specified by tuplet multiplier:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 8, treatments=["3:2"])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> staff = lilypond_file["Staff"]
    >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
    >>> abjad.override(staff).Stem.direction = abjad.DOWN
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            \with
            {
                \override Beam.positions = #'(-6 . -6)
                \override Stem.direction = #down
            }
            {
                \tweak edge-height #'(0.7 . 0)
                \times 2/3
                {
                    \time 7/4
                    c'8
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3
                {
                    d'8
                    [
                    bf'8
                    ]
                }
                \times 2/3
                {
                    fs''8
                    [
                    e''8
                    ef''8
                    ]
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3
                {
                    af''8
                    [
                    g''8
                    a'8
                    c'8
                    ]
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3
                {
                    d'8
                    [
                    bf'8
                    fs''8
                    e''8
                    ef''8
                    ]
                }
                \times 2/3
                {
                    af''8
                    [
                    g''8
                    a'8
                    c'8
                    d'8
                    bf'8
                    ]
                }
            }
        >>

..  container:: example

    Segment durations equal to a quarter:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(collections, [1], 8, treatments=[(1, 4)])
    >>> rmakers.denominator_function(container, (1, 16))
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> staff = lilypond_file["Staff"]
    >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
    >>> abjad.override(staff).Stem.direction = abjad.DOWN
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            \with
            {
                \override Beam.positions = #'(-6 . -6)
                \override Stem.direction = #down
            }
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/2
                    c'4
                }
                \scaleDurations #'(1 . 1)
                {
                    d'8
                    [
                    bf'8
                    ]
                }
                \times 4/6
                {
                    fs''8
                    [
                    e''8
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    af''16
                    [
                    g''16
                    a'16
                    c'16
                    ]
                }
                \times 4/5
                {
                    d'16
                    [
                    bf'16
                    fs''16
                    e''16
                    ef''16
                    ]
                }
                \times 4/6
                {
                    af''16
                    [
                    g''16
                    a'16
                    c'16
                    d'16
                    bf'16
                    ]
                }
            }
        >>

..  container:: example

    Collection durations alternating between a quarter and a dotted quarter:

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2],
    ...     [10, 18, 16, 15, 20],
    ...     [19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections, [1, 1, 2], 8, treatments=[(1, 4), (3, 8)])
    >>> rmakers.denominator_function(container, (1, 16))
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> staff = lilypond_file["Staff"]
    >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
    >>> abjad.override(staff).Stem.direction = abjad.DOWN
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            \with
            {
                \override Beam.positions = #'(-6 . -6)
                \override Stem.direction = #down
            }
            {
                \times 4/6
                {
                    \time 15/8
                    c'16
                    [
                    d'16
                    bf'8
                    fs''16
                    e''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7
                {
                    ef''8
                    [
                    af''16
                    g''16
                    a'8
                    c'16
                    ]
                }
                \times 4/7
                {
                    d'16
                    [
                    bf'8
                    fs''16
                    e''16
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    af''16
                    [
                    g''16
                    a'8
                    c'16
                    d'16
                    ]
                }
                \times 4/7
                {
                    bf'8
                    [
                    fs''16
                    e''16
                    ef''8
                    af''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7
                {
                    g''16
                    [
                    a'8
                    c'16
                    d'16
                    bf'8
                    ]
                }
            }
        >>

    Time treatments defined equal to integers; positive multipliers; positive
    durations; and the strings ``'accel'`` and ``'rit'``.

..  container:: example

    Nest.

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.nest_function(container, "+4/16")
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
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
                \times 13/11
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 13/8
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
            }
        >>


..  container:: example

    Nest. Augments one sixteenth:

    >>> collections = [
    ...     [0, 2, 10, 18],
    ...     [16, 15, 23],
    ...     [19, 13, 9, 8],
    ... ]
    >>> container = baca.figure_function(collections, [1], 16)
    >>> rmakers.beam_groups_function(
    ...     rmakers.nongrace_leaves_in_each_tuplet_function(container, level=-1))
    >>> _ = baca.nest_function(container, "+1/16")
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
                \times 12/11
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \set stemLeftBeamCount = 0
                        \set stemRightBeamCount = 2
                        \time 3/4
                        c'16
                        [
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        d'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        fs''16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        e''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        ef''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        b''16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        g''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        cs''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        a'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 0
                        af'16
                        ]
                    }
                }
            }
        >>

..  container:: example

    With rest affixes:

    >>> collections = [
    ...     [0, 2, 10, 18],
    ...     [16, 15, 23],
    ...     [19, 13, 9, 8],
    ... ]
    >>> affix = baca.rests_around([2], [3])
    >>> container = baca.figure_function(collections, [1], 16, affix=affix)
    >>> rmakers.beam_groups_function(
    ...     rmakers.nongrace_leaves_in_each_tuplet_function(container, level=-1))
    >>> _ = baca.nest_function(container, "+1/16")
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 17/16
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 17/16
                        r8
                        \set stemLeftBeamCount = 0
                        \set stemRightBeamCount = 2
                        c'16
                        [
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        d'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        fs''16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        e''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        ef''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        b''16
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        g''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        cs''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        a'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 0
                        af'16
                        ]
                        r8.
                    }
                }
            }
        >>

..  container:: example

    Affixes rests to complete output when pattern is none:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> affix = baca.RestAffix(
    ...     prefix=[1],
    ...     suffix=[2],
    ... )
    >>> container = baca.figure_function(collections, [1], 16, affix=affix, treatments=[1])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/4
                {
                    \time 15/16
                    r16
                    c'16
                    [
                    d'16
                    bf'16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/5
                {
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3
                {
                    a'16
                    r8
                }
            }
        >>

..  container:: example

    Affixes rest to complete output when pattern is none:

    >>> collections = [[18, 16, 15, 20, 19]]
    >>> affix = baca.RestAffix(
    ...     prefix=[1],
    ...     suffix=[2],
    ... )
    >>> container = baca.figure_function(collections, [1], 16, affix=affix, treatments=[1])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/8
                {
                    \time 9/16
                    r16
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                    r8
                }
            }
        >>

..  container:: example

    Affixes rests to first and last collections only:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> affix = baca.RestAffix(
    ...     pattern=abjad.Pattern(indices=[0, -1]),
    ...     prefix=[1],
    ...     suffix=[2],
    ... )
    >>> container = baca.figure_function(
    ...     collections, [1], 16, affix=affix, treatments=[1])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/6
                {
                    \time 9/8
                    r16
                    c'16
                    [
                    d'16
                    bf'16
                    ]
                    r8
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/5
                {
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/4
                {
                    r16
                    a'16
                    r8
                }
            }
        >>

..  container:: example

    Affixes rests to every collection:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> affix = baca.RestAffix(
    ...     pattern=abjad.index_all(),
    ...     prefix=[1],
    ...     suffix=[2],
    ... )
    >>> container = baca.figure_function(
    ...     collections, [1], 16, affix=affix, treatments=[1])
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/6
                {
                    \time 21/16
                    r16
                    c'16
                    [
                    d'16
                    bf'16
                    ]
                    r8
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/8
                {
                    r16
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                    r8
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/4
                {
                    r16
                    a'16
                    r8
                }
            }
        >>

..  container:: example

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> affix = baca.RestAffix(prefix=[3])
    >>> container = baca.figure_function(collections, [1], 16, affix=affix)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    r8.
                    c'16
                    [
                    d'16
                    bf'16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'16
                }
            }
        >>

..  container:: example

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> affix = baca.RestAffix(suffix=[3])
    >>> container = baca.figure_function(collections, [1], 16, affix=affix)
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \scaleDurations #'(1 . 1)
                {
                    \time 3/4
                    c'16
                    [
                    d'16
                    bf'16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    fs''16
                    [
                    e''16
                    ef''16
                    af''16
                    g''16
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    a'16
                    r8.
                }
            }
        >>

..  container:: example

    Coats pitches:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> figures(
    ...     "Music.2",
    ...     3 * [[0, 2, 10]],
    ...     baca.figure(
    ...         [1],
    ...         16,
    ...         affix=baca.rests_around([2], [4]),
    ...         treatments=[-1],
    ...     ),
    ...     rmakers.beam(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
    ...         rmakers.beam_groups(),
    ...     ),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 3/4
                    s1 * 3/4
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \times 4/5
                        {
                            \voiceOne
                            s8
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            bf'16
                            [
                        }
                        \times 2/3
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            c'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            d'16
                            ]
                            s16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7
                        {
                            s16
                            s16
                            s16
                            s4
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \times 4/5
                        {
                            \voiceTwo
                            r8
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \times 2/3
                        {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7
                        {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                            r4
                        }
                    }
                }
            >>
        }

..  container:: example

    Skips wrapped pitches:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> collections = [
    ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
    ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
    ... ]
    >>> segment = [
    ...     0,
    ...     baca.coat(10),
    ...     baca.coat(18),
    ...     10, 18,
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     rmakers.beam(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         segment,
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...     ),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 9/8
                    s1 * 9/8
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \voiceOne
                            c'16
                            - \accent
                            [
                            s16
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \accent
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            s16
                            s16
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceTwo
                            c'16
                            [
                            d'16
                            bf'16
                            fs''16
                            e''16
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            ef''16
                            [
                            af''16
                            g''16
                            a'16
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            c'16
                            [
                            d'16
                            bf'16
                            fs''16
                            e''16
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            ef''16
                            [
                            af''16
                            g''16
                            a'16
                            ]
                        }
                    }
                }
            >>
        }

..  container:: example

    Imbricates ``segment`` in voice with ``voice_name``.

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         rmakers.beam_groups(),
    ...     ),
    ... )

    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 15/16
                    s1 * 15/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            g''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            a'16
                            ]
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            fs''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            e''16
                            ]
                            s16
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            c'16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            ef''16
                            ]
                        }
                    }
                }
            >>
        }

..  container:: example

    Multiple imbricated voices:

    >>> score = baca.docs.make_empty_score(3)
    >>> figures = baca.FigureAccumulator(score)

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9],
    ...         rmakers.beam_groups(beam_rests=True),
    ...         baca.beam_positions(6),
    ...         baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ...         ),
    ...     baca.imbricate(
    ...         "Music.3",
    ...         [16, 10, 18],
    ...         rmakers.beam_groups(beam_rests=True),
    ...         baca.beam_positions(8),
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         ),
    ...     rmakers.beam_groups(),
    ... )

    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
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
                    \baca-new-spacing-section #1 #32
                    \time 15/16
                    s1 * 15/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \override Beam.positions = #'(6 . 6)
                            s16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \staccato
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \staccato
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            s16
                            s16
                            s16
                            ]
                            \revert Beam.positions
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            c'16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            ef''16
                            ]
                        }
                    }
                }
                \context Voice = "Music.3"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \override Beam.positions = #'(8 . 8)
                            s16
                            [
                            s16
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                            - \accent
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \accent
                            s16
                            s16
                            ]
                            \revert Beam.positions
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
            >>
        }

..  container:: example

    Hides tuplet brackets above imbricated voice:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16, treatments=[1]),
    ...     rmakers.beam_groups(beam_rests=True),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...     ),
    ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 9/8
                    s1 * 9/8
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5
                        {
                            \voiceOne
                            s16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \accent
                            s16
                            s16
                            s16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \accent
                            s16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            - \accent
                            s16
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            c'16
                            - \staccato
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                            - \staccato
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            c'16
                            - \staccato
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            d'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            ef''16
                            - \staccato
                            ]
                        }
                    }
                }
            >>
        }

..  container:: example

    Works with pitch-classes:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> segment = [
    ...     abjad.NumberedPitchClass(10),
    ...     abjad.NumberedPitchClass(6),
    ...     abjad.NumberedPitchClass(4),
    ...     abjad.NumberedPitchClass(3),
    ... ]
    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([3], 16),
    ...     rmakers.beam(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         segment,
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...     ),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 24))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #24
                    \time 27/16
                    s1 * 27/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s8.
                            [
                            s8.
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            bf'8.
                            - \accent
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            fs''8.
                            - \accent
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            e''8.
                            - \accent
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            ef''8.
                            - \accent
                            s8.
                            s8.
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s8.
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceTwo
                            c'8.
                            [
                            d'8.
                            bf'8.
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            fs''8.
                            [
                            e''8.
                            ef''8.
                            af''8.
                            g''8.
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            a'8.
                        }
                    }
                }
            >>
        }

..  container:: example

    Works with chords:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> collections = [
    ...     {0, 2, 10, 18, 16},
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         rmakers.beam_groups(),
    ...     ),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 11/16
                    s1 * 11/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            \voiceOne
                            d'16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            g''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            a'16
                            ]
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            fs''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            e''16
                            ]
                            s16
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            <c' d' bf' e'' fs''>16
                            [
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            c'16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            ef''16
                            ]
                        }
                    }
                }
            >>
        }

..  container:: example

    Works with rests:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16, affix=baca.rests_around([2], [2])),
    ...     rmakers.beam_groups(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         rmakers.beam_groups(),
    ...     ),
    ... )

    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 19/16
                    s1 * 19/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s8
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            g''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            a'16
                            ]
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            fs''16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            e''16
                            ]
                            s16
                            s8
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceTwo
                            r8
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            c'16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            d'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            ef''16
                            ]
                            r8
                        }
                    }
                }
            >>
        }

..  container:: example

    Rests after.

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_after([2]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/8
                {
                    \override TupletBracket.staff-padding = 2
                    \time 9/8
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
                \times 2/3
                {
                    a'16
                    r8
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Rests around.

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [2]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)

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
                \times 2/3
                {
                    a'16
                    r8
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Works together with negative-valued talea:

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [3]),
    ...     treatments=[1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> staff = lilypond_file["Staff"]
    >>> abjad.override(staff).TupletBracket.staff_padding = 4
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            \with
            {
                \override TupletBracket.staff-padding = 4
            }
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/8
                {
                    \time 13/8
                    r8
                    c'16
                    r16
                    d'16
                    r16
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 11/10
                {
                    fs''16
                    r16
                    e''16
                    r16
                    ef''16
                    r16
                    af''16
                    r16
                    g''16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/5
                {
                    a'16
                    r16
                    r8.
                }
            }
        >>

..  container:: example

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [-1, 1],
    ...     16,
    ...     affix=baca.rests_around([2], [3]),
    ...     treatments=[1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> staff = lilypond_file["Staff"]
    >>> abjad.override(staff).TupletBracket.staff_padding = 4
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            \with
            {
                \override TupletBracket.staff-padding = 4
            }
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/8
                {
                    \time 13/8
                    r8
                    r16
                    c'16
                    r16
                    d'16
                    r16
                    bf'16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 11/10
                {
                    r16
                    fs''16
                    r16
                    e''16
                    r16
                    ef''16
                    r16
                    af''16
                    r16
                    g''16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/5
                {
                    r16
                    a'16
                    r8.
                }
            }
        >>

..  container:: example

    With time treatments:

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1],
    ...     16,
    ...     affix=baca.rests_around([1], [1]),
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
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
                \times 3/4
                {
                    \time 9/16
                    r16
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
                \scaleDurations #'(1 . 1)
                {
                    a'16
                    r16
                }
            }
        >>

..  container:: example

    Rests before.

    >>> container = baca.figure_function(
    ... [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_before([2]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
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
                    \time 19/16
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
                \scaleDurations #'(1 . 1)
                {
                    a'16
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Makes skips after music.

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.skips_after([2]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
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
                \times 7/8
                {
                    \override TupletBracket.staff-padding = 2
                    \time 9/8
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
                \times 2/3
                {
                    a'16
                    s8
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Makes skips around music.

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.skips_around([2], [2]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
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
                    s8
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
                \times 2/3
                {
                    a'16
                    s8
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Makes skips before music.

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.skips_before([2]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
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
                    \time 19/16
                    s8
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
                \scaleDurations #'(1 . 1)
                {
                    a'16
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Stack examples.

    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2],
    ...     [10, 18, 16, 15, 20],
    ...     [19, 9, 0, 2, 10],
    ... ]
    >>> container = baca.figure_function(
    ...     collections, [1, 1, 2], 8, treatments=[(1, 4), (3, 8)])
    >>> rmakers.denominator_function(container, (1, 16))
    >>> rmakers.beam_function(rmakers.nongrace_leaves_in_each_tuplet_function(container))
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
    >>> staff = lilypond_file["Staff"]
    >>> abjad.override(staff).Beam.positions = "#'(-6 . -6)"
    >>> abjad.override(staff).Stem.direction = abjad.DOWN
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            \with
            {
                \override Beam.positions = #'(-6 . -6)
                \override Stem.direction = #down
            }
            {
                \times 4/6
                {
                    \time 15/8
                    c'16
                    [
                    d'16
                    bf'8
                    fs''16
                    e''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7
                {
                    ef''8
                    [
                    af''16
                    g''16
                    a'8
                    c'16
                    ]
                }
                \times 4/7
                {
                    d'16
                    [
                    bf'8
                    fs''16
                    e''16
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1)
                {
                    af''16
                    [
                    g''16
                    a'8
                    c'16
                    d'16
                    ]
                }
                \times 4/7
                {
                    bf'8
                    [
                    fs''16
                    e''16
                    ef''8
                    af''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7
                {
                    g''16
                    [
                    a'8
                    c'16
                    d'16
                    bf'8
                    ]
                }
            }
        >>

..  container:: example

    Imbrication allows unused pitches:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(beam_rests=True),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...         allow_unused_pitches=True,
    ...     ),
    ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 5/8
                    s1 * 5/8
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \accent
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \accent
                            s16
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            c'16
                            - \staccato
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                            - \staccato
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            c'16
                            - \staccato
                            ]
                        }
                    }
                }
            >>
        }

..  container:: example exception

    Raises exception on unused pitches:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(beam_rests=True),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...         allow_unused_pitches=False,
    ...     ),
    ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ... )
    Traceback (most recent call last):
        ...
    Exception: Cursor(...) used only 3 of 5 pitches.

..  container:: example

    When imbrication hockets voices:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([1], 16),
    ...     rmakers.beam_groups(beam_rests=True),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...         baca.accent(selector=lambda _: baca.select.pheads(_)),
    ...         rmakers.beam_groups(beam_rests=True),
    ...         hocket=True,
    ...     ),
    ...     baca.staccato(selector=lambda _: baca.select.pheads(_)),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 15/16
                    s1 * 15/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            d'16
                            - \accent
                            s16
                            s16
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            g''16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \accent
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \accent
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            e''16
                            - \accent
                            s16
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            c'16
                            - \staccato
                            [
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            fs''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                            - \staccato
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            ef''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            af''16
                            - \staccato
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            c'16
                            - \staccato
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            d'16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 0
                            ef''16
                            - \staccato
                            ]
                        }
                    }
                }
            >>
        }

..  container:: example

    When imbrication truncates ties:

    >>> score = baca.docs.make_empty_score(2)
    >>> figures = baca.FigureAccumulator(score)
    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> figures(
    ...     "Music.2",
    ...     collections,
    ...     baca.figure([5], 32),
    ...     rmakers.beam(),
    ...     baca.imbricate(
    ...         "Music.1",
    ...         [2, 10, 18, 19, 9],
    ...         rmakers.beam_groups(beam_rests=True),
    ...         truncate_ties=True,
    ...     ),
    ... )
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=figures.time_signatures,
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> figures.populate_commands(score, accumulator)
    >>> _ = baca.voice_one_function(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two_function(abjad.select.leaf(score["Music.2"], 0))
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
                    \baca-new-spacing-section #1 #32
                    \time 45/32
                    s1 * 45/32
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceOne
                            s8
                            [
                            s32
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            d'8
                            s32
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            bf'8
                            s32
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            fs''8
                            s32
                            s8
                            s32
                            s8
                            s32
                            s8
                            s32
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            g''8
                            s32
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            a'8
                            s32
                            ]
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
                \context Voice = "Music.2"
                {
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \voiceTwo
                            c'8
                            [
                            ~
                            c'32
                            d'8
                            ~
                            d'32
                            bf'8
                            ~
                            bf'32
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            fs''8
                            [
                            ~
                            fs''32
                            e''8
                            ~
                            e''32
                            ef''8
                            ~
                            ef''32
                            af''8
                            ~
                            af''32
                            g''8
                            ~
                            g''32
                            ]
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            a'8
                            [
                            ~
                            a'32
                            ]
                        }
                    }
                }
            >>
        }

"""


def dummy():
    """
    Read module-level examples.
    """
