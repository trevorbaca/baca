"""
Figures.
"""
import copy
import dataclasses
import fractions
import math as python_math
import types
import typing
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import cursor as _cursor
from . import select as _select
from . import tags as _tags
from .enums import enums as _enums

SimpleNamespace = types.SimpleNamespace


def _get_figure_start_offset(figure_name, voice_name_to_timespans):
    assert isinstance(figure_name, str)
    for voice_name in sorted(voice_name_to_timespans.keys()):
        for timespan in voice_name_to_timespans[voice_name]:
            leaf_start_offset = timespan.start_offset
            leaves = abjad.iterate.leaves(timespan.annotation)
            for leaf in leaves:
                if abjad.get.annotation(leaf, "figure_name") == figure_name:
                    return leaf_start_offset
                leaf_duration = abjad.get.duration(leaf)
                leaf_start_offset += leaf_duration
    raise Exception(f"can not find figure {figure_name!r}.")


def _get_leaf_timespan(leaf, timespans):
    assert all(isinstance(_, abjad.Timespan) for _ in timespans), repr(timespans)
    found_leaf = False
    for timespan in timespans:
        leaf_start_offset = abjad.Offset(0)
        for leaf_ in abjad.iterate.leaves(timespan.annotation):
            leaf_duration = abjad.get.duration(leaf_)
            if leaf_ is leaf:
                found_leaf = True
                break
            leaf_start_offset += leaf_duration
        if found_leaf:
            break
    if not found_leaf:
        raise Exception(f"can not find {leaf!r} in timespans.")
    leaf_start_offset = timespan.start_offset + leaf_start_offset
    leaf_stop_offset = leaf_start_offset + leaf_duration
    return abjad.Timespan(leaf_start_offset, leaf_stop_offset)


def _get_start_offset(
    containers, contribution, voice_name_to_timespans, current_offset, score_stop_offset
):
    assert all(isinstance(_, abjad.Container) for _ in containers), repr(containers)
    if contribution.anchor is not None and contribution.anchor.figure_name is not None:
        figure_name = contribution.anchor.figure_name
        start_offset = _get_figure_start_offset(
            figure_name,
            voice_name_to_timespans,
        )
        return start_offset
    anchored = False
    if contribution.anchor is not None:
        remote_voice_name = contribution.anchor.remote_voice_name
        remote_selector = contribution.anchor.remote_selector
        use_remote_stop_offset = contribution.anchor.use_remote_stop_offset
        anchored = True
    else:
        remote_voice_name = None
        remote_selector = None
        use_remote_stop_offset = None
    if not anchored:
        return current_offset
    if anchored and remote_voice_name is None:
        return score_stop_offset
    timespans = voice_name_to_timespans[remote_voice_name]
    container_lists = [_.annotation for _ in timespans]
    for container_list in container_lists:
        assert all(isinstance(_, abjad.Container) for _ in container_list)
    if remote_selector is None:
        result = abjad.select.leaf(container_lists, 0)
    else:
        result = remote_selector(container_lists)
    selected_leaves = list(abjad.iterate.leaves(result))
    first_selected_leaf = selected_leaves[0]
    timespan = _get_leaf_timespan(first_selected_leaf, timespans)
    if use_remote_stop_offset:
        remote_anchor_offset = timespan.stop_offset
    else:
        remote_anchor_offset = timespan.start_offset
    local_anchor_offset = abjad.Offset(0)
    if contribution.anchor is not None:
        local_selector = contribution.anchor.local_selector
    else:
        local_selector = None
    if local_selector is not None:
        result = local_selector(containers)
        selected_leaves = list(abjad.iterate.leaves(result))
        first_selected_leaf = selected_leaves[0]
        dummy_container = abjad.Container(containers)
        timespan = abjad.get.timespan(first_selected_leaf)
        del dummy_container[:]
        local_anchor_offset = timespan.start_offset
    start_offset = remote_anchor_offset - local_anchor_offset
    return start_offset


