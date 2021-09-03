r"""
Constellation.

..  container:: example

    Here's the generator of constellation 1:

    >>> circuit = baca.CC1()
    >>> constellation = circuit[1 - 1]
    >>> generator = abjad.Sequence(constellation.generator).flatten()
    >>> generator = abjad.Chord(generator, (1, 4))
    >>> constellation.color_chord(generator)
    >>> constellation.label_chord(generator)
    >>> score, _, _ = abjad.illustrators.make_piano_score([generator], sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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
    >>> score, _, _ = abjad.illustrators.make_piano_score(leaves, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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
    >>> score, _, _ = abjad.illustrators.make_piano_score(leaves, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
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
    >>> score, _, _ = abjad.illustrators.make_piano_score(leaves, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
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
    >>> score, _, _ = abjad.illustrators.make_piano_score(leaves, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble_Staff"
                {
                    \clef "treble"
                    <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
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

    >>> score, _, _ = abjad.illustrators.make_piano_score(generators, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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
    >>> score, _, _ = abjad.illustrators.make_piano_score(chords_, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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

    >>> score, _, _ = abjad.illustrators.make_piano_score(generators, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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
    >>> score, _, _ = abjad.illustrators.make_piano_score(chords_, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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

    >>> score, _, _ = abjad.illustrators.make_piano_score(pivots, sketch=True)
    >>> abjad.show(score) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \new Score
        \with
        {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        }
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
        "_segments",
    )

    ### INITIALIZER ###

    def __init__(self, circuit, generator):
        self._circuit = circuit
        self._generator = generator
        self._segments = self._constellate(generator, circuit.range_)

    ### SPECIAL METHODS ###

    def __contains__(self, segment):
        """
        Is true when constellation contains ``segment``.

        ..  container:: example

            >>> generator = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            >>> constellation = baca.Constellation._constellate(generator, "[A0, C8]")
            >>> numbers = [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
            >>> segment = abjad.PitchSegment(numbers)
            >>> segment in constellation
            True

        """
        return segment in self._segments

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> generator = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            >>> constellation = baca.Constellation._constellate(generator, "[A0, C8]")
            >>> constellation[0]
            PitchSegment([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        """
        return self._segments.__getitem__(argument)

    def __len__(self):
        """
        Gets length of constellation.

        ..  container::

            >>> generator = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            >>> constellation = baca.Constellation._constellate(generator, "[A0, C8]")
            >>> len(constellation)
            180

        """
        return len(self._segments)

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
            >>> segments = baca.Constellation._constellate(generator, "[C4, C#7]")
            >>> for segment in segments:
            ...     segment
            PitchSegment([0, 2, 4, 7, 8, 10])
            PitchSegment([0, 2, 10, 16, 19, 20])
            PitchSegment([0, 2, 10, 28, 31, 32])
            PitchSegment([4, 7, 8, 12, 14, 22])
            PitchSegment([12, 14, 16, 19, 20, 22])
            PitchSegment([12, 14, 22, 28, 31, 32])
            PitchSegment([4, 7, 8, 24, 26, 34])
            PitchSegment([16, 19, 20, 24, 26, 34])
            PitchSegment([24, 26, 28, 31, 32, 34])

        ..  container:: example

            >>> generator = [[4, 8, 11], [7, 15, 17]]
            >>> segments = baca.Constellation._constellate(generator, "[C4, C#7]")
            >>> for segment in segments:
            ...     segment
            PitchSegment([4, 7, 8, 11, 15, 17])
            PitchSegment([4, 8, 11, 19, 27, 29])
            PitchSegment([7, 15, 16, 17, 20, 23])
            PitchSegment([16, 19, 20, 23, 27, 29])
            PitchSegment([7, 15, 17, 28, 32, 35])
            PitchSegment([19, 27, 28, 29, 32, 35])

        """
        assert isinstance(generator, list), repr(generator)
        range_ = abjad.PitchRange(range_)
        transpositions = []
        for part in generator:
            assert isinstance(part, list)
            part = abjad.PitchSegment(part)
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
            transpositions_ = [
                [_.number for _ in segment] for segment in transpositions_
            ]
            transpositions.append(transpositions_)
        sequences = abjad.enumerate.outer_product(transpositions)
        segments = []
        for sequence in sequences:
            numbers = abjad.Sequence(sequence).flatten().sort()
            segment = abjad.PitchSegment(numbers)
            segments.append(segment)
        return segments

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

    # TODO: teach abjad.illustrators.make_piano_score() to preserve markup
    def label_chord(self, chord):
        """
        Labels ``chord`` with constellation and chord number.
        """
        assert isinstance(chord, abjad.Chord)
        constellation_index = self.circuit._constellations.index(self)
        constellation_number = constellation_index + 1
        numbers = [_.number for _ in chord.written_pitches]
        segment = abjad.PitchSegment(numbers)
        chord_index = self._segments.index(segment)
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
        b_generator = abjad.Sequence(constellation_b.generator).flatten().sort()
        b_generator = abjad.PitchSegment(b_generator)
        for segment in constellation_a:
            if segment == b_generator:
                return segment

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
