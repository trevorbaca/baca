# -*- coding: utf-8 -*-
import abjad


class RegisterToOctaveSpecifier(abjad.abctools.AbjadObject):
    r"""Register-to-octave specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example
        
        Chords:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [set([0, 14, 28])],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Bottom,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            <c' d'' e'''>16
                        }
                    }
                }
            >>

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [set([0, 14, 28])],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Center,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            <c d' e''>16
                        }
                    }
                }
            >>

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [set([0, 14, 28])],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Top,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            <c, d e'>16
                        }
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[0, 14, 28]],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Bottom,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c'16 [
                            d''16
                            e'''16 ]
                        }
                    }
                }
            >>

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[0, 14, 28]],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Center,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c16 [
                            d'16
                            e''16 ]
                        }
                    }
                }
            >>

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[0, 14, 28]],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Top,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            c,16 [
                            d16
                            e'16 ]
                        }
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14]],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Bottom,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf'16 [
                            c''16
                            d''16 ]
                        }
                    }
                }
            >>

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14]],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Center,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf16 [
                            c'16
                            d'16 ]
                        }
                    }
                }
            >>

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14]],
            ...     baca.tools.RegisterToOctaveSpecifier(
            ...         anchor=Top,
            ...         octave_number=4,
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf16 [
                            c'16
                            d'16 ]
                        }
                    }
                }
            >>

    ..  container:: example

        ::

            >>> baca.tools.RegisterToOctaveSpecifier()
            RegisterToOctaveSpecifier()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_anchor',
        '_octave_number',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(self, anchor=None, octave_number=None, pattern=None):
        if anchor is not None:
            assert anchor in (Center, Bottom, Top), repr(anchor)
        self._anchor = anchor
        if octave_number is not None:
            assert isinstance(octave_number, int), repr(octave_number)
        self._octave_number = octave_number
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, selections=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        if selections is None:
            return
        if isinstance(selections, abjad.Component):
            selections = abjad.select(selections)
        pattern = self.pattern or abjad.select_all()
        selections = pattern.get_matching_items(selections)
        for selection in selections:
            target_octave_number = self.octave_number or 4
            current_octave_number = self._get_anchor_octave_number(selection)
            octave_adjustment = target_octave_number - current_octave_number
            transposition = abjad.Transposition(12 * octave_adjustment)
            for leaf in abjad.iterate(selection).by_leaf(pitched=True):
                self._set_pitch(leaf, transposition)

    ### PRIVATE METHODS ###

    def _get_anchor_octave_number(self, argument):
        pitches = []
        for leaf in abjad.iterate(argument).by_leaf(pitched=True):
            if isinstance(leaf, abjad.Note):
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pitches.extend(leaf.written_pitches)
            else:
                raise TypeError(leaf)
        pitches = list(set(pitches))
        pitches.sort()
        anchor = self.anchor or Bottom
        if anchor is Bottom:
            pitch = pitches[0]
        elif anchor is Top:
            pitch = pitches[-1]
        elif anchor is Center:
            pitch = self._get_centroid(pitches)
        else:
            raise ValueError(anchor)
        return pitch.octave.number

    @staticmethod
    def _get_centroid(pitches):
        soprano = max(pitches)
        bass = min(pitches)
        centroid = (soprano.number + bass.number) / 2.0
        return abjad.NumberedPitch(centroid)

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            pitches = [transposition(_) for _ in leaf.written_pitches]
            leaf.written_pitches = pitches
        else:
            raise TypeError(leaf)
        abjad.detach('not yet registered', leaf)

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

                >>> chord = abjad.Chord("<c, d e'>1")
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

                >>> chord = abjad.Chord("<c, d e'>1")
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

                >>> chord = abjad.Chord("<c, d e'>1")
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

                >>> chord = abjad.Chord("<c, d e'>1")
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

                >>> chord = abjad.Chord("<c, d e'>1")
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

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            First stage only:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
                ...     baca.tools.RegisterToOctaveSpecifier(
                ...         anchor=Bottom,
                ...         octave_number=3,
                ...         pattern=abjad.select_first(),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                bf16 [
                                c'16
                                d'16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Last stage only:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
                ...     baca.tools.RegisterToOctaveSpecifier(
                ...         anchor=Bottom,
                ...         octave_number=3,
                ...         pattern=abjad.select_last(),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf16 [
                                c'16
                                d'16 ]
                            }
                        }
                    }
                >>

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern
