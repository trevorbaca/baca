"""
Rhythm.
"""

import dataclasses
import math as python_math
import typing
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import helpers as _helpers
from . import select as _select
from . import tags as _tags
from .enums import enums as _enums

_collection_classes = (
    abjad.PitchClassSegment,
    abjad.PitchSegment,
    abjad.PitchSet,
    list,
    tuple,
)

_collection_typing = typing.Union[
    abjad.PitchClassSegment,
    abjad.PitchSegment,
    abjad.PitchSet,
    list,
    tuple,
]


def _evaluate_basic_item(item, denominator, voice_name, tag):
    if isinstance(
        item, BeamLeft | BeamRight | FramedNote | InvisibleMusic | RepeatTie | Tie
    ):
        components = _evaluate_basic_item(item.argument, denominator, voice_name, tag)
        if isinstance(item, BeamLeft):
            for leaf in abjad.select.leaves(components):
                start_beam = abjad.StartBeam()
                abjad.attach(start_beam, leaf, tag=tag)
        elif isinstance(item, BeamRight):
            for leaf in abjad.select.leaves(components):
                stop_beam = abjad.StopBeam()
                abjad.attach(stop_beam, leaf, tag=tag)
        elif isinstance(item, FramedNote):
            for component in components:
                abjad.attach(_enums.FRAMED_LEAF, component)
        elif isinstance(item, InvisibleMusic):
            rmakers.invisible_music(components, tag=tag)
        elif isinstance(item, RepeatTie):
            rmakers.repeat_tie(components, tag=tag)
        elif isinstance(item, Tie):
            rmakers.tie(components, tag=tag)
    elif isinstance(item, int) and 0 < item:
        leaf_duration = abjad.Duration(item, denominator)
        components = abjad.makers.make_leaves([0], [leaf_duration], tag=tag)
    elif isinstance(item, int) and item < 0:
        leaf_duration = abjad.Duration(-item, denominator)
        components = abjad.makers.make_leaves([None], [leaf_duration], tag=tag)
    elif isinstance(item, Chord):
        chord_duration = abjad.Duration(item.numerator, denominator)
        pitch_tuple = item.note_head_count * (0,)
        components = abjad.makers.make_leaves([pitch_tuple], [chord_duration], tag=tag)
    elif isinstance(item, AfterGrace):
        components = item(denominator, tag)
    elif isinstance(item, IndependentAfterGrace):
        components = item(denominator, tag)
    elif isinstance(item, abjad.Tuplet):
        components = [item]
    elif isinstance(item, TremoloContainer):
        container = item(denominator, voice_name, tag)
        components = [container]
    elif isinstance(item, Tuplet):
        tuplet = item(denominator, voice_name, tag)
        components = [tuplet]
    elif isinstance(item, Container):
        container = item(denominator, voice_name, tag)
        components = [container]
    elif isinstance(item, Feather):
        tuplet = item(denominator, voice_name, tag)
        components = [tuplet]
    elif isinstance(item, BeforeGrace):
        components = item(denominator, tag)
    elif isinstance(item, OBGC):
        polyphony_container = item(denominator, voice_name, tag)
        assert type(polyphony_container) is abjad.Container
        components = [polyphony_container]
    elif isinstance(item, WrittenDuration):
        leaf = item(denominator, tag=tag)
        components = [leaf]
    elif isinstance(item, Multiplier):
        components = item(denominator, voice_name, tag)
    elif getattr(item, "custom", False) is True:
        components = _evaluate_basic_item(item.argument, denominator, voice_name, tag)
        components = item(components)
    else:
        raise Exception(item)
    return components