def _make_accelerando(leaves, *, ritardando=False):
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    tuplet = abjad.Tuplet("1:1", leaves, hide=False)
    if len(tuplet) == 1:
        return tuplet
    if ritardando:
        exponent = 1.625
    else:
        exponent = 0.625
    durations = [abjad.get.duration(_) for _ in leaves]
    multipliers = _make_accelerando_multipliers(durations, exponent)
    assert len(leaves) == len(multipliers)
    for multiplier, leaf in zip(multipliers, leaves):
        leaf.multiplier = multiplier
    rmakers.feather_beam([tuplet])
    rmakers.duration_bracket(tuplet)
    return tuplet


def _make_accelerando_multipliers(durations, exponent) -> list[tuple[int, int]]:
    sums = abjad.math.cumulative_sums(durations)
    generator = abjad.sequence.nwise(sums, n=2)
    pairs = list(generator)
    total_duration = pairs[-1][-1]
    start_offsets = [_[0] for _ in pairs]
    start_offsets = [_ / total_duration for _ in start_offsets]
    start_offsets_ = []
    for start_offset in start_offsets:
        start_offset_ = rmakers.rmakers._interpolate_exponential(
            0, total_duration, start_offset, exponent
        )
        start_offsets_.append(start_offset_)
    start_offsets_.append(float(total_duration))
    durations_ = abjad.math.difference_series(start_offsets_)
    durations_ = rmakers.rmakers._round_durations(durations_, 2**10)
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


def _make_figure_tuplets(
    talea,
    treatments,
    collections,
    next_attack,
    next_segment,
    collection_index=None,
    total_collections=None,
) -> tuple[list[abjad.Tuplet], int, int]:
    tuplets = []
    if collection_index is None:
        for i, segment in enumerate(collections):
            tuplet, next_attack, next_segment = _make_figure_tuplet(
                talea,
                treatments,
                segment,
                next_attack,
                next_segment,
            )
            tuplets.append(tuplet)
    else:
        assert len(collections) == 1, repr(collections)
        segment = collections[0]
        tuplet, next_attack, next_segment = _make_figure_tuplet(
            talea,
            treatments,
            segment,
            next_attack,
            next_segment,
        )
        tuplets.append(tuplet)
    assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
    return tuplets, next_attack, next_segment


