r"""
Constellation.

..  container:: example

    Here are the 8 constellations in CC1:

    >>> circuit = baca.CC1()
    >>> for constellation in circuit:
    ...     constellation
    Constellation(180)
    Constellation(140)
    Constellation(80)
    Constellation(100)
    Constellation(180)
    Constellation(150)
    Constellation(120)
    Constellation(108)

    Here are the 180 chords in constellation 1:

    >>> constellation = circuit[1 - 1]
    >>> chords = []
    >>> for set_ in constellation:
    ...     chord = abjad.Chord(set_, (1, 4))
    ...     constellation.label_chord(chord)
    ...     chords.append(chord)

    >>> score = abjad.illustrators.make_piano_score(chords)
    >>> time_signature = abjad.TimeSignature((1, 4))
    >>> first_leaf = abjad.select(score).leaf(0)
    >>> abjad.attach(time_signature, first_leaf)
    >>> last_leaf = abjad.select(score).leaf(-1)
    >>> bar_line = abjad.BarLine("|.")
    >>> abjad.attach(bar_line, last_leaf)
    >>> for string in  (
    ...     r"\override Score.BarLine.stencil = ##t",
    ...     r"\override Score.SpanBar.stencil = ##t",
    ... ):
    ...     literal = abjad.LilyPondLiteral(string, format_slot="after")
    ...     abjad.attach(literal, last_leaf)

    >>> leaves = abjad.select(score["Treble_Staff"]).leaves()
    >>> for i, leaf in enumerate(leaves):
    ...     if 0 < i and i % 12 == 0:
    ...         strut = abjad.Markup(r"\markup A", direction=abjad.Up, literal=True)
    ...         abjad.tweak(strut).staff_padding = 22
    ...         abjad.tweak(strut).transparent = True
    ...         abjad.attach(strut, leaf)

    >>> preamble = r'''#(set-global-staff-size 12)
    ...
    ... \paper {
    ...     left-margin = 0\in
    ...     right-margin = 0\in
    ... }
    ... \layout {
    ...     ragged-right = ##t
    ...     \context {
    ...         \Staff
    ...         \override VerticalAxisGroup.staff-staff-spacing.minimum-distance = 6
    ...     }
    ...     \context {
    ...         \Score
    ...         \override Accidental.X-extent = ##f
    ...         \override BarLine.stencil = ##f
    ...         \override Clef.space-alist.first-note = #'(extra-space . 8)
    ...         \override Rest.transparent = ##t
    ...         \override SpanBar.stencil = ##f
    ...         \override TextScript.color = #blue
    ...         \override TextScript.staff-padding = 10
    ...         \override TimeSignature.stencil = ##f
    ...         proportionalNotationDuration = #(ly:make-moment 1 24)
    ...     }
    ... }'''

    >>> lilypond_file = abjad.LilyPondFile([preamble, score])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \time 1/4
                    \clef "treble"
                    r4
                    ^ \markup { 1-1 }
                    cs'4
                    ^ \markup { 1-2 }
                    <ef' fs' a' cs''>4
                    ^ \markup { 1-3 }
                    <g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-4 }
                    <g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-5 }
                    r4
                    ^ \markup { 1-6 }
                    cs'4
                    ^ \markup { 1-7 }
                    <ef' fs' a' cs''>4
                    ^ \markup { 1-8 }
                    <g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-9 }
                    <g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-10 }
                    <b f'>4
                    ^ \markup { 1-11 }
                    <b cs' f'>4
                    ^ \markup { 1-12 }
                    <b ef' f' fs' a' cs''>4
                    ^ \markup { 1-13 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <b f' g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-14 }
                    <b f' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-15 }
                    <af' b' f''>4
                    ^ \markup { 1-16 }
                    <cs' af' b' f''>4
                    ^ \markup { 1-17 }
                    <ef' fs' af' a' b' cs'' f''>4
                    ^ \markup { 1-18 }
                    <g' af' b' ef'' f'' fs'' a'' cs'''>4
                    ^ \markup { 1-19 }
                    <af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-20 }
                    <bf' af'' b'' f'''>4
                    ^ \markup { 1-21 }
                    <cs' bf' af'' b'' f'''>4
                    ^ \markup { 1-22 }
                    <ef' fs' a' bf' cs'' af'' b'' f'''>4
                    ^ \markup { 1-23 }
                    <g' bf' ef'' fs'' af'' a'' b'' cs''' f'''>4
                    ^ \markup { 1-24 }
                    <bf' g'' af'' b'' ef''' f''' fs''' a''' cs''''>4
                    ^ \markup { 1-25 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <bf'' af''' b''' f''''>4
                    ^ \markup { 1-26 }
                    <cs' bf'' af''' b''' f''''>4
                    ^ \markup { 1-27 }
                    <ef' fs' a' cs'' bf'' af''' b''' f''''>4
                    ^ \markup { 1-28 }
                    <g' ef'' fs'' a'' bf'' cs''' af''' b''' f''''>4
                    ^ \markup { 1-29 }
                    <g'' bf'' ef''' fs''' af''' a''' b''' cs'''' f''''>4
                    ^ \markup { 1-30 }
                    r4
                    ^ \markup { 1-31 }
                    cs'4
                    ^ \markup { 1-32 }
                    <ef' fs' a' cs''>4
                    ^ \markup { 1-33 }
                    <g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-34 }
                    <g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-35 }
                    r4
                    ^ \markup { 1-36 }
                    cs'4
                    ^ \markup { 1-37 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <ef' fs' a' cs''>4
                    ^ \markup { 1-38 }
                    <g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-39 }
                    <g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-40 }
                    <b f'>4
                    ^ \markup { 1-41 }
                    <b cs' f'>4
                    ^ \markup { 1-42 }
                    <b ef' f' fs' a' cs''>4
                    ^ \markup { 1-43 }
                    <b f' g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-44 }
                    <b f' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-45 }
                    <af' b' f''>4
                    ^ \markup { 1-46 }
                    <cs' af' b' f''>4
                    ^ \markup { 1-47 }
                    <ef' fs' af' a' b' cs'' f''>4
                    ^ \markup { 1-48 }
                    <g' af' b' ef'' f'' fs'' a'' cs'''>4
                    ^ \markup { 1-49 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-50 }
                    <bf' af'' b'' f'''>4
                    ^ \markup { 1-51 }
                    <cs' bf' af'' b'' f'''>4
                    ^ \markup { 1-52 }
                    <ef' fs' a' bf' cs'' af'' b'' f'''>4
                    ^ \markup { 1-53 }
                    <g' bf' ef'' fs'' af'' a'' b'' cs''' f'''>4
                    ^ \markup { 1-54 }
                    <bf' g'' af'' b'' ef''' f''' fs''' a''' cs''''>4
                    ^ \markup { 1-55 }
                    <bf'' af''' b''' f''''>4
                    ^ \markup { 1-56 }
                    <cs' bf'' af''' b''' f''''>4
                    ^ \markup { 1-57 }
                    <ef' fs' a' cs'' bf'' af''' b''' f''''>4
                    ^ \markup { 1-58 }
                    <g' ef'' fs'' a'' bf'' cs''' af''' b''' f''''>4
                    ^ \markup { 1-59 }
                    <g'' bf'' ef''' fs''' af''' a''' b''' cs'''' f''''>4
                    ^ \markup { 1-60 }
                    e'4
                    ^ \markup { 1-61 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <cs' e'>4
                    ^ \markup { 1-62 }
                    <ef' e' fs' a' cs''>4
                    ^ \markup { 1-63 }
                    <e' g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-64 }
                    <e' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-65 }
                    e'4
                    ^ \markup { 1-66 }
                    <cs' e'>4
                    ^ \markup { 1-67 }
                    <ef' e' fs' a' cs''>4
                    ^ \markup { 1-68 }
                    <e' g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-69 }
                    <e' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-70 }
                    <b e' f'>4
                    ^ \markup { 1-71 }
                    <b cs' e' f'>4
                    ^ \markup { 1-72 }
                    <b ef' e' f' fs' a' cs''>4
                    ^ \markup { 1-73 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <b e' f' g' ef'' fs'' a'' cs'''>4
                    ^ \markup { 1-74 }
                    <b e' f' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-75 }
                    <e' af' b' f''>4
                    ^ \markup { 1-76 }
                    <cs' e' af' b' f''>4
                    ^ \markup { 1-77 }
                    <ef' e' fs' af' a' b' cs'' f''>4
                    ^ \markup { 1-78 }
                    <e' g' af' b' ef'' f'' fs'' a'' cs'''>4
                    ^ \markup { 1-79 }
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-80 }
                    <e' bf' af'' b'' f'''>4
                    ^ \markup { 1-81 }
                    <cs' e' bf' af'' b'' f'''>4
                    ^ \markup { 1-82 }
                    <ef' e' fs' a' bf' cs'' af'' b'' f'''>4
                    ^ \markup { 1-83 }
                    <e' g' bf' ef'' fs'' af'' a'' b'' cs''' f'''>4
                    ^ \markup { 1-84 }
                    <e' bf' g'' af'' b'' ef''' f''' fs''' a''' cs''''>4
                    ^ \markup { 1-85 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <e' bf'' af''' b''' f''''>4
                    ^ \markup { 1-86 }
                    <cs' e' bf'' af''' b''' f''''>4
                    ^ \markup { 1-87 }
                    <ef' e' fs' a' cs'' bf'' af''' b''' f''''>4
                    ^ \markup { 1-88 }
                    <e' g' ef'' fs'' a'' bf'' cs''' af''' b''' f''''>4
                    ^ \markup { 1-89 }
                    <e' g'' bf'' ef''' fs''' af''' a''' b''' cs'''' f''''>4
                    ^ \markup { 1-90 }
                    <c' d' e''>4
                    ^ \markup { 1-91 }
                    <c' cs' d' e''>4
                    ^ \markup { 1-92 }
                    <c' d' ef' fs' a' cs'' e''>4
                    ^ \markup { 1-93 }
                    <c' d' g' ef'' e'' fs'' a'' cs'''>4
                    ^ \markup { 1-94 }
                    <c' d' e'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-95 }
                    <c' d' e''>4
                    ^ \markup { 1-96 }
                    <c' cs' d' e''>4
                    ^ \markup { 1-97 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <c' d' ef' fs' a' cs'' e''>4
                    ^ \markup { 1-98 }
                    <c' d' g' ef'' e'' fs'' a'' cs'''>4
                    ^ \markup { 1-99 }
                    <c' d' e'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-100 }
                    <b c' d' f' e''>4
                    ^ \markup { 1-101 }
                    <b c' cs' d' f' e''>4
                    ^ \markup { 1-102 }
                    <b c' d' ef' f' fs' a' cs'' e''>4
                    ^ \markup { 1-103 }
                    <b c' d' f' g' ef'' e'' fs'' a'' cs'''>4
                    ^ \markup { 1-104 }
                    <b c' d' f' e'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-105 }
                    <c' d' af' b' e'' f''>4
                    ^ \markup { 1-106 }
                    <c' cs' d' af' b' e'' f''>4
                    ^ \markup { 1-107 }
                    <c' d' ef' fs' af' a' b' cs'' e'' f''>4
                    ^ \markup { 1-108 }
                    <c' d' g' af' b' ef'' e'' f'' fs'' a'' cs'''>4
                    ^ \markup { 1-109 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <c' d' af' b' e'' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-110 }
                    <c' d' bf' e'' af'' b'' f'''>4
                    ^ \markup { 1-111 }
                    <c' cs' d' bf' e'' af'' b'' f'''>4
                    ^ \markup { 1-112 }
                    <c' d' ef' fs' a' bf' cs'' e'' af'' b'' f'''>4
                    ^ \markup { 1-113 }
                    <c' d' g' bf' ef'' e'' fs'' af'' a'' b'' cs''' f'''>4
                    ^ \markup { 1-114 }
                    <c' d' bf' e'' g'' af'' b'' ef''' f''' fs''' a''' cs''''>4
                    ^ \markup { 1-115 }
                    <c' d' e'' bf'' af''' b''' f''''>4
                    ^ \markup { 1-116 }
                    <c' cs' d' e'' bf'' af''' b''' f''''>4
                    ^ \markup { 1-117 }
                    <c' d' ef' fs' a' cs'' e'' bf'' af''' b''' f''''>4
                    ^ \markup { 1-118 }
                    <c' d' g' ef'' e'' fs'' a'' bf'' cs''' af''' b''' f''''>4
                    ^ \markup { 1-119 }
                    <c' d' e'' g'' bf'' ef''' fs''' af''' a''' b''' cs'''' f''''>4
                    ^ \markup { 1-120 }
                    <c'' d'' e'''>4
                    ^ \markup { 1-121 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <cs' c'' d'' e'''>4
                    ^ \markup { 1-122 }
                    <ef' fs' a' c'' cs'' d'' e'''>4
                    ^ \markup { 1-123 }
                    <g' c'' d'' ef'' fs'' a'' cs''' e'''>4
                    ^ \markup { 1-124 }
                    <c'' d'' g'' ef''' e''' fs''' a''' cs''''>4
                    ^ \markup { 1-125 }
                    <c'' d'' e'''>4
                    ^ \markup { 1-126 }
                    <cs' c'' d'' e'''>4
                    ^ \markup { 1-127 }
                    <ef' fs' a' c'' cs'' d'' e'''>4
                    ^ \markup { 1-128 }
                    <g' c'' d'' ef'' fs'' a'' cs''' e'''>4
                    ^ \markup { 1-129 }
                    <c'' d'' g'' ef''' e''' fs''' a''' cs''''>4
                    ^ \markup { 1-130 }
                    <b f' c'' d'' e'''>4
                    ^ \markup { 1-131 }
                    <b cs' f' c'' d'' e'''>4
                    ^ \markup { 1-132 }
                    <b ef' f' fs' a' c'' cs'' d'' e'''>4
                    ^ \markup { 1-133 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <b f' g' c'' d'' ef'' fs'' a'' cs''' e'''>4
                    ^ \markup { 1-134 }
                    <b f' c'' d'' g'' ef''' e''' fs''' a''' cs''''>4
                    ^ \markup { 1-135 }
                    <af' b' c'' d'' f'' e'''>4
                    ^ \markup { 1-136 }
                    <cs' af' b' c'' d'' f'' e'''>4
                    ^ \markup { 1-137 }
                    <ef' fs' af' a' b' c'' cs'' d'' f'' e'''>4
                    ^ \markup { 1-138 }
                    <g' af' b' c'' d'' ef'' f'' fs'' a'' cs''' e'''>4
                    ^ \markup { 1-139 }
                    <af' b' c'' d'' f'' g'' ef''' e''' fs''' a''' cs''''>4
                    ^ \markup { 1-140 }
                    <bf' c'' d'' af'' b'' e''' f'''>4
                    ^ \markup { 1-141 }
                    <cs' bf' c'' d'' af'' b'' e''' f'''>4
                    ^ \markup { 1-142 }
                    <ef' fs' a' bf' c'' cs'' d'' af'' b'' e''' f'''>4
                    ^ \markup { 1-143 }
                    <g' bf' c'' d'' ef'' fs'' af'' a'' b'' cs''' e''' f'''>4
                    ^ \markup { 1-144 }
                    <bf' c'' d'' g'' af'' b'' ef''' e''' f''' fs''' a''' cs''''>4
                    ^ \markup { 1-145 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <c'' d'' bf'' e''' af''' b''' f''''>4
                    ^ \markup { 1-146 }
                    <cs' c'' d'' bf'' e''' af''' b''' f''''>4
                    ^ \markup { 1-147 }
                    <ef' fs' a' c'' cs'' d'' bf'' e''' af''' b''' f''''>4
                    ^ \markup { 1-148 }
                    <g' c'' d'' ef'' fs'' a'' bf'' cs''' e''' af''' b''' f''''>4
                    ^ \markup { 1-149 }
                    <c'' d'' g'' bf'' ef''' e''' fs''' af''' a''' b''' cs'''' f''''>4
                    ^ \markup { 1-150 }
                    <c''' d''' e''''>4
                    ^ \markup { 1-151 }
                    <cs' c''' d''' e''''>4
                    ^ \markup { 1-152 }
                    <ef' fs' a' cs'' c''' d''' e''''>4
                    ^ \markup { 1-153 }
                    <g' ef'' fs'' a'' c''' cs''' d''' e''''>4
                    ^ \markup { 1-154 }
                    <g'' c''' d''' ef''' fs''' a''' cs'''' e''''>4
                    ^ \markup { 1-155 }
                    <c''' d''' e''''>4
                    ^ \markup { 1-156 }
                    <cs' c''' d''' e''''>4
                    ^ \markup { 1-157 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <ef' fs' a' cs'' c''' d''' e''''>4
                    ^ \markup { 1-158 }
                    <g' ef'' fs'' a'' c''' cs''' d''' e''''>4
                    ^ \markup { 1-159 }
                    <g'' c''' d''' ef''' fs''' a''' cs'''' e''''>4
                    ^ \markup { 1-160 }
                    <b f' c''' d''' e''''>4
                    ^ \markup { 1-161 }
                    <b cs' f' c''' d''' e''''>4
                    ^ \markup { 1-162 }
                    <b ef' f' fs' a' cs'' c''' d''' e''''>4
                    ^ \markup { 1-163 }
                    <b f' g' ef'' fs'' a'' c''' cs''' d''' e''''>4
                    ^ \markup { 1-164 }
                    <b f' g'' c''' d''' ef''' fs''' a''' cs'''' e''''>4
                    ^ \markup { 1-165 }
                    <af' b' f'' c''' d''' e''''>4
                    ^ \markup { 1-166 }
                    <cs' af' b' f'' c''' d''' e''''>4
                    ^ \markup { 1-167 }
                    <ef' fs' af' a' b' cs'' f'' c''' d''' e''''>4
                    ^ \markup { 1-168 }
                    <g' af' b' ef'' f'' fs'' a'' c''' cs''' d''' e''''>4
                    ^ \markup { 1-169 }
                    - \tweak staff-padding 22
                    - \tweak transparent ##t
                    ^ \markup A
                    <af' b' f'' g'' c''' d''' ef''' fs''' a''' cs'''' e''''>4
                    ^ \markup { 1-170 }
                    <bf' af'' b'' c''' d''' f''' e''''>4
                    ^ \markup { 1-171 }
                    <cs' bf' af'' b'' c''' d''' f''' e''''>4
                    ^ \markup { 1-172 }
                    <ef' fs' a' bf' cs'' af'' b'' c''' d''' f''' e''''>4
                    ^ \markup { 1-173 }
                    <g' bf' ef'' fs'' af'' a'' b'' c''' cs''' d''' f''' e''''>4
                    ^ \markup { 1-174 }
                    <bf' g'' af'' b'' c''' d''' ef''' f''' fs''' a''' cs'''' e''''>4
                    ^ \markup { 1-175 }
                    <bf'' c''' d''' af''' b''' e'''' f''''>4
                    ^ \markup { 1-176 }
                    <cs' bf'' c''' d''' af''' b''' e'''' f''''>4
                    ^ \markup { 1-177 }
                    <ef' fs' a' cs'' bf'' c''' d''' af''' b''' e'''' f''''>4
                    ^ \markup { 1-178 }
                    <g' ef'' fs'' a'' bf'' c''' cs''' d''' af''' b''' e'''' f''''>4
                    ^ \markup { 1-179 }
                    <g'' bf'' c''' d''' ef''' fs''' af''' a''' b''' cs'''' e'''' f''''>4
                    ^ \markup { 1-180 }
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <bf,,, c,, d,, g,, af,, b,, ef, e, f, fs, a, cs>4
                    <bf,,, c,, d,, af,, b,, e, f, g, ef fs a>4
                    <bf,,, c,, d,, af,, b,, e, f, g>4
                    <bf,,, c,, d,, af,, b,, e, f,>4
                    <bf,,, c,, d,, af,, b,, e, f,>4
                    <c,, d,, g,, bf,, ef, e, fs, af, a, b, cs f>4
                    <c,, d,, bf,, e, g, af, b, ef f fs a>4
                    <c,, d,, bf,, e, af, b, f g>4
                    <c,, d,, bf,, e, af, b, f>4
                    <c,, d,, bf,, e, af, b, f>4
                    <c,, d,, g,, ef, e, fs, a, bf, cs af>4
                    <c,, d,, e, g, bf, ef fs af a>4
                    <c,, d,, e, bf, g af>4
                    <c,, d,, e, bf, af>4
                    <c,, d,, e, bf, af>4
                    <c,, d,, g,, ef, e, fs, a, cs bf>4
                    <c,, d,, e, g, ef fs a bf>4
                    <c,, d,, e, g bf>4
                    <c,, d,, e, bf>4
                    <c,, d,, e, bf>4
                    <c,, d,, g,, ef, e, fs, a, cs>4
                    <c,, d,, e, g, ef fs a>4
                    <c,, d,, e, g>4
                    <c,, d,, e,>4
                    <c,, d,, e,>4
                    <c,, d,, g,, ef, e, fs, a, cs>4
                    <c,, d,, e, g, ef fs a>4
                    <c,, d,, e, g>4
                    <c,, d,, e,>4
                    <c,, d,, e,>4
                    <bf,,, g,, af,, b,, c, d, ef, f, fs, a, cs e>4
                    <bf,,, af,, b,, c, d, f, g, ef e fs a>4
                    <bf,,, af,, b,, c, d, f, e g>4
                    <bf,,, af,, b,, c, d, f, e>4
                    <bf,,, af,, b,, c, d, f, e>4
                    <g,, bf,, c, d, ef, fs, af, a, b, cs e f>4
                    <bf,, c, d, g, af, b, ef e f fs a>4
                    <bf,, c, d, af, b, e f g>4
                    <bf,, c, d, af, b, e f>4
                    <bf,, c, d, af, b, e f>4
                    <g,, c, d, ef, fs, a, bf, cs e af>4
                    <c, d, g, bf, ef e fs af a>4
                    <c, d, bf, e g af>4
                    <c, d, bf, e af>4
                    <c, d, bf, e af>4
                    <g,, c, d, ef, fs, a, cs e bf>4
                    <c, d, g, ef e fs a bf>4
                    <c, d, e g bf>4
                    <c, d, e bf>4
                    <c, d, e bf>4
                    <g,, c, d, ef, fs, a, cs e>4
                    <c, d, g, ef e fs a>4
                    <c, d, e g>4
                    <c, d, e>4
                    <c, d, e>4
                    <g,, c, d, ef, fs, a, cs e>4
                    <c, d, g, ef e fs a>4
                    <c, d, e g>4
                    <c, d, e>4
                    <c, d, e>4
                    <bf,,, g,, af,, b,, ef, f, fs, a, c cs d>4
                    <bf,,, af,, b,, f, g, c d ef fs a>4
                    <bf,,, af,, b,, f, c d g>4
                    <bf,,, af,, b,, f, c d>4
                    <bf,,, af,, b,, f, c d>4
                    <g,, bf,, ef, fs, af, a, b, c cs d f>4
                    <bf,, g, af, b, c d ef f fs a>4
                    <bf,, af, b, c d f g>4
                    <bf,, af, b, c d f>4
                    <bf,, af, b, c d f>4
                    <g,, ef, fs, a, bf, c cs d af>4
                    <g, bf, c d ef fs af a>4
                    <bf, c d g af>4
                    <bf, c d af>4
                    <bf, c d af>4
                    <g,, ef, fs, a, c cs d bf>4
                    <g, c d ef fs a bf>4
                    <c d g bf>4
                    <c d bf>4
                    <c d bf>4
                    <g,, ef, fs, a, c cs d>4
                    <g, c d ef fs a>4
                    <c d g>4
                    <c d>4
                    <c d>4
                    <g,, ef, fs, a, c cs d>4
                    <g, c d ef fs a>4
                    <c d g>4
                    <c d>4
                    <c d>4
                    <bf,,, g,, af,, b,, ef, f, fs, a, cs>4
                    <bf,,, af,, b,, f, g, ef fs a>4
                    <bf,,, af,, b,, f, g>4
                    <bf,,, af,, b,, f,>4
                    <bf,,, af,, b,, f,>4
                    <g,, bf,, ef, fs, af, a, b, cs f>4
                    <bf,, g, af, b, ef f fs a>4
                    <bf,, af, b, f g>4
                    <bf,, af, b, f>4
                    <bf,, af, b, f>4
                    <g,, ef, fs, a, bf, cs af>4
                    <g, bf, ef fs af a>4
                    <bf, g af>4
                    <bf, af>4
                    <bf, af>4
                    <g,, ef, fs, a, cs bf>4
                    <g, ef fs a bf>4
                    <g bf>4
                    bf4
                    bf4
                    <g,, ef, fs, a, cs>4
                    <g, ef fs a>4
                    g4
                    r4
                    r4
                    <g,, ef, fs, a, cs>4
                    <g, ef fs a>4
                    g4
                    r4
                    r4
                    <bf,,, g,, af,, b,, ef, f, fs, a, cs>4
                    <bf,,, af,, b,, f, g, ef fs a>4
                    <bf,,, af,, b,, f, g>4
                    <bf,,, af,, b,, f,>4
                    <bf,,, af,, b,, f,>4
                    <g,, bf,, ef, fs, af, a, b, cs f>4
                    <bf,, g, af, b, ef f fs a>4
                    <bf,, af, b, f g>4
                    <bf,, af, b, f>4
                    <bf,, af, b, f>4
                    <g,, ef, fs, a, bf, cs af>4
                    <g, bf, ef fs af a>4
                    <bf, g af>4
                    <bf, af>4
                    <bf, af>4
                    <g,, ef, fs, a, cs bf>4
                    <g, ef fs a bf>4
                    <g bf>4
                    bf4
                    bf4
                    <g,, ef, fs, a, cs>4
                    <g, ef fs a>4
                    g4
                    r4
                    r4
                    <g,, ef, fs, a, cs>4
                    <g, ef fs a>4
                    g4
                    r4
                    r4
                    <bf,,, g,, af,, b,, ef, f, fs, a, cs>4
                    <bf,,, af,, b,, f, g, ef fs a>4
                    <bf,,, af,, b,, f, g>4
                    <bf,,, af,, b,, f,>4
                    <bf,,, af,, b,, f,>4
                    <g,, bf,, ef, fs, af, a, b, cs f>4
                    <bf,, g, af, b, ef f fs a>4
                    <bf,, af, b, f g>4
                    <bf,, af, b, f>4
                    <bf,, af, b, f>4
                    <g,, ef, fs, a, bf, cs af>4
                    <g, bf, ef fs af a>4
                    <bf, g af>4
                    <bf, af>4
                    <bf, af>4
                    <g,, ef, fs, a, cs bf>4
                    <g, ef fs a bf>4
                    <g bf>4
                    bf4
                    bf4
                    <g,, ef, fs, a, cs>4
                    <g, ef fs a>4
                    g4
                    r4
                    r4
                    <g,, ef, fs, a, cs>4
                    <g, ef fs a>4
                    g4
                    r4
                    r4
                    \bar "|."
                    \override Score.BarLine.stencil = ##t
                    \override Score.SpanBar.stencil = ##t
                }
            >>
        >>

..  container:: example

    Here's the generator of constellation 1:

    >>> circuit = baca.CC1()
    >>> constellation = circuit[1 - 1]
    >>> generator = abjad.Sequence(constellation.generator).flatten()
    >>> generator = abjad.Chord(generator, (1, 4))
    >>> constellation.color_chord(generator)
    >>> constellation.label_chord(generator)
    >>> score = abjad.illustrators.make_piano_score([generator])
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        e'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #green
                        \tweak color #green
                        ef'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        cs''''
                    >4
                    ^ \markup { 1-80 }
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        bf
                    >4
                }
            >>
        >>

..  container:: example

    Here're the generator and pivot for constellation 1:

    >>> circuit = baca.CC1()
    >>> constellation = circuit[1 - 1]
    >>> generator = abjad.Sequence(constellation.generator).flatten()
    >>> generator = abjad.Chord(generator, (1, 4))
    >>> constellation.color_chord(generator)
    >>> constellation.label_chord(generator)
    >>> pivot = circuit.find_pivot(constellation, circuit[1])
    >>> pivot = abjad.Chord(pivot, (1, 4))
    >>> constellation.label_chord(pivot)
    >>> leaves = [generator, pivot]
    >>> score = abjad.illustrators.make_piano_score(leaves)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        e'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #green
                        \tweak color #green
                        ef'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        cs''''
                    >4
                    ^ \markup { 1-80 }
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-80 }
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        bf
                    >4
                    <c d bf>4
                }
            >>
        >>

..  container:: example

    Here's the generator of constellation 1:

    >>> circuit = baca.CC1()
    >>> constellation = circuit[1 - 1]
    >>> generator = abjad.Sequence(constellation.generator).flatten()
    >>> generator = abjad.Chord(generator, (1, 4))
    >>> constellation.label_chord(generator)
    >>> leaves = [generator]
    >>> score = abjad.illustrators.make_piano_score(leaves)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-80 }
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <c d bf>4
                }
            >>
        >>

..  container:: example

    Here's the generator and pivot of constellation 1:

    >>> circuit = baca.CC1()
    >>> constellation = circuit[1 - 1]
    >>> generator = abjad.Sequence(constellation.generator).flatten()
    >>> generator = abjad.Chord(generator, (1, 4))
    >>> constellation.label_chord(generator)
    >>> pivot = circuit.find_pivot(constellation, circuit[1])
    >>> pivot = abjad.Chord(pivot, (1, 4))
    >>> constellation.label_chord(pivot)
    >>> leaves = [generator, pivot]
    >>> score = abjad.illustrators.make_piano_score(leaves)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-80 }
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-80 }
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <c d bf>4
                    <c d bf>4
                }
            >>
        >>

..  container:: example

    Here's the pivot of constellation 1:

    >>> circuit = baca.CC1()
    >>> constellation = circuit[1 - 1]
    >>> pivot = circuit.find_pivot(constellation, circuit[1])
    >>> pivot = abjad.Chord(pivot, (1, 4))
    >>> constellation.label_chord(pivot)
    >>> leaves = [pivot]
    >>> score = abjad.illustrators.make_piano_score(leaves)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    ^ \markup { 1-80 }
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <c d bf>4
                }
            >>
        >>

..  container:: example

    Here's the colored generator chord for each constellation in CC1:

    >>> circuit = baca.CC1()
    >>> generators = []
    >>> for constellation in circuit:
    ...     generator = abjad.Sequence(constellation.generator).flatten()
    ...     generator = abjad.Chord(generator, (1, 4))
    ...     constellation.color_chord(generator)
    ...     generators.append(generator)

    >>> score = abjad.illustrators.make_piano_score(generators)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        e'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #green
                        \tweak color #green
                        ef'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        cs''''
                    >4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        e'
                        \tweak Accidental.color #green
                        \tweak color #green
                        af'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #green
                        \tweak color #green
                        f''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        ef'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        a'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        cs''''
                    >4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #green
                        \tweak color #green
                        c'
                        \tweak Accidental.color #red
                        \tweak color #red
                        d'
                        \tweak Accidental.color #green
                        \tweak color #green
                        bf'
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a''
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs''''
                    >4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        c'
                        \tweak Accidental.color #red
                        \tweak color #red
                        d'
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #green
                        \tweak color #green
                        ef''
                        \tweak Accidental.color #red
                        \tweak color #red
                        a''
                        \tweak Accidental.color #green
                        \tweak color #green
                        cs'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f''''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs''''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''''
                    >4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs'
                        \tweak Accidental.color #red
                        \tweak color #red
                        e'
                        \tweak Accidental.color #green
                        \tweak color #green
                        d''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        fs''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af''
                        \tweak Accidental.color #green
                        \tweak color #green
                        bf''
                        \tweak Accidental.color #green
                        \tweak color #green
                        f'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        a'''
                    >4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        ef'
                        \tweak Accidental.color #red
                        \tweak color #red
                        f'
                        \tweak Accidental.color #green
                        \tweak color #green
                        b'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        cs''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        e''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        af'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a''''
                    >4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #green
                        \tweak color #green
                        c'
                        \tweak Accidental.color #red
                        \tweak color #red
                        f'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g'
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        fs''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af''
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        e'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a'''
                    >4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #green
                        \tweak color #green
                        d'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g'
                        \tweak Accidental.color #green
                        \tweak color #green
                        bf'
                        \tweak Accidental.color #green
                        \tweak color #green
                        e''
                        \tweak Accidental.color #red
                        \tweak color #red
                        f''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        fs''
                        \tweak Accidental.color #green
                        \tweak color #green
                        af''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        a''
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef'''
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs''''
                    >4
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        bf
                    >4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf
                    >4
                    \tweak Accidental.color #red
                    \tweak color #red
                    e4
                    \tweak Accidental.color #red
                    \tweak color #red
                    e4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef
                    >4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf
                    >4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf
                    >4
                    \tweak Accidental.color #red
                    \tweak color #red
                    c4
                }
            >>
        >>

..  container:: example

    Here's the colored generator and pivot for each constellation in CC1:

    >>> circuit = baca.CC1()
    >>> generators, pivots = [], []
    >>> length = len(circuit)
    >>> for i, constellation in enumerate(circuit):
    ...     generator = abjad.Sequence(constellation.generator).flatten()
    ...     generator = abjad.Chord(generator, (1, 4))
    ...     constellation.color_chord(generator)
    ...     generators.append(generator)
    ...     next_constellation = circuit[(i + 1) % length]
    ...     pivot = circuit.find_pivot(constellation, next_constellation)
    ...     pivot = abjad.Chord(pivot, (1, 4))
    ...     pivots.append(pivot)

    >>> chords = list(zip(generators, pivots))
    >>> chords_ = abjad.Sequence(chords).flatten()
    >>> score = abjad.illustrators.make_piano_score(chords_)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        e'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #green
                        \tweak color #green
                        ef'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        cs''''
                    >4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        e'
                        \tweak Accidental.color #green
                        \tweak color #green
                        af'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #green
                        \tweak color #green
                        f''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        ef'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        a'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        cs''''
                    >4
                    <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #green
                        \tweak color #green
                        c'
                        \tweak Accidental.color #red
                        \tweak color #red
                        d'
                        \tweak Accidental.color #green
                        \tweak color #green
                        bf'
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a''
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs''''
                    >4
                    <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        c'
                        \tweak Accidental.color #red
                        \tweak color #red
                        d'
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b'
                        \tweak Accidental.color #green
                        \tweak color #green
                        ef''
                        \tweak Accidental.color #red
                        \tweak color #red
                        a''
                        \tweak Accidental.color #green
                        \tweak color #green
                        cs'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        f''''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs''''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''''
                    >4
                    <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs'
                        \tweak Accidental.color #red
                        \tweak color #red
                        e'
                        \tweak Accidental.color #green
                        \tweak color #green
                        d''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        fs''
                        \tweak Accidental.color #green
                        \tweak color #green
                        g''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af''
                        \tweak Accidental.color #green
                        \tweak color #green
                        bf''
                        \tweak Accidental.color #green
                        \tweak color #green
                        f'''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        a'''
                    >4
                    <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        ef'
                        \tweak Accidental.color #red
                        \tweak color #red
                        f'
                        \tweak Accidental.color #green
                        \tweak color #green
                        b'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        cs''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        e''
                        \tweak Accidental.color #green
                        \tweak color #green
                        fs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        af'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a''''
                    >4
                    <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #green
                        \tweak color #green
                        c'
                        \tweak Accidental.color #red
                        \tweak color #red
                        f'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g'
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        fs''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        af''
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        e'''
                        \tweak Accidental.color #green
                        \tweak color #green
                        a'''
                    >4
                    <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                    <
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        b
                        \tweak Accidental.color #green
                        \tweak color #green
                        d'
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g'
                        \tweak Accidental.color #green
                        \tweak color #green
                        bf'
                        \tweak Accidental.color #green
                        \tweak color #green
                        e''
                        \tweak Accidental.color #red
                        \tweak color #red
                        f''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        fs''
                        \tweak Accidental.color #green
                        \tweak color #green
                        af''
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        a''
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef'''
                        \tweak Accidental.color #red
                        \tweak color #red
                        cs''''
                    >4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        bf
                    >4
                    <c d bf>4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf
                    >4
                    e4
                    \tweak Accidental.color #red
                    \tweak color #red
                    e4
                    e4
                    \tweak Accidental.color #red
                    \tweak color #red
                    e4
                    <c ef>4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        c
                        \tweak Accidental.color #red
                        \tweak color #red
                        ef
                    >4
                    <d g bf>4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #blue
                        \tweak color #blue
                        g
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf
                    >4
                    <d bf>4
                    <
                        \tweak Accidental.color #red
                        \tweak color #red
                        d
                        \tweak Accidental.color #red
                        \tweak color #red
                        bf
                    >4
                    c4
                    \tweak Accidental.color #red
                    \tweak color #red
                    c4
                    <c d bf>4
                }
            >>
        >>

..  container:: example

    Here's the generator for each constellation in CC1:

    >>> circuit = baca.CC1()
    >>> generators = []
    >>> for constellation in circuit:
    ...     generator = abjad.Sequence(constellation.generator).flatten()
    ...     generator = abjad.Chord(generator, (1, 4))
    ...     generators.append(generator)

    >>> score = abjad.illustrators.make_piano_score(generators)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                    <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                    <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                    <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                    <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                    <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <c d bf>4
                    <c d bf>4
                    e4
                    e4
                    <c ef>4
                    <d g bf>4
                    <d bf>4
                    c4
                }
            >>
        >>

..  container:: example

    Here's the generator chord and pivot chord for each constellation in CC1:

    >>> circuit = baca.CC1()
    >>> generators = []
    >>> length = len(circuit)
    >>> for i, constellation in enumerate(circuit):
    ...     generator = abjad.Sequence(constellation.generator).flatten()
    ...     generator = abjad.Chord(generator, (1, 4))
    ...     generators.append(generator)
    ...     next_constellation = circuit[(i + 1) % length]
    ...     pivot = circuit.find_pivot(constellation, next_constellation)
    ...     pivot = abjad.Chord(pivot, (1, 4))
    ...     pivots.append(pivot)

    >>> chords = list(zip(generators, pivots))
    >>> chords_ = abjad.Sequence(chords).flatten()
    >>> score = abjad.illustrators.make_piano_score(chords_)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                    <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                    <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                    <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                    <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                    <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                    <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                    <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                    <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                    <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                    <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                    <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <c d bf>4
                    <c d bf>4
                    <c d bf>4
                    e4
                    e4
                    e4
                    e4
                    <c ef>4
                    <c ef>4
                    <d g bf>4
                    <d g bf>4
                    <d bf>4
                    <d bf>4
                    c4
                    c4
                    <c d bf>4
                }
            >>
        >>

..  container:: example

    Here's the pivot chord for each constellation in CC1:

    >>> circuit = baca.CC1()
    >>> pivots = []
    >>> for i, constellation in enumerate(circuit):
    ...     next_constellation = circuit[(i + 1) % length]
    ...     pivot = circuit.find_pivot(constellation, next_constellation)
    ...     pivot = abjad.Chord(pivot, (1, 4))
    ...     pivots.append(pivot)

    >>> score = abjad.illustrators.make_piano_score(pivots)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                    <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                    <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                    <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                    <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                    <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                }
                \context Staff = "Bass_Staff"
                {
                    \clef "bass"
                    <c d bf>4
                    e4
                    e4
                    <c ef>4
                    <d g bf>4
                    <d bf>4
                    c4
                    <c d bf>4
                }
            >>
        >>

"""
import abjad


