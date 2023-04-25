r"""
Examples: ``baca.from_collection()``.

..  container:: example

    Works with large counts:

    >>> def make_lilypond_file():
    ...     tuplet = baca.from_collection([0, 2], [29], 64)
    ...     lilypond_file = abjad.illustrators.components([tuplet])
    ...     rmakers.beam([tuplet])
    ...     rmakers.force_repeat_tie(tuplet)
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
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
            }
        >>

..  container:: example

    Accelerandi:

    >>> def make_lilypond_file():
    ...     collections = [
    ...         [0],
    ...         [2, 10],
    ...         [18, 16, 15],
    ...         [20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...         [20, 19, 9, 0, 2, 10],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     tuplets = [baca.style_accelerando(_) for _ in tuplets]
    ...     rmakers.beam(tuplets)
    ...     lilypond_file = abjad.illustrators.components(tuplets)
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 1/1
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
            }
        >>

..  container:: example

    Ritardandi:

    >>> def make_lilypond_file():
    ...     collections = [
    ...         [0],
    ...         [2, 10],
    ...         [18, 16, 15],
    ...         [20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...         [20, 19, 9, 0, 2, 10],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     tuplets = [baca.style_ritardando(_) for _ in tuplets]
    ...     rmakers.beam(tuplets)
    ...     lilypond_file = abjad.illustrators.components(tuplets)
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 1/1
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
            }
        >>

..  container:: example

    Accelerandi followed by ritardandi:

    >>> def make_lilypond_file():
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0, 2],
    ...         [10, 18, 16, 15, 20],
    ...         [19, 9, 0, 2, 10, 18],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     baca.style_accelerando(tuplets[0])
    ...     baca.style_ritardando(tuplets[1])
    ...     baca.style_accelerando(tuplets[2])
    ...     baca.style_ritardando(tuplets[3])
    ...     rmakers.beam(tuplets)
    ...     lilypond_file = abjad.illustrators.components(tuplets)
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
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
            }
        >>

..  container:: example

    Mixed accelerandi, ritardandi and prolation:

    >>> def make_lilypond_file():
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...         [20, 19, 9, 0, 2],
    ...         [10, 18, 16, 15, 20],
    ...         [19, 9, 0, 2, 10],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     baca.style_accelerando(tuplets[0])
    ...     baca.prolate(tuplets[1], -2, 16)
    ...     baca.style_ritardando(tuplets[2])
    ...     baca.style_accelerando(tuplets[3])
    ...     baca.prolate(tuplets[4], -2, 16)
    ...     baca.style_ritardando(tuplets[5])
    ...     rmakers.beam(tuplets)
    ...     lilypond_file = abjad.illustrators.components(tuplets)
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
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
            }
        >>

..  container:: example

    Specified by tuplet multiplier:

    >>> def make_lilypond_file():
    ...     collections = [
    ...         [0],
    ...         [2, 10],
    ...         [18, 16, 15],
    ...         [20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...         [20, 19, 9, 0, 2, 10],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 8) for _ in collections]
    ...     tuplets = [baca.prolate(_, "3:2") for _ in tuplets]
    ...     rmakers.beam(tuplets)
    ...     lilypond_file = abjad.illustrators.components(tuplets)
    ...     staff = lilypond_file["Staff"]
    ...     abjad.override(staff).Beam.positions = "#'(-6 . -6)"
    ...     abjad.override(staff).Stem.direction = abjad.DOWN
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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
                \context Voice = "Voice"
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
            }
        >>

..  container:: example

    Segment durations equal to a quarter:

    >>> def make_lilypond_file():
    ...     collections = [
    ...         [0],
    ...         [2, 10],
    ...         [18, 16, 15],
    ...         [20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...         [20, 19, 9, 0, 2, 10],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 8) for _ in collections]
    ...     duration = abjad.Duration(1, 4)
    ...     tuplets = [baca.prolate(_, duration) for _ in tuplets]
    ...     rmakers.denominator(tuplets, (1, 16))
    ...     rmakers.beam(tuplets)
    ...     lilypond_file = abjad.illustrators.components(tuplets)
    ...     staff = lilypond_file["Staff"]
    ...     rmakers.swap_trivial(staff)
    ...     abjad.override(staff).Beam.positions = "#'(-6 . -6)"
    ...     abjad.override(staff).Stem.direction = abjad.DOWN
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
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
                \context Voice = "Voice"
                {
                    {
                        \time 3/2
                        c'4
                    }
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
            }
        >>

..  container:: example

    Nest works like this:

    >>> def make_lilypond_file():
    ...     collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     tuplets = [baca.prolate(_, 1, 16) for _ in tuplets]
    ...     container = abjad.Container(tuplets)
    ...     rmakers.beam(tuplets)
    ...     baca.nest(tuplets, "+4/16")
    ...     baca.tuplet_bracket_staff_padding(tuplets, 2)
    ...     components = abjad.mutate.eject_contents(container)
    ...     lilypond_file = abjad.illustrators.components(components)
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 15/11
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3
                        {
                            \override TupletBracket.staff-padding = 2
                            \time 15/16
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
                        {
                            a'16
                            \revert TupletBracket.staff-padding
                        }
                    }
                }
            }
        >>

..  container:: example

    Imbricates ``segment`` in voice with ``voice_name``.

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     rmakers.beam_groups(tuplets)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(
    ...         container,
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...     )
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups)
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 15/16
                    s1 * 15/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(3)
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications_1 = baca.imbricate(container, "Music.1", [2, 19, 9])
    ...     score["Music.1"].extend(imbrications_1["Music.1"])
    ...     for imbrication in imbrications_1.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.beam_positions(imbrication, 6)
    ...         baca.staccato(baca.select.pheads(imbrication))
    ...     imbrications_3 = baca.imbricate(container, "Music.3", [16, 10, 18])
    ...     score["Music.3"].extend(imbrications_3["Music.3"])
    ...     for imbrication in imbrications_3.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.beam_positions(imbrication, 8)
    ...         baca.accent(baca.select.pheads(imbrication))
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 15/16
                    s1 * 15/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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
                        {
                            s16
                            s16
                            s16
                            s16
                            s16
                        }
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     tuplets = [baca.prolate(_, 1, 16) for _ in tuplets]
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(
    ...         container,
    ...         "Music.1",
    ...         [2, 19, 9, 18, 16],
    ...     )
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.accent(baca.select.pheads(imbrication))
    ...     baca.staccato(baca.select.pheads(container))
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     segment = [
    ...         abjad.NumberedPitchClass(10),
    ...         abjad.NumberedPitchClass(6),
    ...         abjad.NumberedPitchClass(4),
    ...         abjad.NumberedPitchClass(3),
    ...     ]
    ...     collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    ...     tuplets = [baca.from_collection(_, [3], 16) for _ in collections]
    ...     rmakers.beam(tuplets)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(container, "Music.1", segment)
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.accent(baca.select.pheads(imbrication))
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 24))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #24
                    \time 27/16
                    s1 * 27/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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
                        {
                            \voiceTwo
                            c'8.
                            [
                            d'8.
                            bf'8.
                            ]
                        }
                        {
                            fs''8.
                            [
                            e''8.
                            ef''8.
                            af''8.
                            g''8.
                            ]
                        }
                        {
                            a'8.
                        }
                    }
                }
            >>
        }

..  container:: example

    Works with chords:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [
    ...         (0, 2, 10, 18, 16),
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(container, "Music.1", [2, 19, 9, 18, 16])
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups)
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 11/16
                    s1 * 11/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        {
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            \voiceOne
                            d'16
                        }
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
                        {
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 2
                            \voiceTwo
                            <c' d' bf' e'' fs''>16
                            [
                        }
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     tuplets[0].insert(0, "r8")
    ...     tuplets[-1].append("r8")
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(container, "Music.1", [2, 19, 9, 18, 16])
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups)
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 19/16
                    s1 * 19/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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

    Imbrication allows unused pitches:

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(
    ...         container, "Music.1", [2, 19, 9, 18, 16], allow_unused_pitches=True
    ...     )
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.accent(baca.select.pheads(imbrication))
    ...     baca.staccato(baca.select.pheads(container))
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 5/8
                    s1 * 5/8
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [
    ...         [0, 2, 10, 18, 16],
    ...         [15, 20, 19, 9, 0],
    ...         [2, 10, 18, 16, 15],
    ...     ]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups, beam_rests=True)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(
    ...         container, "Music.1", [2, 19, 9, 18, 16], hocket=True
    ...     )
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.accent(baca.select.pheads(imbrication))
    ...     baca.staccato(baca.select.pheads(container))
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 15/16
                    s1 * 15/16
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
    ...     tuplets = [baca.from_collection(_, [5], 32) for _ in collections]
    ...     rmakers.beam(tuplets)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(
    ...         container, "Music.1", [2, 10, 18, 19, 9], truncate_ties=True
    ...     )
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...     duration = abjad.get.duration(container)
    ...     time_signature = abjad.TimeSignature(duration.pair)
    ...     time_signatures = baca.section.wrap([time_signature])
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.docs.remove_deactivated_wrappers(score)
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     rmakers.swap_trivial(lilypond_file["Staff"])
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
                    \baca-new-spacing-section #1 #32
                    \time 45/32
                    s1 * 45/32
                }
                \context Voice = "Music.1"
                {
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
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

    >>> def make_lilypond_file():
    ...     score = baca.docs.make_empty_score(2)
    ...     collections = [[0, 2, 10, 18], [16, 15, 23]]
    ...     tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    ...     rmakers.beam_groups(groups)
    ...     container = abjad.Container(tuplets)
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(container, "Music.1", [2, 10])
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         baca.staccato(baca.select.pheads(imbrication))
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.extend_beam(abjad.select.leaf(imbrication, -1))
    ...     tuplet = baca.from_collection([19, 13, 9, 8], [1], 16)
    ...     groups = rmakers.nongrace_leaves_in_each_tuplet(tuplet)
    ...     rmakers.beam_groups(groups)
    ...     container = abjad.Container([tuplet])
    ...     score["Music.2"].append(container)
    ...     imbrications = baca.imbricate(container, "Music.1", [13, 9])
    ...     score["Music.1"].extend(imbrications["Music.1"])
    ...     for imbrication in imbrications.values():
    ...         groups = rmakers.nongrace_leaves_in_each_tuplet(imbrication)
    ...         rmakers.beam_groups(groups, beam_rests=True)
    ...         baca.staccato(baca.select.pheads(imbrication))
    ...     durations = [abjad.get.duration(_) for _ in score["Music.2"]]
    ...     time_signatures = [abjad.TimeSignature(_.pair) for _ in durations]
    ...     time_signatures = baca.section.wrap(time_signatures)
    ...     baca.section.set_up_score(score, time_signatures(), docs=True)
    ...     baca.SpacingSpecifier((1, 32))(score)
    ...     baca.voice_number(abjad.select.leaf(score["Music.1"], 0), 1)
    ...     baca.voice_number(abjad.select.leaf(score["Music.2"], 0), 2)
    ...     baca.section.extend_beams(score)
    ...     rmakers.swap_skip_filled(score)
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1
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
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1
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


def sphinx():
    """
    Makes Sphinx read this module.
    """
    pass