def _evaluate_item(
    item,
    components,
    denominator,
    i,
    timespan_to_original_item,
    tag,
    voice_name,
) -> abjad.Component | list[abjad.Component]:
    capture_original_item: bool | abjad.Component = False
    if isinstance(item, int) and 0 < item:
        leaf_duration = abjad.Duration(item, denominator)
        notes = abjad.makers.make_leaves([0], [leaf_duration], tag=tag)
        components.extend(notes)
        result = notes
    elif isinstance(item, int) and item < 0:
        leaf_duration = abjad.Duration(-item, denominator)
        rests = abjad.makers.make_leaves([None], [leaf_duration], tag=tag)
        components.extend(rests)
        result = rests
    elif isinstance(item, Chord):
        chord_duration = abjad.Duration(item.numerator, denominator)
        pitch_tuple = item.note_head_count * (0,)
        chords = abjad.makers.make_leaves([pitch_tuple], [chord_duration], tag=tag)
        components.extend(chords)
        result = chords
    elif isinstance(item, abjad.Tuplet):
        duration = abjad.get.duration(item)
        dummy_notes = abjad.makers.make_leaves([99], [duration], tag=tag)
        components.extend(dummy_notes)
        result = dummy_notes
        capture_original_item = item
    elif isinstance(item, AfterGrace):
        components_ = item(denominator, tag)
        components.extend(components_)
        result = components_
    elif isinstance(item, IndependentAfterGrace):
        components_ = item(denominator, tag)
        components.extend(components_)
        result = components_
    elif isinstance(item, Container):
        container = item(denominator, voice_name, tag)
        duration = abjad.get.duration(container)
        dummy_notes = abjad.makers.make_leaves([100], [duration], tag=tag)
        components.extend(dummy_notes)
        result = dummy_notes
        capture_original_item = container
    elif isinstance(item, Feather):
        tuplet = item(denominator, voice_name, tag)
        duration = abjad.get.duration(tuplet)
        dummy_notes = abjad.makers.make_leaves([98], [duration], tag=tag)
        components.extend(dummy_notes)
        result = dummy_notes
        capture_original_item = tuplet
    elif isinstance(item, BeforeGrace):
        components_ = item(denominator, tag)
        components.extend(components_)
        result = components_
    elif isinstance(item, OBGC):
        polyphony_container = item(denominator, voice_name, tag)
        assert type(polyphony_container) is abjad.Container
        assert len(polyphony_container) == 2
        obgc, nongrace_voice = polyphony_container
        assert isinstance(obgc, abjad.OnBeatGraceContainer)
        assert isinstance(nongrace_voice, abjad.Voice)
        assert nongrace_voice.name == voice_name
        nongrace_leaves = abjad.mutate.eject_contents(nongrace_voice)
        components.extend(nongrace_leaves)
        result = nongrace_leaves
        capture_original_item = polyphony_container
    elif isinstance(
        item, BeamLeft | BeamRight | FramedNote | InvisibleMusic | RepeatTie | Tie
    ):
        result = _evaluate_item(
            item.argument,
            components,
            denominator,
            i,
            timespan_to_original_item,
            tag,
            voice_name,
        )
        if isinstance(item, BeamLeft):
            for leaf in abjad.select.leaves(result):
                start_beam = abjad.StartBeam()
                abjad.attach(start_beam, leaf, tag=tag)
        elif isinstance(item, BeamRight):
            for leaf in abjad.select.leaves(result):
                stop_beam = abjad.StopBeam()
                abjad.attach(stop_beam, leaf, tag=tag)
        elif isinstance(item, FramedNote):
            for component in components:
                abjad.attach(_enums.FRAMED_LEAF, component)
        elif isinstance(item, InvisibleMusic):
            rmakers.invisible_music(result, tag=tag)
        elif isinstance(item, RepeatTie):
            rmakers.repeat_tie(result, tag=tag)
        elif isinstance(item, Tie):
            rmakers.tie(result, tag=tag)
    elif isinstance(item, TremoloContainer):
        container = item(denominator, voice_name, tag)
        duration = abjad.get.duration(container)
        dummy_notes = abjad.makers.make_leaves([101], [duration], tag=tag)
        components.extend(dummy_notes)
        result = dummy_notes
        capture_original_item = container
    elif isinstance(item, Tuplet):
        tuplet = item(denominator, voice_name, tag)
        duration = abjad.get.duration(tuplet)
        dummy_notes = abjad.makers.make_leaves([97], [duration], tag=tag)
        components.extend(dummy_notes)
        result = dummy_notes
        capture_original_item = tuplet
    elif isinstance(item, WrittenDuration):
        leaf = item(denominator, tag=tag)
        components.append(leaf)
        result = leaf
    elif isinstance(item, Multiplier):
        components_ = item(denominator, voice_name, tag)
        components.extend(components_)
        result = components_
    elif item in ("+", "-"):
        skip = abjad.Skip(1, multiplier=(99, 1))
        abjad.attach("SPACER", skip)
        abjad.attach(item, skip)
        components.append(skip)
        result = skip
    elif getattr(item, "custom", False) is True:
        old_dummy_count = len(timespan_to_original_item)
        result = _evaluate_item(
            item.argument,
            components,
            denominator,
            i,
            timespan_to_original_item,
            tag,
            voice_name,
        )
        new_dummy_count = len(timespan_to_original_item)
        if old_dummy_count == new_dummy_count:
            result = item(result)
        else:
            assert old_dummy_count < new_dummy_count
            timespan, original_item = timespan_to_original_item[-1]
            modified_original_item = item(original_item)
            modified_pair = timespan, modified_original_item
            timespan_to_original_item[-1] = modified_pair
    else:
        raise Exception(item)
    if capture_original_item is not False or isinstance(item, OBGC):
        components = [_ for _ in components if not isinstance(_, abjad.Skip)]
        total_duration = abjad.get.duration(components)
        stop_offset = abjad.Offset(total_duration)
        if isinstance(item, OBGC):
            item_duration = abjad.get.duration(result)
        else:
            item_duration = abjad.get.duration(capture_original_item)
        start_offset = stop_offset - item_duration
        timespan = abjad.Timespan(start_offset, stop_offset)
        pair = (timespan, capture_original_item)
        timespan_to_original_item.append(pair)
    assert isinstance(result, abjad.Component | list), repr(result)
    return result


def _make_accelerando_multipliers(
    durations: list[abjad.Duration], exponent: float
) -> list[tuple[int, int]]:
    sums = abjad.math.cumulative_sums(durations)
    generator = abjad.sequence.nwise(sums, n=2)
    pairs = list(generator)
    total_duration = pairs[-1][-1]
    start_offsets = [_[0] for _ in pairs]
    start_offsets = [_ / total_duration for _ in start_offsets]
    start_offsets_ = []
    for start_offset in start_offsets:
        start_offset_ = rmakers.functions._interpolate_exponential(
            0, total_duration, start_offset, exponent
        )
        start_offsets_.append(start_offset_)
    start_offsets_.append(float(total_duration))
    durations_ = abjad.math.difference_series(start_offsets_)
    durations_ = rmakers.makers._round_durations(durations_, 2**10)
    current_duration = sum(durations_)
    if current_duration < total_duration:
        missing_duration = total_duration - current_duration
        if durations_[0] < durations_[-1]:
            durations_[-1] += missing_duration
        else:
            durations_[0] += missing_duration
    elif total_duration < current_duration:
        extra_duration = current_duration - total_duration
        if durations_[0] < durations_[-1]:
            durations_[-1] -= extra_duration
        else:
            durations_[0] -= extra_duration
    assert sum(durations_) == total_duration
    pairs = []
    assert len(durations) == len(durations_)
    for duration_, duration in zip(durations_, durations):
        fraction = duration_ / duration
        pair = abjad.duration.with_denominator(fraction, 2**10)
        pairs.append(pair)
    return pairs


