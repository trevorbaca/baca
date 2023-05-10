"""
Pitch collections.
"""
import dataclasses
import math
import typing

import abjad

from . import sequence as _sequence


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ArpeggiationSpacingSpecifier:
    r"""
    Arpeggiation spacing specifier.

    ..  container:: example

        >>> specifier = baca.ArpeggiationSpacingSpecifier()
        >>> specifier([[6, 0, 4, 5, 8]])
        [PitchSegment([6, 12, 16, 17, 20])]

    ..  container:: example

        >>> specifier = baca.ArpeggiationSpacingSpecifier()
        >>> specifier([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        [PitchSegment([0, 2, 10]), PitchSegment([6, 16, 27, 32, 43]), PitchSegment([9])]

    ..  container:: example

        >>> baca.ArpeggiationSpacingSpecifier()
        ArpeggiationSpacingSpecifier(direction=None, pattern=None)

    ..  container:: example

        Arpeggiate up:

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]
        >>> collections = [abjad.PitchClassSegment(_) for _ in collections]
        >>> collections = [baca.pcollections.arpeggiate_up(_) for _ in collections]
        >>> containers = [baca.from_collection(_, [1], 16) for _ in collections]
        >>> lilypond_file = abjad.illustrators.components(containers)
        >>> rmakers.beam(containers)
        >>> baca.bass_to_octave(containers, 2)
        >>> rmakers.swap_trivial(lilypond_file["Staff"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                {
                    \context Voice = "Voice"
                    {
                        {
                            \time 9/16
                            c,16
                            [
                            d,16
                            bf,16
                            ]
                        }
                        {
                            fs,16
                            [
                            e16
                            ef'16
                            af'16
                            g''16
                            ]
                        }
                        {
                            a,16
                        }
                    }
                }
            }

    ..  container:: example

        Arpeggiate down:

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> collections = [abjad.PitchClassSegment(_) for _ in collections]
        >>> collections = [baca.pcollections.arpeggiate_down(_) for _ in collections]
        >>> containers = [baca.from_collection(_, [1], 16) for _ in collections]
        >>> lilypond_file = abjad.illustrators.components(containers)
        >>> rmakers.beam(containers)
        >>> baca.bass_to_octave(containers, 2)
        >>> rmakers.swap_trivial(lilypond_file["Staff"])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                {
                    \context Voice = "Voice"
                    {
                        {
                            \time 9/16
                            c'16
                            [
                            d16
                            bf,16
                            ]
                        }
                        {
                            fs16
                            [
                            e16
                            ef16
                            af,16
                            g,16
                            ]
                        }
                        {
                            a,16
                        }
                    }
                }
            }

    """

    direction: int | None = None
    pattern: abjad.Pattern | None = None

    def __post_init__(self):
        if self.direction is not None:
            assert self.direction in (abjad.UP, abjad.DOWN), repr(self.direction)
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern), repr(self.pattern)

    def __call__(
        self, collections=None
    ) -> abjad.PitchSegment | list[abjad.PitchSegment | abjad.PitchSet] | None:
        if collections is None:
            return None
        if collections == []:
            return abjad.PitchSegment()
        if not isinstance(collections, list):
            collections = list(collections)
        pitch_class_collections = [
            type(item)([abjad.NumberedPitchClass(_) for _ in item])
            for item in collections
        ]
        pattern = self.pattern or abjad.index_all()
        collections_ = []
        total_length = len(collections)
        direction = self.direction or abjad.UP
        for i in range(total_length):
            if pattern.matches_index(i, total_length):
                pitch_class_collection = pitch_class_collections[i]
                if isinstance(pitch_class_collection, frozenset):
                    pitch_classes = list(sorted(pitch_class_collection))
                else:
                    pitch_classes = list(pitch_class_collection)
                if direction == abjad.UP:
                    pitches = _to_tightly_spaced_pitches_ascending(pitch_classes)
                else:
                    pitches = _to_tightly_spaced_pitches_descending(pitch_classes)
                collection_: abjad.PitchSet | abjad.PitchSegment
                if isinstance(pitch_class_collection, frozenset):
                    collection_ = abjad.PitchSet(pitches)
                else:
                    collection_ = abjad.PitchSegment(pitches)
                collections_.append(collection_)
            else:
                collections_.append(collections[i])
        assert isinstance(collections_, list)
        return collections_


def _to_tightly_spaced_pitches_ascending(pitch_classes):
    pitches = []
    pitch_class = pitch_classes[0]
    pitch = abjad.NumberedPitch((pitch_class, 4))
    pitches.append(pitch)
    for pitch_class in pitch_classes[1:]:
        candidate_octave = pitches[-1].octave.number
        candidate = abjad.NumberedPitch((pitch_class, candidate_octave))
        if pitches[-1] <= candidate:
            pitches.append(candidate)
        else:
            octave = candidate_octave + 1
            pitch = abjad.NumberedPitch((pitch_class, octave))
            assert pitches[-1] <= pitch
            pitches.append(pitch)
    return pitches


