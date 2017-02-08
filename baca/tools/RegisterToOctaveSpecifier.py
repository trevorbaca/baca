# -*- coding: utf-8 -*-
import abjad


class RegisterToOctaveSpecifier(abjad.abctools.AbjadObject):
    r'''Register-to-octave specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.RegisterToOctaveSpecifier()
            RegisterToOctaveSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_anchor',
        '_octave_number',
        )

    ### INITIALIZER ###

    def __init__(self, anchor=None, octave_number=None):
        if anchor is not None:
            assert anchor in (Center, Bottom, Top), repr(anchor)
        self._anchor = anchor
        if octave_number is not None:
            assert isinstance(octave_number, int), repr(octave_number)
        self._octave_number = octave_number

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        transposition = self._get_transposition()
        for logical_tie in abjad.iterate(argument).by_logical_tie(
            pitched=True,
            with_grace_notes=True,
            ):
            for leaf in logical_tie:
                self._set_pitch(leaf, transposition)

    ### PRIVATE METHODS ###

    def _get_chord_anchor_octave_number(self, chord):
        anchor = self.anchor or Bottom
        if anchor is Bottom:
            pitch = chord.written_pitches[0]
        elif anchor is Top:
            pitch = chord.written_pitches[-1]
        elif anchor is Center:
            pitch = self._get_chord_centroid(chord)
        else:
            raise ValueError(anchor)
        return pitch.octave.number

    @staticmethod
    def _get_chord_centroid(chord):
        soprano = max(chord.written_pitches)
        bass = min(chord.written_pitches)
        centroid = (soprano.number + bass.number) / 2.0
        return abjad.NumberedPitch(centroid)

    def _get_transposition(self):
        octave_number = self.octave_number or 4
        n = 12 * (octave_number - 4)
        return abjad.Transposition(n=n)

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            self._transpose_chord(leaf)
        else:
            raise TypeError(leaf)
        abjad.detach('not yet registered', leaf)

    def _transpose_chord(self, chord):
        octave_number = self.octave_number or 4
        octave_down = abjad.Transposition(n=-12)
        octave_up = abjad.Transposition(n=12)
        while self._get_chord_anchor_octave_number(chord) < octave_number:
            pitches_ = [octave_up(_) for _ in chord.written_pitches]
            chord.written_pitches = pitches_
        while octave_number < self._get_chord_anchor_octave_number(chord):
            pitches_ = [octave_down(_) for _ in chord.written_pitches]
            chord.written_pitches = pitches_
        assert self._get_chord_anchor_octave_number(chord) == octave_number

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        r"""Gets anchor.

        ..  container:: example

            Bass anchored at octave 5:

            ::

                >>> chord = abjad.Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     anchor=Bottom,
                ...     octave_number=5,
                ...     )
                >>> specifier(chord)
                >>> staff = abjad.Staff([chord])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <c'' d''' e''''>1

        ..  container:: example

            Center anchored at octave 5:

            ::

                >>> chord = abjad.Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     anchor=Center,
                ...     octave_number=5,
                ...     )
                >>> specifier(chord)
                >>> staff = abjad.Staff([chord])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <c' d'' e'''>1

        ..  container:: example

            Soprano anchored at octave 5:

            ::

                >>> chord = abjad.Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     anchor=Top,
                ...     octave_number=5,
                ...     )
                >>> specifier(chord)
                >>> staff = abjad.Staff([chord])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <c d' e''>1

        Set to up, down, center or none.

        Returns up, down, center or none.
        """
        return self._anchor

    @property
    def octave_number(self):
        r"""Gets octave number.

        ..  container:: example

            ::

                >>> chord = abjad.Chord("<c, d e'>1")
                >>> staff = abjad.Staff([chord])
                >>> abjad.attach(abjad.Clef('bass'), staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            ::

                >>> chord = Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     octave_number=1,
                ...     )
                >>> specifier(chord)
                >>> staff = abjad.Staff([chord])
                >>> abjad.attach(abjad.Clef('bass'), staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                \clef "bass"
                <c,, d, e>1

        ..  container:: example

            ::

                >>> chord = Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     octave_number=2,
                ...     )
                >>> specifier(chord)
                >>> staff = abjad.Staff([chord])
                >>> abjad.attach(abjad.Clef('bass'), staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            ::

                >>> chord = Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     octave_number=3,
                ...     )
                >>> specifier(chord)
                >>> staff = abjad.Staff([chord])
                >>> abjad.attach(abjad.Clef('bass'), staff[0])
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                \clef "bass"
                <c d' e''>1

        ..  container:: example

            ::

                >>> chord = Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     octave_number=4,
                ...     )
                >>> specifier(chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <c' d'' e'''>1

        ..  container:: example

            ::

                >>> chord = Chord("<c, d e'>1")
                >>> specifier = baca.tools.RegisterToOctaveSpecifier(
                ...     octave_number=5,
                ...     )
                >>> specifier(chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> f(chord)
                <c'' d''' e''''>1

        Returns integer.
        """
        return self._octave_number