def _style_accelerando(
    container: abjad.Container | abjad.Tuplet,
    exponent: float,
    total_duration: abjad.Duration | None = None,
) -> abjad.Container | abjad.Tuplet:
    assert isinstance(container, abjad.Container), repr(container)
    temporary_voice = None
    if container._parent is None:
        temporary_voice = abjad.Voice([container], name="TemporaryVoice")
    if 1 < len(container):
        assert isinstance(container, abjad.Tuplet), repr(container)
        assert isinstance(exponent, float), repr(exponent)
        if total_duration is not None:
            assert isinstance(total_duration, abjad.Duration), repr(total_duration)
        hleaves = _select.hleaves(container)
        leaf_durations = [abjad.get.duration(_) for _ in hleaves]
        pairs = _make_accelerando_multipliers(leaf_durations, exponent)
        if total_duration is not None:
            multiplier = total_duration / sum(leaf_durations)
            scaled_pairs = []
            for pair in pairs:
                numerator, denominator = pair
                numerator *= multiplier.numerator
                denominator *= multiplier.denominator
                scaled_pair = (numerator, denominator)
                scaled_pairs.append(scaled_pair)
            pairs = scaled_pairs
        assert len(hleaves) == len(pairs)
        for pair, leaf in zip(pairs, hleaves):
            leaf.multiplier = pair
        if abjad.select.rests(hleaves):
            stemlet_length = 0.75
        else:
            stemlet_length = None
        rmakers.feather_beam([hleaves], beam_rests=True, stemlet_length=stemlet_length)
        rmakers.duration_bracket(container)
    if temporary_voice is not None:
        temporary_voice[:] = []
    return container


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AfterGrace:
    grace_note_numerators: list
    main_note_numerator: int

    def __post_init__(self):
        assert isinstance(self.grace_note_numerators, list), repr(
            self.grace_note_numerators
        )

    def __call__(self, denominator, tag: abjad.Tag):
        tag = tag.append(_helpers.function_name(_frame()))
        voice_name = None
        main_components = _evaluate_basic_item(
            self.main_note_numerator,
            denominator,
            voice_name,
            tag,
        )
        grace_leaves = []
        for item in self.grace_note_numerators:
            components = _evaluate_basic_item(item, denominator, "", tag)
            grace_leaves.extend(components)
        if 1 < len(grace_leaves):
            temporary_voice = abjad.Voice(grace_leaves, name="TemporaryVoice")
            abjad.beam(grace_leaves)
            temporary_voice[:] = []
        agc = abjad.AfterGraceContainer(grace_leaves, tag=tag)
        last_leaf = abjad.get.leaf(main_components, -1)
        abjad.attach(agc, last_leaf)
        return main_components


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BeamLeft:
    argument: typing.Any


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BeamRight:
    argument: typing.Any


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class BeforeGrace:
    grace_note_numerators: list
    main_note_numerator: typing.Any
    slash: bool = True
    slur: bool = True

    def __post_init__(self):
        assert isinstance(self.grace_note_numerators, list), repr(
            self.grace_note_numerators
        )
        assert isinstance(self.slash, bool), repr(self.slash)
        assert isinstance(self.slur, bool), repr(self.slur)

    def __call__(self, denominator, tag: abjad.Tag):
        tag = tag.append(_helpers.function_name(_frame()))
        beam = True
        if self.slash is True:
            assert beam is True, repr(beam)
        main_components = _evaluate_basic_item(
            self.main_note_numerator, denominator, "", tag
        )
        first_leaf = abjad.get.leaf(main_components, 0)
        grace_leaves = []
        for item in self.grace_note_numerators:
            components = _evaluate_basic_item(item, denominator, "", tag)
            grace_leaves.extend(components)
        if len(grace_leaves) == 1:
            if self.slash is False and self.slur is False:
                command = r"\grace"
            elif self.slash is False and self.slur is True:
                command = r"\appoggiatura"
            elif self.slash is True and self.slur is False:
                command = r"\slashedGrace"
            elif self.slash is True and self.slur is True:
                command = r"\acciaccatura"
            else:
                raise Exception
        elif 1 < len(grace_leaves):
            if beam is True:
                temporary_voice = abjad.Voice(grace_leaves, name="TemporaryVoice")
                abjad.beam(grace_leaves, tag=tag)
                temporary_voice[:] = []
            if self.slash is True:
                literal = abjad.LilyPondLiteral(r"\slash", site="before")
                abjad.attach(literal, grace_leaves[0], tag=tag)
            if self.slash is False and self.slur is False:
                command = r"\grace"
            elif self.slash is False and self.slur is True:
                command = r"\appoggiatura"
            elif self.slash is True and self.slur is False:
                command = r"\slashedGrace"
            elif self.slash is True and self.slur is True:
                command = r"\acciaccatura"
            else:
                raise Exception
        bgc = abjad.BeforeGraceContainer(grace_leaves, command=command, tag=tag)
        abjad.attach(bgc, first_leaf, tag=tag)
        return main_components


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Chord:
    numerator: int
    note_head_count: int

    def __post_init__(self):
        assert isinstance(self.numerator, int), repr(self.numerator)
        assert 1 <= self.numerator, repr(self.numerator)
        assert isinstance(self.note_head_count, int), repr(self.note_head_count)
        assert 1 <= self.note_head_count, repr(self.note_head_count)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Container:
    items: list

    def __call__(
        self, denominator: int, voice_name: str, tag: abjad.Tag
    ) -> abjad.Container:
        assert isinstance(denominator, int), repr(denominator)
        tag = tag.append(_helpers.function_name(_frame()))
        components = []
        for item in self.items:
            components_ = _evaluate_basic_item(item, denominator, voice_name, tag)
            components.extend(components_)
        container = abjad.Container(components, tag=tag)
        return container


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Feather:
    items: list
    denominator: int
    numerator: int
    exponent: float = dataclasses.field(default=0.625, kw_only=True)

    def __post_init__(self):
        assert isinstance(self.items, list), repr(self.items)
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert isinstance(self.numerator, int), repr(self.numerator)
        assert isinstance(self.exponent, float), repr(self.exponent)

    def __call__(self, denominator: int, voice_name: str, tag: abjad.Tag):
        assert isinstance(denominator, int), repr(denominator)
        tag = tag.append(_helpers.function_name(_frame()))
        feather_duration = abjad.Duration(self.numerator, denominator)
        tuplet = make_accelerando(
            self.items,
            denominator,
            feather_duration,
            exponent=self.exponent,
            voice_name=voice_name,
            tag=tag,
        )
        return tuplet


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class FramedNote:
    argument: typing.Any


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class IndependentAfterGrace:
    grace_note_numerators: list
    main_note_numerator: int

    def __post_init__(self):
        assert isinstance(self.grace_note_numerators, list), repr(
            self.grace_note_numerators
        )

    def __call__(self, denominator, tag: abjad.Tag):
        tag = tag.append(_helpers.function_name(_frame()))
        voice_name = None
        main_components = _evaluate_basic_item(
            self.main_note_numerator,
            denominator,
            voice_name,
            tag,
        )
        grace_leaves = []
        for item in self.grace_note_numerators:
            components = _evaluate_basic_item(item, denominator, "", tag)
            grace_leaves.extend(components)
        if 1 < len(grace_leaves):
            temporary_voice = abjad.Voice(grace_leaves, name="TemporaryVoice")
            abjad.beam(grace_leaves)
            temporary_voice[:] = []
        iagc = abjad.IndependentAfterGraceContainer(grace_leaves, tag=tag)
        main_components.append(iagc)
        return main_components


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class InvisibleMusic:
    argument: typing.Any


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LMR:
    left_counts: typing.Sequence[int] = ()
    left_cyclic: bool = False
    left_length: int = 0
    left_reversed: bool = False
    middle_counts: typing.Sequence[int] = ()
    middle_cyclic: bool = False
    middle_reversed: bool = False
    priority: int | None = None
    right_counts: typing.Sequence[int] = ()
    right_cyclic: bool = False
    right_length: int = 0
    right_reversed: bool = False

    def __post_init__(self):
        if self.left_counts is not None:
            assert abjad.math.all_are_positive_integers(self.left_counts)
        assert isinstance(self.left_cyclic, bool), repr(self.left_cyclic)
        if self.left_length is not None:
            assert isinstance(self.left_length, int), repr(self.left_length)
            assert 0 <= self.left_length, repr(self.left_length)
        assert isinstance(self.left_reversed, bool), repr(self.left_reversed)
        if self.middle_counts is not None:
            assert abjad.math.all_are_positive_integers(self.middle_counts)
        assert isinstance(self.middle_cyclic, bool), repr(self.middle_cyclic)
        assert isinstance(self.middle_reversed, bool), repr(self.middle_reversed)
        if self.priority is not None:
            assert self.priority in (abjad.LEFT, abjad.RIGHT)
        if self.right_counts is not None:
            assert abjad.math.all_are_positive_integers(self.right_counts)
        assert isinstance(self.right_cyclic, bool), repr(self.right_cyclic)
        if self.right_length is not None:
            assert isinstance(self.right_length, int), repr(self.right_length)
            assert 0 <= self.right_length, repr(self.right_length)
        assert isinstance(self.right_reversed, bool), repr(self.right_reversed)

    def __call__(self, sequence=None):
        assert isinstance(sequence, list), repr(sequence)
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence.partition_by_counts(
            list(sequence), top_lengths, cyclic=False, overhang=abjad.EXACT
        )
        parts = []
        left_part, middle_part, right_part = top_parts
        if left_part:
            if self.left_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    left_part,
                    self.left_counts,
                    cyclic=self.left_cyclic,
                    overhang=True,
                    reversed_=self.left_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(left_part)
        if middle_part:
            if self.middle_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    middle_part,
                    self.middle_counts,
                    cyclic=self.middle_cyclic,
                    overhang=True,
                    reversed_=self.middle_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(middle_part)
        if right_part:
            if self.right_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    right_part,
                    self.right_counts,
                    cyclic=self.right_cyclic,
                    overhang=True,
                    reversed_=self.right_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(right_part)
        assert isinstance(parts, list), repr(parts)
        assert all(isinstance(_, list) for _ in parts)
        return parts

    def _get_priority(self):
        if self.priority is None:
            return abjad.LEFT
        return self.priority

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() == abjad.LEFT:
                left_length = self.left_length or 0
                left_length = min([left_length, total_length])
                remaining_length = total_length - left_length
                if self.right_length is None:
                    right_length = remaining_length
                    middle_length = 0
                else:
                    right_length = self.right_length or 0
                    right_length = min([right_length, remaining_length])
                    remaining_length = total_length - (left_length + right_length)
                    middle_length = remaining_length
            else:
                right_length = self.right_length or 0
                right_length = min([right_length, total_length])
                remaining_length = total_length - right_length
                if self.left_length is None:
                    left_length = remaining_length
                    middle_length = 0
                else:
                    left_length = self.left_length or 0
                    left_length = min([left_length, remaining_length])
                    remaining_length = total_length - (right_length + left_length)
                    middle_length = remaining_length
        elif left_length and not right_length:
            left_length = min([left_length, total_length])
            remaining_length = total_length - left_length
            right_length = remaining_length
        elif not left_length and right_length:
            right_length = min([right_length, total_length])
            remaining_length = total_length - right_length
            left_length = remaining_length
        elif not left_length and not right_length:
            middle_length = total_length
        return left_length, middle_length, right_length


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Multiplier:
    argument: typing.Any
    multiplier: tuple[int, int]

    def __post_init__(self):
        assert isinstance(self.multiplier, tuple), repr(self.multiplier)

    def __call__(
        self, denominator: int, voice_name: str, tag: abjad.Tag
    ) -> list[abjad.Component]:
        assert isinstance(denominator, int), repr(denominator)
        tag = _helpers.function_name(_frame())
        components = _evaluate_basic_item(self.argument, denominator, voice_name, tag)
        for leaf in abjad.select.leaves(components):
            leaf.multiplier = self.multiplier
        return components


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OBGC:
    grace_note_numerators: list[int]
    nongrace_note_numerators: list
    do_not_attach_one_voice_command: bool = False
    grace_leaf_duration: abjad.Duration | bool | None = None
    grace_polyphony_command: abjad.VoiceNumber = abjad.VoiceNumber(1)
    nongrace_polyphony_command: abjad.VoiceNumber = abjad.VoiceNumber(2)

    def __post_init__(self):
        assert all(isinstance(_, int) for _ in self.grace_note_numerators), repr(
            self.grace_note_numerators
        )
        assert isinstance(self.nongrace_note_numerators, list), repr(
            self.nongrace_note_numerators
        )
        assert isinstance(self.do_not_attach_one_voice_command, bool), repr(
            self.do_not_attach_one_voice_command
        )
        if self.grace_leaf_duration is not None:
            assert isinstance(self.grace_leaf_duration, abjad.Duration | bool), repr(
                self.grace_leaf_duration
            )

    def __call__(
        self, denominator: int, voice_name: str, tag: abjad.Tag
    ) -> abjad.Container:
        assert isinstance(denominator, int), repr(denominator)
        assert isinstance(voice_name, str), repr(voice_name)
        tag = tag.append(_helpers.function_name(_frame()))
        nongrace_leaves = []
        for item in self.nongrace_note_numerators:
            components = _evaluate_basic_item(item, denominator, voice_name, tag)
            nongrace_leaves.extend(components)
        dummy_voice = abjad.Voice(nongrace_leaves, name=voice_name, tag=tag)
        grace_note_durations = [
            abjad.Duration(_, denominator) for _ in self.grace_note_numerators
        ]
        grace_leaves = abjad.makers.make_leaves([0], grace_note_durations, tag=tag)
        if self.grace_leaf_duration is True:
            nongrace_duration = abjad.get.duration(nongrace_leaves)
            grace_leaf_duration = nongrace_duration / len(grace_leaves)
        else:
            grace_leaf_duration = self.grace_leaf_duration
        abjad.on_beat_grace_container(
            grace_leaves,
            nongrace_leaves,
            do_not_attach_one_voice_command=self.do_not_attach_one_voice_command,
            grace_leaf_duration=grace_leaf_duration,
            grace_polyphony_command=self.grace_polyphony_command,
            nongrace_polyphony_command=self.nongrace_polyphony_command,
            tag=tag,
        )
        assert len(dummy_voice) == 1
        polyphony_container = abjad.mutate.eject_contents(dummy_voice)[0]
        assert type(polyphony_container) is abjad.Container
        assert len(polyphony_container) == 2
        obgc, nongrace_voice = polyphony_container
        assert isinstance(obgc, abjad.OnBeatGraceContainer)
        assert isinstance(nongrace_voice, abjad.Voice)
        assert nongrace_voice.name == voice_name
        return polyphony_container


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RepeatTie:
    argument: typing.Any


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tie:
    argument: typing.Any


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class TremoloContainer:
    count: int
    items: list[int]

    def __post_init__(self):
        assert isinstance(self.count, int), repr(self.count)
        assert isinstance(self.items, list), repr(self.items)
        assert len(self.items) == 2, repr(self.items)

    def __call__(
        self, denominator: int, voice_name: str, tag: abjad.Tag
    ) -> abjad.TremoloContainer:
        assert isinstance(denominator, int), repr(denominator)
        tag = _helpers.function_name(_frame())
        components = []
        for item in self.items:
            components_ = _evaluate_basic_item(item, denominator, voice_name, tag)
            components.extend(components_)
        container = abjad.TremoloContainer(self.count, components, tag=tag)
        return container


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Tuplet:
    items: list
    extra_counts: int

    def __post_init__(self):
        assert isinstance(self.items, list), repr(self.items)
        assert isinstance(self.extra_counts, int | str), repr(self.extra_counts)

    def __call__(
        self, denominator: int, voice_name: str, tag: abjad.Tag
    ) -> abjad.Tuplet:
        assert isinstance(denominator, int), repr(denominator)
        tag = _helpers.function_name(_frame())
        components = []
        for item in self.items:
            components_ = _evaluate_basic_item(item, denominator, voice_name, tag)
            components.extend(components_)
        contents_duration = sum([abjad.get.duration(_) for _ in components])
        if isinstance(self.extra_counts, int):
            extra_duration = abjad.Duration(self.extra_counts, denominator)
            prolated_duration = contents_duration + extra_duration
            multiplier = prolated_duration / contents_duration
            pair = multiplier.numerator, multiplier.denominator
            tuplet = abjad.Tuplet(pair, components, tag=tag)
        else:
            assert isinstance(self.extra_counts, str)
            tuplet = abjad.Tuplet(self.extra_counts, components, tag=tag)
        return tuplet


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class WrittenDuration:
    real_n: typing.Any
    written_n: int

    def __post_init__(self):
        assert isinstance(self.written_n, int), repr(self.written_n)

    def __call__(self, denominator: int, tag: abjad.Tag) -> abjad.Leaf:
        assert isinstance(denominator, int), repr(denominator)
        tag = tag or abjad.Tag()
        tag = tag.append(_helpers.function_name(_frame()))
        components = _evaluate_basic_item(self.real_n, denominator, "", tag)
        if 1 < len(components):
            raise NotImplementedError(f"multiple leaves: {components}")
        leaf = components[0]
        written_duration = abjad.Duration(self.written_n, denominator)
        rmakers.written_duration([leaf], written_duration)
        return leaf