def _to_tightly_spaced_pitches_descending(pitch_classes):
    pitches = []
    pitch_class = pitch_classes[0]
    pitch = abjad.NumberedPitch((pitch_class, 4))
    pitches.append(pitch)
    for pitch_class in pitch_classes[1:]:
        candidate_octave = pitches[-1].octave.number
        candidate = abjad.NumberedPitch((pitch_class, candidate_octave))
        if candidate <= pitches[-1]:
            pitches.append(candidate)
        else:
            octave = candidate_octave - 1
            pitch = abjad.NumberedPitch((pitch_class, octave))
            assert pitch <= pitches[-1]
            pitches.append(pitch)
    collection = abjad.PitchSegment(pitches)
    while collection[-1].octave.number < 4:
        collection = collection.transpose(n=12)
    return collection


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ChordalSpacingSpecifier:
    """
    Chordal spacing specifier.

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 9, 11, 17, 19])]

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.DOWN,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([19, 17, 11, 9, 6])]

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=11,
        ...     direction=abjad.DOWN,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([31, 30, 29, 21, 11])]

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier()
        >>> specifier([[0, 1, 2]])
        [PitchSegment([0, 1, 2])]

        >>> specifier([[0, 2, 1]])
        [PitchSegment([0, 1, 2])]

        >>> specifier([[1, 0, 2]])
        [PitchSegment([1, 2, 12])]

        >>> specifier([[1, 2, 0]])
        [PitchSegment([1, 2, 12])]

        >>> specifier([[2, 0, 1]])
        [PitchSegment([2, 12, 13])]

        >>> specifier([[2, 1, 0]])
        [PitchSegment([2, 12, 13])]

    ..  container:: example

        Up-directed bass specification:

        >>> specifier = baca.ChordalSpacingSpecifier(bass=None)
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 7, 9, 11, 17])]

        >>> specifier = baca.ChordalSpacingSpecifier(bass=6)
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 7, 9, 11, 17])]

        >>> specifier = baca.ChordalSpacingSpecifier(bass=7)
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([7, 9, 11, 17, 18])]

        >>> specifier = baca.ChordalSpacingSpecifier(bass=9)
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([9, 11, 17, 18, 19])]

        >>> specifier = baca.ChordalSpacingSpecifier(bass=11)
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([11, 17, 18, 19, 21])]

        >>> specifier = baca.ChordalSpacingSpecifier(bass=5)
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([5, 6, 7, 9, 11])]

    ..  container:: example

        Up-directed joint control:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 9, 11, 17, 19])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=9,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 7, 11, 17, 21])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=11,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 7, 9, 17, 23])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=5
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([6, 7, 9, 11, 17])]

    ..  container:: example

        Up-directed spacing with semitone constraints.

        First three examples give the same spacing:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([6, 9, 11, 17, 19])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     minimum_semitones=1,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([6, 9, 11, 17, 19])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     minimum_semitones=2,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([6, 9, 11, 17, 19])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     minimum_semitones=3,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([6, 9, 17, 23, 31])]

    ..  container:: example

        Down-directed spacing with semitone constraints.

        First three examples give the same spacing:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.DOWN,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([19, 17, 11, 9, 6])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.DOWN,
        ...     minimum_semitones=1,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([19, 17, 11, 9, 6])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.DOWN,
        ...     minimum_semitones=2,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([19, 17, 11, 9, 6])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.DOWN,
        ...     minimum_semitones=3,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        [PitchSegment([31, 23, 17, 9, 6])]

    ..  container:: example

        Down-directed soprano control:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.DOWN,
        ...     soprano=None,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([18, 17, 11, 9, 7])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.DOWN,
        ...     soprano=6,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([18, 17, 11, 9, 7])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.DOWN,
        ...     soprano=5,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([17, 11, 9, 7, 6])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.DOWN,
        ...     soprano=11,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([11, 9, 7, 6, 5])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.DOWN,
        ...     soprano=9,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([21, 19, 18, 17, 11])]

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.DOWN,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        [PitchSegment([19, 18, 17, 11, 9])]

    """

    bass: typing.Any = None
    direction: int | None = None
    minimum_semitones: typing.Any = None
    pattern: typing.Any = None
    soprano: typing.Any = None

    def __post_init__(self):
        if self.direction is not None:
            assert self.direction in (abjad.UP, abjad.DOWN)
        if self.minimum_semitones is not None:
            assert isinstance(self.minimum_semitones, int)
            assert 1 <= self.minimum_semitones
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern)

    def __call__(self, collections=None):
        if collections is None:
            return None
        if not isinstance(collections, list):
            collections = list(collections)
        pattern = self.pattern or abjad.index_all()
        collections_ = []
        total_length = len(collections)
        for i in range(total_length):
            if not pattern.matches_index(i, total_length):
                collections_.append(collections[i])
            else:
                collection = collections[i]
                collection_ = self._space_collection(collection)
                collections_.append(collection_)
        return collections_

    def _sort_pitch_classes_ascending(self, start, pitch_classes):
        pitch_classes, pitch_classes_, iterations = pitch_classes[:], [], 0
        if self.minimum_semitones is not None:
            candidate = start + self.minimum_semitones
        else:
            candidate = start + 1
        while pitch_classes:
            if candidate in pitch_classes:
                pitch_classes_.append(candidate)
                pitch_classes.remove(candidate)
                if self.minimum_semitones is not None:
                    candidate += self.minimum_semitones
            else:
                candidate += 1
            if 999 <= iterations:
                raise Exception("stuck in while-loop.")
            iterations += 1
        assert not pitch_classes, repr(pitch_classes)
        return pitch_classes_

    def _sort_pitch_classes_descending(self, start, pitch_classes):
        pitch_classes, pitch_classes_, iterations = pitch_classes[:], [], 0
        if self.minimum_semitones is not None:
            candidate = abjad.NumberedPitchClass(start.number - self.minimum_semitones)
        else:
            candidate = abjad.NumberedPitchClass(start.number - 1)
        while pitch_classes:
            if candidate in pitch_classes:
                pitch_classes_.append(candidate)
                pitch_classes.remove(candidate)
                if self.minimum_semitones is not None:
                    candidate = abjad.NumberedPitchClass(
                        candidate.number - self.minimum_semitones
                    )
            else:
                candidate = abjad.NumberedPitchClass(candidate.number - 1)
            if 999 <= iterations:
                raise Exception("stuck in while-loop.")
            iterations += 1
        assert not pitch_classes, repr(pitch_classes)
        return pitch_classes_

    def _space_collection(self, collection):
        original_collection = collection
        if isinstance(collection, frozenset):
            pitch_classes = [abjad.NumberedPitchClass(_) for _ in collection]
            pitch_classes.sort()
        else:
            pitch_classes = [abjad.NumberedPitchClass(_) for _ in collection]
        bass, soprano, outer = None, None, []
        if self.bass is not None:
            bass = abjad.NumberedPitchClass(self.bass)
            if bass not in pitch_classes:
                raise ValueError(f"bass pc {bass} not in {pitch_classes}.")
            outer.append(bass)
        if self.soprano is not None:
            soprano = abjad.NumberedPitchClass(self.soprano)
            if soprano not in pitch_classes:
                raise ValueError(f"soprano pc {bass} not in {pitch_classes}.")
            outer.append(soprano)
        inner = []
        for pitch_class in pitch_classes:
            if pitch_class not in outer:
                inner.append(pitch_class)
        pitch_classes = []
        pitches = []
        direction = self.direction or abjad.UP
        if direction is abjad.UP:
            if bass is not None:
                pitch_classes.append(bass)
            elif inner:
                pitch_classes.append(inner.pop(0))
            elif soprano:
                pitch_classes.append(soprano)
                soprano = None
            start = pitch_classes[0]
            inner = self._sort_pitch_classes_ascending(start, inner)
            pitch_classes.extend(inner)
            if soprano:
                pitch_classes.append(soprano)
            pitches = _to_tightly_spaced_pitches_ascending(pitch_classes)
        else:
            if soprano is not None:
                pitch_classes.append(soprano)
            elif inner:
                pitch_classes.append(inner.pop(0))
            elif bass:
                pitch_classes.append(bass)
                bass = None
            start = pitch_classes[0]
            inner = self._sort_pitch_classes_descending(start, inner)
            pitch_classes.extend(inner)
            if bass:
                pitch_classes.append(bass)
            pitches = _to_tightly_spaced_pitches_descending(pitch_classes)
        if isinstance(original_collection, frozenset):
            return abjad.PitchSet(pitches)
        else:
            return abjad.PitchSegment(pitches)


class HarmonicSeries:
    r"""
    Harmonic series.

    ..  container:: example

        >>> harmonic_series = baca.HarmonicSeries('C2')
        >>> lilypond_file = baca.pcollections.illustrate_harmonic_series(harmonic_series)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file["Staff"]
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            \with
            {
                \override BarLine.stencil = ##f
                \override Stem.transparent = ##t
                \override TextScript.font-size = -1
                \override TextScript.staff-padding = 6
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                c,4
                _ \markup 1
                c4
                _ \markup 2
                g4
                ^ \markup +2
                _ \markup 3
                \clef "treble"
                c'4
                _ \markup 4
                e'4
                ^ \markup -14
                _ \markup 5
                g'4
                ^ \markup +2
                _ \markup 6
                bf'4
                ^ \markup -31
                _ \markup 7
                c''4
                _ \markup 8
                d''4
                ^ \markup +4
                _ \markup 9
                e''4
                ^ \markup -14
                _ \markup 10
                fqs''4
                ^ \markup +1
                _ \markup 11
                g''4
                ^ \markup +2
                _ \markup 12
                aqf''4
                ^ \markup -9
                _ \markup 13
                bf''4
                ^ \markup -31
                _ \markup 14
                b''4
                ^ \markup -12
                _ \markup 15
                c'''4
                _ \markup 16
                cs'''4
                ^ \markup +5
                _ \markup 17
                d'''4
                ^ \markup +4
                _ \markup 18
                ef'''4
                ^ \markup -2
                _ \markup 19
                e'''4
                ^ \markup -14
                _ \markup 20
            }

    """

    __slots__ = ("_fundamental",)

    def __init__(self, fundamental: str | abjad.NamedPitch = "C1") -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental

    @property
    def fundamental(self) -> abjad.NamedPitch:
        """
        Gets fundamental.

        ..  container:: example

            >>> baca.HarmonicSeries("C2").fundamental
            NamedPitch('c,')

        """
        return self._fundamental

    def partial(self, n: int) -> "Partial":
        """
        Gets partial ``n``.

        ..  container:: example

            >>> baca.HarmonicSeries("C2").partial(7)
            Partial(fundamental=NamedPitch('c,'), number=7)

        """
        return Partial(fundamental=self.fundamental, number=n)


