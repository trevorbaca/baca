"""
Pitch collections.
"""
import collections as collections_module
import copy
import dataclasses
import math
import typing

import abjad

from . import classes as _classes
from . import sequence as _sequence


@dataclasses.dataclass(slots=True)
class ArpeggiationSpacingSpecifier:
    r"""
    Arpeggiation spacing specifier.

    ..  container:: example

        >>> specifier = baca.ArpeggiationSpacingSpecifier()
        >>> specifier([[6, 0, 4, 5, 8]])
        CollectionList([<6, 12, 16, 17, 20>])

    ..  container:: example

        >>> specifier = baca.ArpeggiationSpacingSpecifier()
        >>> specifier([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        CollectionList([<0, 2, 10>, <6, 16, 27, 32, 43>, <9>])

    ..  container:: example

        >>> baca.ArpeggiationSpacingSpecifier()
        ArpeggiationSpacingSpecifier(direction=None, pattern=None)

    ..  container:: example

        Arpeggiate up:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(2),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> collections = baca.CollectionList(collections)
        >>> collections = collections.arpeggiate_up()
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/16
                        c,16
                        [
                        d,16
                        bf,16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs,16
                        [
                        e16
                        ef'16
                        af'16
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a,16
                    }
                }
            >>

    ..  container:: example

        Arpeggiate down:

        >>> stack = baca.stack(
        ...     baca.figure([1], 16),
        ...     rmakers.beam(),
        ...     baca.bass_to_octave(2),
        ... )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> collections = baca.CollectionList(collections)
        >>> collections = collections.arpeggiate_down()
        >>> selection = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 9/16
                        c'16
                        [
                        d16
                        bf,16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        fs16
                        [
                        e16
                        ef16
                        af,16
                        g,16
                        ]
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a,16
                    }
                }
            >>

    """

    direction: abjad.enums.VerticalAlignment | None = None
    pattern: abjad.Pattern | None = None

    def __post_init__(self):
        if self.direction is not None:
            assert self.direction in (abjad.Up, abjad.Down), repr(self.direction)
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern), repr(self.pattern)

    def __call__(
        self, collections=None
    ) -> typing.Union["PitchSegment", "CollectionList", None]:
        if collections is None:
            return None
        if collections == []:
            return PitchSegment(item_class=abjad.NumberedPitch)
        if not isinstance(collections, CollectionList):
            collections = CollectionList(collections)
        if collections.item_class is abjad.NamedPitch:
            pitch_class_collections = collections.to_named_pitch_classes()
        else:
            assert collections.item_class in (abjad.NumberedPitch, None), repr(
                collections.item_class
            )
            pitch_class_collections = collections.to_numbered_pitch_classes()
        pattern = self.pattern or abjad.index_all()
        collections_ = []
        total_length = len(collections)
        direction = self.direction or abjad.Up
        for i in range(total_length):
            if pattern.matches_index(i, total_length):
                pitch_class_collection = pitch_class_collections[i]
                if isinstance(pitch_class_collection, abjad.Set):
                    pitch_classes = list(sorted(pitch_class_collection))
                else:
                    pitch_classes = list(pitch_class_collection)
                if direction == abjad.Up:
                    pitches = _to_tightly_spaced_pitches_ascending(pitch_classes)
                else:
                    pitches = _to_tightly_spaced_pitches_descending(pitch_classes)
                collection_: CollectionTyping
                if isinstance(pitch_class_collection, abjad.Set):
                    collection_ = PitchSet(items=pitches)
                else:
                    collection_ = PitchSegment(items=pitches)
                collections_.append(collection_)
            else:
                collections_.append(collections[i])
        return CollectionList(collections_)


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
    collection = PitchSegment(pitches)
    while collection[-1].octave.number < 4:
        collection = collection.transpose(n=12)
    return collection


@dataclasses.dataclass(slots=True)
class ChordalSpacingSpecifier:
    """
    Chordal spacing specifier.

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 9, 11, 17, 19>])

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.Down,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<19, 17, 11, 9, 6>])

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=11,
        ...     direction=abjad.Down,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<31, 30, 29, 21, 11>])

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier()
        >>> specifier([[0, 1, 2]])
        CollectionList([<0, 1, 2>])

        >>> specifier([[0, 2, 1]])
        CollectionList([<0, 1, 2>])

        >>> specifier([[1, 0, 2]])
        CollectionList([<1, 2, 12>])

        >>> specifier([[1, 2, 0]])
        CollectionList([<1, 2, 12>])

        >>> specifier([[2, 0, 1]])
        CollectionList([<2, 12, 13>])

        >>> specifier([[2, 1, 0]])
        CollectionList([<2, 12, 13>])

    ..  container:: example

        Up-directed bass specification:

        >>> specifier = baca.ChordalSpacingSpecifier(bass=None)
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 7, 9, 11, 17>])

        >>> specifier = baca.ChordalSpacingSpecifier(bass=6)
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 7, 9, 11, 17>])

        >>> specifier = baca.ChordalSpacingSpecifier(bass=7)
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<7, 9, 11, 17, 18>])

        >>> specifier = baca.ChordalSpacingSpecifier(bass=9)
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<9, 11, 17, 18, 19>])

        >>> specifier = baca.ChordalSpacingSpecifier(bass=11)
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<11, 17, 18, 19, 21>])

        >>> specifier = baca.ChordalSpacingSpecifier(bass=5)
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<5, 6, 7, 9, 11>])

    ..  container:: example

        Up-directed joint control:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 9, 11, 17, 19>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=9,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 7, 11, 17, 21>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=11,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 7, 9, 17, 23>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=5
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 7, 9, 11, 17>])

    ..  container:: example

        Up-directed spacing with semitone constraints.

        First three examples give the same spacing:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<6, 9, 11, 17, 19>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     minimum_semitones=1,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<6, 9, 11, 17, 19>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     minimum_semitones=2,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<6, 9, 11, 17, 19>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     minimum_semitones=3,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<6, 9, 17, 23, 31>])

    ..  container:: example

        Down-directed spacing with semitone constraints.

        First three examples give the same spacing:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.Down,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<19, 17, 11, 9, 6>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.Down,
        ...     minimum_semitones=1,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<19, 17, 11, 9, 6>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.Down,
        ...     minimum_semitones=2,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<19, 17, 11, 9, 6>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.Down,
        ...     minimum_semitones=3,
        ...     soprano=7,
        ... )
        >>> specifier([[5, 6, 7, 9, 11]])
        CollectionList([<31, 23, 17, 9, 6>])

    ..  container:: example

        Down-directed soprano control:

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.Down,
        ...     soprano=None,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<18, 17, 11, 9, 7>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.Down,
        ...     soprano=6,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<18, 17, 11, 9, 7>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.Down,
        ...     soprano=5,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<17, 11, 9, 7, 6>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.Down,
        ...     soprano=11,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<11, 9, 7, 6, 5>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.Down,
        ...     soprano=9,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<21, 19, 18, 17, 11>])

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     direction=abjad.Down,
        ...     soprano=7,
        ... )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<19, 18, 17, 11, 9>])

    """

    bass: typing.Any = None
    direction: typing.Any = None
    minimum_semitones: typing.Any = None
    pattern: typing.Any = None
    soprano: typing.Any = None

    def __post_init__(self):
        if self.direction is not None:
            assert self.direction in (abjad.Up, abjad.Down)
        if self.minimum_semitones is not None:
            assert isinstance(self.minimum_semitones, int)
            assert 1 <= self.minimum_semitones
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern)

    def __call__(self, collections=None) -> typing.Union["CollectionList", None]:
        if collections is None:
            return None
        if not isinstance(collections, CollectionList):
            collections = CollectionList(collections)
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
        return CollectionList(collections_)

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
        if isinstance(collection, abjad.Set):
            pitch_classes = [abjad.NumberedPitchClass(_) for _ in collection]
            pitch_classes.sort()
        else:
            pitch_classes = list(collection.to_numbered_pitch_classes())
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
        direction = self.direction or abjad.Up
        if direction is abjad.Up:
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
        if isinstance(original_collection, abjad.Set):
            return PitchSet(pitches)
        else:
            return PitchSegment(pitches)