def attach_bgcs(
    bgcs: list[abjad.BeforeGraceContainer],
    argument: abjad.Component | list[abjad.Component],
) -> None:
    tag = _helpers.function_name(_frame())
    bgcs = bgcs or []
    lts = abjad.select.logical_ties(argument)
    assert len(bgcs) == len(lts)
    pairs = zip(bgcs, lts)
    for bgc, lt in pairs:
        if bgc is not None:
            abjad.attach(bgc, lt.head, tag=tag)


def from_collection(
    collection: _collection_typing,
    counts: list[int],
    denominator: int,
    prolation: int | str | abjad.Duration | None = None,
) -> abjad.Tuplet:
    collection = getattr(collection, "argument", collection)
    prototype = (
        abjad.PitchClassSegment,
        abjad.PitchSegment,
        abjad.PitchSet,
        list,
        tuple,
    )
    assert isinstance(collection, prototype), repr(collection)
    if isinstance(collection, tuple | abjad.PitchSet):
        collection = [tuple(collection)]
    talea = rmakers.Talea(counts, denominator)
    leaves, i = [], 0
    for item in collection:
        item = getattr(item, "number", item)
        assert isinstance(item, int | float | str | tuple), repr(item)
        while abjad.Fraction(*talea[i]) < 0:
            pair = talea[i]
            duration = -abjad.Duration(*pair)
            tag = _helpers.function_name(_frame(), n=1)
            rests = abjad.makers.make_leaves([None], [duration], tag=tag)
            leaves.extend(rests)
            i += 1
        pair = talea[i]
        duration = abjad.Duration(*pair)
        assert 0 < duration, repr(duration)
        tag = _helpers.function_name(_frame(), n=3)
        pleaves = abjad.makers.make_leaves([item], [duration], tag=tag)
        leaves.extend(pleaves)
        i += 1
        while abjad.Fraction(*talea[i]) < 0 and not i % len(talea) == 0:
            pair = talea[i]
            duration = -abjad.Duration(*pair)
            tag = _helpers.function_name(_frame(), n=4)
            rests = abjad.makers.make_leaves([None], [duration], tag=tag)
            leaves.extend(rests)
            i += 1
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    tuplet = abjad.Tuplet("1:1", leaves)
    if prolation is not None:
        prolate(tuplet, prolation, denominator=denominator)
    return tuplet