def illustrate_harmonic_series(harmonic_series) -> abjad.LilyPondFile:
    r"""
    Illustrates harmonic series.

    ..  container:: example

        >>> harmonic_series = baca.HarmonicSeries('A1')
        >>> lilypond_file = baca.pcollections.illustrate_harmonic_series(harmonic_series)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff = lilypond_file["Staff"]
            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \context Staff = "Staff"
            \with
            {
                \override BarLine.stencil = ##f
                \override Stem.transparent = ##t
                \override TextScript.font-size = -1
                \override TextScript.staff-padding = 6
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                a,,4
                _ \markup 1
                a,4
                _ \markup 2
                e4
                ^ \markup +2
                _ \markup 3
                a4
                _ \markup 4
                \clef "treble"
                cs'4
                ^ \markup -14
                _ \markup 5
                e'4
                ^ \markup +2
                _ \markup 6
                g'4
                ^ \markup -31
                _ \markup 7
                a'4
                _ \markup 8
                b'4
                ^ \markup +4
                _ \markup 9
                cs''4
                ^ \markup -14
                _ \markup 10
                dqs''4
                ^ \markup +1
                _ \markup 11
                e''4
                ^ \markup +2
                _ \markup 12
                fqs''4
                ^ \markup -9
                _ \markup 13
                g''4
                ^ \markup -31
                _ \markup 14
                af''4
                ^ \markup -12
                _ \markup 15
                a''4
                _ \markup 16
                bf''4
                ^ \markup +5
                _ \markup 17
                b''4
                ^ \markup +4
                _ \markup 18
                c'''4
                ^ \markup -2
                _ \markup 19
                cs'''4
                ^ \markup -14
                _ \markup 20
            }

    """
    staff = abjad.Staff(name="Staff")
    for n in range(1, 20 + 1):
        partial = harmonic_series.partial(n)
        pitch = partial.approximation()
        note = abjad.Note.from_pitch_and_duration(pitch, (1, 4))
        staff.append(note)
        deviation = partial.deviation()
        if 0 < deviation:
            markup = abjad.Markup(rf"\markup +{deviation}")
            abjad.attach(markup, note, direction=abjad.UP)
        elif deviation < 0:
            markup = abjad.Markup(rf"\markup {deviation}")
            abjad.attach(markup, note, direction=abjad.UP)
        markup = abjad.Markup(rf"\markup {n}")
        abjad.attach(markup, note, direction=abjad.DOWN)
    notes = abjad.select.notes(staff)
    if notes[0].written_pitch < abjad.NamedPitch("C4"):
        abjad.attach(abjad.Clef("bass"), staff[0])
        for note in notes[1:]:
            if abjad.NamedPitch("C4") <= note.written_pitch:
                abjad.attach(abjad.Clef("treble"), note)
                break
    abjad.override(staff).BarLine.stencil = False
    abjad.override(staff).Stem.transparent = True
    abjad.override(staff).TextScript.font_size = -1
    abjad.override(staff).TextScript.staff_padding = 6
    abjad.override(staff).TimeSignature.stencil = False
    score = abjad.Score([staff], name="Score")
    abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 8)"
    lilypond_file = abjad.LilyPondFile([score])
    return lilypond_file


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Partial:
    """
    Partial.

    ..  container:: example

        >>> baca.Partial(abjad.NamedPitch("C1"), 7)
        Partial(fundamental=NamedPitch('c,,'), number=7)

    """

    fundamental: abjad.NamedPitch = abjad.NamedPitch("C1")
    number: int = 1

    def __post_init__(self):
        assert isinstance(self.fundamental, abjad.NamedPitch), repr(self.fundamental)
        assert isinstance(self.number, int), repr(self.number)
        assert 1 <= self.number, repr(self.number)

    def approximation(self) -> abjad.NamedPitch:
        """
        Gets approximation.

        ..  container:: example

            >>> baca.Partial(abjad.NamedPitch("C1"), 7).approximation()
            NamedPitch('bf')

        """
        hertz = self.number * self.fundamental.hertz
        return abjad.NamedPitch.from_hertz(hertz)

    def deviation(self) -> int:
        """
        Gets deviation in cents.

        ..  container:: example

            >>> baca.Partial(abjad.NamedPitch("C1"), 7).deviation()
            -31

        """
        deviation_multiplier = (
            self.number * self.fundamental.hertz / self.approximation().hertz
        )
        semitone_base = 2 ** abjad.Fraction(1, 12)
        deviation_semitones = math.log(deviation_multiplier, semitone_base)
        deviation_cents = 100 * deviation_semitones
        deviation = round(deviation_cents)
        return deviation


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RegistrationComponent:
    source_pitch_range: abjad.PitchRange = abjad.PitchRange("[A0, C8]")
    target_octave_start_pitch: abjad.NumberedPitch = abjad.NumberedPitch(0)

    def __post_init__(self):
        assert isinstance(self.source_pitch_range, abjad.PitchRange), repr(
            self.source_pitch_range
        )
        assert isinstance(self.target_octave_start_pitch, abjad.NumberedPitch), repr(
            self.target_octave_start_pitch
        )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Registration:
    components: typing.Sequence[RegistrationComponent] = ()

    def __post_init__(self):
        for component in self.components:
            assert isinstance(component, RegistrationComponent), repr(component)

    def __call__(self, pitches) -> list[abjad.NamedPitch]:
        r"""
        Calls registration on ``pitches``.

        Transposes four pitches:

        ..  container:: example

            >>> components = [
            ...     baca.RegistrationComponent(
            ...         abjad.PitchRange("[A0, C4)"), abjad.NumberedPitch(15)
            ...     ),
            ...     baca.RegistrationComponent(
            ...         abjad.PitchRange("[C4, C8)"), abjad.NumberedPitch(27)
            ...     ),
            ... ]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([-24, -22, -23, -21])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("c'''")
            NamedPitch("d'''")
            NamedPitch("cs'''")
            NamedPitch("ef''")

        ..  container:: example

            Transposes four other pitches:

            >>> components = [
            ...     baca.RegistrationComponent(
            ...         abjad.PitchRange("[A0, C4)"), abjad.NumberedPitch(15)
            ...     ),
            ...     baca.RegistrationComponent(
            ...         abjad.PitchRange("[C4, C8)"), abjad.NumberedPitch(27)
            ...     ),
            ... ]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0, 2, 1, 3])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("c''''")
            NamedPitch("d''''")
            NamedPitch("cs''''")
            NamedPitch("ef'''")

        ..  container:: example

            Transposes four quartertones:

            >>> components = [
            ...     baca.RegistrationComponent(
            ...         abjad.PitchRange("[A0, C4)"), abjad.NumberedPitch(15)
            ...     ),
            ...     baca.RegistrationComponent(
            ...         abjad.PitchRange("[C4, C8)"), abjad.NumberedPitch(27)
            ...     ),
            ... ]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0.5, 2.5, 1.5, 3.5])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("cqs''''")
            NamedPitch("dqs''''")
            NamedPitch("dqf''''")
            NamedPitch("eqf'''")

        """
        return [self._transpose_pitch(_) for _ in pitches]

    def _transpose_pitch(self, pitch) -> abjad.NamedPitch:
        pitch = abjad.NamedPitch(pitch)
        for component in self.components:
            if pitch in component.source_pitch_range:
                start_pitch = component.target_octave_start_pitch
                stop_pitch = start_pitch + 12
                if start_pitch <= pitch < stop_pitch:
                    return pitch
                elif pitch < start_pitch:
                    while pitch < start_pitch:
                        pitch += 12
                    return pitch
                elif stop_pitch <= pitch:
                    while stop_pitch <= pitch:
                        pitch -= 12
                    return pitch
                else:
                    raise ValueError(pitch, self)
        else:
            raise ValueError(f"{pitch!r} not in {self!r}.")


def accumulate_and_repartition(segments, ratios, counts):
    segments = _sequence.helianthate(segments, -1, 1)
    sequences = [segments, ratios]
    subsegments = []
    for segment, ratio in abjad.sequence.zip(sequences, cyclic=True, truncate=False):
        subsegments_ = abjad.sequence.partition_by_ratio_of_lengths(segment, ratio)
        subsegments.extend(subsegments_)
    groups = abjad.sequence.partition_by_counts(
        subsegments, counts, cyclic=True, overhang=True
    )
    return groups


def alpha(collection):
    r"""
    Gets alpha transform of collection.

    ..  container:: example

        Example segment:

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> J = abjad.PitchClassSegment(items=items)

        >>> lilypond_file = abjad.illustrate(J)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Gets alpha transform of segment:

        >>> segment = baca.pcollections.alpha(J)
        >>> segment
        PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                b'8
                bqs'8
                g'8
                fs'8
                bqs'8
                fs'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        Gets alpha transform of alpha transform of segment:

        >>> segment = baca.pcollections.alpha(J)
        >>> segment = baca.pcollections.alpha(segment)
        >>> segment
        PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> segment == J
        True

    """
    numbers = []
    for pc in collection:
        pc = abs(float(pc.number))
        is_integer = True
        if not abjad.math.is_integer_equivalent_number(pc):
            is_integer = False
            fraction_part = pc - int(pc)
            pc = int(pc)
        if abs(pc) % 2 == 0:
            number = (abs(pc) + 1) % 12
        else:
            number = abs(pc) - 1
        if not is_integer:
            number += fraction_part
        else:
            number = int(number)
        numbers.append(number)
    return type(collection)(items=numbers)


def arpeggiate_down(collection):
    r"""
    Arpeggiates collection down.

    ..  container:: example

        >>> segment = abjad.PitchClassSegment([6, 0, 4, 5, 8])
        >>> segment = baca.pcollections.arpeggiate_down(segment)
        >>> segment
        PitchSegment([42, 36, 28, 17, 8])

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        fs''''1 * 1/8
                        c''''1 * 1/8
                        e'''1 * 1/8
                        f''1 * 1/8
                        af'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    Returns new collection.
    """
    specifier = ArpeggiationSpacingSpecifier(direction=abjad.DOWN)
    result = specifier([collection])
    assert len(result) == 1
    segment = result[0]
    assert isinstance(segment, abjad.PitchSegment), repr(segment)
    return segment


