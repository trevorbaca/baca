r"""
figures.py examples.

..  container:: example

    Spells nonassignable durations with monontonically decreasing durations by
    default:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets =  baca.from_collections(collections, [4, 4, 5], 32)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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

    Sixteenths and eighths:

    >>> collections = [[0, 2, 10, 8]]
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 16)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 16)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 16)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 16)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [3, -1, 2, 2], 16)
    >>> rmakers.beam(
    ...     tuplets,
    ...     beam_rests=True,
    ...     stemlet_length=1.5,
    ... )
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections([[0, 2]], [29], 64)
    >>> container = abjad.Container(tuplets)
    >>> rmakers.beam(tuplets)
    >>> rmakers.force_repeat_tie(container)
    >>> components = abjad.mutate.eject_contents(container)
    >>> lilypond_file = abjad.illustrators.components(components)
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

    One extra count per duration:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 16)
    >>> tuplets = [baca.prolate(_, 1, 16) for _ in tuplets]
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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

    One missing count per duration:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 16)
    >>> tuplets = [baca.prolate(_, -1, 16) for _ in tuplets]
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> tuplets = [baca.prolate(_, "accel") for _ in tuplets]
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 8 }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #right
                    d'16 * 1328/1024
                    [
                    bf'16 * 720/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 8. }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #right
                    fs''16 * 1552/1024
                    [
                    e''16 * 832/1024
                    ef''16 * 688/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4. }
                \times 1/1
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
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> tuplets = [baca.prolate(_, "rit") for _ in tuplets]
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 8 }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #left
                    d'16 * 656/1024
                    [
                    bf'16 * 1392/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 8. }
                \times 1/1
                {
                    \once \override Beam.grow-direction = #left
                    fs''16 * 512/1024
                    [
                    e''16 * 1072/1024
                    ef''16 * 1488/1024
                    ]
                }
                \revert TupletNumber.text
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4. }
                \times 1/1
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
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> _ = baca.prolate(tuplets[0], "accel")
    >>> _ = baca.prolate(tuplets[1], "rit")
    >>> _ = baca.prolate(tuplets[2], "accel")
    >>> _ = baca.prolate(tuplets[3], "rit")
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4. }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4. }
                \times 1/1
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
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> _ = baca.prolate(tuplets[0], "accel")
    >>> _ = baca.prolate(tuplets[1], -2, 16)
    >>> _ = baca.prolate(tuplets[2], "rit")
    >>> _ = baca.prolate(tuplets[3], "accel")
    >>> _ = baca.prolate(tuplets[4], -2, 16)
    >>> _ = baca.prolate(tuplets[5], "rit")
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
                \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 ~ 16 }
                \times 1/1
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
    >>> tuplets = baca.from_collections(collections, [1], 8)
    >>> tuplets = [baca.prolate(_, "3:2") for _ in tuplets]
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1], 8)
    >>> duration = abjad.Duration(1, 4)
    >>> tuplets = [baca.prolate(_, duration) for _ in tuplets]
    >>> rmakers.denominator(tuplets, (1, 16))
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1, 1, 2], 8)
    >>> for i, tuplet in enumerate(tuplets):
    ...     if i % 2 == 0:
    ...         duration = abjad.Duration(1, 4)
    ...     else:
    ...         duration = abjad.Duration(3, 8)
    ...     _ = baca.prolate(tuplet, duration)

    >>> rmakers.denominator(tuplets, (1, 16))
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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

    >>> tuplets = baca.from_collections(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ... )
    >>> tuplets = [baca.prolate(_, "10:9") for _ in tuplets]
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> container = abjad.Container(tuplets)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.nest(tuplets, "+4/16")
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> components = abjad.mutate.eject_contents(container)
    >>> lilypond_file = abjad.illustrators.components(components)
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
                \times 31/27
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 31/16
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
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        a'4
                        ~
                        a'16
                        r16
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
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> rmakers.beam_groups(tuplets)
    >>> container = abjad.Container(tuplets)
    >>> _ = baca.nest(tuplets, "+1/16")
    >>> components = abjad.mutate.eject_contents(container)
    >>> lilypond_file = abjad.illustrators.components(components)
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

    Affixes rests to complete output when pattern is none:

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> _ = baca.prolate(tuplets[0], "4:5")
    >>> _ = baca.prolate(tuplets[1], "5:6")
    >>> _ = baca.prolate(tuplets[2], "3:4")
    >>> baca.rests_around(tuplets, [1], [2], 16)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> tuplets = [baca.prolate(_, "8:9") for _ in tuplets]
    >>> baca.rests_around(tuplets, [1], [2], 16)
    >>> rmakers.beam(tuplets)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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

    Imbricates ``segment`` in voice with ``voice_name``.

    >>> score = baca.docs.make_empty_score(2)
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> rmakers.beam_groups(tuplets)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(
    ...     container,
    ...     "Music.1",
    ...     [2, 19, 9, 18, 16],
    ... )
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups)

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups)
    >>> container = abjad.Container(tuplets)
    >>> imbrications_1 = baca.imbricate(container, "Music.1", [2, 19, 9])
    >>> for imbrication in imbrications_1.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.beam_positions(imbrication, 6)
    ...     _ = baca.staccato(baca.select.pheads(imbrication))

    >>> imbrications_3 = baca.imbricate(container, "Music.3", [16, 10, 18])
    >>> for imbrication in imbrications_3.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.beam_positions(imbrication, 8)
    ...     _ = baca.accent(baca.select.pheads(imbrication))

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications_1 | imbrications_3,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
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
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> tuplets = [baca.prolate(_, 1, 16) for _ in tuplets]
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups, beam_rests=True)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(
    ...     container,
    ...     "Music.1",
    ...     [2, 19, 9, 18, 16],
    ... )
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.accent(baca.select.pheads(imbrication))

    >>> _ = baca.staccato(baca.select.pheads(container))
    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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
    >>> accumulator = baca.Accumulator(score)
    >>> segment = [
    ...     abjad.NumberedPitchClass(10),
    ...     abjad.NumberedPitchClass(6),
    ...     abjad.NumberedPitchClass(4),
    ...     abjad.NumberedPitchClass(3),
    ... ]
    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets = baca.from_collections(collections, [3], 16)
    >>> rmakers.beam(tuplets)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", segment)
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.accent(baca.select.pheads(imbrication))

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 24))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     {0, 2, 10, 18, 16},
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", [2, 19, 9, 18, 16])
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups)

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> baca.rests_around(tuplets, [2], [2], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", [2, 19, 9, 18, 16])
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups)

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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

    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets = baca.from_collections(collections, [1, 1, 5, -1], 16)
    >>> _ = baca.prolate(tuplets[0], "8:7")
    >>> _ = baca.prolate(tuplets[1], "10:9")
    >>> _ = baca.prolate(tuplets[2], "8:7")
    >>> baca.rests_after(tuplets, [2], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
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
                    \time 23/16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/8
                {
                    a'4
                    ~
                    a'16
                    r16
                    r8
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Imbrication allows unused pitches:

    >>> score = baca.docs.make_empty_score(2)
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(
    ...     container, "Music.1", [2, 19, 9, 18, 16], allow_unused_pitches=True)
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.accent(baca.select.pheads(imbrication))

    >>> _ = baca.staccato(baca.select.pheads(container))
    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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

..  container:: example

    When imbrication hockets voices:

    >>> score = baca.docs.make_empty_score(2)
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [
    ...     [0, 2, 10, 18, 16],
    ...     [15, 20, 19, 9, 0],
    ...     [2, 10, 18, 16, 15],
    ... ]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups, beam_rests=True)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", [2, 19, 9, 18, 16],
    ...     hocket=True)
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.accent(baca.select.pheads(imbrication))

    >>> _ = baca.staccato(baca.select.pheads(container))
    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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
    >>> accumulator = baca.Accumulator(score)
    >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    >>> tuplets = baca.from_collections(collections, [5], 32)
    >>> rmakers.beam(tuplets)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", [2, 10, 18, 19, 9],
    ...     truncate_ties=True)
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
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

..  container:: example

    Attaches RIGHT_BROKEN_BEAM to selector output.

    >>> score = baca.docs.make_empty_score(2)
    >>> accumulator = baca.Accumulator(score)

    >>> collections = [[0, 2, 10, 18], [16, 15, 23]]
    >>> tuplets = baca.from_collections(collections, [1], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", [2, 10])
    >>> for imbrication in imbrications.values():
    ...     _ = baca.staccato(baca.select.pheads(imbrication))
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.extend_beam(abjad.select.leaf(imbrication, -1))

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> tuplets = baca.from_collections([[19, 13, 9, 8]], [1], 16)
    >>> groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    >>> rmakers.beam_groups(groups)
    >>> container = abjad.Container(tuplets)
    >>> imbrications = baca.imbricate(container, "Music.1", [13, 9])
    >>> for imbrication in imbrications.values():
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     _ = baca.staccato(baca.select.pheads(imbrication))

    >>> accumulator.cache(
    ...     "Music.2",
    ...     container,
    ...     imbrications=imbrications,
    ... )
    >>> time_signatures = baca.section.time_signatures(accumulator.time_signatures)
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier((1, 32))(score)
    >>> accumulator.populate(score)
    >>> _ = baca.voice_one(abjad.select.leaf(score["Music.1"], 0))
    >>> _ = baca.voice_two(abjad.select.leaf(score["Music.2"], 0))
    >>> baca.section.extend_beams(score)
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
                    \baca-new-spacing-section #1 #32
                    \time 7/16
                    s1 * 7/16
                    \baca-new-spacing-section #1 #32
                    \time 1/4
                    s1 * 1/4
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
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            bf'16
                            - \staccato
                            s16
                        }
                        \scaleDurations #'(1 . 1)
                        {
                            s16
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            s16
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            s16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            cs''16
                            - \staccato
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            a'16
                            - \staccato
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
                            \set stemRightBeamCount = 0
                            b''16
                            ]
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1)
                        {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            g''16
                            [
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
        }

"""


def dummy():
    """
    Read module-level examples.
    """