def _make_figure_tuplet(
    talea,
    treatments,
    segment,
    next_attack,
    next_segment,
) -> tuple[abjad.Tuplet, int, int]:
    next_segment += 1
    leaves = []
    if treatments:
        treatment = abjad.CyclicTuple(treatments)[next_segment - 1]
    else:
        treatment = 0
    if isinstance(segment, set | frozenset):
        segment = [segment]
    for pitch_expression in segment:
        is_chord = False
        if isinstance(pitch_expression, set | frozenset):
            is_chord = True
        prototype = abjad.NumberedPitchClass
        if isinstance(pitch_expression, prototype):
            pitch_expression = pitch_expression.number
        count = next_attack
        while abjad.Fraction(*talea[count]) < 0:
            next_attack += 1
            this_one = talea[count]
            duration = -abjad.Duration(*this_one)
            leaves_ = abjad.makers.make_leaves(
                [None], [duration], tag=_tags.function_name(_frame(), n=1)
            )
            leaves.extend(leaves_)
            count = next_attack
        next_attack += 1
        this_one = talea[count]
        duration = this_one
        assert 0 < abjad.Duration(duration), repr(duration)
        if (
            isinstance(pitch_expression, tuple)
            and len(pitch_expression) == 2
            and pitch_expression[-1] in (None, "skip")
        ):
            multiplier = pitch_expression[0]
            duration = (
                multiplier.numerator,
                multiplier.denominator * talea.denominator,
            )
            pitch_expression = None
        if is_chord:
            leaves_ = abjad.makers.make_leaves(
                [tuple(pitch_expression)],
                [duration],
                tag=_tags.function_name(_frame(), n=2),
            )
        else:
            leaves_ = abjad.makers.make_leaves(
                [pitch_expression], [duration], tag=_tags.function_name(_frame(), n=3)
            )
        leaves.extend(leaves_)
        count = next_attack
        while abjad.Fraction(*talea[count]) < 0 and not count % len(talea) == 0:
            next_attack += 1
            this_one = talea[count]
            duration = -abjad.Duration(*this_one)
            leaves_ = abjad.makers.make_leaves(
                [None], [duration], tag=_tags.function_name(_frame(), n=4)
            )
            leaves.extend(leaves_)
            count = next_attack
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    assert isinstance(talea, rmakers.Talea), repr(talea)
    leaf_list = leaves
    if isinstance(treatment, int):
        extra_count = treatment
        denominator = talea.denominator
        contents_duration = abjad.get.duration(leaf_list)
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
            message = f"{leaf_list!r} gives {tuplet_multiplier}"
            message += " with {contents_count} and {new_contents_count}."
            raise Exception(message)
        pair = abjad.duration.pair(tuplet_multiplier)
        tuplet = abjad.Tuplet(pair, leaf_list)
    elif treatment in ("accel", "rit"):
        tuplet = _make_accelerando(leaf_list, ritardando=treatment == "rit")
    elif isinstance(treatment, str) and ":" in treatment:
        numerator_str, denominator_str = treatment.split(":")
        numerator, denominator = int(numerator_str), int(denominator_str)
        tuplet = abjad.Tuplet((denominator, numerator), leaf_list)
    elif treatment.__class__ is abjad.Duration:
        tuplet_duration = treatment
        contents_duration = abjad.get.duration(leaf_list)
        multiplier = tuplet_duration / contents_duration
        tuplet = abjad.Tuplet(multiplier, leaf_list)
        if not abjad.Duration(tuplet.multiplier).normalized():
            tuplet.normalize_multiplier()
    elif isinstance(treatment, abjad.Fraction):
        tuplet = abjad.Tuplet(treatment, leaf_list)
    elif isinstance(treatment, tuple) and len(treatment) == 2:
        tuplet_duration = abjad.Duration(treatment)
        contents_duration = abjad.get.duration(leaf_list)
        multiplier = tuplet_duration / contents_duration
        pair = abjad.duration.pair(multiplier)
        tuplet = abjad.Tuplet(pair, leaf_list)
        if not abjad.Duration(tuplet.multiplier).normalized():
            tuplet.normalize_multiplier()
    else:
        raise Exception(f"bad time treatment: {treatment!r}.")
    assert isinstance(tuplet, abjad.Tuplet)
    if tuplet.trivial():
        tuplet.hide = True
    assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
    return tuplet, next_attack, next_segment