def arpeggiate_up(collection):
    r"""
    Arpeggiates collection up.

    ..  container:: example

        >>> segment = abjad.PitchClassSegment([6, 0, 4, 5, 8])
        >>> segment = baca.pcollections.arpeggiate_up(segment)
        >>> segment
        PitchSegment([6, 12, 16, 17, 20])

        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        fs'1 * 1/8
                        c''1 * 1/8
                        e''1 * 1/8
                        f''1 * 1/8
                        af''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    Returns new collection.
    """
    specifier = ArpeggiationSpacingSpecifier(direction=abjad.UP)
    result = specifier([collection])
    assert len(result) == 1
    segment = result[0]
    assert isinstance(segment, abjad.PitchSegment), repr(segment)
    return segment


def bass_to_octave(collection, n=4):
    r"""
    Octave-transposes collection to bass in octave ``n``.

    ..  container:: example

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.bass_to_octave(segment, n=4)
        PitchSegment([10, 10.5, 18, 19, 10.5, 19])

        >>> segment = baca.pcollections.bass_to_octave(segment, n=4)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs''1 * 1/8
                        g''1 * 1/8
                        bqf'1 * 1/8
                        g''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    Returns new collection.
    """
    octave_adjustment = pitches_to_octave_adjustment(
        collection, anchor=abjad.DOWN, octave_number=n
    )
    segment = collection.transpose(n=12 * octave_adjustment)
    return dataclasses.replace(collection, items=segment)


def center_to_octave(collection, n=4):
    r"""
    Octave-transposes collection to center in octave ``n``.

    ..  container:: example

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.center_to_octave(segment, n=3)
        PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

        >>> segment = baca.pcollections.center_to_octave(segment, n=3)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                }
            >>

    Returns new collection.
    """
    octave_adjustment = pitches_to_octave_adjustment(
        collection, anchor=abjad.CENTER, octave_number=n
    )
    segment = collection.transpose(n=12 * octave_adjustment)
    return dataclasses.replace(collection, items=segment)


def get_matching_transforms(
    collection,
    segment_2,
    inversion=False,
    multiplication=False,
    retrograde=False,
    rotation=False,
    transposition=False,
):
    r"""
    Gets transforms of ``collection`` that match ``segment_2``.

    ..  container:: example

        Example segments:

        >>> items = [-2, -1, 6, 7, -1, 7]
        >>> segment_1 = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment_1)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> items = [9, 2, 1, 6, 2, 6]
        >>> segment_2 = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment_2)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Gets matching transforms:

        >>> transforms = baca.pcollections.get_matching_transforms(
        ...     segment_1,
        ...     segment_2,
        ...     inversion=True,
        ...     multiplication=True,
        ...     retrograde=True,
        ...     rotation=False,
        ...     transposition=True,
        ...     )
        >>> for operator, transform in transforms:
        ...     compound = "".join(operator)
        ...     print(compound, str(transform))
        ...
        M5T11 PC<9, 2, 1, 6, 2, 6>
        M7T1I PC<9, 2, 1, 6, 2, 6>

        >>> transforms = baca.pcollections.get_matching_transforms(
        ...     segment_2,
        ...     segment_1,
        ...     inversion=True,
        ...     multiplication=True,
        ...     retrograde=True,
        ...     rotation=False,
        ...     transposition=True,
        ...     )
        >>> for operator, transform in transforms:
        ...     compound = "".join(operator)
        ...     print(compound, str(transform))
        ...
        M5T5 PC<10, 11, 6, 7, 11, 7>
        M7T7I PC<10, 11, 6, 7, 11, 7>

    ..  container:: example

        No matching transforms. Segments of differing lengths never transform into
        each other:

        >>> segment_2 = abjad.PitchClassSegment(items=[0, 1, 2])
        >>> baca.pcollections.get_matching_transforms(
        ...     segment_2,
        ...     segment_1,
        ...     inversion=True,
        ...     multiplication=True,
        ...     retrograde=True,
        ...     rotation=False,
        ...     transposition=True,
        ... )
        []

    """
    result = []
    if not len(collection) == len(segment_2):
        return result
    transforms = get_transforms(
        collection,
        inversion=inversion,
        multiplication=multiplication,
        retrograde=retrograde,
        rotation=rotation,
        transposition=transposition,
    )
    for operator, transform in transforms:
        if transform == segment_2:
            result.append((operator, transform))
    return result