def get_previous_rhythm_state(
    previous_parameter_to_state: dict, name: str
) -> dict | None:
    previous_rhythm_state = None
    if previous_parameter_to_state:
        previous_rhythm_state = previous_parameter_to_state.get(_enums.RHYTHM.name)
        if (
            previous_rhythm_state is not None
            and previous_rhythm_state.get("name") != name
        ):
            previous_rhythm_state = None
    if previous_rhythm_state is not None:
        assert len(previous_rhythm_state) in (4, 5), repr(previous_rhythm_state)
        assert previous_rhythm_state["name"] == name, repr(previous_rhythm_state)
    return previous_rhythm_state


def make_accelerando(
    items: list,
    denominator: int,
    duration: abjad.Duration,
    *,
    exponent: float = 0.625,
    voice_name: str | None = None,
    tag: abjad.Tag | None = None,
) -> abjad.Tuplet:
    tag = tag or abjad.Tag()
    tag = tag.append(_helpers.function_name(_frame()))
    leaves = []
    assert isinstance(denominator, int), repr(denominator)
    assert isinstance(duration, abjad.Duration), repr(duration)
    assert isinstance(exponent, float), repr(exponent)
    for item in items:
        components = _evaluate_basic_item(item, denominator, voice_name, tag)
        leaves.extend(components)
    tuplet = abjad.Tuplet("1:1", leaves, tag=tag)
    abjad.attach("FEATHER_BEAM_CONTAINER", tuplet)
    _style_accelerando(tuplet, exponent, total_duration=duration)
    return tuplet


