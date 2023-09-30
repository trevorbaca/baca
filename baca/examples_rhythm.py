r"""
Examples: rhythm.

..  container:: example

    Helper functions for this file:

    >>> def make_score(voice, time_signatures, pnd=(1, 36)):
    ...     staff = abjad.Staff([voice], lilypond_type="RhythmicStaff")
    ...     score = abjad.Score([staff], name="Score")
    ...     leaf = abjad.select.leaf(staff, 0)
    ...     abjad.attach(time_signatures[0], leaf)
    ...     abjad.override(score).TimeSignature.style = "#'numbered"
    ...     abjad.override(score).TupletBracket.bracket_visibility = True
    ...     abjad.override(score).TupletBracket.padding = 2
    ...     abjad.setting(score).autoBeaming = False
    ...     string = f"#(ly:make-moment {pnd[0]} {pnd[1]})"
    ...     abjad.setting(score).proportionalNotationDuration = string
    ...     abjad.setting(score).tupletFullLength = True
    ...     rmakers.force_fraction(score)
    ...     return score

    >>> def sixteenths(pairs, items, voice_name=None, *, do_not_rewrite_meter=False):
    ...     time_signatures = [abjad.TimeSignature(_) for _ in pairs]
    ...     voice = baca.make_rhythm(
    ...         items,
    ...         16,
    ...         time_signatures,
    ...         voice_name=voice_name,
    ...         do_not_rewrite_meter=do_not_rewrite_meter
    ...     )
    ...     return voice, time_signatures

    >>> def A(items, numerator):
    ...     denominator = 16
    ...     return baca.Feather(items, denominator, numerator, exponent=0.625)

    >>> def C(items):
    ...     return baca.Container(items)

    >>> def G(*arguments):
    ...     return baca.Grace(*arguments)

    >>> def R(items, numerator):
    ...     denominator = 16
    ...     return baca.Feather(items, denominator, numerator, exponent=1.625)

    >>> def T(items, extra_counts):
    ...     return baca.Tuplet(items, extra_counts)

    >>> def bl(argument):
    ...     return baca.BeamLeft(argument)

    >>> def br(argument):
    ...     return baca.BeamRight(argument)

    >>> def h(argument):
    ...     return baca.InvisibleMusic(argument)

    >>> def rt(argument):
    ...     return baca.RepeatTie(argument)

    >>> def t(argument):
    ...     return baca.Tie(argument)

    >>> def w(real_n, written_n):
    ...     return baca.WrittenDuration(real_n, written_n)

..  container:: example

    Displaced, graced quarter notes:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [-2, G([1], 4), G([1], 4), -2],
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
            \override TimeSignature.style = #'numbered
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
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [-1, A([1, 1, 1, 1, 1], 4), R([1, 1, 1, 1, 1], 4), -3],
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
            \override TimeSignature.style = #'numbered
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
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [
    ...             -1,
    ...             A([G([1, 1, 1], 1), G([1, 1], 1), G([1], 1), 1, 1], 4),
    ...             R([1, 1, G([1], 1), G([1, 1], 1), G([1, 1, 1], 1)], 4),
    ...             -3,
    ...         ],
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
            \override TimeSignature.style = #'numbered
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


    >>> def obgc(grace_note_numerators, nongrace_note_numerator):
    ...     return baca.OBGC(
    ...         grace_note_numerators,
    ...         nongrace_note_numerator,
    ...         grace_leaf_duration=abjad.Duration(1, 64),
    ...     )


    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [
    ...             -1,
    ...             R([1, 1, 1, G([1], 1), obgc([1, 1, 1, 1], 1)], 4),
    ...             A([1, obgc([1, 1, 1], 1), 1, 1, G([1, 1], 1)], 4),
    ...             -3,
    ...         ],
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
            \override TimeSignature.style = #'numbered
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

    >>> def obgc(grace_note_numerators, nongrace_note_numerator):
    ...     return baca.OBGC(
    ...         grace_note_numerators,
    ...         nongrace_note_numerator,
    ...         grace_leaf_duration=abjad.Duration(1, 36),
    ...     )

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [-2, obgc([1, 1, 1, 1], 4), obgc([1, 1, 1, 1], 4), -2],
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
            \override TimeSignature.style = #'numbered
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

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [
    ...             -2,
    ...             T([2, G([1, 1], 2), G([1], 2)], -2),
    ...             T([1, 1, 1, G([1], 1), G([1], 1)], -1),
    ...             -2,
    ...         ],
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

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TimeSignature.style = #'numbered
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

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [
    ...             -2,
    ...             T([G([1, 1], 2), A([1, G([1], 1), 1, 1], 4)], -2),
    ...             T([R([1, 1, 1, G([1], 1)], 3), 1, G([1, 1], 1)], -1),
    ...             -2,
    ...         ],
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

    >>> lilypond_file = make_lilypond_file()
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        \with
        {
            \override TimeSignature.style = #'numbered
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

    >>> def obgc(grace_note_numerators, nongrace_note_numerator):
    ...     return baca.OBGC(
    ...         grace_note_numerators,
    ...         nongrace_note_numerator,
    ...         grace_leaf_duration=abjad.Duration(1, 64),
    ...         grace_polyphony_command=abjad.VoiceNumber(2),
    ...         nongrace_polyphony_command=abjad.VoiceNumber(1),
    ...     )

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [
    ...             -1,
    ...             R([1, 1, 1, G([1, 1], 1), obgc([1, 1, 1, 1], 1)], 4),
    ...             A([1, obgc([1, 1, 1], 1), 1, 1, G([1, 1], 1)], 4),
    ...             -3,
    ...         ],
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
            \override TimeSignature.style = #'numbered
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

..  container:: example

    Written durations different than real durations:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [w(4, 16), w(4, 16), w(4, 16)],
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
            \override TimeSignature.style = #'numbered
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
                    c'1 * 1/4
                    c'1 * 1/4
                    c'1 * 1/4
                }
            }
        >>

..  container:: example

    Invisible music:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [4, h(4), 4],
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["abjad.ily"])
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
            \override TimeSignature.style = #'numbered
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
                    c'4
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c'4
                    c'4
                }
            }
        >>

..  container:: example

    Invisible music with written durations different than real durations:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [w(4, 16), h(w(4, 16)), w(4, 16)],
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["abjad.ily"])
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
            \override TimeSignature.style = #'numbered
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
                    c'1 * 1/4
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c'1 * 1/4
                    c'1 * 1/4
                }
            }
        >>


..  container:: example

    Ties:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(3 * [(1, 4)], [t(4), t(4), 4])
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["abjad.ily"])
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
            \override TimeSignature.style = #'numbered
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
                    c'4
                    ~
                    c'4
                    ~
                    c'4
                }
            }
        >>


..  container:: example

    Repeat ties:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(3 * [(1, 4)], [4, rt(4), rt(4)])
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score, includes=["abjad.ily"])
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
            \override TimeSignature.style = #'numbered
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
                    c'4
                    c'4
                    \repeatTie
                    c'4
                    \repeatTie
                }
            }
        >>

..  container:: example

    Swell schema:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         3 * [(1, 4)],
    ...         [w(2, 4), h(w(2, 4)), rt(w(2, 4)), h(w(2, 4)), rt(4)],
    ...     )
    ...     baca.hairpin(voice, "p < f >", pieces=baca.select.clparts(voice[:-1], [1])),
    ...     baca.dynamic(voice[-1], "p")
    ...     score = make_score(voice, time_signatures)
    ...     baca.dls_staff_padding(voice, 4)
    ...     result = baca.lilypond.file(score, includes=["abjad.ily"])
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
            \override TimeSignature.style = #'numbered
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
                    \override DynamicLineSpanner.staff-padding = 4
                    \time 1/4
                    c'4 * 1/2
                    \p
                    \<
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c'4 * 1/2
                    \f
                    \>
                    c'4 * 1/2
                    \p
                    \<
                    \repeatTie
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c'4 * 1/2
                    \f
                    \>
                    c'4
                    \p
                    \repeatTie
                    \revert DynamicLineSpanner.staff-padding
                }
            }
        >>


..  container:: example

    Rewrites meter:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         2 * [(4, 4)],
    ...         [4, 8, 8, 8, 4]
    ...     )
    ...     score = make_score(voice, time_signatures, pnd=(1, 16))
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 16)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \time 4/4
                    c'4
                    c'2
                    c'4
                    ~
                    c'4
                    c'2
                    c'4
                }
            }
        >>

..  container:: example

    Nested tuplets:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         2 * [(4, 4)],
    ...         [T([4, 4, 4, T([4, 4, 4], -4)], -4), 16],
    ...     )
    ...     score = make_score(voice, time_signatures, pnd=(1, 16))
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 16)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/5
                    {
                        \time 4/4
                        c'4
                        c'4
                        c'4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 2/3
                        {
                            c'4
                            c'4
                            c'4
                        }
                    }
                    c'1
                }
            }
        >>

..  container:: example

    Containers:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         2 * [(4, 4)],
    ...         [C([4, 4, 4, 4]), C([4, 4, T([4, 4, 4], -4)])],
    ...     )
    ...     score = make_score(voice, time_signatures, pnd=(1, 16))
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 16)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    {
                        \time 4/4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                    {
                        c'4
                        c'4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 2/3
                        {
                            c'4
                            c'4
                            c'4
                        }
                    }
                }
            }
        >>

..  container:: example

    Tuplets with explicit ratio:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         2 * [(4, 4)],
    ...         [T([4, 4, 4, 4, 4, 4], -8), T([4, 4, 4, 4, 4, 4], "6:4")],
    ...     )
    ...     score = make_score(voice, time_signatures, pnd=(1, 16))
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
            \override TupletBracket.bracket-visibility = ##t
            \override TupletBracket.padding = 2
            autoBeaming = ##f
            proportionalNotationDuration = #(ly:make-moment 1 16)
            tupletFullLength = ##t
        }
        <<
            \new RhythmicStaff
            {
                \new Voice
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 2/3
                    {
                        \time 4/4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/6
                    {
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }
            }
        >>


..  container:: example

    Tupletted ties, tupletted containers:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         [(1, 4)],
    ...         [T([t(1), t(1), C([1, 1, 1]), rt(1), rt(1)], -3)],
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
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
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/7
                    {
                        \time 1/4
                        c'16
                        ~
                        c'16
                        ~
                        {
                            c'16
                            c'16
                            c'16
                        }
                        c'16
                        \repeatTie
                        c'16
                        \repeatTie
                    }
                }
            }
        >>


..  container:: example

    Beams:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         [(1, 4)],
    ...         [T([bl(1), 1, br(1), bl(1), 1, br(1), 1], -3)],
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
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
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/7
                    {
                        \time 1/4
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        c'16
                        [
                        c'16
                        c'16
                        ]
                        c'16
                    }
                }
            }
        >>

..  container:: example

    Trims large rhythms when time signatures are given:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         [(1, 4)],
    ...         [3, 3, 3, 3, "+"]
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     result = baca.lilypond.file(score)
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
            \override TimeSignature.style = #'numbered
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
                    c'8.
                    [
                    c'16
                    ]
                }
            }
        >>

..  container:: example

    Tied invisible music:

    >>> def make_lilypond_file():
    ...     voice, time_signatures = sixteenths(
    ...         [(1, 4)],
    ...         [1, rt(h(1)), h(rt(1)), 1],
    ...         do_not_rewrite_meter=True
    ...     )
    ...     score = make_score(voice, time_signatures)
    ...     baca.dls_staff_padding(voice, 4)
    ...     result = baca.lilypond.file(score, includes=["abjad.ily"])
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
            \override TimeSignature.style = #'numbered
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
                    \override DynamicLineSpanner.staff-padding = 4
                    \time 1/4
                    c'16
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c'16
                    \repeatTie
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c'16
                    \repeatTie
                    c'16
                    \revert DynamicLineSpanner.staff-padding
                }
            }
        >>

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