def get_transforms(
    collection,
    inversion=False,
    multiplication=False,
    retrograde=False,
    rotation=False,
    show_identity_operators=False,
    transposition=False,
):
    """
    Applies transform strings.

    ..  container:: example

        >>> items = [-2, -1, 6, 7, -1, 7]
        >>> J = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(J)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> pairs = baca.pcollections.get_transforms(
        ...     J,
        ...     inversion=True,
        ...     multiplication=True,
        ...     retrograde=True,
        ...     transposition=True,
        ... )

        >>> for rank, (list_, transform) in enumerate(pairs, start=1):
        ...     compound = "".join(list_)
        ...     string = "{:3}:{:>9}(J): {!s}"
        ...     string = string.format(rank, compound, transform)
        ...     print(string)
        1:     M1T0(J): PC<10, 11, 6, 7, 11, 7>
        2:     M1T1(J): PC<11, 0, 7, 8, 0, 8>
        3:     M1T2(J): PC<0, 1, 8, 9, 1, 9>
        4:     M1T3(J): PC<1, 2, 9, 10, 2, 10>
        5:     M1T4(J): PC<2, 3, 10, 11, 3, 11>
        6:     M1T5(J): PC<3, 4, 11, 0, 4, 0>
        7:     M1T6(J): PC<4, 5, 0, 1, 5, 1>
        8:     M1T7(J): PC<5, 6, 1, 2, 6, 2>
        9:     M1T8(J): PC<6, 7, 2, 3, 7, 3>
        10:     M1T9(J): PC<7, 8, 3, 4, 8, 4>
        11:    M1T10(J): PC<8, 9, 4, 5, 9, 5>
        12:    M1T11(J): PC<9, 10, 5, 6, 10, 6>
        13:    M1T0I(J): PC<2, 1, 6, 5, 1, 5>
        14:    M1T1I(J): PC<3, 2, 7, 6, 2, 6>
        15:    M1T2I(J): PC<4, 3, 8, 7, 3, 7>
        16:    M1T3I(J): PC<5, 4, 9, 8, 4, 8>
        17:    M1T4I(J): PC<6, 5, 10, 9, 5, 9>
        18:    M1T5I(J): PC<7, 6, 11, 10, 6, 10>
        19:    M1T6I(J): PC<8, 7, 0, 11, 7, 11>
        20:    M1T7I(J): PC<9, 8, 1, 0, 8, 0>
        21:    M1T8I(J): PC<10, 9, 2, 1, 9, 1>
        22:    M1T9I(J): PC<11, 10, 3, 2, 10, 2>
        23:   M1T10I(J): PC<0, 11, 4, 3, 11, 3>
        24:   M1T11I(J): PC<1, 0, 5, 4, 0, 4>
        25:     M5T0(J): PC<2, 7, 6, 11, 7, 11>
        26:     M5T1(J): PC<7, 0, 11, 4, 0, 4>
        27:     M5T2(J): PC<0, 5, 4, 9, 5, 9>
        28:     M5T3(J): PC<5, 10, 9, 2, 10, 2>
        29:     M5T4(J): PC<10, 3, 2, 7, 3, 7>
        30:     M5T5(J): PC<3, 8, 7, 0, 8, 0>
        31:     M5T6(J): PC<8, 1, 0, 5, 1, 5>
        32:     M5T7(J): PC<1, 6, 5, 10, 6, 10>
        33:     M5T8(J): PC<6, 11, 10, 3, 11, 3>
        34:     M5T9(J): PC<11, 4, 3, 8, 4, 8>
        35:    M5T10(J): PC<4, 9, 8, 1, 9, 1>
        36:    M5T11(J): PC<9, 2, 1, 6, 2, 6>
        37:    M5T0I(J): PC<10, 5, 6, 1, 5, 1>
        38:    M5T1I(J): PC<3, 10, 11, 6, 10, 6>
        39:    M5T2I(J): PC<8, 3, 4, 11, 3, 11>
        40:    M5T3I(J): PC<1, 8, 9, 4, 8, 4>
        41:    M5T4I(J): PC<6, 1, 2, 9, 1, 9>
        42:    M5T5I(J): PC<11, 6, 7, 2, 6, 2>
        43:    M5T6I(J): PC<4, 11, 0, 7, 11, 7>
        44:    M5T7I(J): PC<9, 4, 5, 0, 4, 0>
        45:    M5T8I(J): PC<2, 9, 10, 5, 9, 5>
        46:    M5T9I(J): PC<7, 2, 3, 10, 2, 10>
        47:   M5T10I(J): PC<0, 7, 8, 3, 7, 3>
        48:   M5T11I(J): PC<5, 0, 1, 8, 0, 8>
        49:     M7T0(J): PC<10, 5, 6, 1, 5, 1>
        50:     M7T1(J): PC<5, 0, 1, 8, 0, 8>
        51:     M7T2(J): PC<0, 7, 8, 3, 7, 3>
        52:     M7T3(J): PC<7, 2, 3, 10, 2, 10>
        53:     M7T4(J): PC<2, 9, 10, 5, 9, 5>
        54:     M7T5(J): PC<9, 4, 5, 0, 4, 0>
        55:     M7T6(J): PC<4, 11, 0, 7, 11, 7>
        56:     M7T7(J): PC<11, 6, 7, 2, 6, 2>
        57:     M7T8(J): PC<6, 1, 2, 9, 1, 9>
        58:     M7T9(J): PC<1, 8, 9, 4, 8, 4>
        59:    M7T10(J): PC<8, 3, 4, 11, 3, 11>
        60:    M7T11(J): PC<3, 10, 11, 6, 10, 6>
        61:    M7T0I(J): PC<2, 7, 6, 11, 7, 11>
        62:    M7T1I(J): PC<9, 2, 1, 6, 2, 6>
        63:    M7T2I(J): PC<4, 9, 8, 1, 9, 1>
        64:    M7T3I(J): PC<11, 4, 3, 8, 4, 8>
        65:    M7T4I(J): PC<6, 11, 10, 3, 11, 3>
        66:    M7T5I(J): PC<1, 6, 5, 10, 6, 10>
        67:    M7T6I(J): PC<8, 1, 0, 5, 1, 5>
        68:    M7T7I(J): PC<3, 8, 7, 0, 8, 0>
        69:    M7T8I(J): PC<10, 3, 2, 7, 3, 7>
        70:    M7T9I(J): PC<5, 10, 9, 2, 10, 2>
        71:   M7T10I(J): PC<0, 5, 4, 9, 5, 9>
        72:   M7T11I(J): PC<7, 0, 11, 4, 0, 4>
        73:    M11T0(J): PC<2, 1, 6, 5, 1, 5>
        74:    M11T1(J): PC<1, 0, 5, 4, 0, 4>
        75:    M11T2(J): PC<0, 11, 4, 3, 11, 3>
        76:    M11T3(J): PC<11, 10, 3, 2, 10, 2>
        77:    M11T4(J): PC<10, 9, 2, 1, 9, 1>
        78:    M11T5(J): PC<9, 8, 1, 0, 8, 0>
        79:    M11T6(J): PC<8, 7, 0, 11, 7, 11>
        80:    M11T7(J): PC<7, 6, 11, 10, 6, 10>
        81:    M11T8(J): PC<6, 5, 10, 9, 5, 9>
        82:    M11T9(J): PC<5, 4, 9, 8, 4, 8>
        83:   M11T10(J): PC<4, 3, 8, 7, 3, 7>
        84:   M11T11(J): PC<3, 2, 7, 6, 2, 6>
        85:   M11T0I(J): PC<10, 11, 6, 7, 11, 7>
        86:   M11T1I(J): PC<9, 10, 5, 6, 10, 6>
        87:   M11T2I(J): PC<8, 9, 4, 5, 9, 5>
        88:   M11T3I(J): PC<7, 8, 3, 4, 8, 4>
        89:   M11T4I(J): PC<6, 7, 2, 3, 7, 3>
        90:   M11T5I(J): PC<5, 6, 1, 2, 6, 2>
        91:   M11T6I(J): PC<4, 5, 0, 1, 5, 1>
        92:   M11T7I(J): PC<3, 4, 11, 0, 4, 0>
        93:   M11T8I(J): PC<2, 3, 10, 11, 3, 11>
        94:   M11T9I(J): PC<1, 2, 9, 10, 2, 10>
        95:  M11T10I(J): PC<0, 1, 8, 9, 1, 9>
        96:  M11T11I(J): PC<11, 0, 7, 8, 0, 8>
        97:    RM1T0(J): PC<7, 11, 7, 6, 11, 10>
        98:    RM1T1(J): PC<8, 0, 8, 7, 0, 11>
        99:    RM1T2(J): PC<9, 1, 9, 8, 1, 0>
        100:    RM1T3(J): PC<10, 2, 10, 9, 2, 1>
        101:    RM1T4(J): PC<11, 3, 11, 10, 3, 2>
        102:    RM1T5(J): PC<0, 4, 0, 11, 4, 3>
        103:    RM1T6(J): PC<1, 5, 1, 0, 5, 4>
        104:    RM1T7(J): PC<2, 6, 2, 1, 6, 5>
        105:    RM1T8(J): PC<3, 7, 3, 2, 7, 6>
        106:    RM1T9(J): PC<4, 8, 4, 3, 8, 7>
        107:   RM1T10(J): PC<5, 9, 5, 4, 9, 8>
        108:   RM1T11(J): PC<6, 10, 6, 5, 10, 9>
        109:   RM1T0I(J): PC<5, 1, 5, 6, 1, 2>
        110:   RM1T1I(J): PC<6, 2, 6, 7, 2, 3>
        111:   RM1T2I(J): PC<7, 3, 7, 8, 3, 4>
        112:   RM1T3I(J): PC<8, 4, 8, 9, 4, 5>
        113:   RM1T4I(J): PC<9, 5, 9, 10, 5, 6>
        114:   RM1T5I(J): PC<10, 6, 10, 11, 6, 7>
        115:   RM1T6I(J): PC<11, 7, 11, 0, 7, 8>
        116:   RM1T7I(J): PC<0, 8, 0, 1, 8, 9>
        117:   RM1T8I(J): PC<1, 9, 1, 2, 9, 10>
        118:   RM1T9I(J): PC<2, 10, 2, 3, 10, 11>
        119:  RM1T10I(J): PC<3, 11, 3, 4, 11, 0>
        120:  RM1T11I(J): PC<4, 0, 4, 5, 0, 1>
        121:    RM5T0(J): PC<11, 7, 11, 6, 7, 2>
        122:    RM5T1(J): PC<4, 0, 4, 11, 0, 7>
        123:    RM5T2(J): PC<9, 5, 9, 4, 5, 0>
        124:    RM5T3(J): PC<2, 10, 2, 9, 10, 5>
        125:    RM5T4(J): PC<7, 3, 7, 2, 3, 10>
        126:    RM5T5(J): PC<0, 8, 0, 7, 8, 3>
        127:    RM5T6(J): PC<5, 1, 5, 0, 1, 8>
        128:    RM5T7(J): PC<10, 6, 10, 5, 6, 1>
        129:    RM5T8(J): PC<3, 11, 3, 10, 11, 6>
        130:    RM5T9(J): PC<8, 4, 8, 3, 4, 11>
        131:   RM5T10(J): PC<1, 9, 1, 8, 9, 4>
        132:   RM5T11(J): PC<6, 2, 6, 1, 2, 9>
        133:   RM5T0I(J): PC<1, 5, 1, 6, 5, 10>
        134:   RM5T1I(J): PC<6, 10, 6, 11, 10, 3>
        135:   RM5T2I(J): PC<11, 3, 11, 4, 3, 8>
        136:   RM5T3I(J): PC<4, 8, 4, 9, 8, 1>
        137:   RM5T4I(J): PC<9, 1, 9, 2, 1, 6>
        138:   RM5T5I(J): PC<2, 6, 2, 7, 6, 11>
        139:   RM5T6I(J): PC<7, 11, 7, 0, 11, 4>
        140:   RM5T7I(J): PC<0, 4, 0, 5, 4, 9>
        141:   RM5T8I(J): PC<5, 9, 5, 10, 9, 2>
        142:   RM5T9I(J): PC<10, 2, 10, 3, 2, 7>
        143:  RM5T10I(J): PC<3, 7, 3, 8, 7, 0>
        144:  RM5T11I(J): PC<8, 0, 8, 1, 0, 5>
        145:    RM7T0(J): PC<1, 5, 1, 6, 5, 10>
        146:    RM7T1(J): PC<8, 0, 8, 1, 0, 5>
        147:    RM7T2(J): PC<3, 7, 3, 8, 7, 0>
        148:    RM7T3(J): PC<10, 2, 10, 3, 2, 7>
        149:    RM7T4(J): PC<5, 9, 5, 10, 9, 2>
        150:    RM7T5(J): PC<0, 4, 0, 5, 4, 9>
        151:    RM7T6(J): PC<7, 11, 7, 0, 11, 4>
        152:    RM7T7(J): PC<2, 6, 2, 7, 6, 11>
        153:    RM7T8(J): PC<9, 1, 9, 2, 1, 6>
        154:    RM7T9(J): PC<4, 8, 4, 9, 8, 1>
        155:   RM7T10(J): PC<11, 3, 11, 4, 3, 8>
        156:   RM7T11(J): PC<6, 10, 6, 11, 10, 3>
        157:   RM7T0I(J): PC<11, 7, 11, 6, 7, 2>
        158:   RM7T1I(J): PC<6, 2, 6, 1, 2, 9>
        159:   RM7T2I(J): PC<1, 9, 1, 8, 9, 4>
        160:   RM7T3I(J): PC<8, 4, 8, 3, 4, 11>
        161:   RM7T4I(J): PC<3, 11, 3, 10, 11, 6>
        162:   RM7T5I(J): PC<10, 6, 10, 5, 6, 1>
        163:   RM7T6I(J): PC<5, 1, 5, 0, 1, 8>
        164:   RM7T7I(J): PC<0, 8, 0, 7, 8, 3>
        165:   RM7T8I(J): PC<7, 3, 7, 2, 3, 10>
        166:   RM7T9I(J): PC<2, 10, 2, 9, 10, 5>
        167:  RM7T10I(J): PC<9, 5, 9, 4, 5, 0>
        168:  RM7T11I(J): PC<4, 0, 4, 11, 0, 7>
        169:   RM11T0(J): PC<5, 1, 5, 6, 1, 2>
        170:   RM11T1(J): PC<4, 0, 4, 5, 0, 1>
        171:   RM11T2(J): PC<3, 11, 3, 4, 11, 0>
        172:   RM11T3(J): PC<2, 10, 2, 3, 10, 11>
        173:   RM11T4(J): PC<1, 9, 1, 2, 9, 10>
        174:   RM11T5(J): PC<0, 8, 0, 1, 8, 9>
        175:   RM11T6(J): PC<11, 7, 11, 0, 7, 8>
        176:   RM11T7(J): PC<10, 6, 10, 11, 6, 7>
        177:   RM11T8(J): PC<9, 5, 9, 10, 5, 6>
        178:   RM11T9(J): PC<8, 4, 8, 9, 4, 5>
        179:  RM11T10(J): PC<7, 3, 7, 8, 3, 4>
        180:  RM11T11(J): PC<6, 2, 6, 7, 2, 3>
        181:  RM11T0I(J): PC<7, 11, 7, 6, 11, 10>
        182:  RM11T1I(J): PC<6, 10, 6, 5, 10, 9>
        183:  RM11T2I(J): PC<5, 9, 5, 4, 9, 8>
        184:  RM11T3I(J): PC<4, 8, 4, 3, 8, 7>
        185:  RM11T4I(J): PC<3, 7, 3, 2, 7, 6>
        186:  RM11T5I(J): PC<2, 6, 2, 1, 6, 5>
        187:  RM11T6I(J): PC<1, 5, 1, 0, 5, 4>
        188:  RM11T7I(J): PC<0, 4, 0, 11, 4, 3>
        189:  RM11T8I(J): PC<11, 3, 11, 10, 3, 2>
        190:  RM11T9I(J): PC<10, 2, 10, 9, 2, 1>
        191: RM11T10I(J): PC<9, 1, 9, 8, 1, 0>
        192: RM11T11I(J): PC<8, 0, 8, 7, 0, 11>

    """
    lists = []
    if transposition:
        for n in range(12):
            lists.append([f"T{n}"])
    else:
        lists.append(["T0"])
    if inversion:
        lists = lists + [_[:] + ["I"] for _ in lists]

    if multiplication:
        lists = (
            [["M1"] + _[:] for _ in lists]
            + [["M5"] + _[:] for _ in lists]
            + [["M7"] + _[:] for _ in lists]
            + [["M11"] + _[:] for _ in lists]
        )
    if retrograde:
        lists = lists + [["R"] + _[:] for _ in lists]
    if rotation:
        lists_ = []
        for n in range(len(collection)):
            lists_.extend([f"r{n}"] + _[:] for _ in lists)
        lists = lists_
    pairs = []
    for list_ in lists:
        transform = collection
        for string in reversed(list_):
            if string == "I":
                transform = transform.invert()
            elif string.startswith("T"):
                n = int(string.removeprefix("T"))
                transform = transform.transpose(n=n)
            elif string.startswith("M"):
                n = int(string.removeprefix("M"))
                transform = transform.multiply(n=n)
            elif string == "R":
                transform = transform.retrograde()
            else:
                assert string.startswith("r")
                n = int(string.removeprefix("r"))
                transform = transform.rotate(n=n)
        pairs.append((list_, transform))
    return pairs