def _matches_pitch(pitched_leaf, pitch_object):
    if pitch_object is None:
        return False
    if isinstance(pitched_leaf, abjad.Note):
        written_pitches = [pitched_leaf.written_pitch]
    elif isinstance(pitched_leaf, abjad.Chord):
        written_pitches = pitched_leaf.written_pitches
    else:
        raise TypeError(pitched_leaf)
    if isinstance(pitch_object, int | float):
        source = [_.number for _ in written_pitches]
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
    if isinstance(logical_tie.head, abjad.Note):
        return
    assert isinstance(logical_tie.head, abjad.Chord), repr(logical_tie)
    if isinstance(pitch_object, abjad.PitchClass):
        raise NotImplementedError(logical_tie, pitch_object)
    for chord in logical_tie:
        duration = chord.written_duration
        note = abjad.Note(pitch_object, duration)
        abjad.mutate.replace(chord, [note])


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Accelerando:
    denominator: int
    items: list
    numerator: int
    coefficient: fractions.Fraction | None = None
    ritardando: bool = False

    def __post_init__(self):
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert isinstance(self.items, list), repr(self.items)
        assert isinstance(self.numerator, int), repr(self.numerator)
        assert isinstance(self.ritardando, bool), repr(self.ritardando)

    def __call__(self):
        pass


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
class Anchor:
    """
    Anchor.

    ``use_remote_stop_offset`` is true when contribution anchors to remote components'
    stop offset; otherwise anchors to remote components' start offset.
    """

    figure_name: str | None = None
    local_selector: typing.Callable | None = None
    remote_selector: typing.Callable | None = None
    remote_voice_name: str | None = None
    use_remote_stop_offset: bool = False

    def __post_init__(self):
        if self.figure_name is not None:
            assert isinstance(self.figure_name, str), repr(self.figure_name)
        if self.local_selector is not None and not callable(self.local_selector):
            raise TypeError(f"must be callable: {self.local_selector!r}.")
        if self.remote_selector is not None and not callable(self.remote_selector):
            raise TypeError(f"must be callable: {self.remote_selector!r}.")
        if self.remote_voice_name is not None:
            assert isinstance(self.remote_voice_name, str), repr(self.remote_voice_name)
        assert isinstance(self.use_remote_stop_offset, bool), repr(
            self.use_remote_stop_offset
        )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Contribution:
    voice_name_to_containers: dict[str, list]
    anchor: Anchor | None = None
    hide_time_signature: bool | None = None
    time_signature: abjad.TimeSignature | None = None

    def __post_init__(self):
        assert isinstance(self.voice_name_to_containers, dict), repr(
            self.voice_name_to_containers
        )
        for value in self.voice_name_to_containers.values():
            assert isinstance(value, list), repr(value)
            assert len(value) == 1, repr(value)
            assert isinstance(value[0], abjad.Container), repr(value)
        if self.anchor is not None:
            assert isinstance(self.anchor, Anchor), repr(self.anchor)
        if self.hide_time_signature is not None:
            assert isinstance(self.hide_time_signature, bool), repr(
                self.hide_time_signature
            )
        if self.time_signature is not None:
            assert isinstance(self.time_signature, abjad.TimeSignature)