def make_bgcs(
    collection: list[int | float],
    lmr: LMR,
    *,
    duration: abjad.Duration = abjad.Duration(1, 16),
) -> tuple[list[abjad.BeforeGraceContainer | None], list[int | float]]:
    assert isinstance(collection, list), repr(collection)
    assert all(isinstance(_, int | float) for _ in collection), repr(collection)
    assert isinstance(duration, abjad.Duration), repr(duration)
    assert isinstance(lmr, LMR), repr(LMR)
    segment_parts = lmr(collection)
    segment_parts = [_ for _ in segment_parts if _]
    collection = [_[-1] for _ in segment_parts]
    bgcs: list[abjad.BeforeGraceContainer | None] = []
    for segment_part in segment_parts:
        if len(segment_part) <= 1:
            bgcs.append(None)
            continue
        grace_token = list(segment_part[:-1])
        grace_leaves = abjad.makers.make_leaves(
            grace_token, [duration], tag=_helpers.function_name(_frame(), n=1)
        )
        container = abjad.BeforeGraceContainer(
            grace_leaves,
            command=r"\acciaccatura",
            tag=_helpers.function_name(_frame(), n=2),
        )
        bgcs.append(container)
    assert len(bgcs) == len(collection)
    assert isinstance(collection, list), repr(collection)
    return bgcs, collection