def has_duplicate_pitch_classes(collections, level=-1) -> bool:
    """
    Is true when collections have duplicate pitch-classes at ``level``.

    ..  container:: example

        >>> collections = [[4, 5, 7], [15, 16, 17, 19]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_duplicate_pitch_classes(collections, level=1)
        False

        >>> baca.pcollections.has_duplicate_pitch_classes(collections, level=-1)
        True

    Set ``level`` to 1 or -1.
    """
    pitch_class_class = abjad.NumberedPitchClass
    if level == 1:
        for collection in collections:
            known_pitch_classes: list[abjad.PitchClass] = []
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class in known_pitch_classes:
                    return True
                known_pitch_classes.append(pitch_class)
    elif level == -1:
        known_pitch_classes_: list[abjad.PitchClass] = []
        for collection in collections:
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class in known_pitch_classes_:
                    return True
                known_pitch_classes_.append(pitch_class)
    else:
        raise ValueError(f"level must be 1 or -1: {level!r}.")
    return False


def has_duplicates(collections, level=-1) -> bool:
    r"""
    Is true when collections have duplicates at ``level``.

    ..  container:: example

        >>> collections = [[16, 17], [13], [16, 17]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_duplicates(collections, level=0)
        True

        >>> baca.pcollections.has_duplicates(collections, level=1)
        False

        >>> baca.pcollections.has_duplicates(collections, level=-1)
        True

    ..  container:: example

        >>> collections = [[16, 17], [14, 20, 14]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_duplicates(collections, level=0)
        False

        >>> baca.pcollections.has_duplicates(collections, level=1)
        True

        >>> baca.pcollections.has_duplicates(collections, level=-1)
        True

    ..  container:: example

        >>> collections = [[16, 17], [14, 20], [14]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_duplicates(collections, level=0)
        False

        >>> baca.pcollections.has_duplicates(collections, level=1)
        False

        >>> baca.pcollections.has_duplicates(collections, level=-1)
        True

    ..  container:: example

        >>> items = [-2, -1.5, 6, 7]
        >>> segment = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.pcollections.has_duplicates([segment])
        False

    ..  container:: example

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> segment = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.pcollections.has_duplicates([segment])
        True

    Set ``level`` to 0, 1 or -1.
    """
    if level == 0:
        known_items: list = []
        for collection in collections:
            if collection in known_items:
                return True
            known_items.append(collection)
    elif level == 1:
        for collection in collections:
            known_items = []
            for item in collection:
                if item in known_items:
                    return True
                known_items.append(item)
    elif level == -1:
        known_items = []
        for collection in collections:
            for item in collection:
                if item in known_items:
                    return True
                known_items.append(item)
    else:
        raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
    return False


def has_repeat_pitch_classes(collections, level=-1) -> bool:
    """
    Is true when collections have repeat pitch-classes as ``level``.

    ..  container:: example

        >>> collections = [[4, 5, 4, 5], [17, 18]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_repeat_pitch_classes(collections, level=1)
        False

        >>> baca.pcollections.has_repeat_pitch_classes(collections, level=-1)
        True

    Set ``level`` to 0 or -1.
    """
    pitch_class_class = abjad.NumberedPitchClass
    if level == 1:
        for collection in collections:
            previous_pitch_class = None
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class == previous_pitch_class:
                    return True
                previous_pitch_class = pitch_class
    elif level == -1:
        previous_pitch_class = None
        for collection in collections:
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class == previous_pitch_class:
                    return True
                previous_pitch_class = pitch_class
    else:
        raise ValueError(f"level must be 0 or -1: {level!r}.")
    return False


