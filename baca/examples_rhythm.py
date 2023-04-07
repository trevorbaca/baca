r"""
Examples: rhythm.

..  container:: example

    >>> def make_score(voice, time_signatures):
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     score = abjad.Score([staff], name="Score")
    ...     abjad.override(score).TupletBracket.bracket_visibility = True
    ...     abjad.override(score).TupletBracket.padding = 2
    ...     abjad.setting(score).autoBeaming = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 36)"
    ...     abjad.setting(score).tupletFullLength = True
    ...     rmakers.force_fraction(score)
    ...     return score

..  container:: example

    Displaced, graced quarter notes:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [-2, baca.Grace([1], 4), baca.Grace([1], 4), -2],
    ...         16,
    ...         time_signatures,
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \time 1/4
                    r8
                    \acciaccatura {
                        c'16
                    }
                    c'8
                    ~
                    c'8
                    [
                    \acciaccatura {
                        c'16
                    }
                    c'8
                    ]
                    ~
                    c'8
                    r8
                }
            }
        >>

..  container:: example

    Displaced feathers:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -1,
    ...             baca.Feather([1, 1, 1, 1, 1], 16, 4, exponent=0.625),
    ...             baca.Feather([1, 1, 1, 1, 1], 16, 4, exponent=1.625),
    ...             -3
    ...         ],
    ...         16,
    ...         time_signatures,
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = abjad.LilyPondFile([score])
    ...     return result

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
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
                    r8.
                }
            }
        >>

..  container:: example

    Displaced, graced feathers:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -1,
    ...             baca.Feather(
    ...                 [
    ...                     baca.Grace([1, 1, 1], 1),
    ...                     baca.Grace([1, 1], 1),
    ...                     baca.Grace([1], 1),
    ...                     1,
    ...                     1,
    ...                 ],
    ...                 16,
    ...                 4,
    ...                 exponent=0.625,
    ...             ),
    ...             baca.Feather(
    ...                 [
    ...                     1,
    ...                     1,
    ...                     baca.Grace([1], 1),
    ...                     baca.Grace([1, 1], 1),
    ...                     baca.Grace([1, 1, 1], 1),
    ...                 ],
    ...                 16,
    ...                 4,
    ...                 exponent=1.625,
    ...             ),
    ...             -3,
    ...         ],
    ...         16,
    ...         time_signatures,
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \time 1/4
                    r16
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                    \times 1/1
                    {
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            c'16
                            ]
                        }
                        \once \override Beam.grow-direction = #right
                        c'16 * 7488/5120
                        [
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'16 * 4032/5120
                        \acciaccatura {
                            c'16
                        }
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
                        \acciaccatura {
                            c'16
                        }
                        c'16 * 4288/5120
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'16 * 5312/5120
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            c'16
                            ]
                        }
                        c'16 * 6272/5120
                        ]
                    }
                    \revert TupletNumber.text
                    r8.
                }
            }
        >>

..  container:: example

    Displaced, graced feathers with on-beat grace notes:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -1,
    ...             baca.Feather(
    ...                 [
    ...                     1,
    ...                     1,
    ...                     1,
    ...                     baca.Grace([1], 1),
    ...                     baca.OBGC(
    ...                         [1, 1, 1, 1],
    ...                         1,
    ...                         grace_leaf_duration=abjad.Duration(1, 64),
    ...                     ),
    ...                 ],
    ...                 16,
    ...                 4,
    ...                 exponent=1.625,
    ...             ),
    ...             baca.Feather(
    ...                 [
    ...                     1,
    ...                     baca.OBGC(
    ...                         [1, 1, 1],
    ...                         1,
    ...                         grace_leaf_duration=abjad.Duration(1, 64),
    ...                     ),
    ...                     1,
    ...                     1,
    ...                     baca.Grace([1, 1], 1),
    ...                 ],
    ...                 16,
    ...                 4,
    ...                 exponent=0.625,
    ...             ),
    ...             -3,
    ...         ],
    ...         16,
    ...         time_signatures,
    ...         voice_name="Example.Voice",
    ...     )
    ...     leaf = abjad.select.leaf(voice, 0)
    ...     command = abjad.VoiceNumber(2)
    ...     abjad.attach(command, leaf)
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \context Voice = "Example.Voice"
                {
                    \voiceTwo
                    \time 1/4
                    r16
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                    \times 1/1
                    {
                        \once \override Beam.grow-direction = #left
                        c'16 * 1472/5120
                        [
                        c'16 * 3136/5120
                        c'16 * 4288/5120
                        \acciaccatura {
                            c'16
                        }
                        c'16 * 5312/5120
                        \context Voice = "Example.Voice"
                        {
                            <<
                                \context Voice = "On_Beat_Grace_Container"
                                {
                                    \set fontSize = #-3
                                    \slash
                                    \voiceOne
                                    <
                                        \tweak font-size 0
                                        \tweak transparent ##t
                                        c'
                                    >16 * 1/4
                                    [
                                    (
                                    c'16 * 1/4
                                    c'16 * 1/4
                                    c'16 * 1/4
                                    )
                                    ]
                                }
                                \context Voice = "Example.Voice"
                                {
                                    \voiceTwo
                                    c'16 * 6272/5120
                                    ]
                                }
                            >>
                        }
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                    \times 1/1
                    {
                        \once \override Beam.grow-direction = #right
                        c'16 * 7488/5120
                        [
                        \context Voice = "Example.Voice"
                        {
                            <<
                                \context Voice = "On_Beat_Grace_Container"
                                {
                                    \set fontSize = #-3
                                    \slash
                                    \voiceOne
                                    <
                                        \tweak font-size 0
                                        \tweak transparent ##t
                                        c'
                                    >16 * 1/4
                                    [
                                    (
                                    c'16 * 1/4
                                    c'16 * 1/4
                                    )
                                    ]
                                }
                                \context Voice = "Example.Voice"
                                {
                                    \voiceTwo
                                    c'16 * 4032/5120
                                }
                            >>
                        }
                        c'16 * 3328/5120
                        c'16 * 2944/5120
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'16 * 2688/5120
                        ]
                    }
                    \revert TupletNumber.text
                    r8.
                }
            }
        >>

..  container:: example

    Displaced on-beat grace containers:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -2,
    ...             baca.OBGC([1, 1, 1, 1], 4, grace_leaf_duration=abjad.Duration(1, 36)),
    ...             baca.OBGC([1, 1, 1, 1], 4, grace_leaf_duration=abjad.Duration(1, 36)),
    ...             -2,
    ...         ],
    ...         16,
    ...         time_signatures,
    ...         voice_name="Example.Voice",
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \context Voice = "Example.Voice"
                {
                    \time 1/4
                    r8
                    \context Voice = "Example.Voice"
                    {
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    c'
                                >16 * 4/9
                                [
                                (
                                c'16 * 4/9
                                c'16 * 4/9
                                c'16 * 4/9
                                )
                                ]
                            }
                            \context Voice = "Example.Voice"
                            {
                                \voiceTwo
                                c'8
                                ~
                                c'8
                                [
                            }
                        >>
                    }
                    \context Voice = "Example.Voice"
                    {
                        <<
                            \context Voice = "On_Beat_Grace_Container"
                            {
                                \set fontSize = #-3
                                \slash
                                \voiceOne
                                <
                                    \tweak font-size 0
                                    \tweak transparent ##t
                                    c'
                                >16 * 4/9
                                [
                                (
                                c'16 * 4/9
                                c'16 * 4/9
                                c'16 * 4/9
                                )
                                ]
                            }
                            \context Voice = "Example.Voice"
                            {
                                \voiceTwo
                                c'8
                                ]
                                ~
                                c'8
                            }
                        >>
                    }
                    r8
                }
            }
        >>

..  container:: example

    Displaced, graced tuplets:

    >>> def make_lilypond_foo():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -2,
    ...             baca.Tuplet(
    ...                 [
    ...                     2,
    ...                     baca.Grace([1, 1], 2),
    ...                     baca.Grace([1], 2),
    ...                 ],
    ...                 -2,
    ...             ),
    ...             baca.Tuplet(
    ...                 [
    ...                     1,
    ...                     1,
    ...                     1,
    ...                     baca.Grace([1], 1),
    ...                     baca.Grace([1], 1),
    ...                 ],
    ...                 -1,
    ...             ),
    ...             -2,
    ...         ],
    ...         16,
    ...         time_signatures,
    ...     )
    ...     for tuplet in abjad.select.tuplets(voice):
    ...         hleaves = baca.select.hleaves(tuplet)
    ...         rmakers.beam([hleaves])
    ...         pleaf = baca.select.pleaf(hleaves, 0)
    ...         if pleaf is not None:
    ...             abjad.override(pleaf).Beam.positions = (4, 4)
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_foo()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \time 1/4
                    r8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 2/3
                    {
                        \once \override Beam.positions = #'(4 . 4)
                        c'8
                        [
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'8
                        \acciaccatura {
                            c'16
                        }
                        c'8
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/5
                    {
                        \once \override Beam.positions = #'(4 . 4)
                        c'16
                        [
                        c'16
                        c'16
                        \acciaccatura {
                            c'16
                        }
                        c'16
                        \acciaccatura {
                            c'16
                        }
                        c'16
                        ]
                    }
                    r8
                }
            }
        >>

..  container:: example

    Displaced, graced tuplets with graced feathers:

    >>> def make_lilypond_foo():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -2,
    ...             baca.Tuplet(
    ...                 [
    ...                     baca.Grace([1, 1], 2),
    ...                     baca.Feather(
    ...                         [1, baca.Grace([1], 1), 1, 1], 16, 4, exponent=0.625
    ...                     ),
    ...                 ],
    ...                 -2,
    ...             ),
    ...             baca.Tuplet(
    ...                 [
    ...                     baca.Feather(
    ...                         [1, 1, 1, baca.Grace([1], 1)], 16, 3, exponent=1.625
    ...                     ),
    ...                     1,
    ...                     baca.Grace([1, 1], 1),
    ...                 ],
    ...                 -1,
    ...             ),
    ...             -2,
    ...         ],
    ...         16,
    ...         time_signatures,
    ...     )
    ...     for tuplet in abjad.select.tuplets(voice, level=1):
    ...         hleaves = []
    ...         for leaf in abjad.select.leaves(tuplet):
    ...             if abjad.get.parentage(leaf).parent is tuplet:
    ...                 hleaves.append(leaf)
    ...         rmakers.beam([hleaves])
    ...     for tuplet in abjad.select.tuplets(voice):
    ...         hleaves = baca.select.hleaves(tuplet)
    ...         pleaf = baca.select.pleaf(hleaves, 0)
    ...         if pleaf is not None:
    ...             abjad.override(pleaf).Beam.positions = (4, 4)
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_foo()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \time 1/4
                    r8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 2/3
                    {
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        \once \override Beam.positions = #'(4 . 4)
                        c'8
                        \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                        \times 1/1
                        {
                            \once \override Beam.grow-direction = #right
                            \once \override Beam.positions = #'(4 . 4)
                            c'16 * 1728/1024
                            [
                            \acciaccatura {
                                c'16
                            }
                            c'16 * 928/1024
                            c'16 * 768/1024
                            c'16 * 672/1024
                            ]
                        }
                        \revert TupletNumber.text
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/5
                    {
                        \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 8. }
                        \times 1/1
                        {
                            \once \override Beam.grow-direction = #left
                            \once \override Beam.positions = #'(4 . 4)
                            c'16 * 1296/4096
                            [
                            c'16 * 2688/4096
                            c'16 * 3696/4096
                            \acciaccatura {
                                c'16
                            }
                            c'16 * 4608/4096
                            ]
                        }
                        \revert TupletNumber.text
                        c'16
                        [
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'16
                        ]
                    }
                    r8
                }
            }
        >>

..  container:: example

    Feathers with before-grace music and on-beat grace music:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -1,
    ...             baca.Feather(
    ...                 [
    ...                     1,
    ...                     1,
    ...                     1,
    ...                     baca.Grace([1, 1], 1),
    ...                     baca.OBGC(
    ...                         [1, 1, 1, 1],
    ...                         1,
    ...                         grace_leaf_duration=abjad.Duration(1, 64),
    ...                         grace_polyphony_command=abjad.VoiceNumber(2),
    ...                         nongrace_polyphony_command=abjad.VoiceNumber(1),
    ...                     ),
    ...                 ],
    ...                 16,
    ...                 4,
    ...                 exponent=1.625,
    ...             ),
    ...             baca.Feather(
    ...                 [
    ...                     1,
    ...                     baca.OBGC(
    ...                         [1, 1, 1],
    ...                         1,
    ...                         grace_leaf_duration=abjad.Duration(1, 64),
    ...                         grace_polyphony_command=abjad.VoiceNumber(2),
    ...                         nongrace_polyphony_command=abjad.VoiceNumber(1),
    ...                     ),
    ...                     1,
    ...                     1,
    ...                     baca.Grace([1, 1], 1),
    ...                 ],
    ...                 16,
    ...                 4,
    ...                 exponent=0.625,
    ...             ),
    ...             -3,
    ...         ],
    ...         16,
    ...         time_signatures,
    ...         voice_name="Example.Voice",
    ...     )
    ...     leaf = voice[2][2]
    ...     command = abjad.VoiceNumber()
    ...     abjad.attach(command, leaf)
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return result

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 36)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \context Voice = "Example.Voice"
                {
                    \time 1/4
                    r16
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                    \times 1/1
                    {
                        \once \override Beam.grow-direction = #left
                        c'16 * 1472/5120
                        [
                        c'16 * 3136/5120
                        c'16 * 4288/5120
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'16 * 5312/5120
                        \context Voice = "Example.Voice"
                        {
                            <<
                                \context Voice = "On_Beat_Grace_Container"
                                {
                                    \set fontSize = #-3
                                    \slash
                                    \voiceTwo
                                    <
                                        \tweak font-size 0
                                        \tweak transparent ##t
                                        c'
                                    >16 * 1/4
                                    [
                                    (
                                    c'16 * 1/4
                                    c'16 * 1/4
                                    c'16 * 1/4
                                    )
                                    ]
                                }
                                \context Voice = "Example.Voice"
                                {
                                    \voiceOne
                                    c'16 * 6272/5120
                                    ]
                                }
                            >>
                        }
                    }
                    \revert TupletNumber.text
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                    \times 1/1
                    {
                        \once \override Beam.grow-direction = #right
                        c'16 * 7488/5120
                        [
                        \context Voice = "Example.Voice"
                        {
                            <<
                                \context Voice = "On_Beat_Grace_Container"
                                {
                                    \set fontSize = #-3
                                    \slash
                                    \voiceTwo
                                    <
                                        \tweak font-size 0
                                        \tweak transparent ##t
                                        c'
                                    >16 * 1/4
                                    [
                                    (
                                    c'16 * 1/4
                                    c'16 * 1/4
                                    )
                                    ]
                                }
                                \context Voice = "Example.Voice"
                                {
                                    \voiceOne
                                    c'16 * 4032/5120
                                }
                            >>
                        }
                        \oneVoice
                        c'16 * 3328/5120
                        c'16 * 2944/5120
                        \acciaccatura {
                            \slash
                            c'16
                            [
                            c'16
                            ]
                        }
                        c'16 * 2688/5120
                        ]
                    }
                    \revert TupletNumber.text
                    r8.
                }
            }
        >>

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