def _to_baca_collection(collection):
    abjad_prototype = (
        abjad.PitchClassSegment,
        abjad.PitchClassSet,
        abjad.PitchSegment,
        abjad.PitchSet,
    )
    assert isinstance(collection, abjad_prototype), repr(collection)
    baca_prototype = (
        PitchClassSegment,
        abjad.PitchClassSet,
        PitchSegment,
        PitchSet,
    )
    if isinstance(collection, baca_prototype):
        pass
    elif isinstance(collection, abjad.PitchClassSegment):
        collection = PitchClassSegment(
            items=collection, item_class=collection.item_class
        )
    elif isinstance(collection, abjad.PitchClassSet):
        collection = abjad.PitchClassSet(
            items=collection, item_class=collection.item_class
        )
    elif isinstance(collection, abjad.PitchSegment):
        collection = PitchSegment(items=collection, item_class=collection.item_class)
    elif isinstance(collection, abjad.PitchSet):
        collection = PitchSet(items=collection, item_class=collection.item_class)
    elif isinstance(collection, abjad.PitchSet):
        collection = PitchSet(items=collection, item_class=collection.item_class)
    else:
        raise TypeError(collection)
    assert isinstance(collection, baca_prototype)
    return collection


@dataclasses.dataclass
class CollectionList(collections_module.abc.Sequence):
    """
    Collection list.

    ..  container:: example

        Initializes numbered pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     [16, 20, 19],
        ...     ]):
        ...     collection
        ...
        PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
        PitchSegment(items=[16, 20, 19], item_class=NumberedPitch)

    ..  container:: example

        Initializes named pitch segments:

        >>> for collection in baca.CollectionList(
        ...     [
        ...         [12, 14, 18, 17],
        ...         [16, 20, 19],
        ...     ],
        ...     item_class=abjad.NamedPitch,
        ...     ):
        ...     collection
        ...
        PitchSegment(items="c'' d'' fs'' f''", item_class=NamedPitch)
        PitchSegment(items="e'' af'' g''", item_class=NamedPitch)

    ..  container:: example

        Initializes numbered pitch-class segments:

        >>> for collection in baca.CollectionList(
        ...     [
        ...         [12, 14, 18, 17],
        ...         [16, 20, 19],
        ...     ],
        ...     item_class=abjad.NumberedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSegment(items=[0, 2, 6, 5], item_class=NumberedPitchClass)
        PitchClassSegment(items=[4, 8, 7], item_class=NumberedPitchClass)

    ..  container:: example

        Initializes named pitch-class segments:

        >>> for collection in baca.CollectionList(
        ...     [
        ...         [12, 14, 18, 17],
        ...         [16, 20, 19],
        ...     ],
        ...     item_class=abjad.NamedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSegment(items="c d fs f", item_class=NamedPitchClass)
        PitchClassSegment(items="e af g", item_class=NamedPitchClass)

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     "ff'' gs'' g''",
        ...     ]):
        ...     collection
        ...
        PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
        PitchSegment(items="ff'' gs'' g''", item_class=NamedPitch)

    ..  container:: example

        Initializes numbered pitch sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ]):
        ...     collection
        ...
        PitchSet(items=[12, 14, 17, 18], item_class=abjad.NumberedPitch)
        PitchSet(items=[16, 19, 20], item_class=abjad.NumberedPitch)

    ..  container:: example

        Initializes named pitch sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ],
        ...     item_class=abjad.NamedPitch,
        ...     ):
        ...     collection
        ...
        PitchSet(items=["c''", "d''", "f''", "fs''"], item_class=abjad.NamedPitch)
        PitchSet(items=["e''", "g''", "af''"], item_class=abjad.NamedPitch)

    ..  container:: example

        Initializes numbered pitch-class sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ],
        ...     item_class=abjad.NumberedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSet(items=[0, 2, 5, 6], item_class=abjad.NumberedPitchClass)
        PitchClassSet(items=[4, 7, 8], item_class=abjad.NumberedPitchClass)

    ..  container:: example

        Initializes named pitch-class sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ],
        ...     item_class=abjad.NamedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSet(items=['c', 'd', 'f', 'fs'], item_class=abjad.NamedPitchClass)
        PitchClassSet(items=['e', 'g', 'af'], item_class=abjad.NamedPitchClass)

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     "ff'' gs'' g''",
        ...     ]):
        ...     collection
        ...
        PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
        PitchSegment(items="ff'' gs'' g''", item_class=NamedPitch)

    ..  container:: example

        Initializes mixed segments and sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     [16, 20, 19],
        ...     ]):
        ...     collection
        ...
        PitchSet(items=[12, 14, 17, 18], item_class=abjad.NumberedPitch)
        PitchSegment(items=[16, 20, 19], item_class=NumberedPitch)

    ..  container:: example

        Initializes from collection list:

        >>> collections = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
        >>> baca.CollectionList(collections)
        CollectionList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes from list of collection lists:

        >>> collection_list_1 = baca.CollectionList([[12, 13, 14]])
        >>> collection_list_2 = baca.CollectionList([[15, 16, 17]])
        >>> baca.CollectionList([collection_list_1, collection_list_2])
        CollectionList([<12, 13, 14>, <15, 16, 17>])

    """

    collections: typing.Any = None
    item_class: typing.Any = None

    _item_class_prototype = (
        abjad.NumberedPitch,
        abjad.NumberedPitchClass,
        abjad.NamedPitch,
        abjad.NamedPitchClass,
    )

    def __post_init__(self):
        if self.item_class is not None:
            if self.item_class not in self._item_class_prototype:
                raise TypeError(f"only pitch or pitch-class: {self.item_class!r}.")
        self.collections = self._coerce(self.collections)
        self.collections = self.collections or []
        self.collections = tuple(self.collections)

    def __add__(self, argument) -> "CollectionList":
        """
        Adds ``argument`` to collections.

        ..  container:: example

            >>> collections_1 = baca.CollectionList([[12, 14, 18, 17]])
            >>> collections_2 = baca.CollectionList([[16, 20, 19]])
            >>> collections_1 + collections_2
            CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

        """
        if not isinstance(argument, collections_module.abc.Iterable):
            raise TypeError(f"must be collection list: {argument!r}.")
        argument_collections = [self._initialize_collection(_) for _ in argument]
        collections = list(self.collections) + argument_collections
        return dataclasses.replace(self, collections=collections)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a collection list with collections equal to those of
        this collection list.

        ..  container:: example

            >>> collections_1 = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
            >>> collections_2 = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
            >>> collections_3 = baca.CollectionList([[12, 13, 14]])

            >>> collections_1 == collections_1
            True
            >>> collections_1 == collections_2
            True
            >>> collections_1 == collections_3
            False

            >>> collections_2 == collections_1
            True
            >>> collections_2 == collections_2
            True
            >>> collections_2 == collections_3
            False

            >>> collections_3 == collections_1
            False
            >>> collections_3 == collections_2
            False
            >>> collections_3 == collections_3
            True

        ..  container:: example

            Ignores item class:

            >>> collections_1 = baca.CollectionList(
            ...     collections=[[12, 13, 14], [15, 16, 17]],
            ...     item_class=None,
            ... )
            >>> collections_2 = baca.CollectionList(
            ...     collections=[[12, 13, 14], [15, 16, 17]],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> collections_1.item_class == collections_2.item_class
            False

            >>> collections_1 == collections_2
            True

        """
        if not isinstance(argument, type(self)):
            return False
        return self.collections == argument.collections

    def __getitem__(self, argument):
        """
        Gets collection or collection slice identified by ``argument``.

        ..  container:: example

            Gets collections:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ... ])

            >>> collections[0]
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)

            >>> collections[-1]
            PitchSegment(items=[16, 20, 19], item_class=NumberedPitch)

        ..  container:: example

            Gets collections lists:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ... ])

            >>> collections[:1]
            CollectionList([<12, 14, 18, 17>])

            >>> collections[-1:]
            CollectionList([<16, 20, 19>])

        Returns collection.
        """
        collections = self.collections or []
        result = collections.__getitem__(argument)
        try:
            return dataclasses.replace(self, collections=result)
        except TypeError:
            return result

    def __len__(self) -> int:
        """
        Gets length of collections.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ... ])

            >>> len(collections)
            2

        """
        if self.collections:
            return len(self.collections)
        else:
            return 0

    def __repr__(self) -> str:
        """
        Gets interpreter representation of collections.

        ..  container:: example

            >>> baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ... ])
            CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

        """
        collections = self.collections or []
        collections_ = ", ".join([str(_) for _ in collections])
        string = f"{type(self).__name__}([{collections_}])"
        return string

    def _coerce(self, collections):
        prototype = (PitchSegment, PitchSet, PitchClassSegment, abjad.PitchClassSet)
        collections_ = []
        for item in collections or []:
            if isinstance(item, type(self)):
                for collection in item:
                    collection_ = self._initialize_collection(collection)
                    collections_.append(collection_)
            else:
                collection_ = self._initialize_collection(item)
                collections_.append(collection_)
        collections_ = [_to_baca_collection(_) for _ in collections_]
        assert all(isinstance(_, prototype) for _ in collections_)
        return collections_

    def _get_pitch_class_class(self):
        item_class = self.item_class or abjad.NumberedPitch
        if item_class in (abjad.NumberedPitchClass, abjad.NamedPitchClass):
            return item_class
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        else:
            raise TypeError(f"only pitch or pc class: {item_class!r}.")

    def _initialize_collection(self, argument, prototype=None):
        items = argument
        item_class = self.item_class or abjad.NumberedPitch
        if prototype is not None:
            return dataclasses.replace(prototype, items=items)
        elif isinstance(argument, abjad.Segment):
            return argument
        elif isinstance(argument, abjad.Set):
            return argument
        elif isinstance(argument, set):
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return abjad.PitchSet(items=items, item_class=item_class)
            elif item_class in (
                abjad.NumberedPitchClass,
                abjad.NamedPitchClass,
            ):
                return abjad.PitchClassSet(items=items, item_class=item_class)
            else:
                raise TypeError(item_class)
        elif self.item_class is not None:
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return PitchSegment(items=items, item_class=item_class)
            elif item_class in (
                abjad.NumberedPitchClass,
                abjad.NamedPitchClass,
            ):
                return PitchClassSegment(items=items, item_class=item_class)
            else:
                raise TypeError(item_class)
        else:
            if isinstance(argument, str):
                return PitchSegment(items=items, item_class=abjad.NamedPitch)
            elif isinstance(argument, collections_module.abc.Iterable):
                return PitchSegment(items=items, item_class=abjad.NumberedPitch)
            else:
                raise TypeError(f"only string or iterable: {argument!r}.")

    def arpeggiate_down(self, pattern=None) -> "CollectionList":
        """
        Apreggiates collections down according to ``pattern``.

        ..  container:: example

            Down-arpeggiates all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )

            >>> collections.arpeggiate_down()
            CollectionList([<29, 24, 14, 6, 5>, <28, 17, 7>, <3, 2, 1, 0>])

        ..  container:: example

            Down-arpeggiates collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )

            >>> collections.arpeggiate_down(pattern=[-1])
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <3, 2, 1, 0>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                if isinstance(collection, abjad.PitchSegment):
                    collection = collection.to_numbered_pitch_classes()
                    collection = PitchClassSegment(
                        items=collection, item_class=collection.item_class
                    )
                collection = collection.arpeggiate_down()
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def arpeggiate_up(self, pattern=None) -> "CollectionList":
        """
        Apreggiates collections up according to ``pattern``.

        ..  container:: example

            Up-arpeggiates all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )

            >>> collections.arpeggiate_up()
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

        ..  container:: example

            Up-arpeggiates collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )

            >>> collections.arpeggiate_up(pattern=[-1])
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <3, 14, 25, 36>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                if isinstance(collection, abjad.PitchSegment):
                    collection = collection.to_numbered_pitch_classes()
                    collection = PitchClassSegment(
                        items=collection, item_class=collection.item_class
                    )
                collection = collection.arpeggiate_up()
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def bass_to_octave(self, n=4, pattern=None) -> "CollectionList":
        """
        Octave-transposes collections to bass in octave ``n``.

        ..  container:: example

            Octave-transposes all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.bass_to_octave(n=3)
            CollectionList([<-7, 0, 2, 6, 17>, <-8, -7, -5>, <-9, 2, 13, 24>])

        ..  container:: example

            Octave-transposes collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.bass_to_octave(n=3, pattern=[-1])
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-9, 2, 13, 24>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.bass_to_octave(n=n)
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def center_to_octave(self, n=4, pattern=None) -> "CollectionList":
        """
        Octave-transposes collections to center in octave ``n``.

        ..  container:: example

            Octave-transposes all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.center_to_octave(n=3)
            CollectionList([<-19, -12, -10, -6, 5>, <-8, -7, -5>, <-21, -10, 1, 12>])

        ..  container:: example

            Octave-transposes collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.center_to_octave(n=3, pattern=[-1])
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-21, -10, 1, 12>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.center_to_octave(n=n)
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def chords(self, pattern=None) -> "CollectionList":
        """
        Turns collections into chords according to ``pattern``.

        ..  container:: example

            Without pattern:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ... ])

            >>> for collection in collections:
            ...     collection
            ...
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSegment(items=[16, 20, 19], item_class=NumberedPitch)
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSegment(items=[16, 20, 19], item_class=NumberedPitch)

            >>> for collection in collections.chords():
            ...     collection
            ...
            PitchSet(items=[12, 14, 17, 18], item_class=abjad.NumberedPitch)
            PitchSet(items=[16, 19, 20], item_class=abjad.NumberedPitch)
            PitchSet(items=[12, 14, 17, 18], item_class=abjad.NumberedPitch)
            PitchSet(items=[16, 19, 20], item_class=abjad.NumberedPitch)

        ..  container:: example

            With pattern:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ... ])

            >>> pattern = abjad.index([1], 2)
            >>> for collection in collections.chords(pattern=pattern):
            ...     collection
            ...
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSet(items=[16, 19, 20], item_class=abjad.NumberedPitch)
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSet(items=[16, 19, 20], item_class=abjad.NumberedPitch)

        """
        collections = []
        length = len(self)
        pattern = pattern or abjad.index_all()
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collections.append(collection.chord())
            else:
                collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def cursor(self, cyclic=None, singletons=None) -> _classes.Cursor:
        """
        Wraps collections in cursor.

        ..  container:: example

            >>> collections = baca.CollectionList([[5, 12, 14, 18], [16, 17]])
            >>> cursor = collections.cursor()

            >>> cursor
            Cursor(source=CollectionList([<5, 12, 14, 18>, <16, 17>]), cyclic=None, position=None, singletons=None, suppress_exception=None)

            >>> cursor.next()
            [PitchSegment(items=[5, 12, 14, 18], item_class=NumberedPitch)]

            >>> cursor.next()
            [PitchSegment(items=[16, 17], item_class=NumberedPitch)]

        """
        return _classes.Cursor(cyclic=cyclic, singletons=singletons, source=self)

    def flatten(self) -> "CollectionTyping":
        """
        Flattens collections.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ... )

            >>> str(collections.flatten())
            '<5, 12, 14, 18, 17, 16, 17, 19>'

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ...     item_class=abjad.NamedPitch,
            ... )

            >>> str(collections.flatten())
            "<f' c'' d'' fs'' f'' e'' f'' g''>"

        """
        return self.join()[0]

    def has_duplicate_pitch_classes(self, level=-1) -> bool:
        """
        Is true when collections have duplicate pitch-classes at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [4, 5, 7],
            ...     [15, 16, 17, 19]
            ... ])

            >>> collections.has_duplicate_pitch_classes(level=1)
            False

            >>> collections.has_duplicate_pitch_classes(level=-1)
            True

        Set ``level`` to 1 or -1.
        """
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for collection in self:
                known_pitch_classes: typing.List[abjad.PitchClass] = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        return True
                    known_pitch_classes.append(pitch_class)
        elif level == -1:
            known_pitch_classes_: typing.List[abjad.PitchClass] = []
            for collection in self:
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes_:
                        return True
                    known_pitch_classes_.append(pitch_class)
        else:
            raise ValueError(f"level must be 1 or -1: {level!r}.")
        return False

    def has_duplicates(self, level=-1) -> bool:
        """
        Is true when collections have duplicates at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [16, 17], [13], [16, 17],
            ... ])

            >>> collections.has_duplicates(level=0)
            True

            >>> collections.has_duplicates(level=1)
            False

            >>> collections.has_duplicates(level=-1)
            True

        ..  container:: example

            >>> collections = baca.CollectionList([[16, 17], [14, 20, 14]])

            >>> collections.has_duplicates(level=0)
            False

            >>> collections.has_duplicates(level=1)
            True

            >>> collections.has_duplicates(level=-1)
            True

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [16, 17], [14, 20], [14],
            ... ])

            >>> collections.has_duplicates(level=0)
            False

            >>> collections.has_duplicates(level=1)
            False

            >>> collections.has_duplicates(level=-1)
            True

        Set ``level`` to 0, 1 or -1.
        """
        if level == 0:
            known_items: list = []
            for collection in self:
                if collection in known_items:
                    return True
                known_items.append(collection)
        elif level == 1:
            for collection in self:
                known_items = []
                for item in collection:
                    if item in known_items:
                        return True
                    known_items.append(item)
        elif level == -1:
            known_items = []
            for collection in self:
                for item in collection:
                    if item in known_items:
                        return True
                    known_items.append(item)
        else:
            raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
        return False

    def has_repeat_pitch_classes(self, level=-1) -> bool:
        """
        Is true when collections have repeat pitch-classes as ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5, 4, 5], [17, 18]])

            >>> collections.has_repeat_pitch_classes(level=1)
            False

            >>> collections.has_repeat_pitch_classes(level=-1)
            True

        Set ``level`` to 0 or -1.
        """
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for collection in self:
                previous_pitch_class = None
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        elif level == -1:
            previous_pitch_class = None
            for collection in self:
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        else:
            raise ValueError(f"level must be 0 or -1: {level!r}.")
        return False

    def has_repeats(self, level=-1) -> bool:
        """
        Is true when collections have repeats at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5], [4, 5]])

            >>> collections.has_repeats(level=0)
            True

            >>> collections.has_repeats(level=1)
            False

            >>> collections.has_repeats(level=-1)
            False

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [4, 5], [18, 18], [4, 5],
            ... ])

            >>> collections.has_repeats(level=0)
            False

            >>> collections.has_repeats(level=1)
            True

            >>> collections.has_repeats(level=-1)
            True

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [4, 5], [5, 18], [4, 5],
            ... ])

            >>> collections.has_repeats(level=0)
            False

            >>> collections.has_repeats(level=1)
            False

            >>> collections.has_repeats(level=-1)
            True

        Set ``level`` to 0, 1 or -1.
        """
        if level == 0:
            previous_collection = None
            for collection in self:
                if collection == previous_collection:
                    return True
                previous_collection = collection
        elif level == 1:
            for collection in self:
                previous_item = None
                for item in collection:
                    if item == previous_item:
                        return True
                    previous_item = item
        elif level == -1:
            previous_item = None
            for collection in self:
                for item in collection:
                    if item == previous_item:
                        return True
                    previous_item = item
        else:
            raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
        return False

    def helianthate(self, n=0, m=0) -> "CollectionList":
        """
        Helianthates collections.

        ..  container:: example

            >>> collections = baca.CollectionList([[1, 2, 3], [4, 5], [6, 7, 8]])
            >>> for collection in collections.helianthate(n=-1, m=1):
            ...     collection
            ...
            PitchSegment(items=[1, 2, 3], item_class=NumberedPitch)
            PitchSegment(items=[4, 5], item_class=NumberedPitch)
            PitchSegment(items=[6, 7, 8], item_class=NumberedPitch)
            PitchSegment(items=[5, 4], item_class=NumberedPitch)
            PitchSegment(items=[8, 6, 7], item_class=NumberedPitch)
            PitchSegment(items=[3, 1, 2], item_class=NumberedPitch)
            PitchSegment(items=[7, 8, 6], item_class=NumberedPitch)
            PitchSegment(items=[2, 3, 1], item_class=NumberedPitch)
            PitchSegment(items=[4, 5], item_class=NumberedPitch)
            PitchSegment(items=[1, 2, 3], item_class=NumberedPitch)
            PitchSegment(items=[5, 4], item_class=NumberedPitch)
            PitchSegment(items=[6, 7, 8], item_class=NumberedPitch)
            PitchSegment(items=[4, 5], item_class=NumberedPitch)
            PitchSegment(items=[8, 6, 7], item_class=NumberedPitch)
            PitchSegment(items=[3, 1, 2], item_class=NumberedPitch)
            PitchSegment(items=[7, 8, 6], item_class=NumberedPitch)
            PitchSegment(items=[2, 3, 1], item_class=NumberedPitch)
            PitchSegment(items=[5, 4], item_class=NumberedPitch)

        """
        collections = _sequence.helianthate(self, n=n, m=m)
        return dataclasses.replace(self, collections=collections)

    def join(self) -> "CollectionList":
        """
        Joins collections.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ... ])

            >>> collections.join()
            CollectionList([<5, 12, 14, 18, 17, 16, 17, 19>])

        """
        collections = []
        if self:
            collection = self[0]
            for collection_ in self[1:]:
                collection = collection + collection_
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def partition(
        self, argument, cyclic=False, join=False, overhang=False
    ) -> typing.Union["CollectionList", "PitchSegment", list]:
        """
        Partitions collections according to ``argument``.

        ..  container:: example

            Returns sequence:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     [16, 17, 19],
            ... ])

            >>> sequence = collections.partition([1, 2], overhang=abjad.Exact)
            >>> for collection_list in sequence:
            ...     collection_list
            ...
            CollectionList([<5, 12, 14, 18, 17>])
            CollectionList([<16, 17, 19>, <16, 17, 19>])

        ..  container:: example

            Joins parts. Returns new collection list:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     [16, 17, 19],
            ... ])

            >>> collections
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <16, 17, 19>])

            >>> collections.partition([1, 2], join=True, overhang=abjad.Exact)
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19, 16, 17, 19>])

        ..  container:: example

            Repeats, partitions, joins parts. Returns new collection list:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     [16, 17, 19],
            ... ])

            >>> collections = collections.repeat(2)
            >>> for collection in collections.partition(
            ...     [2],
            ...     cyclic=True,
            ...     join=True,
            ...     ):
            ...     collection
            ...
            PitchSegment(items=[5, 12, 14, 18, 17, 16, 17, 19], item_class=NumberedPitch)
            PitchSegment(items=[16, 17, 19, 5, 12, 14, 18, 17], item_class=NumberedPitch)
            PitchSegment(items=[16, 17, 19, 16, 17, 19], item_class=NumberedPitch)

        """
        if isinstance(argument, abjad.Ratio):
            raise NotImplementedError("implement ratio-partition at some point.")
        sequence = list(self)
        parts = abjad.sequence.partition_by_counts(
            sequence, argument, cyclic=cyclic, overhang=overhang
        )
        collection_lists = [dataclasses.replace(self, collections=_) for _ in parts]
        if join:
            collections = [_.join()[0] for _ in collection_lists]
            result = dataclasses.replace(self, collections=collections)
        else:
            result = collection_lists[:]
        return result

    def read(self, counts=None, check=None) -> "CollectionList":
        """
        Reads collections by ``counts``.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ... ])

            >>> for collection in collections.read([3, 3, 3, 5, 5, 5]):
            ...     collection
            ...
            PitchSegment(items=[5, 12, 14], item_class=NumberedPitch)
            PitchSegment(items=[18, 17, 16], item_class=NumberedPitch)
            PitchSegment(items=[17, 19, 5], item_class=NumberedPitch)
            PitchSegment(items=[12, 14, 18, 17, 16], item_class=NumberedPitch)
            PitchSegment(items=[17, 19, 5, 12, 14], item_class=NumberedPitch)
            PitchSegment(items=[18, 17, 16, 17, 19], item_class=NumberedPitch)

        ..  container:: example exception

            Raises exception on inexact read:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ... ])

            >>> len(collections.flatten())
            8

            >>> collections.read([10, 10, 10], check=abjad.Exact)
            Traceback (most recent call last):
                ...
            ValueError: call reads 30 items; not a multiple of 8 items.

        """
        if counts in (None, []):
            return dataclasses.replace(self)
        counts = list(counts)
        assert all(isinstance(_, int) for _ in counts), repr(counts)
        collection = self.join()[0]
        source = abjad.CyclicTuple(collection)
        i = 0
        collections = []
        for count in counts:
            stop = i + count
            items = source[i:stop]
            collection = self._initialize_collection(items)
            collections.append(collection)
            i += count
        result = dataclasses.replace(self, collections=collections)
        if check == abjad.Exact:
            self_item_count = len(self.flatten())
            result_item_count = len(result.flatten())
            quotient = result_item_count / self_item_count
            if quotient != int(quotient):
                message = f"call reads {result_item_count} items;"
                message += f" not a multiple of {self_item_count} items."
                raise ValueError(message)
        return result

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def remove(self, indices=None, period=None) -> "CollectionList":
        """
        Removes collections at ``indices``.

        ..  container:: example

            >>> collections = baca.CollectionList([[0, 1], [2, 3], [4], [5, 6]])
            >>> collections.remove([0, -1])
            CollectionList([<2, 3>, <4>])

        """
        sequence = list(self)
        collections = abjad.sequence.remove(sequence, indices=indices, period=period)
        return dataclasses.replace(self, collections=collections)

    def remove_duplicate_pitch_classes(self, level=-1) -> "CollectionList":
        """
        Removes duplicate pitch-classes at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5, 7], [16, 17, 16, 18]])

            >>> collections.remove_duplicate_pitch_classes(level=1)
            CollectionList([<4, 5, 7>, <16, 17, 18>])

            >>> collections.remove_duplicate_pitch_classes(level=-1)
            CollectionList([<4, 5, 7>, <18>])

        Set ``level`` to 1 or -1.
        """
        pitch_class_class = self._get_pitch_class_class()
        collections_ = []
        if level == 1:
            for collection in self:
                items: typing.List[CollectionTyping] = []
                known_pitch_classes: typing.List[CollectionTyping] = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            known_pitch_classes = []
            for collection in self:
                items = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items, collection)
                    collections_.append(collection_)
        else:
            raise ValueError(f"level must be 1 or -1: {level!r}.")
        return dataclasses.replace(self, collections=collections_)

    def remove_duplicates(self, level=-1) -> "CollectionList":
        """
        Removes duplicates at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[16, 17, 16], [13, 14, 16], [16, 17, 16]],
            ... )

            >>> collections.remove_duplicates(level=0)
            CollectionList([<16, 17, 16>, <13, 14, 16>])

            >>> collections.remove_duplicates(level=1)
            CollectionList([<16, 17>, <13, 14, 16>, <16, 17>])

            >>> collections.remove_duplicates(level=-1)
            CollectionList([<16, 17>, <13, 14>])

        Set ``level`` to 0, 1 or -1.
        """
        collections_: typing.List[CollectionTyping] = []
        if level == 0:
            collections_ = []
            known_items: typing.List[CollectionTyping] = []
            # collections_, known_items = [], []
            for collection in self:
                if collection in known_items:
                    continue
                known_items.append(collection)
                collections_.append(collection)
        elif level == 1:
            for collection in self:
                items, known_items = [], []
                for item in collection:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            known_items = []
            for collection in self:
                items = []
                for item in collection:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
        return dataclasses.replace(self, collections=collections_)

    def remove_repeat_pitch_classes(self, level=-1) -> "CollectionList":
        """
        Removes repeat pitch-classes at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 4, 4, 5], [17, 18]])

            >>> collections.remove_repeat_pitch_classes(level=1)
            CollectionList([<4, 5>, <17, 18>])

            >>> collections.remove_repeat_pitch_classes(level=-1)
            CollectionList([<4, 5>, <18>])

        Set ``level`` to 1 or -1.
        """
        pitch_class_class = self._get_pitch_class_class()
        collections_ = []
        if level == 1:
            for collection in self:
                items, previous_pitch_class = [], None
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            previous_pitch_class = None
            for collection in self:
                items = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            raise ValueError(f"level must be 1 or -1: {level!r}.")
        return dataclasses.replace(self, collections=collections_)

    def remove_repeats(self, level=-1) -> "CollectionList":
        """
        Removes repeats at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5], [4, 5], [5, 7, 7]])

            >>> collections.remove_repeats(level=0)
            CollectionList([<4, 5>, <5, 7, 7>])

            >>> collections.remove_repeats(level=1)
            CollectionList([<4, 5>, <4, 5>, <5, 7>])

            >>> collections.remove_repeats(level=-1)
            CollectionList([<4, 5>, <4, 5>, <7>])

        Set ``level`` to 0, 1 or -1.
        """
        collections_ = []
        if level == 0:
            previous_collection = None
            for collection in self:
                if collection == previous_collection:
                    continue
                collections_.append(collection)
                previous_collection = collection
        elif level == 1:
            for collection in self:
                items, previous_item = [], None
                for item in collection:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            previous_item = None
            for collection in self:
                items = []
                for item in collection:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            raise ValueError(f"level must be 0, 1 or -1: {level!r}.")
        return dataclasses.replace(self, collections=collections_)

    def repeat(self, n=1) -> "CollectionList":
        """
        Repeats collections.

        ..  container:: example

            >>> collections = baca.CollectionList([[12, 14, 18, 17], [16, 19]])
            >>> for collection in collections.repeat(n=3):
            ...     collection
            ...
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSegment(items=[16, 19], item_class=NumberedPitch)
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSegment(items=[16, 19], item_class=NumberedPitch)
            PitchSegment(items=[12, 14, 18, 17], item_class=NumberedPitch)
            PitchSegment(items=[16, 19], item_class=NumberedPitch)

        """
        collections = list(self)
        collections = abjad.sequence.repeat(collections, n=n)
        collections = abjad.sequence.flatten(collections, depth=1)
        return dataclasses.replace(self, collections=collections)

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def retain(self, indices=None, period=None) -> "CollectionList":
        """
        Retains collections at ``indices``.

        ..  container:: example

            >>> collections = baca.CollectionList([[0, 1], [2, 3], [4], [5, 6]])
            >>> collections.retain([0, -1])
            CollectionList([<0, 1>, <5, 6>])

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[0, 1], [2, 3], [4], [5, 6], [7], [8]],
            ... )
            >>> collections.retain([0], period=2)
            CollectionList([<0, 1>, <4>, <7>])

        """
        sequence = list(self)
        collections = abjad.sequence.retain(sequence, indices=indices, period=period)
        return dataclasses.replace(self, collections=collections)

    def soprano_to_octave(self, n=4, pattern=None) -> "CollectionList":
        """
        Octave-transposes collections to soprano in octave ``n``.

        ..  container:: example

            Octave-transposes all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.soprano_to_octave(n=4)
            CollectionList([<-19, -12, -10, -6, 5>, <4, 5, 7>, <-33, -22, -11, 0>])

        ..  container:: example

            Octave-transposes collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ... )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.soprano_to_octave(n=4, pattern=[-1])
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-33, -22, -11, 0>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.soprano_to_octave(n=n)
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def space_down(
        self, bass=None, pattern=None, semitones=None, soprano=None
    ) -> "CollectionList":
        """
        Spaces collections down.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ... )

            >>> collections.space_down(bass=5)
            CollectionList([<24, 18, 14, 5>, <16, 7, 5>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.space_down(
                    bass=bass, semitones=semitones, soprano=soprano
                )
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def space_up(self, bass=None, pattern=None, semitones=None, soprano=None):
        """
        Spaces collections up.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ... )

            >>> collections.space_up(bass=5)
            CollectionList([<5, 6, 12, 14>, <5, 7, 16>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.space_up(
                    bass=bass, semitones=semitones, soprano=soprano
                )
            collections.append(collection)
        return dataclasses.replace(self, collections=collections)

    def to_named_pitch_classes(self) -> "CollectionList":
        """
        Changes to named pitch-class collections.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> collections.to_named_pitch_classes()
            CollectionList([PC<c d fs f>, PC<e af g>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NumberedPitchClass,
            ... )

            >>> collections.to_named_pitch_classes()
            CollectionList([PC<c d fs f>, PC<e af g>])

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NamedPitch,
            ... )

            >>> collections.to_named_pitch_classes()
            CollectionList([PC<c d fs f>, PC<e af g>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NamedPitchClass,
            ... )

            >>> collections.to_named_pitch_classes()
            CollectionList([PC<c d fs f>, PC<e af g>])

        """
        collections = [_.to_named_pitch_classes() for _ in self]
        return CollectionList(collections, item_class=abjad.NamedPitchClass)

    def to_named_pitches(self) -> "CollectionList":
        """
        Changes to named pitch collections.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> collections.to_named_pitches()
            CollectionList([<c'' d'' fs'' f''>, <e'' af'' g''>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NumberedPitchClass,
            ... )

            >>> collections.to_named_pitches()
            CollectionList([<c' d' fs' f'>, <e' af' g'>])

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NamedPitch,
            ... )

            >>> collections.to_named_pitches()
            CollectionList([<c'' d'' fs'' f''>, <e'' af'' g''>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NamedPitchClass,
            ... )

            >>> collections.to_named_pitches()
            CollectionList([<c' d' fs' f'>, <e' af' g'>])

        """
        collections = [_.to_named_pitches() for _ in self]
        return CollectionList(collections=collections, item_class=abjad.NamedPitch)

    def to_numbered_pitch_classes(self) -> "CollectionList":
        """
        Changes to numbered pitch-class collections.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> collections.to_numbered_pitch_classes()
            CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NumberedPitchClass,
            ... )

            >>> collections.to_numbered_pitch_classes()
            CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NamedPitch,
            ... )

            >>> collections.to_numbered_pitch_classes()
            CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NamedPitchClass,
            ... )

            >>> collections.to_numbered_pitch_classes()
            CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

        """
        collections = [_.to_numbered_pitch_classes() for _ in self]
        return CollectionList(collections, item_class=abjad.NumberedPitchClass)

    def to_numbered_pitches(self) -> "CollectionList":
        """
        Changes to numbered pitch collections.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NumberedPitch,
            ... )

            >>> collections.to_numbered_pitches()
            CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NumberedPitchClass,
            ... )

            >>> collections.to_numbered_pitches()
            CollectionList([<0, 2, 6, 5>, <4, 8, 7>])

            >>> collections = baca.CollectionList(
            ...     [[12, 14, 18, 17], [16, 20, 19]],
            ...     item_class=abjad.NamedPitch,
            ... )

            >>> collections.to_numbered_pitches()
            CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NamedPitchClass,
            ... )

            >>> collections.to_numbered_pitches()
            CollectionList([<0, 2, 6, 5>, <4, 8, 7>])

        """
        collections = [_.to_numbered_pitches() for _ in self]
        return CollectionList(collections=collections, item_class=abjad.NumberedPitch)

    def transpose(self, n=0) -> "CollectionList":
        """
        Transposes collections.

        ..  container:: example

            To numbered pitch collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NumberedPitch,
                ... )

                >>> collections.transpose(28)
                CollectionList([<40, 42, 46, 45>, <44, 48, 47>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ... )

                >>> collections.transpose(28)
                CollectionList([PC<4, 6, 10, 9>, PC<8, 0, 11>])

        ..  container:: example

            To named pitch collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NamedPitch,
                ... )

                >>> collections.transpose(-28)
                CollectionList([<af, bf, d df>, <c ff ef>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NamedPitchClass,
                ... )

                >>> collections.transpose(-28)
                CollectionList([PC<af bf d df>, PC<c ff ef>])

        """
        collections_ = []
        for collection in self:
            collection_ = collection.transpose(n)
            collections_.append(collection_)
        return dataclasses.replace(self, collections=collections_)


def illustrate_collection_list(
    collection_list,
    *,
    cell_indices=False,
    set_classes=False,
) -> abjad.LilyPondFile:
    r"""
    Illustrates collection list.

    ..  container:: example

        >>> collections = baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     [16, 20, 19],
        ... ])

        >>> lilypond_file = baca.pcollections.illustrate_collection_list(collections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = 4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = 2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \context Staff = "Staff"
                {
                    \context Voice = "Voice"
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        c''8
                        \startGroup
                        d''8
                        fs''8
                        f''8
                        \stopGroup
                        s8
                        e''8
                        \startGroup
                        af''8
                        g''8
                        \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
        >>> collections = baca.CollectionList(items)
        >>> lilypond_file = baca.pcollections.illustrate_collection_list(collections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = 4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = 2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \context Staff = "Staff"
                {
                    \context Voice = "Voice"
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e'8
                        \startGroup
                        fs'8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        With segment indices and set-classes:

        >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
        >>> collections = baca.CollectionList(items)
        >>> lilypond_file = baca.pcollections.illustrate_collection_list(
        ...     collections,
        ...     cell_indices=abjad.Down,
        ...     set_classes=True,
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = 4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = 2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \context Staff = "Staff"
                {
                    \context Voice = "Voice"
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e'8
                        ^ \markup \small \line { "SC(3-9){0, 2, 6}" }
                        - \tweak staff-padding 7
                        _ \markup 0
                        \startGroup
                        fs'8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        ^ \markup \small \line { "SC(5-6){0, 1, 2, 4, 6}" }
                        - \tweak staff-padding 7
                        _ \markup 1
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        ^ \markup \small \line { "SC(4-19){0, 2, 3, 5}" }
                        - \tweak staff-padding 7
                        _ \markup 2
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    """
    assert cell_indices in (True, False, abjad.Up, abjad.Down), repr(cell_indices)
    voice = abjad.Voice(name="Voice")
    voice.consists_commands.append("Horizontal_bracket_engraver")
    staff = abjad.Staff([voice], name="Staff")
    score = abjad.Score([staff], name="Score")
    for i, segment in enumerate(collection_list):
        notes = [abjad.Note(_.number, (1, 8)) for _ in segment]
        abjad.horizontal_bracket(notes)
        if cell_indices:
            if cell_indices is True:
                direction = abjad.Up
            else:
                direction = cell_indices
            cell_index = i
            markup = abjad.Markup(rf"\markup {cell_index}", direction=direction)
            if direction == abjad.Down:
                abjad.tweak(markup).staff_padding = 7
            abjad.attach(markup, notes[0])
        if set_classes:
            pitches = abjad.iterate.pitches(notes)
            pitch_class_set = abjad.PitchClassSet.from_pitches(pitches)
            if pitch_class_set:
                set_class = abjad.SetClass.from_pitch_class_set(
                    pitch_class_set, lex_rank=True, transposition_only=True
                )
                string = rf'\markup \small \line {{ "{set_class}" }}'
                label = abjad.Markup(string, direction=abjad.Up)
                if label is not None:
                    abjad.attach(label, notes[0])
        voice.extend(notes)
        voice.append("s8")
    leaf = abjad.get.leaf(voice, 0)
    time_signature = abjad.TimeSignature((1, 8))
    abjad.attach(time_signature, leaf)
    leaf = abjad.select.leaf(score, -1)
    bar_line = abjad.BarLine("|.")
    abjad.attach(bar_line, leaf)
    abjad.override(score).BarLine.transparent = True
    abjad.override(score).BarNumber.stencil = False
    abjad.override(score).Beam.stencil = False
    abjad.override(score).Flag.stencil = False
    abjad.override(score).HorizontalBracket.staff_padding = 4
    abjad.override(score).Stem.stencil = False
    abjad.override(score).TextScript.staff_padding = 2
    abjad.override(score).TimeSignature.stencil = False
    final_leaf = abjad.get.leaf(score, -1)
    string = r"\override Score.BarLine.transparent = ##f"
    literal = abjad.LilyPondLiteral(string, "after")
    abjad.attach(literal, final_leaf)
    abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 16)"
    preamble = "#(set-global-staff-size 16)\n"
    lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', preamble, score])
    abjad.override(score).SpacingSpanner.strict_grace_spacing = True
    abjad.override(score).SpacingSpanner.strict_note_spacing = True
    abjad.override(score).SpacingSpanner.uniform_stretching = True
    abjad.override(score).TextScript.X_extent = False
    return lilypond_file


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

    ### CLASS VARIABLES ###

    __slots__ = ("_fundamental",)

    ### INITIALIZER ###

    def __init__(self, fundamental: typing.Union[str, abjad.NamedPitch] = "C1") -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental

    ### PUBLIC PROPERTIES ###

    @property
    def fundamental(self) -> abjad.NamedPitch:
        """
        Gets fundamental.

        ..  container:: example

            >>> baca.HarmonicSeries("C2").fundamental
            NamedPitch('c,')

        """
        return self._fundamental

    ### PUBLIC METHODS ###

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
            markup = abjad.Markup(rf"\markup +{deviation}", direction=abjad.Up)
            abjad.attach(markup, note)
        elif deviation < 0:
            markup = abjad.Markup(rf"\markup {deviation}", direction=abjad.Up)
            abjad.attach(markup, note)
        markup = abjad.Markup(rf"\markup {n}", direction=abjad.Down)
        abjad.attach(markup, note)
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


@dataclasses.dataclass(slots=True)
class Partial:
    """
    Partial.

    ..  container:: example

        >>> baca.Partial("C1", 7)
        Partial(fundamental=NamedPitch('c,,'), number=7)

    """

    fundamental: typing.Union[str, abjad.NamedPitch] = "C1"
    number: int = 1

    def __post_init__(self):
        self.fundamental = abjad.NamedPitch(self.fundamental)
        assert isinstance(self.number, int), repr(self.number)
        assert 1 <= self.number, repr(self.number)

    def approximation(self) -> abjad.NamedPitch:
        """
        Gets approximation.

        ..  container:: example

            >>> baca.Partial("C1", 7).approximation()
            NamedPitch('bf')

        """
        hertz = self.number * self.fundamental.hertz
        return abjad.NamedPitch.from_hertz(hertz)

    def deviation(self) -> int:
        """
        Gets deviation in cents.

        ..  container:: example

            >>> baca.Partial("C1", 7).deviation()
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


class PitchClassSegment(abjad.PitchClassSegment):
    r"""
    Pitch-class segment.

    ..  container:: example

        Initializes segment:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.PitchClassSegment(items=items)
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when segment equals ``argument``.

        ..  container:: example

            Works with Abjad pitch-class segments:

            >>> segment_1 = abjad.PitchClassSegment([0, 1, 2, 3])
            >>> segment_2 = baca.PitchClassSegment([0, 1, 2, 3])

            >>> segment_1 == segment_2
            True

            >>> segment_2 == segment_1
            True

        """
        if not issubclass(type(argument), type(self)) and not issubclass(
            type(self), type(argument)
        ):
            return False
        return self.items == argument.items

    ### PUBLIC METHODS ###

    def alpha(self):
        r"""
        Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = baca.PitchClassSegment(items=items)

            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ..  container:: example

                >>> J.alpha()
                PitchClassSegment(items=[11, 11.5, 7, 6, 11.5, 6], item_class=NumberedPitchClass)

                >>> segment = J.alpha()
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

            ..  container:: example

                >>> J.alpha().alpha()
                PitchClassSegment(items=[10, 10.5, 6, 7, 10.5, 7], item_class=NumberedPitchClass)

                >>> segment = J.alpha().alpha()
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

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, baca.PitchClassSegment)
            True

        """
        numbers = []
        for pc in self:
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
        return type(self)(items=numbers)

    def arpeggiate_down(self):
        r"""
        Arpeggiates pitch-class segment down.

        ..  container:: example

            >>> segment = baca.PitchClassSegment([6, 0, 4, 5, 8])

            >>> segment.arpeggiate_down()
            PitchSegment(items=[42, 36, 28, 17, 8], item_class=NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment.arpeggiate_down())
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        fs''''1 * 1/8
                        c''''1 * 1/8
                        e'''1 * 1/8
                        f''1 * 1/8
                        af'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns pitch segment.
        """
        specifier = ArpeggiationSpacingSpecifier(direction=abjad.Down)
        result = specifier([self])
        assert len(result) == 1
        segment = result[0]
        assert isinstance(segment, PitchSegment), repr(segment)
        return segment

    def arpeggiate_up(self):
        r"""
        Arpeggiates pitch-class segment up.

        ..  container:: example

            >>> segment = baca.PitchClassSegment([6, 0, 4, 5, 8])

            >>> segment.arpeggiate_up()
            PitchSegment(items=[6, 12, 16, 17, 20], item_class=NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment.arpeggiate_up())
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff_group = lilypond_file["Piano_Staff"]
                >>> string = abjad.lilypond(staff_group)
                >>> print(string)
                \context PianoStaff = "Piano_Staff"
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        fs'1 * 1/8
                        c''1 * 1/8
                        e''1 * 1/8
                        f''1 * 1/8
                        af''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns pitch segment.
        """
        specifier = ArpeggiationSpacingSpecifier(direction=abjad.Up)
        result = specifier([self])
        assert len(result) == 1
        segment = result[0]
        assert isinstance(segment, PitchSegment), repr(segment)
        return segment

    def chord(self):
        r"""
        Changes segment to set.

        ..  container:: example

            >>> segment = baca.PitchClassSegment([-2, -1.5, 6, 7])

            >>> segment.chord()
            PitchClassSet(items=[6, 7, 10, 10.5], item_class=abjad.NumberedPitchClass)

            >>> lilypond_file = abjad.illustrate(segment.chord())
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file["Voice"]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \context Voice = "Voice"
                {
                    <fs' g' bf' bqf'>1
                }

        Returns pitch-class set.
        """
        return abjad.PitchClassSet(items=self, item_class=self.item_class)

    def get_matching_transforms(
        self,
        segment_2,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        transposition=False,
    ):
        r"""
        Gets transforms of segment that match ``segment_2``.

        ..  container:: example

            Example segments:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment_1 = baca.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment_1)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> items = [9, 2, 1, 6, 2, 6]
            >>> segment_2 = baca.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(segment_2)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  container:: example

            Gets matching transforms:

            >>> transforms = segment_1.get_matching_transforms(
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

            >>> transforms = segment_2.get_matching_transforms(
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

            >>> segment_2 = baca.PitchClassSegment(items=[0, 1, 2])
            >>> segment_2.get_matching_transforms(
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
        if not len(self) == len(segment_2):
            return result
        transforms = self.get_transforms(
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
        self,
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
            >>> J = baca.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(J)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> pairs = J.get_transforms(
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
            for n in range(len(self)):
                lists_.extend([f"r{n}"] + _[:] for _ in lists)
            lists = lists_
        pairs = []
        for list_ in lists:
            transform = self
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

    def has_duplicates(self):
        r"""
        Is true when pitch-class segment has duplicates.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7]
            >>> segment = baca.PitchClassSegment(items=items)
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

            >>> segment.has_duplicates()
            False

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.PitchClassSegment(items=items)
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

            >>> segment.has_duplicates()
            True

        Returns true or false.
        """
        return not len(set(self)) == len(self)

    def has_repeats(self):
        r"""
        Is true when pitch-class segment has repeats.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.PitchClassSegment(items=items)
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

            >>> segment.has_repeats()
            False

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, 7]
            >>> segment = baca.PitchClassSegment(items=items)
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

            >>> segment.has_repeats()
            True

        Returns true or false.
        """
        previous_item = None
        for item in self:
            if item == previous_item:
                return True
            previous_item = item
        return False

    def sequence(self):
        r"""
        Changes pitch-class segment into a sequence.

        ..  container:: example

            >>> segment = baca.PitchClassSegment([10, 11, 5, 6, 7])
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

            >>> segment.sequence()
            [NumberedPitchClass(10), NumberedPitchClass(11), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)]

        Returns sequence.
        """
        return list(self)

    def space_down(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces segment down.

        ..  container:: example

            >>> segment = baca.PitchClassSegment([10, 11, 5, 6, 7])
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

            >>> segment.space_down(bass=6, soprano=7)
            PitchSegment(items=[19, 17, 11, 10, 6], item_class=NumberedPitch)

            >>> segment = segment.space_down(bass=6, soprano=7)
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
                            \clef "treble"
                            g''1 * 1/8
                            f''1 * 1/8
                            b'1 * 1/8
                            bf'1 * 1/8
                            fs'1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
        )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        if not isinstance(segment, PitchSegment):
            raise TypeError(f"pitch segment only: {segment!r}.")
        return segment

    def space_up(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces segment up.

        ..  container:: example

            >>> segment = baca.PitchClassSegment([10, 11, 5, 6, 7])
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

            >>> segment.space_up(bass=6, soprano=7)
            PitchSegment(items=[6, 10, 11, 17, 19], item_class=NumberedPitch)

            >>> segment = segment.space_up(bass=6, soprano=7)
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
                            \clef "treble"
                            fs'1 * 1/8
                            bf'1 * 1/8
                            b'1 * 1/8
                            f''1 * 1/8
                            g''1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
        )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        assert isinstance(segment, PitchSegment)
        return segment


@dataclasses.dataclass
class PitchSegment(abjad.PitchSegment):
    r"""
    Pitch segment.

    ..  container:: example

        Initializes segment:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.PitchSegment(items=items)
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

    """

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        if self.item_class is abjad.NamedPitch:
            contents = " ".join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ", ".join([str(_) for _ in self])
            contents = "[" + contents + "]"
        return f"{type(self).__name__}(items={contents}, item_class={self.item_class.__name__})"

    def _to_selection(self):
        maker = abjad.NoteMaker()
        return maker(self, [(1, 4)])

    ### PUBLIC METHODS ###

    def bass_to_octave(self, n=4):
        r"""
        Octave-transposes segment to bass in octave ``n``.

        ..  container:: example

            >>> segment = baca.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.bass_to_octave(n=4)
            PitchSegment(items=[10, 10.5, 18, 19, 10.5, 19], item_class=NumberedPitch)

            >>> segment = segment.bass_to_octave(n=4)
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
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs''1 * 1/8
                        g''1 * 1/8
                        bqf'1 * 1/8
                        g''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        from .commandclasses import RegisterToOctaveCommand

        # TODO: remove reference to RegisterToOctaveCommand;
        #       implement as segment-only operation
        command = RegisterToOctaveCommand(anchor=abjad.Down, octave_number=n)
        selection = self._to_selection()
        command([selection])
        pitches = abjad.iterate.pitches(selection)
        segment = PitchSegment.from_pitches(pitches)
        return dataclasses.replace(self, items=segment)

    def center_to_octave(self, n=4):
        r"""
        Octave-transposes segment to center in octave ``n``.

        ..  container:: example

            >>> segment = baca.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.center_to_octave(n=3)
            PitchSegment(items=[-14, -13.5, -6, -5, -13.5, -5], item_class=NumberedPitch)

            >>> segment = segment.center_to_octave(n=3)
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns new segment.
        """
        from .commandclasses import RegisterToOctaveCommand

        # TODO: remove reference to RegisterToOctaveCommand;
        #       implement as segment-only operation
        command = RegisterToOctaveCommand(anchor=abjad.Center, octave_number=n)
        selection = self._to_selection()
        command([selection])
        pitches = abjad.iterate.pitches(selection)
        segment = PitchSegment.from_pitches(pitches)
        return dataclasses.replace(self, items=segment)

    def chord(self):
        r"""
        Changes segment to set.

        ..  container:: example

            >>> segment = baca.PitchSegment([-2, -1.5, 6, 7])

            >>> segment.chord()
            PitchSet(items=[-2, -1.5, 6, 7], item_class=abjad.NumberedPitch)

            >>> lilypond_file = abjad.illustrate(segment.chord())
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
                            <fs' g'>1
                        }
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \context Voice = "Bass_Voice"
                        {
                            <bf bqf>1
                        }
                    }
                >>

        Returns pitch set.
        """
        return PitchSet(items=self, item_class=self.item_class)

    def soprano_to_octave(self, n=4):
        r"""
        Octave-transposes segment to soprano in octave ``n``.

        ..  container:: example

            >>> segment = baca.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.soprano_to_octave(n=3)
            PitchSegment(items=[-14, -13.5, -6, -5, -13.5, -5], item_class=NumberedPitch)

            >>> segment = segment.soprano_to_octave(n=3)
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns new segment.
        """
        from .commandclasses import RegisterToOctaveCommand

        # TODO: remove reference to RegisterToOctaveCommand;
        #       implement as segment-only operation
        command = RegisterToOctaveCommand(anchor=abjad.Up, octave_number=n)
        selection = self._to_selection()
        command([selection])
        pitches = abjad.iterate.pitches(selection)
        segment = PitchSegment.from_pitches(pitches)
        return dataclasses.replace(self, items=segment)

    def space_down(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces pitch segment down.

        ..  container:: example

            >>> segment = baca.PitchSegment([12, 14, 21, 22])
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
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_down(bass=0)
            PitchSegment(items=[14, 10, 9, 0], item_class=NumberedPitch)

            >>> segment = segment.space_down(bass=0)
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
                        \clef "treble"
                        d''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        c'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> segment = baca.PitchSegment([12, 14, 21, 22])
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
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_down(bass=2)
            PitchSegment(items=[12, 10, 9, 2], item_class=NumberedPitch)

            >>> segment = segment.space_down(bass=2)
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
                        \clef "treble"
                        c''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        d'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
        )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def space_up(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces pitch segment up.

        ..  container:: example

            >>> segment = baca.PitchSegment([12, 14, 21, 22])
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
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_up(bass=0)
            PitchSegment(items=[0, 2, 9, 10], item_class=NumberedPitch)

            >>> segment = segment.space_up(bass=0)
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
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> segment = baca.PitchSegment([12, 14, 21, 22])
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
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_up(bass=2)
            PitchSegment(items=[2, 9, 10, 12], item_class=NumberedPitch)

            >>> segment = segment.space_up(bass=2)
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
                        \clef "treble"
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                        c''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
        )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def split(self, pitch=0):
        r"""
        Splits segment at ``pitch``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.PitchSegment(items=items)
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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> upper, lower = segment.split(pitch=0)

            >>> upper
            PitchSegment(items=[6, 7, 7], item_class=NumberedPitch)

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
                        \clef "treble"
                        fs'1 * 1/8
                        g'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> lower
            PitchSegment(items=[-2, -1.5, -1.5], item_class=NumberedPitch)

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
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        Returns upper, lower segments.
        """
        upper, lower = [], []
        for pitch_ in self:
            if pitch_ < pitch:
                lower.append(pitch_)
            else:
                upper.append(pitch_)
        upper = dataclasses.replace(self, items=upper)
        lower = dataclasses.replace(self, items=lower)
        return upper, lower


class PitchSet(abjad.PitchSet):
    r"""
    Pitch set.

    ..  container:: example

        Initializes set:

        ..  container:: example

            >>> setting = baca.PitchSet([-2, -1.5, 6, 7, -1.5, 7])
            >>> lilypond_file = abjad.illustrate(setting)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context PianoStaff = "Piano_Staff"
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \context Voice = "Treble_Voice"
                            {
                                <fs' g'>1
                            }
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \context Voice = "Bass_Voice"
                            {
                                <bf bqf>1
                            }
                        }
                    >>
                >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when segment equals ``argument``.

        ..  container:: example

            Works with Abjad pitch sets:

            >>> set_1 = abjad.PitchSet([0, 1, 2, 3])
            >>> set_2 = baca.PitchSet([0, 1, 2, 3])

            >>> set_1 == set_2
            True

            >>> set_2 == set_1
            True

        """
        if not issubclass(type(argument), type(self)) and not issubclass(
            type(self), type(argument)
        ):
            return False
        return self.items == argument.items

    ### PUBLIC METHODS ###

    def space_down(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces pitch set down.

        ..  container:: example

            >>> setting = baca.PitchSet([12, 14, 21, 22])
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

            >>> setting.space_down(bass=0)
            PitchSet(items=[0, 9, 10, 14], item_class=abjad.NumberedPitch)

            >>> setting = setting.space_down(bass=0)
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

            >>> setting = baca.PitchSet([12, 14, 21, 22])
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

            >>> setting.space_down(bass=2)
            PitchSet(items=[2, 9, 10, 12], item_class=abjad.NumberedPitch)

            >>> setting = setting.space_down(bass=2)
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

        Returns new pitch set.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
        )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def space_up(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces pitch set up.

        ..  container:: example

            >>> setting = baca.PitchSet([12, 14, 21, 22])
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

            >>> setting.space_up(bass=0)
            PitchSet(items=[0, 2, 9, 10], item_class=abjad.NumberedPitch)

            >>> setting = setting.space_up(bass=0)
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

            >>> setting = baca.PitchSet([12, 14, 21, 22])
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

            >>> setting.space_up(bass=2)
            PitchSet(items=[2, 9, 10, 12], item_class=abjad.NumberedPitch)

            >>> setting = setting.space_up(bass=2)
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

        Returns new pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
        )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment


CollectionTyping = typing.Union[PitchSet, PitchSegment]


@dataclasses.dataclass(slots=True)
class Registration:
    """
    Registration.

    ..  container:: example

        Registration in two parts:

        >>> components = [("[A0, C4)", 15), ("[C4, C8)", 27)]
        >>> registration = baca.Registration(components)

        >>> registration
        Registration(components=[RegistrationComponent(source_pitch_range=PitchRange(range_string='[A0, C4)'), target_octave_start_pitch=NumberedPitch(15)), RegistrationComponent(source_pitch_range=PitchRange(range_string='[C4, C8)'), target_octave_start_pitch=NumberedPitch(27))])

    """

    components: typing.Any = None

    def __post_init__(self):
        components_ = []
        for component in self.components or []:
            if isinstance(component, RegistrationComponent):
                components_.append(component)
            else:
                component_ = RegistrationComponent(*component)
                components_.append(component_)
        self.components = components_ or None

    def __call__(self, pitches):
        r"""
        Calls registration on ``pitches``.

        ..  container:: example

            Transposes four pitches:

            >>> components = [("[A0, C4)", 15), ("[C4, C8)", 27)]
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

            >>> components = [("[A0, C4)", 15), ("[C4, C8)", 27)]
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

            >>> components = [("[A0, C4)", 15), ("[C4, C8)", 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0.5, 2.5, 1.5, 3.5])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("cqs''''")
            NamedPitch("dqs''''")
            NamedPitch("dqf''''")
            NamedPitch("eqf'''")

        Returns list of new pitches.
        """
        return [self._transpose_pitch(_) for _ in pitches]

    def _transpose_pitch(self, pitch):
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


@dataclasses.dataclass(slots=True)
class RegistrationComponent:
    """
    Registration component.

    ..  container:: example

        Initializes a registration component that specifies that all pitches from A0 up
        to and including C8 should be transposed to the octave starting at Eb5 (numbered
        pitch 15):

        >>> component = baca.RegistrationComponent("[A0, C8]", 15)
        >>> component
        RegistrationComponent(source_pitch_range=PitchRange(range_string='[A0, C8]'), target_octave_start_pitch=NumberedPitch(15))

    """

    source_pitch_range: typing.Any = "[A0, C8]"
    target_octave_start_pitch: typing.Any = 0

    def __post_init__(self):
        if isinstance(self.source_pitch_range, abjad.PitchRange):
            self.source_pitch_range = copy.copy(self.source_pitch_range)
        else:
            self.source_pitch_range = abjad.PitchRange(self.source_pitch_range)
        self.target_octave_start_pitch = abjad.NumberedPitch(
            self.target_octave_start_pitch
        )


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