def has_repeats(collections, level=-1) -> bool:
    r"""
    Is true when collections have repeats at ``level``.

    ..  container:: example

        >>> collections = [[4, 5], [4, 5]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_repeats(collections, level=0)
        True

        >>> baca.pcollections.has_repeats(collections, level=1)
        False

        >>> baca.pcollections.has_repeats(collections, level=-1)
        False

    ..  container:: example

        >>> collections = [[4, 5], [18, 18], [4, 5]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_repeats(collections, level=0)
        False

        >>> baca.pcollections.has_repeats(collections, level=1)
        True

        >>> baca.pcollections.has_repeats(collections, level=-1)
        True

    ..  container:: example

        >>> collections = [[4, 5], [5, 18], [4, 5]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.has_repeats(collections, level=0)
        False

        >>> baca.pcollections.has_repeats(collections, level=1)
        False

        >>> baca.pcollections.has_repeats(collections, level=-1)
        True

    ..  container:: example

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> segment = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.pcollections.has_repeats([segment])
        False

    ..  container:: example

        >>> items = [-2, -1.5, 6, 7, 7]
        >>> segment = abjad.PitchClassSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                bqf'8
                fs'8
                g'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.pcollections.has_repeats([segment])
        True

    Set ``level`` to 0, 1 or -1.
    """
    if level == 0:
        previous_collection = None
        for collection in collections:
            if collection == previous_collection:
                return True
            previous_collection = collection
    elif level == 1:
        for collection in collections:
            previous_item = None
            for item in collection:
                if item == previous_item:
                    return True
                previous_item = item
    elif level == -1:
        previous_item = None
        for collection in collections:
            for item in collection:
                if item == previous_item:
                    return True
                previous_item = item
    else:
        raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
    return False


def read(collections, counts=None, check=None):
    """
    Reads collections by ``counts``.

    ..  container:: example

        >>> collections = [[5, 12, 14, 18, 17], [16, 17, 19]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> for collection in baca.pcollections.read(collections, [3, 3, 3, 5, 5, 5]):
        ...     collection
        ...
        PitchSegment([5, 12, 14])
        PitchSegment([18, 17, 16])
        PitchSegment([17, 19, 5])
        PitchSegment([12, 14, 18, 17, 16])
        PitchSegment([17, 19, 5, 12, 14])
        PitchSegment([18, 17, 16, 17, 19])

    ..  container:: example exception

        Raises exception on inexact read:

        >>> collections = [[5, 12, 14, 18, 17], [16, 17, 19]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.read(collections, [10, 10, 10], check=abjad.EXACT)
        Traceback (most recent call last):
            ...
        ValueError: call reads 30 items; not a multiple of 8 items.

    """
    if counts in (None, []):
        type(collections)(collections)
    counts = list(counts)
    assert all(isinstance(_, int) for _ in counts), repr(counts)
    source_collection_type = type(collections[0])
    collection = abjad.sequence.join([_.items for _ in collections])[0]
    source = abjad.CyclicTuple(collection)
    i = 0
    collections_ = []
    for count in counts:
        stop = i + count
        items = source[i:stop]
        items = source_collection_type(items)
        if hasattr(collections, "_initialize_collection"):
            collection = collections._initialize_collection(items)
        else:
            collection = items
        collections_.append(collection)
        i += count
    result = collections_
    if check == abjad.EXACT:
        self_item_count = len(abjad.sequence.join([_.items for _ in collections])[0])
        result_item_count = len(abjad.sequence.join([_.items for _ in result])[0])
        quotient = result_item_count / self_item_count
        if quotient != int(quotient):
            message = f"call reads {result_item_count} items;"
            message += f" not a multiple of {self_item_count} items."
            raise ValueError(message)
    return result


def register_pcs(pitches, pcs):
    """
    Registers ``pcs`` by ``pitches``.

    ..  container:: example

        >>> pitches = [10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40]
        >>> pitches = [abjad.NumberedPitch(_) for _ in pitches]
        >>> pcs = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
        >>> pcs = [abjad.NumberedPitchClass(_) for _ in pcs]
        >>> pitches = baca.pcollections.register_pcs(pitches, pcs)
        >>> for _ in pitches: _
        NumberedPitch(10)
        NumberedPitch(24)
        NumberedPitch(26)
        NumberedPitch(30)
        NumberedPitch(20)
        NumberedPitch(19)
        NumberedPitch(29)
        NumberedPitch(27)
        NumberedPitch(37)
        NumberedPitch(33)
        NumberedPitch(40)
        NumberedPitch(23)

    """
    prototype = (abjad.NumberedPitch, abjad.NamedPitch)
    assert all(isinstance(_, prototype) for _ in pitches), repr(pitches)
    pitches = list(pitches)
    prototype = (abjad.NumberedPitchClass, abjad.NamedPitchClass)
    assert all(isinstance(_, prototype) for _ in pcs), repr(pcs)
    pcs = list(pcs)
    reference_pcs = [_.pitch_class for _ in pitches]
    result = []
    for pc in pcs:
        index = reference_pcs.index(pc)
        pitch = pitches[index]
        result.append(pitch)
    return result


def pitches_to_octave_adjustment(pitches, *, anchor=abjad.DOWN, octave_number=4):
    def _get_anchor_octave_number(pitches, anchor):
        pitches = list(set(pitches))
        pitches.sort()
        if anchor == abjad.DOWN:
            pitch = pitches[0]
        elif anchor == abjad.UP:
            pitch = pitches[-1]
        elif anchor == abjad.CENTER:
            soprano = max(pitches)
            bass = min(pitches)
            centroid = (soprano.number + bass.number) / 2.0
            pitch = abjad.NumberedPitch(centroid)
        else:
            raise ValueError(anchor)
        return pitch.octave.number

    target_octave_number = octave_number
    current_octave_number = _get_anchor_octave_number(pitches, anchor=anchor)
    octave_adjustment = target_octave_number - current_octave_number
    return octave_adjustment


def remove_duplicate_pitch_classes(collections, level=-1):
    """
    Removes duplicate pitch-classes at ``level``.

    ..  container:: example

        >>> collections = [[4, 5, 7], [16, 17, 16, 18]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.remove_duplicate_pitch_classes(collections, level=1)
        [PitchSegment([4, 5, 7]), PitchSegment([16, 17, 18])]

        >>> baca.pcollections.remove_duplicate_pitch_classes(collections, level=-1)
        [PitchSegment([4, 5, 7]), PitchSegment([18])]

    Set ``level`` to 1 or -1.
    """
    pitch_class_class = abjad.NamedPitchClass
    collections_ = []
    if level == 1:
        for collection in collections:
            items = []
            known_pitch_classes = []
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class in known_pitch_classes:
                    continue
                known_pitch_classes.append(pitch_class)
                items.append(item)
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    elif level == -1:
        known_pitch_classes = []
        for collection in collections:
            items = []
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class in known_pitch_classes:
                    continue
                known_pitch_classes.append(pitch_class)
                items.append(item)
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    else:
        raise ValueError(f"level must be 1 or -1: {level!r}.")
    return collections_


def remove_duplicates(collections, level=-1):
    """
    Removes duplicates at ``level``.

    ..  container:: example

        >>> collections = [[16, 17, 16], [13, 14, 16], [16, 17, 16]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.remove_duplicates(collections, level=0)
        [PitchSegment([16, 17, 16]), PitchSegment([13, 14, 16])]

        >>> baca.pcollections.remove_duplicates(collections, level=1)
        [PitchSegment([16, 17]), PitchSegment([13, 14, 16]), PitchSegment([16, 17])]

        >>> baca.pcollections.remove_duplicates(collections, level=-1)
        [PitchSegment([16, 17]), PitchSegment([13, 14])]

    Set ``level`` to 0, 1 or -1.
    """
    collections_ = []
    if level == 0:
        collections_ = []
        known_items = []
        for collection in collections:
            if collection in known_items:
                continue
            known_items.append(collection)
            collections_.append(collection)
    elif level == 1:
        for collection in collections:
            items, known_items = [], []
            for item in collection:
                if item in known_items:
                    continue
                known_items.append(item)
                items.append(item)
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    elif level == -1:
        known_items = []
        for collection in collections:
            items = []
            for item in collection:
                if item in known_items:
                    continue
                known_items.append(item)
                items.append(item)
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    else:
        raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
    return collections_


def remove_repeat_pitch_classes(collections, level=-1):
    """
    Removes repeat pitch-classes at ``level``.

    ..  container:: example

        >>> collections = [[4, 4, 4, 5], [17, 18]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.remove_repeat_pitch_classes(collections, level=1)
        [PitchSegment([4, 5]), PitchSegment([17, 18])]

        >>> baca.pcollections.remove_repeat_pitch_classes(collections, level=-1)
        [PitchSegment([4, 5]), PitchSegment([18])]

    Set ``level`` to 1 or -1.
    """
    pitch_class_class = abjad.NamedPitchClass
    collections_ = []
    if level == 1:
        for collection in collections:
            items, previous_pitch_class = [], None
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class == previous_pitch_class:
                    continue
                items.append(item)
                previous_pitch_class = pitch_class
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    elif level == -1:
        previous_pitch_class = None
        for collection in collections:
            items = []
            for item in collection:
                pitch_class = pitch_class_class(item)
                if pitch_class == previous_pitch_class:
                    continue
                items.append(item)
                previous_pitch_class = pitch_class
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    else:
        raise ValueError(f"level must be 1 or -1: {level!r}.")
    return collections_