def make_even_divisions(time_signatures) -> list[abjad.Leaf | abjad.Tuplet]:
    tag = _helpers.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    tuplets = rmakers.even_division(durations, [8], tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(tuplets, time_signatures)
    rmakers.beam(voice, tag=tag)
    rmakers.extract_trivial(voice)
    components = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in components:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_mmrests(
    time_signatures, *, head: str = ""
) -> list[abjad.MultimeasureRest | abjad.Container]:
    assert isinstance(head, str), repr(head)
    mmrests: list[abjad.MultimeasureRest | abjad.Container] = []
    if not head:
        tag = _helpers.function_name(_frame(), n=1)
        for time_signature in time_signatures:
            mmrest = abjad.MultimeasureRest(1, multiplier=time_signature.pair, tag=tag)
            mmrests.append(mmrest)
    else:
        assert isinstance(head, str)
        voice_name = head
        for i, time_signature in enumerate(time_signatures):
            if i == 0:
                tag = _helpers.function_name(_frame(), n=2)
                tag = tag.append(_tags.HIDDEN)
                note_or_rest = _tags.NOTE
                tag = tag.append(_tags.NOTE)
                note = abjad.Note("c'1", multiplier=time_signature.pair, tag=tag)
                abjad.override(note).Accidental.stencil = False
                abjad.override(note).NoteColumn.ignore_collision = True
                abjad.attach(_enums.NOTE, note)
                abjad.attach(_enums.NOT_YET_PITCHED, note)
                abjad.attach(_enums.HIDDEN, note)
                tag = _helpers.function_name(_frame(), n=3)
                tag = tag.append(note_or_rest)
                tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
                literal = abjad.LilyPondLiteral(
                    r"\abjad-invisible-music-coloring", site="before"
                )
                abjad.attach(literal, note, tag=tag)
                tag = _helpers.function_name(_frame(), n=4)
                tag = tag.append(note_or_rest)
                tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
                literal = abjad.LilyPondLiteral(
                    r"\abjad-invisible-music", site="before"
                )
                abjad.attach(literal, note, deactivate=True, tag=tag)
                tag = _helpers.function_name(_frame(), n=5)
                hidden_note_voice = abjad.Voice([note], name=voice_name, tag=tag)
                abjad.attach(_enums.INTERMITTENT, hidden_note_voice)
                tag = _helpers.function_name(_frame(), n=6)
                tag = tag.append(_tags.REST_VOICE)
                tag = tag.append(_tags.MULTIMEASURE_REST)
                rest = abjad.MultimeasureRest(
                    1, multiplier=time_signature.pair, tag=tag
                )
                abjad.attach(_enums.MULTIMEASURE_REST, rest)
                abjad.attach(_enums.REST_VOICE, rest)
                if "Music" in voice_name:
                    name = voice_name.replace("Music", "Rests")
                else:
                    assert "Voice" in voice_name
                    name = f"{voice_name}.Rests"
                tag = _helpers.function_name(_frame(), n=7)
                multimeasure_rest_voice = abjad.Voice([rest], name=name, tag=tag)
                abjad.attach(_enums.INTERMITTENT, multimeasure_rest_voice)
                tag = _helpers.function_name(_frame(), n=8)
                container = abjad.Container(
                    [hidden_note_voice, multimeasure_rest_voice],
                    simultaneous=True,
                    tag=tag,
                )
                abjad.attach(_enums.MULTIMEASURE_REST_CONTAINER, container)
                mmrests.append(container)
            else:
                mmrest = abjad.MultimeasureRest(
                    1, multiplier=time_signature.pair, tag=tag
                )
                mmrests.append(mmrest)
    assert all(isinstance(_, abjad.MultimeasureRest | abjad.Container) for _ in mmrests)
    return mmrests


def make_monads(fractions) -> list[abjad.Leaf | abjad.Tuplet]:
    music: list[abjad.Leaf | abjad.Tuplet] = []
    pitch = 0
    for fraction in fractions.split():
        leaves = abjad.makers.make_leaves([pitch], [fraction])
        music.extend(leaves)
    assert all(isinstance(_, abjad.Leaf | abjad.Tuplet) for _ in music)
    return music


def make_notes(
    time_signatures,
    *,
    repeat_ties: bool = False,
) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _helpers.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    rmakers.rewrite_meter(voice)
    if repeat_ties is True:
        rmakers.force_repeat_tie(voice)
    contents, music = abjad.mutate.eject_contents(voice), []
    for component in contents:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_repeat_tied_notes(
    time_signatures,
    *,
    do_not_rewrite_meter: bool = False,
) -> list[abjad.Leaf | abjad.Tuplet]:
    tag = _helpers.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    leaves_and_tuplets = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(leaves_and_tuplets, time_signatures)
    rmakers.beam(_select.plts(voice))
    rmakers.repeat_tie(_select.pheads(voice)[1:], tag=tag)
    if not do_not_rewrite_meter:
        rmakers.rewrite_meter(voice)
    rmakers.force_repeat_tie(voice)
    components = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in components:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_repeated_duration_notes(
    time_signatures,
    weights,
    *,
    do_not_rewrite_meter=None,
) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _helpers.function_name(_frame())
    if isinstance(weights, abjad.Duration):
        weights = [weights]
    elif isinstance(weights, tuple):
        assert len(weights) == 2
        weights = [abjad.Duration(weights)]
    durations = [_.duration for _ in time_signatures]
    durations = [sum(durations)]
    weights = abjad.durations(weights)
    durations = abjad.sequence.split(durations, weights, cyclic=True, overhang=True)
    durations = abjad.sequence.flatten(durations, depth=-1)
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    if not do_not_rewrite_meter:
        rmakers.rewrite_meter(voice, tag=tag)
    rmakers.force_repeat_tie(voice)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_rests(time_signatures) -> list[abjad.Rest | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _helpers.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    lts = _select.lts(voice)
    rmakers.force_rest(lts, tag=tag)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Rest | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Rest | abjad.Tuplet)
        music.append(component)
    return music


def make_rhythm(
    items: list,
    denominator: int,
    time_signatures: list[abjad.TimeSignature] | None = None,
    *,
    boundary_depth: int | None = None,
    do_not_rewrite_meter: bool = False,
    reference_meters: typing.Sequence[abjad.Meter] = (),
    tag: abjad.Tag | None = None,
    voice_name: str | None = None,
) -> abjad.Voice:
    assert isinstance(items, list), repr(items)
    assert isinstance(denominator, int), repr(denominator)
    if time_signatures is not None:
        assert isinstance(time_signatures, list), repr(time_signatures)
        assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    if do_not_rewrite_meter is False:
        assert time_signatures is not None, repr(time_signatures)
    tag = tag or abjad.Tag()
    tag = tag.append(_helpers.function_name(_frame()))
    timespan_to_original_item: list[tuple[abjad.Timespan, typing.Any]] = []
    components: list[abjad.Component] = []
    for i, item in enumerate(items):
        result = _evaluate_item(
            item,
            components,
            denominator,
            i,
            timespan_to_original_item,
            tag,
            voice_name,
        )
        assert isinstance(result, abjad.Component | list), repr(result)
    assert all(isinstance(_, abjad.Component) for _ in components), repr(components)
    if time_signatures is not None:
        total_duration = sum(_.duration for _ in time_signatures)
        existing_duration = sum(
            [abjad.get.duration(_) for _ in components if not isinstance(_, abjad.Skip)]
        )
        if existing_duration < total_duration:
            spacer_skip = None
            for i, component in enumerate(components):
                if isinstance(component, abjad.Skip):
                    strings = abjad.get.indicators(component, str)
                    if "SPACER" in strings:
                        spacer_skip = component
                        if "+" in strings:
                            spacer_pitch = 0
                        else:
                            assert "-" in strings
                            spacer_pitch = None
                        needed_duration = total_duration - existing_duration
                        leaves = abjad.makers.make_leaves(
                            [spacer_pitch], [needed_duration], tag=tag
                        )
                        assert abjad.get.duration(leaves) == needed_duration
                        unchanged_duration = abjad.get.duration(components[:i])
                        pairs = []
                        for pair in timespan_to_original_item:
                            timespan, original_item = pair
                            if unchanged_duration <= timespan.start_offset:
                                timespan = timespan.translate(needed_duration)
                                pair = (timespan, original_item)
                            pairs.append(pair)
                        timespan_to_original_item = pairs
                        index = components.index(spacer_skip)
                        components[index : index + 1] = leaves
                        break
        elif total_duration < existing_duration:
            components = [_ for _ in components if not isinstance(_, abjad.Skip)]
            lists = abjad.mutate.split(components, [total_duration], tag=tag)
            components[:] = []
            for component in lists[0]:
                components.append(component)
            last_leaf = abjad.select.leaf(components, -1)
            rmakers.untie(last_leaf)
        if do_not_rewrite_meter is False:
            voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
            rmakers.rewrite_meter(
                voice,
                boundary_depth=boundary_depth,
                reference_meters=reference_meters,
                tag=tag,
            )
            components = abjad.mutate.eject_contents(voice)
    voice = abjad.Voice(components, name=voice_name)
    if timespan_to_original_item:
        for timespan, original_item in timespan_to_original_item:
            is_obgc_polyphony_container = False
            if (
                type(original_item) is abjad.Container
                and len(original_item) == 2
                and isinstance(original_item[0], abjad.OnBeatGraceContainer)
            ):
                is_obgc_polyphony_container = True
            timespan_components = []
            for component in voice:
                timespan_ = abjad.get.timespan(component)
                if timespan_ in timespan:
                    timespan_components.append(component)
                elif timespan_components:
                    break
            assert timespan_components, repr(timespan_components)
            if not is_obgc_polyphony_container:
                rmakers.unbeam(timespan_components, smart=True)
            abjad.mutate.replace(timespan_components, original_item)
            if is_obgc_polyphony_container:
                nongrace_voice = original_item[1]
                assert isinstance(nongrace_voice, abjad.Voice)
                assert len(nongrace_voice) == 0
                nongrace_voice.extend(timespan_components)
    return voice


def make_single_attack(time_signatures, duration) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    durations = [_.duration for _ in time_signatures]
    tag = _helpers.function_name(_frame())
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    tuplets = rmakers.incised(
        durations,
        fill_with_rests=True,
        outer_tuplets_only=True,
        prefix_talea=[numerator],
        prefix_counts=[1],
        tag=tag,
        talea_denominator=denominator,
    )
    voice = rmakers.wrap_in_time_signature_staff(tuplets, time_signatures)
    rmakers.beam(voice)
    rmakers.extract_trivial(voice)
    components = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in components:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_tied_notes(time_signatures) -> list[abjad.Note | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    durations = [_.duration for _ in time_signatures]
    tag = _helpers.function_name(_frame())
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    plts = _select.plts(voice)
    rmakers.beam(plts, tag=tag)
    ptails = _select.ptails(voice)[:-1]
    rmakers.tie(ptails, tag=tag)
    rmakers.rewrite_meter(voice, tag=tag)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Note | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Note | abjad.Tuplet)
        music.append(component)
    return music


def make_tied_repeated_durations(
    time_signatures, weights
) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _helpers.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    durations = [sum(durations)]
    weights = abjad.durations(weights)
    durations = abjad.sequence.split(durations, weights, cyclic=True, overhang=True)
    durations = abjad.sequence.flatten(durations, depth=-1)
    if isinstance(weights, abjad.Duration):
        weights = [weights]
    elif isinstance(weights, tuple):
        assert len(weights) == 2
        weights = [abjad.Duration(weights)]
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    pheads = _select.pheads(voice)[1:]
    rmakers.repeat_tie(pheads, tag=tag)
    rmakers.force_repeat_tie(voice)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_time_signatures(
    time_signatures: list[list[abjad.TimeSignature]],
    count: int,
    *,
    fermata_measures: list[int] | None = None,
    rotation: int = 0,
) -> list[abjad.TimeSignature]:
    assert isinstance(time_signatures, list), repr(time_signatures)
    for item in time_signatures:
        assert isinstance(item, list), repr(item)
        assert all(isinstance(_, abjad.TimeSignature) for _ in item), repr(item)
    assert isinstance(count, int), repr(count)
    fermata_measures = fermata_measures or []
    assert isinstance(fermata_measures, list), repr(fermata_measures)
    assert all(isinstance(_, int) for _ in fermata_measures)
    result = []
    time_signatures = abjad.sequence.rotate(time_signatures, rotation)
    time_signatures = abjad.sequence.flatten(time_signatures, depth=1)
    time_signatures_ = abjad.CyclicTuple(time_signatures)
    nfms = []
    for n in fermata_measures:
        if 0 < n:
            nfms.append(n)
        elif n == 0:
            raise ValueError(n)
        else:
            nfms.append(count - abs(n) + 1)
    nfms.sort()
    i = 0
    for j in range(count):
        measure_number = j + 1
        if measure_number in nfms:
            result.append(abjad.TimeSignature((1, 4)))
        else:
            time_signature = time_signatures_[i]
            result.append(time_signature)
            i += 1
    return result


def nest(containers: list[abjad.Tuplet], treatment: str) -> abjad.Tuplet:
    assert isinstance(containers, list), repr(containers)
    assert all(isinstance(_, abjad.Container) for _ in containers), repr(containers)
    assert isinstance(treatment, str), repr(treatment)
    if "/" in treatment:
        assert treatment.startswith("+") or treatment.startswith("-"), repr(treatment)
        addendum = abjad.Duration(treatment)
        contents_duration = abjad.get.duration(containers)
        target_duration = contents_duration + addendum
        multiplier = target_duration / contents_duration
        pair = abjad.duration.pair(multiplier)
        nested_tuplet = abjad.Tuplet(pair, [])
        abjad.mutate.wrap(containers, nested_tuplet)
    else:
        assert ":" in treatment
        nested_tuplet = abjad.Tuplet(treatment, [])
        abjad.mutate.wrap(containers, nested_tuplet)
    return nested_tuplet


def prolate(
    tuplet: abjad.Tuplet,
    treatment: int | str | abjad.Duration,
    denominator: int | None = None,
) -> abjad.Tuplet:
    if isinstance(treatment, int):
        extra_count = treatment
        contents_duration = abjad.get.duration(tuplet)
        pair = abjad.duration.with_denominator(contents_duration, denominator)
        contents_duration_pair = pair
        contents_count = contents_duration_pair[0]
        if 0 < extra_count:
            extra_count %= contents_count
        elif extra_count < 0:
            extra_count = abs(extra_count)
            extra_count %= python_math.ceil(contents_count / 2.0)
            extra_count *= -1
        new_contents_count = contents_count + extra_count
        tuplet_multiplier = abjad.Fraction(new_contents_count, contents_count)
        if not abjad.Duration(tuplet_multiplier).normalized():
            message = f"{tuplet!r} gives {tuplet_multiplier}"
            message += " with {contents_count} and {new_contents_count}."
            raise Exception(message)
        pair = abjad.duration.pair(tuplet_multiplier)
        multiplier = pair
    elif isinstance(treatment, str) and ":" in treatment:
        n, d = treatment.split(":")
        multiplier = (int(d), int(n))
    elif isinstance(treatment, abjad.Duration):
        tuplet_duration = treatment
        contents_duration = abjad.get.duration(tuplet)
        multiplier = tuplet_duration / contents_duration
        pair = abjad.duration.pair(multiplier)
        multiplier = pair
    else:
        raise Exception(f"bad treatment: {treatment!r}.")
    tuplet.multiplier = multiplier
    if not abjad.Duration(tuplet.multiplier).normalized():
        tuplet.normalize_multiplier()
    return tuplet


def style_accelerando(
    container: abjad.Container | abjad.Tuplet, exponent: float = 0.625
) -> abjad.Container | abjad.Tuplet:
    assert isinstance(container, abjad.Container), repr(container)
    assert isinstance(exponent, float), repr(exponent)
    return _style_accelerando(container, exponent)


def style_ritardando(
    container: abjad.Container | abjad.Tuplet, exponent: float = 1.625
) -> abjad.Container | abjad.Tuplet:
    assert isinstance(container, abjad.Container), repr(container)
    assert isinstance(exponent, float), repr(exponent)
    return _style_accelerando(container, exponent)


# ALIASES


def A(items, numerator):
    denominator = 16
    return Feather(items, denominator, numerator, exponent=0.625)


def AG(*arguments):
    return AfterGrace(*arguments)


def BG(*arguments, **keywords):
    return BeforeGrace(*arguments, **keywords)


def C(*arguments):
    return Container(*arguments)


def IAG(*arguments):
    return IndependentAfterGrace(*arguments)


def R(items, numerator):
    denominator = 16
    return Feather(items, denominator, numerator, exponent=1.625)


def T(items, extra_counts):
    return Tuplet(items, extra_counts)


def TC(items, extra_counts):
    return TremoloContainer(items, extra_counts)


def bl(argument):
    return BeamLeft(argument)


def br(argument):
    return BeamRight(argument)


def c(numerator, note_head_count):
    return Chord(numerator, note_head_count)


def h(argument):
    return InvisibleMusic(argument)


def m(argument, multiplier):
    return Multiplier(argument, multiplier)


def rt(argument):
    return RepeatTie(argument)


def t(argument):
    return Tie(argument)


def w(real_n, written_n):
    return WrittenDuration(real_n, written_n)
