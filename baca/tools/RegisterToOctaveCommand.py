import abjad
import baca
from .Command import Command


class RegisterToOctaveCommand(Command):
    r"""Register-to-octave command.

    ..  container:: example

        Chords:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 14, 28}],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Bottom,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c' d'' e'''>16
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 14, 28}],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c d' e''>16
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [{0, 14, 28}],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Top,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c, d e'>16
                        }
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 14, 28]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Bottom,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d''16
                            e'''16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 14, 28]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c16
                            [
                            d'16
                            e''16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 14, 28]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Top,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c,16
                            [
                            d16
                            e'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[10, 12, 14]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Bottom,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[10, 12, 14]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf16
                            [
                            c'16
                            d'16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[10, 12, 14]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Top,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf16
                            [
                            c'16
                            d'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        >>> baca.RegisterToOctaveCommand()
        RegisterToOctaveCommand(selector=baca.plts())

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_anchor',
        '_octave_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        anchor=None,
        octave_number=None,
        selector='baca.plts()',
        ):
        Command.__init__(self, selector=selector)
        if anchor is not None:
            prototype = (abjad.Center, abjad.Bottom, abjad.Top)
            assert anchor in prototype, repr(anchor)
        self._anchor = anchor
        if octave_number is not None:
            assert isinstance(octave_number, int), repr(octave_number)
        self._octave_number = octave_number

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.octave_number is None:
            return
        if self.selector:
            argument = self.selector(argument)
        target_octave_number = self.octave_number or 4
        current_octave_number = self._get_anchor_octave_number(argument)
        octave_adjustment = target_octave_number - current_octave_number
        transposition = abjad.Transposition(12 * octave_adjustment)
        for pleaf in baca.select(argument).pleaves():
            self._set_pitch(pleaf, transposition)

    ### PRIVATE METHODS ###

    def _get_anchor_octave_number(self, argument):
        pitches = []
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            if isinstance(leaf, abjad.Note):
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pitches.extend(leaf.written_pitches)
            else:
                raise TypeError(leaf)
        pitches = list(set(pitches))
        pitches.sort()
        anchor = self.anchor or abjad.Bottom
        if anchor == abjad.Bottom:
            pitch = pitches[0]
        elif anchor == abjad.Top:
            pitch = pitches[-1]
        elif anchor == abjad.Center:
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
        abjad.detach(abjad.tags.NOT_YET_REGISTERED, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        r"""Gets anchor.

        ..  container:: example

            Bass anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Bottom,
            ...     octave_number=5,
            ...     )
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c'' d''' e''''>1

        ..  container:: example

            Center anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Center,
            ...     octave_number=5,
            ...     )
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c' d'' e'''>1

        ..  container:: example

            Soprano anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Top,
            ...     octave_number=5,
            ...     )
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c d' e''>1

        Set to up, down, center or none.

        Returns up, down, center or none.
        """
        return self._anchor

    @property
    def octave_number(self):
        r"""Gets octave number.

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=1)
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c,, d, e>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=2)
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=3)
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c d' e''>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=4)
            >>> command(chord)
            >>> abjad.show(chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c' d'' e'''>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=5)
            >>> command(chord)
            >>> abjad.show(chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c'' d''' e''''>1

        Returns integer.
        """
        return self._octave_number