class Accumulator:
    __slots__ = (
        "current_offset",
        "figure_number",
        "music_maker",
        "score_stop_offset",
        "voice_names",
        "score",
        "time_signatures",
        "voice_name_to_timespans",
    )

    def __init__(self, score: abjad.Score) -> None:
        assert isinstance(score, abjad.Score), repr(score)
        self.score = score
        voice_names = []
        for voice in abjad.iterate.components(score, abjad.Voice):
            voice_names.append(voice.name)
        self.voice_names = voice_names
        self.current_offset = abjad.Offset(0)
        self.figure_number = 1
        self.score_stop_offset = abjad.Offset(0)
        self.time_signatures: list[abjad.TimeSignature] = []
        self.voice_name_to_timespans: dict = dict([(_, []) for _ in self.voice_names])

    def assemble(self, voice_name: str) -> list[abjad.Component]:
        timespans = self.voice_name_to_timespans[voice_name]
        total_duration = sum([_.duration for _ in self.time_signatures])
        for timespan in timespans:
            assert isinstance(timespan, abjad.Timespan)
        timespans = list(timespans)
        timespans.sort()
        try:
            first_start_offset = timespans[0].start_offset
        except Exception:
            first_start_offset = abjad.Offset(0)
        timespan_list = abjad.TimespanList(timespans)
        if timespan_list:
            gaps = ~timespan_list
        else:
            sectionwide_gap = abjad.Timespan(0, total_duration)
            gaps = abjad.TimespanList([sectionwide_gap])
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        if timespans:
            final_stop_offset = timespans[-1].stop_offset
        else:
            final_stop_offset = total_duration
        if final_stop_offset < total_duration:
            final_gap = abjad.Timespan(final_stop_offset, total_duration)
            gaps.append(final_gap)
        timespans = timespans + list(gaps)
        timespans.sort()
        components = []
        for timespan in timespans:
            if timespan.annotation is not None:
                components_ = timespan.annotation
            else:
                components_ = [abjad.Skip(1, multiplier=timespan.duration.pair)]
            components.extend(components_)
        return components

    def cache(
        self,
        voice_name: str,
        tuplets: abjad.Container | list[abjad.Tuplet],
        *,
        anchor: Anchor | None = None,
        do_not_increment: bool = False,
        hide_time_signature: bool | None = None,
        imbrications: dict[str, list[abjad.Container]] | None = None,
        tsd: int | None = None,
    ):
        assert isinstance(voice_name, str), repr(voice_name)
        assert all(isinstance(_, abjad.Tuplet) for _ in tuplets), repr(tuplets)
        if isinstance(tuplets, abjad.Container):
            container = tuplets
        else:
            container = abjad.Container(tuplets)
        imbrications = imbrications or {}
        assert isinstance(imbrications, dict), repr(imbrications)
        duration = abjad.get.duration(container)
        if tsd is not None:
            pair = abjad.duration.with_denominator(duration, tsd)
        else:
            pair = duration.pair
        time_signature = abjad.TimeSignature(pair)
        voice_name_to_containers = {voice_name: [container]}
        assert isinstance(imbrications, dict)
        for voice_name, containers in imbrications.items():
            assert all(isinstance(_, abjad.Container) for _ in containers), repr(
                containers
            )
            voice_name_to_containers[voice_name] = containers
        if anchor is not None:
            anchor = dataclasses.replace(
                anchor, remote_voice_name=anchor.remote_voice_name
            )
        contribution = Contribution(
            voice_name_to_containers,
            anchor=anchor,
            hide_time_signature=hide_time_signature,
            time_signature=time_signature,
        )
        for voice_name, containers in contribution.voice_name_to_containers.items():
            start_offset = _get_start_offset(
                containers,
                contribution,
                self.voice_name_to_timespans,
                self.current_offset,
                self.score_stop_offset,
            )
            stop_offset = start_offset + abjad.get.duration(containers)
            timespan = abjad.Timespan(start_offset, stop_offset)
            timespan = abjad.Timespan(
                timespan.start_offset,
                timespan.stop_offset,
                annotation=containers,
            )
            self.voice_name_to_timespans[voice_name].append(timespan)
        self.current_offset = stop_offset
        self.score_stop_offset = max(self.score_stop_offset, stop_offset)
        if not contribution.hide_time_signature:
            if (
                contribution.anchor is None
                or contribution.hide_time_signature is False
                or (
                    contribution.anchor
                    and contribution.anchor.remote_voice_name is None
                )
            ):
                assert isinstance(contribution.time_signature, abjad.TimeSignature)
                self.time_signatures.append(contribution.time_signature)

    def populate(self, score):
        assert isinstance(score, abjad.Score), repr(score)
        for voice_name in sorted(self.voice_name_to_timespans):
            components = self.assemble(voice_name)
            if components:
                voice = score[voice_name]
                voice.extend(components)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Grace:
    denominator: int
    grace_note_numerators: list[int]
    main_note_numerator: int

    def __post_init__(self):
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert isinstance(self.main_note_numerator, int), repr(self.main_note_numerator)
        assert all(isinstance(_, int) for _ in self.grace_note_numerators), repr(
            self.grace_note_numerators
        )

    def __call__(self):
        main_duration = abjad.Duration(abs(self.main_note_numerator), self.denominator)
        if 0 < self.main_note_numerator:
            pitch = 0
        else:
            pitch = None
        main_components = abjad.makers.make_leaves([pitch], main_duration)
        first_leaf = abjad.get.leaf(main_components, 0)
        grace_durations = [
            abjad.Duration(abs(_), self.denominator) for _ in self.grace_note_numerators
        ]
        pitches = []
        for grace_note_numerator in self.grace_note_numerators:
            if 0 < grace_note_numerator:
                pitches.append(0)
            else:
                pitches.append(None)
        grace_leaves = abjad.makers.make_leaves(pitches, grace_durations)
        grace_container = abjad.BeforeGraceContainer(grace_leaves)
        abjad.attach(grace_container, first_leaf)
        return main_components


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OBGC:
    denominator: int
    grace_note_numerators: list[int]
    main_note_numerator: int

    def __post_init__(self):
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert all(isinstance(_, int) for _ in self.grace_note_numerators), repr(
            self.grace_note_numerators
        )
        assert isinstance(self.main_note_numerator, int), repr(self.main_note_numerator)

    def __call__(self):
        pass


