r"""
Examples: ``baca.make_bgcs()``.

..  container:: example

    Sixteenth-note BGCs by default:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(),
    ...     )
    ...     container = baca.from_collection(collection, [1], 8)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
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
            }
        }

..  container:: example

    Eighth-note BGCs:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(),
    ...         duration=abjad.Duration(1, 8),
    ...     )
    ...     container = baca.from_collection(collection, [1], 8)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'8
                        }
                        bf'8
                    }
                    {
                        \acciaccatura {
                            fs''8
                            [
                            e''8
                            ]
                        }
                        ef''8
                    }
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
            }
        }

..  container:: example

    At most two BGCs at the beginning of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(
    ...             left_length=3,
    ...             right_counts=[1],
    ...             right_cyclic=True,
    ...         ),
    ...     )
    ...     container = baca.from_collection(collection, [1], 8)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        \time 3/2
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
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
            }
        }

..  container:: example

    At most two BGCs at the end of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(
    ...             right_length=3,
    ...             left_counts=[1],
    ...             left_cyclic=True,
    ...         ),
    ...     )
    ...     container = baca.from_collection(collection, [1], 8)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        \time 3/2
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
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
            }
        }

..  container:: example

    At most two before-braces at the beginning of every collection and then at
    most two BGCs at the end of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(
    ...             left_length=3,
    ...             middle_counts=[1],
    ...             middle_cyclic=True,
    ...             right_length=3,
    ...         ),
    ...     )
    ...     container = baca.from_collection(collection, [1], 8)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        \time 9/8
                        c'8
                    }
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''8
                    }
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
            }
        }

..  container:: example

    As many BGCs as possible in the middle of every collection:

    >>> collections = [
    ...     [0],
    ...     [2, 10],
    ...     [18, 16, 15],
    ...     [20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ...     [20, 19, 9, 0, 2, 10],
    ... ]
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(left_length=1),
    ...     )
    ...     container = baca.from_collection(collection, [1], 8)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        \time 11/8
                        c'8
                    }
                    {
                        d'8
                        [
                        bf'8
                        ]
                    }
                    {
                        fs''8
                        [
                        \acciaccatura {
                            e''16
                        }
                        ef''8
                        ]
                    }
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
            }
        }

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
    >>> containers = []
    >>> for collection in collections:
    ...     bgcs, collection = baca.make_bgcs(
    ...         collection,
    ...         baca.LMR(),
    ...     )
    ...     container = baca.from_collection(collection, [1], 4)
    ...     baca.attach_bgcs(bgcs, container)
    ...     containers.append(container)

    >>> rmakers.beam(rmakers.nongrace_leaves_in_each_tuplet(containers))
    >>> lilypond_file = abjad.illustrators.components(containers)
    >>> voice = lilypond_file["Voice"]
    >>> containers = abjad.select.components(voice, abjad.BeforeGraceContainer)
    >>> rmakers.beam(containers)
    >>> rmakers.swap_trivial(lilypond_file["Staff"])
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
                        \time 3/2
                        c'4
                    }
                    {
                        \acciaccatura {
                            d'16
                        }
                        bf'4
                    }
                    {
                        \acciaccatura {
                            fs''16
                            [
                            e''16
                            ]
                        }
                        ef''4
                    }
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
            }
        }

"""


def sphinx():
    """
    Makes Sphinx read this module.
    """
    pass
