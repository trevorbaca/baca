"""
Imbricate.
"""

import copy

import abjad

from . import select as _select
from .enums import enums as _enums


def _matches_pitch(pitched_leaf, pitch_object):
    if pitch_object is None:
        return False
    if pitch_object == []:
        return False
    if isinstance(pitched_leaf, abjad.Note):
        written_pitches = [pitched_leaf.written_pitch()]
    elif isinstance(pitched_leaf, abjad.Chord):
        written_pitches = pitched_leaf.written_pitches()
    else:
        raise TypeError(pitched_leaf)
    if isinstance(pitch_object, int | float):
        source = [_.number() for _ in written_pitches]
    elif isinstance(pitch_object, abjad.NamedPitch):
        source = written_pitches
    elif isinstance(pitch_object, abjad.NumberedPitch):
        source = [abjad.NumberedPitch(_) for _ in written_pitches]
    elif isinstance(pitch_object, abjad.NamedPitchClass):
        source = [abjad.NamedPitchClass(_) for _ in written_pitches]
    elif isinstance(pitch_object, abjad.NumberedPitchClass):
        source = [abjad.NumberedPitchClass(_) for _ in written_pitches]
    else:
        raise TypeError(f"unknown pitch object: {pitch_object!r}.")
    if not type(source[0]) is type(pitch_object):
        raise TypeError(f"{source!r} type must match {pitch_object!r}.")
    return pitch_object in source


def _trim_matching_chord(logical_tie, pitch_object):
    if isinstance(logical_tie.head(), abjad.Note):
        return
    assert isinstance(logical_tie.head(), abjad.Chord), repr(logical_tie)
    if isinstance(pitch_object, abjad.PitchClass):
        raise NotImplementedError(logical_tie, pitch_object)
    for chord in logical_tie:
        duration = chord.written_duration()
        pitch = abjad.NamedPitch(pitch_object)
        note = abjad.Note.from_duration_and_pitch(duration, pitch)
        abjad.mutate.replace(chord, [note])


def imbricate(
    container: abjad.Container,
    voice_name: str,
    segment: list,
    *,
    allow_unused_pitches: bool = False,
    by_pitch_class: bool = False,
    hocket: bool = False,
    truncate_ties: bool = False,
) -> dict[str, list]:
    """
    Imbricates ``segment`` in ``container``.
    """
    if isinstance(container, list):
        container = abjad.Container(container)
    original_container = container
    container = copy.deepcopy(container)
    abjad.override(container).TupletBracket.stencil = False
    abjad.override(container).TupletNumber.stencil = False
    segment = abjad.sequence.flatten(segment, depth=-1)
    if by_pitch_class:
        segment = [abjad.NumberedPitchClass(_) for _ in segment]
    i = 0
    pitch_number = [segment[i]]
    if isinstance(pitch_number, list):
        assert len(pitch_number) == 1
        pitch_number = pitch_number[0]
    original_logical_ties = abjad.select.logical_ties(original_container)
    logical_ties = abjad.select.logical_ties(container)
    pairs = zip(logical_ties, original_logical_ties)
    for logical_tie, original_logical_tie in pairs:
        if isinstance(logical_tie.head(), abjad.Rest):
            for leaf in logical_tie:
                duration = leaf.written_duration()
                skip = abjad.Skip.from_duration(duration)
                abjad.mutate.replace(leaf, [skip])
        elif isinstance(logical_tie.head(), abjad.Skip):
            pass
        elif _matches_pitch(logical_tie.head(), pitch_number):
            _trim_matching_chord(logical_tie, pitch_number)
            i += 1
            if i < len(segment):
                pitch_number = [segment[i]]
            else:
                pitch_number = []
            if isinstance(pitch_number, list):
                if pitch_number == []:
                    pass
                else:
                    assert len(pitch_number) == 1, repr(pitch_number)
                    pitch_number = pitch_number[0]
            if truncate_ties:
                head = logical_tie.head()
                tail = logical_tie.tail()
                for leaf in logical_tie[1:]:
                    duration = leaf.written_duration()
                    skip = abjad.Skip.from_duration(duration)
                    abjad.mutate.replace(leaf, [skip])
                abjad.detach(abjad.Tie, head)
                next_leaf = abjad.get.leaf(tail, 1)
                if next_leaf is not None:
                    abjad.detach(abjad.RepeatTie, next_leaf)
            if hocket:
                for leaf in original_logical_tie:
                    duration = leaf.written_duration()
                    skip = abjad.Skip.from_duration(duration)
                    abjad.mutate.replace(leaf, [skip])
        else:
            for leaf in logical_tie:
                duration = leaf.written_duration()
                skip = abjad.Skip.from_duration(duration)
                abjad.mutate.replace(leaf, [skip])
    if not allow_unused_pitches and i < len(segment):
        current, total = i, len(segment)
        raise Exception(f"{segment!r} used only {current} of {total} pitches.")
    if not hocket:
        pleaves = _select.pleaves(container)
        assert isinstance(pleaves, list)
        for pleaf in pleaves:
            abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
    return {voice_name: [container]}