def anchor(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to start offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
    )


def anchor_after(
    remote_voice_name: str,
    remote_selector=None,
    local_selector=None,
) -> Anchor:
    """
    Anchors music in this figure (filtered by ``local_selector``) to stop offset of
    ``remote_voice_name`` (filtered by ``remote_selector``).
    """
    return Anchor(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def anchor_to_figure(figure_name: str) -> Anchor:
    """
    Anchors music in this figure to start of ``figure_name``.
    """
    return Anchor(figure_name=figure_name)


def attach_before_grace_containers(before_grace_containers, tuplet):
    tag = _tags.function_name(_frame())
    if before_grace_containers is None:
        return
    logical_ties = abjad.iterate.logical_ties(tuplet)
    pairs = zip(before_grace_containers, logical_ties)
    for before_grace_container, logical_tie in pairs:
        if before_grace_container is None:
            continue
        abjad.attach(before_grace_container, logical_tie.head, tag=tag)


def figure(
    collections,
    counts: typing.Sequence[int],
    denominator: int,
    *,
    tsd: int | None = None,
    treatments: typing.Sequence = (),
) -> list[abjad.Tuplet]:
    if hasattr(collections, "argument"):
        collections = collections.argument
    prototype = (
        abjad.PitchClassSegment,
        abjad.PitchSegment,
        set,
        frozenset,
    )
    if isinstance(collections, prototype):
        collections = [collections]
    collection_prototype = (
        abjad.PitchClassSegment,
        abjad.PitchSegment,
        abjad.PitchSet,
        list,
        set,
    )
    pitch_prototype = (int, float, str, abjad.NumberedPitch)
    for collection in collections:
        assert isinstance(collection, collection_prototype), repr(collection)
        if isinstance(collection, list | set):
            assert all(isinstance(_, pitch_prototype) for _ in collection), repr(
                collection
            )
    assert all(isinstance(_, int) for _ in counts), repr(counts)
    talea = rmakers.Talea(counts=counts, denominator=denominator)
    next_attack, next_segment = 0, 0
    tuplets: list[abjad.Tuplet] = []
    tuplets_, next_attack, next_segment = _make_figure_tuplets(
        talea,
        treatments,
        collections,
        next_attack,
        next_segment,
    )
    tuplets.extend(tuplets_)
    assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
    return tuplets


def imbricate(
    container: abjad.Container,
    voice_name: str,
    segment: list,
    *commands: typing.Any,
    allow_unused_pitches: bool = False,
    by_pitch_class: bool = False,
    hocket: bool = False,
    truncate_ties: bool = False,
) -> dict[str, list]:
    if isinstance(container, list):
        container = abjad.Container(container)
    original_container = container
    container = copy.deepcopy(container)
    abjad.override(container).TupletBracket.stencil = False
    abjad.override(container).TupletNumber.stencil = False
    segment = abjad.sequence.flatten(segment, depth=-1)
    if by_pitch_class:
        segment = [abjad.NumberedPitchClass(_) for _ in segment]
    cursor = _cursor.Cursor(singletons=True, source=segment, suppress_exception=True)
    pitch_number = cursor.next()
    original_logical_ties = abjad.select.logical_ties(original_container)
    logical_ties = abjad.select.logical_ties(container)
    pairs = zip(logical_ties, original_logical_ties)
    for logical_tie, original_logical_tie in pairs:
        if isinstance(logical_tie.head, abjad.Rest):
            for leaf in logical_tie:
                duration = leaf.written_duration
                skip = abjad.Skip(duration)
                abjad.mutate.replace(leaf, [skip])
        elif isinstance(logical_tie.head, abjad.Skip):
            pass
        elif _matches_pitch(logical_tie.head, pitch_number):
            _trim_matching_chord(logical_tie, pitch_number)
            pitch_number = cursor.next()
            if truncate_ties:
                head = logical_tie.head
                tail = logical_tie.tail
                for leaf in logical_tie[1:]:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
                abjad.detach(abjad.Tie, head)
                next_leaf = abjad.get.leaf(tail, 1)
                if next_leaf is not None:
                    abjad.detach(abjad.RepeatTie, next_leaf)
            if hocket:
                for leaf in original_logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
        else:
            for leaf in logical_tie:
                duration = leaf.written_duration
                skip = abjad.Skip(duration)
                abjad.mutate.replace(leaf, [skip])
    if not allow_unused_pitches and not cursor.exhausted:
        assert cursor.position is not None
        current, total = cursor.position - 1, len(cursor)
        raise Exception(f"{cursor!r} used only {current} of {total} pitches.")
    for command in commands:
        command(container)
    if not hocket:
        pleaves = _select.pleaves(container)
        assert isinstance(pleaves, list)
        for pleaf in pleaves:
            abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
    return {voice_name: [container]}


def label_figure(
    tuplets, figure_name, accumulator, direction=None, do_not_increment=False
):
    figure_number = accumulator.figure_number
    if not do_not_increment:
        accumulator.figure_number += 1
    parts = figure_name.split("_")
    if len(parts) == 1:
        body = parts[0]
        figure_label_string = f'"{body}"'
    elif len(parts) == 2:
        body, subscript = parts
        figure_label_string = rf'\concat {{ "{body}" \sub {subscript} }}'
    else:
        raise Exception(f"unrecognized figure name: {figure_name!r}.")
    string = r"\markup"
    string += rf" \concat {{ [ \raise #0.25 \fontsize #-2 ({figure_number})"
    if figure_name:
        string += rf" \hspace #1 {figure_label_string} ] }}"
    else:
        string += r" ] }"
    figure_label_markup = abjad.Markup(string)
    bundle = abjad.bundle(figure_label_markup, r"- \tweak color #blue")
    leaf = abjad.select.leaf(tuplets, 0)
    abjad.annotate(leaf, "figure_name", figure_name)
    if not do_not_increment:
        pleaves = _select.pleaves(tuplets)
        if pleaves:
            leaf = pleaves[0]
        else:
            leaf = abjad.select.leaf(tuplets, 0)
        abjad.attach(
            bundle,
            leaf,
            deactivate=True,
            direction=direction,
            tag=_tags.FIGURE_LABEL,
        )


def lmr(
    *,
    left_counts: typing.Sequence[int] = (),
    left_cyclic: bool = False,
    left_length: int = 0,
    left_reversed: bool = False,
    middle_counts: typing.Sequence[int] = (),
    middle_cyclic: bool = False,
    middle_reversed: bool = False,
    priority: int | None = None,
    right_counts: typing.Sequence[int] = (),
    right_cyclic: bool = False,
    right_length: int = 0,
    right_reversed: bool = False,
) -> LMR:
    return LMR(
        left_counts=left_counts,
        left_cyclic=left_cyclic,
        left_length=left_length,
        left_reversed=left_reversed,
        middle_counts=middle_counts,
        middle_cyclic=middle_cyclic,
        middle_reversed=middle_reversed,
        priority=priority,
        right_counts=right_counts,
        right_cyclic=right_cyclic,
        right_length=right_length,
        right_reversed=right_reversed,
    )


def make_before_grace_containers(
    collection, lmr: LMR, *, duration: abjad.Duration = abjad.Duration(1, 16)
):
    assert isinstance(collection, list), repr(collection)
    assert isinstance(duration, abjad.Duration), repr(duration)
    assert isinstance(lmr, LMR), repr(LMR)
    segment_parts = lmr(collection)
    segment_parts = [_ for _ in segment_parts if _]
    collection = [_[-1] for _ in segment_parts]
    before_grace_containers: list[abjad.BeforeGraceContainer | None] = []
    for segment_part in segment_parts:
        if len(segment_part) <= 1:
            before_grace_containers.append(None)
            continue
        grace_token = list(segment_part[:-1])
        grace_leaves = abjad.makers.make_leaves(
            grace_token, [duration], tag=_tags.function_name(_frame(), n=1)
        )
        container = abjad.BeforeGraceContainer(
            grace_leaves,
            command=r"\acciaccatura",
            tag=_tags.function_name(_frame(), n=2),
        )
        if 1 < len(container):
            abjad.beam(
                container[:],
                tag=_tags.function_name(_frame(), n=3),
            )
        before_grace_containers.append(container)
    assert len(before_grace_containers) == len(collection)
    assert isinstance(collection, list), repr(collection)
    return before_grace_containers, collection


def nest(tuplets: list[abjad.Tuplet], treatment: str) -> abjad.Tuplet:
    assert isinstance(tuplets, list), repr(tuplets)
    assert all(isinstance(_, abjad.Tuplet) for _ in tuplets), repr(tuplets)
    assert isinstance(treatment, str), repr(treatment)
    if "/" in treatment:
        assert treatment.startswith("+") or treatment.startswith("-"), repr(treatment)
        addendum = abjad.Duration(treatment)
        contents_duration = abjad.get.duration(tuplets)
        target_duration = contents_duration + addendum
        multiplier = target_duration / contents_duration
        pair = abjad.duration.pair(multiplier)
        nested_tuplet = abjad.Tuplet(pair, [])
        abjad.mutate.wrap(tuplets, nested_tuplet)
    else:
        assert ":" in treatment
        nested_tuplet = abjad.Tuplet(treatment, [])
        abjad.mutate.wrap(tuplets, nested_tuplet)
    return nested_tuplet


def rests_after(
    tuplets: list[abjad.Tuplet], counts: list[int], denominator: int
) -> None:
    durations = [abjad.Duration(_, denominator) for _ in counts]
    rests = abjad.makers.make_leaves([None], durations)
    last_leaf = abjad.select.leaf(tuplets, -1)
    last_tuplet = abjad.get.parentage(last_leaf).parent
    assert isinstance(last_tuplet, abjad.Tuplet), repr(last_tuplet)
    last_tuplet.extend(rests)


def rests_around(
    tuplets: list[abjad.Tuplet],
    before_counts: list[int],
    after_counts: list[int],
    denominator: int,
) -> None:
    rests_before(tuplets, before_counts, denominator)
    rests_after(tuplets, after_counts, denominator)


def rests_before(
    tuplets: list[abjad.Tuplet], counts: list[int], denominator: int
) -> None:
    durations = [abjad.Duration(_, denominator) for _ in counts]
    rests = abjad.makers.make_leaves([None], durations)
    first_leaf = abjad.select.leaf(tuplets, 0)
    first_tuplet = abjad.get.parentage(first_leaf).parent
    assert isinstance(first_tuplet, abjad.Tuplet), repr(first_tuplet)
    first_tuplet[0:0] = rests


def resume() -> Anchor:
    """
    Resumes music at next offset across all voices in score.
    """
    return Anchor()


def resume_after(remote_voice_name) -> Anchor:
    """
    Resumes music after remote components.
    """
    return Anchor(
        remote_selector=lambda _: abjad.select.leaf(_, -1),
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def skips_before(
    tuplets: list[abjad.Tuplet], counts: list[int], denominator: int
) -> None:
    durations = [abjad.Duration(_, denominator) for _ in counts]
    rests = abjad.makers.make_leaves([None], durations)
    skips = [abjad.Skip(_) for _ in rests]
    first_leaf = abjad.select.leaf(tuplets, 0)
    first_tuplet = abjad.get.parentage(first_leaf).parent
    assert isinstance(first_tuplet, abjad.Tuplet), repr(first_tuplet)
    first_tuplet[0:0] = skips
