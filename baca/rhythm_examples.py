r"""
rhythm.py examples.

..  container:: example

    Displaced quarter notes with grace music:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     voice = baca.make_rhythm(
    ...         [-2, baca.Grace([1], 4), baca.Grace([1], 4), -2],
    ...         16,
    ...         time_signatures,
    ...     )
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     score = abjad.Score([staff], name="Score")
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 36)"
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            proportionalNotationDuration = #(ly:make-moment 1 36)
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

    Displaced accelerandi, ritardandi:

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
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     score = abjad.Score([staff], name="Score")
    ...     abjad.override(score).TupletBracket.bracket_visibility = True
    ...     abjad.override(score).TupletBracket.padding = 2
    ...     abjad.setting(score).autoBeaming = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 36)"
    ...     abjad.setting(score).tupletFullLength = True
    ...     lilypond_file = abjad.LilyPondFile([score])
    ...     return lilypond_file

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

    Displaced accelerandi, ritardandi with grace notes:

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
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     score = abjad.Score([staff], name="Score")
    ...     abjad.override(score).TupletBracket.bracket_visibility = True
    ...     abjad.override(score).TupletBracket.padding = 2
    ...     abjad.setting(score).autoBeaming = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 36)"
    ...     abjad.setting(score).tupletFullLength = True
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

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

    Displaced accelerandi, ritardandi with on-beat grace notes:

    >>> def make_lilypond_file():
    ...     time_signatures = 3 * [abjad.TimeSignature((1, 4))]
    ...     duration = abjad.Duration(1, 4)
    ...     voice = baca.make_rhythm(
    ...         [
    ...             -1,
    ...             baca.Feather(
    ...                 [
    ...                     1,
    ...                     1,
    ...                     1,
    ...                     1,
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
    ...                         do_not_stop_polyphony=True,
    ...                         grace_leaf_duration=abjad.Duration(1, 64),
    ...                     ),
    ...                     1,
    ...                     1,
    ...                     1,
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
    ...     literal = abjad.LilyPondLiteral(r"\voiceTwo")
    ...     abjad.attach(literal, leaf)
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     score = abjad.Score([staff], name="Score")
    ...     abjad.override(score).TupletBracket.bracket_visibility = True
    ...     abjad.override(score).TupletBracket.padding = 2
    ...     abjad.setting(score).autoBeaming = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 36)"
    ...     abjad.setting(score).tupletFullLength = True
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

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
                    \voiceTwo
                    r16
                    \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
                    \times 1/1
                    {
                        \once \override Beam.grow-direction = #left
                        c'16 * 1472/5120
                        [
                        c'16 * 3136/5120
                        c'16 * 4288/5120
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
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     score = abjad.Score([staff], name="Score")
    ...     abjad.override(score).TupletBracket.bracket_visibility = True
    ...     abjad.override(score).TupletBracket.padding = 2
    ...     abjad.setting(score).autoBeaming = False
    ...     abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 36)"
    ...     abjad.setting(score).tupletFullLength = True
    ...     lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    ...     return lilypond_file

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

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