def remove_repeats(collections, level=-1):
    """
    Removes repeats at ``level``.

    ..  container:: example

        >>> collections = [[4, 5], [4, 5], [5, 7, 7]]
        >>> collections = [abjad.PitchSegment(_) for _ in collections]

        >>> baca.pcollections.remove_repeats(collections, level=0)
        [PitchSegment([4, 5]), PitchSegment([5, 7, 7])]

        >>> baca.pcollections.remove_repeats(collections, level=1)
        [PitchSegment([4, 5]), PitchSegment([4, 5]), PitchSegment([5, 7])]

        >>> baca.pcollections.remove_repeats(collections, level=-1)
        [PitchSegment([4, 5]), PitchSegment([4, 5]), PitchSegment([7])]

    Set ``level`` to 0, 1 or -1.
    """
    collections_ = []
    if level == 0:
        previous_collection = None
        for collection in collections:
            if collection == previous_collection:
                continue
            collections_.append(collection)
            previous_collection = collection
    elif level == 1:
        for collection in collections:
            items, previous_item = [], None
            for item in collection:
                if item == previous_item:
                    continue
                items.append(item)
                previous_item = item
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    elif level == -1:
        previous_item = None
        for collection in collections:
            items = []
            for item in collection:
                if item == previous_item:
                    continue
                items.append(item)
                previous_item = item
            if items:
                collection_ = type(collection)(items)
                collections_.append(collection_)
    else:
        raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
    return collections_


def soprano_to_octave(collection, n=4):
    r"""
    Octave-transposes collection to soprano in octave ``n``.

    ..  container:: example

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.soprano_to_octave(segment, n=3)
        PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

        >>> segment = baca.pcollections.soprano_to_octave(segment, n=3)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                }
            >>

    Returns new segment.
    """
    octave_adjustment = pitches_to_octave_adjustment(
        collection, anchor=abjad.UP, octave_number=n
    )
    segment = collection.transpose(n=12 * octave_adjustment)
    return dataclasses.replace(collection, items=segment)


def space_down(collection, bass=None, semitones=None, soprano=None):
    r"""
    Spaces collection down.

    ..  container:: example

        >>> segment = abjad.PitchClassSegment([10, 11, 5, 6, 7])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                b'8
                f'8
                fs'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.pcollections.space_down(segment, bass=6, soprano=7)
        PitchSegment([19, 17, 11, 10, 6])

        >>> segment = baca.pcollections.space_down(segment, bass=6, soprano=7)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.stencil = ##f
                \override Rest.transparent = ##t
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            }
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            g''1 * 1/8
                            f''1 * 1/8
                            b'1 * 1/8
                            bf'1 * 1/8
                            fs'1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> segment = abjad.PitchSegment([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.space_down(segment, bass=0)
        PitchSegment([14, 10, 9, 0])

        >>> segment = baca.pcollections.space_down(segment, bass=0)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        d''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        c'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    ..  container:: example

        With 2 in bass:

        >>> segment = abjad.PitchSegment([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.space_down(segment, bass=2)
        PitchSegment([12, 10, 9, 2])

        >>> segment = baca.pcollections.space_down(segment, bass=2)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        d'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>


    ..  container:: example

        >>> set_ = abjad.PitchSet([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(set_)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <c'' d'' a'' bf''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

        >>> baca.pcollections.space_down(set_, bass=0)
        PitchSet([0, 9, 10, 14])

        >>> set_ = baca.pcollections.space_down(set_, bass=0)
        >>> lilypond_file = abjad.illustrate(set_)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <c' a' bf' d''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

    ..  container:: example

        With 2 in bass:

        >>> set_ = abjad.PitchSet([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(set_)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <c'' d'' a'' bf''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

        >>> baca.pcollections.space_down(set_, bass=2)
        PitchSet([2, 9, 10, 12])

        >>> set_ = baca.pcollections.space_down(set_, bass=2)
        >>> lilypond_file = abjad.illustrate(set_)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <d' a' bf' c''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

    Returns new collection.
    """
    specifier = ChordalSpacingSpecifier(
        bass=bass,
        direction=abjad.DOWN,
        minimum_semitones=semitones,
        soprano=soprano,
    )
    result = specifier([collection])
    assert len(result) == 1, repr(result)
    collection_ = result[0]
    return collection_


def space_up(collection, bass=None, semitones=None, soprano=None):
    r"""
    Spaces collection up.

    ..  container:: example

        >>> segment = abjad.PitchClassSegment([10, 11, 5, 6, 7])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> voice = lilypond_file["Voice"]
            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \context Voice = "Voice"
            {
                bf'8
                b'8
                f'8
                fs'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

        >>> baca.pcollections.space_up(segment, bass=6, soprano=7)
        PitchSegment([6, 10, 11, 17, 19])

        >>> segment = baca.pcollections.space_up(segment, bass=6, soprano=7)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.stencil = ##f
                \override Rest.transparent = ##t
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            }
            <<
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \context Voice = "Treble_Voice"
                        {
                            \clef "treble"
                            fs'1 * 1/8
                            bf'1 * 1/8
                            b'1 * 1/8
                            f''1 * 1/8
                            g''1 * 1/8
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> segment = abjad.PitchSegment([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.space_up(segment, bass=0)
        PitchSegment([0, 2, 9, 10])

        >>> segment = baca.pcollections.space_up(segment, bass=0)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    ..  container:: example

        With 2 in bass:

        >>> segment = abjad.PitchSegment([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> baca.pcollections.space_up(segment, bass=2)
        PitchSegment([2, 9, 10, 12])

        >>> segment = baca.pcollections.space_up(segment, bass=2)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                        c''1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

    ..  container:: example

        >>> setting = abjad.PitchSet([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(setting)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <c'' d'' a'' bf''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

        >>> baca.pcollections.space_up(setting, bass=0)
        PitchSet([0, 2, 9, 10])

        >>> setting = baca.pcollections.space_up(setting, bass=0)
        >>> lilypond_file = abjad.illustrate(setting)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <c' d' a' bf'>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

    ..  container:: example

        With 2 in bass:

        >>> setting = abjad.PitchSet([12, 14, 21, 22])
        >>> lilypond_file = abjad.illustrate(setting)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <c'' d'' a'' bf''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>

        >>> baca.pcollections.space_up(setting, bass=2)
        PitchSet([2, 9, 10, 12])

        >>> setting = baca.pcollections.space_up(setting, bass=2)
        >>> lilypond_file = abjad.illustrate(setting)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        <d' a' bf' c''>1
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        s1
                    }
                }
            >>


    Returns new collection.
    """
    specifier = ChordalSpacingSpecifier(
        bass=bass,
        direction=abjad.UP,
        minimum_semitones=semitones,
        soprano=soprano,
    )
    result = specifier([collection])
    assert len(result) == 1, repr(result)
    collection_ = result[0]
    return collection_


def split(collection, pitch=0):
    r"""
    Splits collection at ``pitch``.

    ..  container:: example

        >>> items = [-2, -1.5, 6, 7, -1.5, 7]
        >>> segment = abjad.PitchSegment(items=items)
        >>> lilypond_file = abjad.illustrate(segment)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> upper, lower = baca.pcollections.split(segment, pitch=0)

        >>> upper
        PitchSegment([6, 7, 7])

        >>> lilypond_file = abjad.illustrate(upper)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        fs'1 * 1/8
                        g'1 * 1/8
                        g'1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
            >>

        >>> lower
        PitchSegment([-2, -1.5, -1.5])

        >>> lilypond_file = abjad.illustrate(lower)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> staff_group = lilypond_file["Piano_Staff"]
            >>> string = abjad.lilypond(staff_group)
            >>> print(string)
            \context PianoStaff = "Piano_Staff"
            <<
                \context Staff = "Treble_Staff"
                {
                    \context Voice = "Treble_Voice"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                }
                \context Staff = "Bass_Staff"
                {
                    \context Voice = "Bass_Voice"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        bqf1 * 1/8
                    }
                }
            >>

    Returns upper, lower collections.
    """
    upper, lower = [], []
    for pitch_ in collection:
        if pitch_ < pitch:
            lower.append(pitch_)
        else:
            upper.append(pitch_)
    upper = dataclasses.replace(collection, items=upper)
    lower = dataclasses.replace(collection, items=lower)
    return upper, lower