class Constellation:
    """
    Constellation.

    ..  container:: example

        >>> generators = [
        ...     [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        ...     [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        ...     [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        ...     [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        ...     [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        ...     [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        ...     [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        ...     [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
        ... ]
        >>> circuit = baca.Circuit(generators, "[A0, C8]")
        >>> circuit[1 - 1]
        Constellation(180)

    """

    __slots__ = (
        "_circuit",
        "_generator",
        "_sets",
    )

    ### INITIALIZER ###

    def __init__(self, circuit, generator):
        self._circuit = circuit
        self._generator = generator
        self._sets = self._constellate(generator, circuit.range_)

    ### SPECIAL METHODS ###

    def __contains__(self, set_):
        """
        Is true when constellation contains ``set_``.

        ..  container:: example

            >>> generator = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            >>> constellation = baca.Constellation._constellate(generator, "[A0, C8]")
            >>> numbers = [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
            >>> set_ = abjad.PitchSet(numbers)
            >>> set_ in constellation
            True

        """
        return set_ in self._sets

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> generator = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            >>> constellation = baca.Constellation._constellate(generator, "[A0, C8]")
            >>> constellation[0]
            PitchSet([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        """
        return self._sets.__getitem__(argument)

    def __len__(self):
        """
        Gets length of constellation.

        ..  container::

            >>> generator = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            >>> constellation = baca.Constellation._constellate(generator, "[A0, C8]")
            >>> len(constellation)
            180

        """
        return len(self._sets)

    def __repr__(self):
        """
        Gets interpreter representation of constellation.

        ..  container:: example

            >>> circuit = baca.CC1()
            >>> constellation = circuit[1 - 1]
            >>> constellation
            Constellation(180)

        """
        return f"{type(self).__name__}({len(self)})"

    ### PRIVATE METHODS ###

    @staticmethod
    def _constellate(generator, range_):
        """
        Constellates ``generator`` in ``range_``.

        ..  container:: example

            >>> generator = [[0, 2, 10], [16, 19, 20]]
            >>> sets = baca.Constellation._constellate(generator, "[C4, C#7]")
            >>> for set_ in sets:
            ...     set_
            PitchSet([0, 2, 4, 7, 8, 10])
            PitchSet([0, 2, 10, 16, 19, 20])
            PitchSet([0, 2, 10, 28, 31, 32])
            PitchSet([4, 7, 8, 12, 14, 22])
            PitchSet([12, 14, 16, 19, 20, 22])
            PitchSet([12, 14, 22, 28, 31, 32])
            PitchSet([4, 7, 8, 24, 26, 34])
            PitchSet([16, 19, 20, 24, 26, 34])
            PitchSet([24, 26, 28, 31, 32, 34])

        ..  container:: example

            >>> generator = [[4, 8, 11], [7, 15, 17]]
            >>> sets = baca.Constellation._constellate(generator, "[C4, C#7]")
            >>> for set_ in sets:
            ...     set_
            PitchSet([4, 7, 8, 11, 15, 17])
            PitchSet([4, 8, 11, 19, 27, 29])
            PitchSet([7, 15, 16, 17, 20, 23])
            PitchSet([16, 19, 20, 23, 27, 29])
            PitchSet([7, 15, 17, 28, 32, 35])
            PitchSet([19, 27, 28, 29, 32, 35])

        """
        assert isinstance(generator, list), repr(generator)
        range_ = abjad.PitchRange(range_)
        transpositions = []
        for part in generator:
            assert isinstance(part, list)
            part = abjad.PitchSet(part)
            transpositions_ = []
            interval = -12
            while True:
                candidate = part.transpose(interval)
                if all(pitch in range_ for pitch in candidate):
                    transpositions_.append(candidate)
                    interval -= 12
                else:
                    break
            transpositions_.reverse()
            interval = 0
            while True:
                candidate = part.transpose(interval)
                if all(pitch in range_ for pitch in candidate):
                    transpositions_.append(candidate)
                    interval += 12
                else:
                    break
            transpositions_ = [[_.number for _ in set_] for set_ in transpositions_]
            transpositions.append(transpositions_)
        sequences = abjad.enumerate.outer_product(transpositions)
        sets = []
        for sequence in sequences:
            numbers = abjad.Sequence(sequence).flatten()
            set_ = abjad.PitchSet(numbers)
            sets.append(set_)
        return sets

    ### PUBLIC PROPERTIES ###

    @property
    def circuit(self):
        """
        Gets circuit to which constellation belongs.

        ..  container:: example

            >>> circuit = baca.CC1()
            >>> constellation = circuit[1 - 1]
            >>> constellation.circuit
            Circuit(8)

            >>> constellation.circuit is circuit
            True

        """
        return self._circuit

    @property
    def generator(self):
        """
        Gets constellation generator.

        ..  container:: example

            >>> circuit = baca.CC1()
            >>> constellation = circuit[1 - 1]
            >>> constellation.generator
            [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]

        """
        return self._generator

    ### PUBLIC METHODS ###

    def color_chord(self, chord):
        """
        Colors ``chord`` according to constellation generator.
        """
        colors = ["#red", "#blue", "#green"]
        color_map = abjad.ColorMap(colors=colors, pitch_iterables=self.generator)
        abjad.Label(chord).color_note_heads(color_map)

    def label_chord(self, chord):
        """
        Labels ``chord`` with constellation and chord number.
        """
        assert isinstance(chord, abjad.Chord)
        constellation_index = self.circuit._constellations.index(self)
        constellation_number = constellation_index + 1
        numbers = [_.number for _ in chord.written_pitches]
        set_ = abjad.PitchSet(numbers)
        chord_index = self._sets.index(set_)
        chord_number = chord_index + 1
        string = rf"\markup {{ {constellation_number}-{chord_number} }}"
        markup = abjad.Markup(string, direction=abjad.Up, literal=True)
        abjad.attach(markup, chord)


class Circuit:
    """
    Circuit.

    ..  container:: example

        >>> circuit = baca.CC1()
        >>> for constellation in circuit:
        ...     constellation
        Constellation(180)
        Constellation(140)
        Constellation(80)
        Constellation(100)
        Constellation(180)
        Constellation(150)
        Constellation(120)
        Constellation(108)

    """

    __slots__ = (
        "_constellations",
        "_generators",
        "_range",
    )

    ### INITIALIZER ###

    def __init__(self, generators, range_):
        self._generators = generators
        range_ = abjad.PitchRange(range_)
        self._range = range_
        constellations = []
        for generator in generators:
            constellation = Constellation(self, generator)
            constellations.append(constellation)
        self._constellations = constellations

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument`` in circuit.

        ..  container:: example

            >>> circuit = baca.CC1()
            >>> circuit[-1]
            Constellation(108)

        """
        return self._constellations.__getitem__(argument)

    def __len__(self):
        """
        Gets length of circuit.

        ..  container:: example

            >>> circuit = baca.CC1()
            >>> len(circuit)
            8

        """
        return len(self._constellations)

    def __repr__(self):
        """
        Gets interpreter representation of circuit.

        ..  container:: example

            >>> baca.CC1()
            Circuit(8)

        """
        return f"{type(self).__name__}({len(self)})"

    ### PRIVATE METHODS ###

    @staticmethod
    def find_pivot(constellation_a, constellation_b):
        """
        Finds pivot from ``constellation_a`` to ``constellation_b``.
        """
        b_generator = abjad.Sequence(constellation_b.generator).flatten()
        b_generator = abjad.PitchSet(b_generator)
        for set_ in constellation_a:
            if set_ == b_generator:
                return set_

    ### PUBLIC PROPERTIES ###

    @property
    def range_(self):
        """
        Gets pitch range.

        ..  container:: example

            >>> baca.CC1().range_
            PitchRange('[A0, C8]')

        """
        return self._range


def CC1():
    """
    Makes constellation circuit 1.

    ..  container:: example

        >>> circuit = baca.CC1()
        >>> for constellation in circuit:
        ...     constellation
        Constellation(180)
        Constellation(140)
        Constellation(80)
        Constellation(100)
        Constellation(180)
        Constellation(150)
        Constellation(120)
        Constellation(108)

    """
    generators = [
        [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
    ]
    return Circuit(generators, "[A0, C8]")
