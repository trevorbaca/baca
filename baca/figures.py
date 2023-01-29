"""
Figures.
"""
import copy
import dataclasses
import math as python_math
import typing
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import cursor as _cursor
from . import select as _select
from . import tags as _tags
from .enums import enums as _enums


def _add_rest_affixes(
    leaves,
    talea,
    rest_prefix,
    rest_suffix,
    affix_skips_instead_of_rests,
    increase_monotonic,
):
    if rest_prefix:
        durations = [(_, talea.denominator) for _ in rest_prefix]
        leaves_ = abjad.makers.make_leaves(
            [None],
            durations,
            increase_monotonic=increase_monotonic,
            skips_instead_of_rests=affix_skips_instead_of_rests,
        )
        leaves[0:0] = leaves_
    if rest_suffix:
        durations = [(_, talea.denominator) for _ in rest_suffix]
        leaves_ = abjad.makers.make_leaves(
            [None],
            durations,
            increase_monotonic=increase_monotonic,
            skips_instead_of_rests=affix_skips_instead_of_rests,
        )
        leaves.extend(leaves_)
    return leaves


def _call_figure_maker(
    affix,
    talea,
    spelling,
    treatments,
    acciaccatura,
    collections: typing.Sequence,
    restart_talea: bool = False,
) -> list[abjad.Tuplet]:
    collections = _coerce_collections(collections)
    next_attack = 0
    next_segment = 0
    tuplets: list[abjad.Tuplet] = []
    if restart_talea:
        total_collections = len(collections)
        for i, collection in enumerate(collections):
            next_attack = 0
            next_segment = 0
            selection_, next_attack, next_segment = _make_figure_music(
                affix,
                talea,
                spelling,
                treatments,
                acciaccatura,
                [collection],
                next_attack,
                next_segment,
                collection_index=i,
                total_collections=total_collections,
            )
            tuplets.extend(selection_)
    else:
        selection_, next_attack, next_segment = _make_figure_music(
            affix,
            talea,
            spelling,
            treatments,
            acciaccatura,
            collections,
            next_attack,
            next_segment,
        )
        tuplets.extend(selection_)
    assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
    return tuplets


def _coerce_collections(collections):
    prototype = (
        abjad.PitchClassSegment,
        abjad.PitchSegment,
        set,
        frozenset,
    )
    if isinstance(collections, prototype):
        return [collections]
    return collections


def _collections_to_container(
    accumulator, voice_name, collections, *commands, tsd=None
):
    collection_prototype = (
        list,
        str,
        frozenset,
        set,
        abjad.PitchClassSegment,
        abjad.PitchSegment,
    )
    assert isinstance(collections, collection_prototype), repr(collections)
    command, figure_maker = None, None
    if isinstance(collections, str):
        tuplet = abjad.Tuplet((1, 1), collections, hide=True)
        tuplets = [tuplet]
    elif all(isinstance(_, abjad.Component) for _ in collections):
        tuplet = abjad.Tuplet((1, 1), collections, hide=True)
        tuplets = [tuplet]
    elif isinstance(commands[0], FigureMaker):
        figure_maker = commands[0]
        tuplets = figure_maker(collections)
        commands = commands[1:]
    else:
        raise Exception
    assert isinstance(tuplets, list), repr(tuplets)
    assert all(isinstance(_, abjad.Tuplet) for _ in tuplets), repr(tuplets)
    container = abjad.Container(tuplets)
    if tsd is None and figure_maker:
        tsd = figure_maker.tsd
    if tsd is None and command:
        tsd = command.assignments[0].maker.tsd
    imbrications = {}
    command_prototype = (rmakers.Command, Nest)
    for command in commands:
        if isinstance(command, Imbrication):
            voice_name_to_selection = command(container)
            imbrications.update(voice_name_to_selection)
        else:
            assert isinstance(command, command_prototype), repr(command)
            command(container)
    return container, imbrications, tsd


def _do_imbrication(
    container: abjad.Container,
    segment: list,
    voice_name: str,
    *commands,
    allow_unused_pitches: bool = False,
    by_pitch_class: bool = False,
    hocket: bool = False,
    truncate_ties: bool = False,
) -> dict[str, list]:
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
            if isinstance(pitch_number, Coat):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate.replace(leaf, [skip])
                pitch_number = cursor.next()
                continue
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
    if not allow_unused_pitches and not cursor.is_exhausted:
        assert cursor.position is not None
        current, total = cursor.position - 1, len(cursor)
        raise Exception(f"{cursor!r} used only {current} of {total} pitches.")
    for command in commands:
        command(container)
    selection = [container]
    if not hocket:
        pleaves = _select.pleaves(container)
        assert isinstance(pleaves, list)
        for pleaf in pleaves:
            abjad.attach(_enums.ALLOW_OCTAVE, pleaf)
    return {voice_name: selection}


def _do_nest_command(argument, *, lmr=None, treatments=None) -> list[abjad.Tuplet]:
    cyclic_treatments = abjad.CyclicTuple(treatments)
    assert cyclic_treatments is not None
    tuplets = []
    for item in argument:
        if isinstance(item, abjad.Tuplet):
            tuplets.append(item)
        else:
            assert isinstance(item, list), repr(item)
            assert len(item) == 1, repr(item)
            assert isinstance(item[0], abjad.Tuplet), repr(item)
            tuplet = item[0]
            tuplets.append(tuplet)
    if lmr is None:
        tuplet_selections = [tuplets]
    else:
        tuplet_selections = lmr(tuplets)
        tuplet_selections = [list(_) for _ in tuplet_selections]
    tuplets = []
    for i, tuplet_selection in enumerate(tuplet_selections):
        assert isinstance(tuplet_selection, list)
        treatment = cyclic_treatments[i]
        if treatment is None:
            tuplets.extend(tuplet_selection)
        else:
            assert isinstance(tuplet_selection, list)
            for tuplet in tuplet_selection:
                assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
            if isinstance(treatment, str):
                addendum = abjad.Duration(treatment)
                contents_duration = abjad.get.duration(tuplet_selection)
                target_duration = contents_duration + addendum
                multiplier = target_duration / contents_duration
                pair = multiplier.pair
                tuplet = abjad.Tuplet(pair, [])
                abjad.mutate.wrap(tuplet_selection, tuplet)
            elif treatment.__class__ is abjad.Multiplier:
                pair = treatment.pair
                tuplet = abjad.Tuplet(pair, [])
                abjad.mutate.wrap(tuplet_selection, tuplet)
            elif treatment.__class__ is abjad.Duration:
                target_duration = treatment
                contents_duration = abjad.get.duration(tuplet_selection)
                multiplier = target_duration / contents_duration
                pair = multiplier.pair
                tuplet = abjad.Tuplet(pair, [])
                abjad.mutate.wrap(tuplet_selection, tuplet)
            else:
                raise Exception(f"bad time treatment: {treatment!r}.")
            nested_tuplet = tuplet
            tuplets.append(nested_tuplet)
    return tuplets


def _fix_rounding_error(durations, total_duration):
    current_duration = sum(durations)
    if current_duration < total_duration:
        missing_duration = total_duration - current_duration
        if durations[0] < durations[-1]:
            durations[-1] += missing_duration
        else:
            durations[0] += missing_duration
    elif sum(durations) == total_duration:
        return durations
    elif total_duration < current_duration:
        extra_duration = current_duration - total_duration
        if durations[0] < durations[-1]:
            durations[-1] -= extra_duration
        else:
            durations[0] -= extra_duration
    assert sum(durations) == total_duration
    return durations


def _get_figure_start_offset(figure_name, floating_selections):
    for voice_name in sorted(floating_selections.keys()):
        for floating_selection in floating_selections[voice_name]:
            leaf_start_offset = floating_selection.start_offset
            leaves = abjad.iterate.leaves(floating_selection.annotation)
            for leaf in leaves:
                if abjad.get.annotation(leaf, "figure_name") == figure_name:
                    return leaf_start_offset
                leaf_duration = abjad.get.duration(leaf)
                leaf_start_offset += leaf_duration
    raise Exception(f"can not find figure {figure_name!r}.")


def _get_leaf_timespan(leaf, floating_selections):
    found_leaf = False
    for floating_selection in floating_selections:
        leaf_start_offset = abjad.Offset(0)
        for leaf_ in abjad.iterate.leaves(floating_selection.annotation):
            leaf_duration = abjad.get.duration(leaf_)
            if leaf_ is leaf:
                found_leaf = True
                break
            leaf_start_offset += leaf_duration
        if found_leaf:
            break
    if not found_leaf:
        raise Exception(f"can not find {leaf!r} in floating selections.")
    selection_start_offset = floating_selection.start_offset
    leaf_start_offset = selection_start_offset + leaf_start_offset
    leaf_stop_offset = leaf_start_offset + leaf_duration
    return abjad.Timespan(leaf_start_offset, leaf_stop_offset)


def _get_start_offset(
    selection, contribution, floating_selections, current_offset, score_stop_offset
):
    if contribution.anchor is not None and contribution.anchor.figure_name is not None:
        figure_name = contribution.anchor.figure_name
        start_offset = _get_figure_start_offset(
            figure_name,
            floating_selections,
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
    if remote_selector is None:

        def remote_selector(argument):
            return abjad.select.leaf(argument, 0)

    floating_selections_ = floating_selections[remote_voice_name]
    selections = [_.annotation for _ in floating_selections_]
    result = remote_selector(selections)
    selected_leaves = list(abjad.iterate.leaves(result))
    first_selected_leaf = selected_leaves[0]
    timespan = _get_leaf_timespan(first_selected_leaf, floating_selections_)
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
        result = local_selector(selection)
        selected_leaves = list(abjad.iterate.leaves(result))
        first_selected_leaf = selected_leaves[0]
        dummy_container = abjad.Container(selection)
        timespan = abjad.get.timespan(first_selected_leaf)
        del dummy_container[:]
        local_anchor_offset = timespan.start_offset
    start_offset = remote_anchor_offset - local_anchor_offset
    return start_offset


def _is_treatment(argument):
    if argument is None:
        return True
    elif isinstance(argument, int):
        return True
    elif isinstance(argument, str):
        return True
    elif isinstance(argument, tuple) and len(argument) == 2:
        return True
    elif isinstance(argument, abjad.Ratio):
        return True
    elif isinstance(argument, abjad.Multiplier):
        return True
    elif argument.__class__ is abjad.Duration:
        return True
    elif argument in ("accel", "rit"):
        return True
    return False


def _label_figure(container, figure_name, figure_label_direction, figure_number):
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
    pleaves = _select.pleaves(container)
    if pleaves:
        leaf = pleaves[0]
    else:
        leaf = abjad.select.leaf(container, 0)
    abjad.attach(
        bundle,
        leaf,
        deactivate=True,
        direction=figure_label_direction,
        tag=_tags.FIGURE_LABEL,
    )


def _make_accelerando(leaf_selection, accelerando_indicator):
    assert accelerando_indicator in ("accel", "rit")
    tuplet = abjad.Tuplet((1, 1), leaf_selection, hide=True)
    if len(tuplet) == 1:
        return tuplet
    durations = [abjad.get.duration(_) for _ in leaf_selection]
    if accelerando_indicator == "accel":
        exponent = 0.625
    elif accelerando_indicator == "rit":
        exponent = 1.625
    multipliers = _make_accelerando_multipliers(durations, exponent)
    assert len(leaf_selection) == len(multipliers)
    for multiplier, leaf in zip(multipliers, leaf_selection):
        leaf.multiplier = multiplier
    if rmakers.rmakers._is_accelerando(leaf_selection):
        abjad.override(leaf_selection[0]).Beam.grow_direction = abjad.RIGHT
    elif rmakers.rmakers._is_ritardando(leaf_selection):
        abjad.override(leaf_selection[0]).Beam.grow_direction = abjad.LEFT
    duration = abjad.get.duration(tuplet)
    notes = abjad.makers.make_notes([0], [duration])
    string = abjad.illustrators.selection_to_score_markup_string(notes)
    string = rf"\markup \scale #'(0.75 . 0.75) {string}"
    abjad.override(tuplet).TupletNumber.text = string
    return tuplet


def _make_accelerando_multipliers(durations, exponent):
    r"""
    Makes accelerando multipliers.

    ..  container:: example

        Set exponent less than 1 for decreasing durations:

        >>> durations = 4 * [abjad.Duration(1)]
        >>> result = baca.figures._make_accelerando_multipliers(durations, 0.5)
        >>> for multiplier in result: multiplier
        ...
        (2048, 1024)
        (848, 1024)
        (651, 1024)
        (549, 1024)

    ..  container:: example

        Set exponent to 1 for trivial multipliers:

        >>> durations = 4 * [abjad.Duration(1)]
        >>> result = baca.figures._make_accelerando_multipliers(durations, 1)
        >>> for multiplier in result: multiplier
        ...
        (1024, 1024)
        (1024, 1024)
        (1024, 1024)
        (1024, 1024)

    ..  container:: example

        Set exponent greater than 1 for increasing durations:

        >>> durations = 4 * [abjad.Duration(1)]
        >>> result = baca.figures._make_accelerando_multipliers(
        ...     durations,
        ...     0.5,
        ... )
        >>> for multiplier in result: multiplier
        ...
        (2048, 1024)
        (848, 1024)
        (651, 1024)
        (549, 1024)

    Set exponent greater than 1 for ritardando.

    Set exponent less than 1 for accelerando.
    """
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
    durations_ = _fix_rounding_error(durations_, total_duration)
    multipliers = []
    assert len(durations) == len(durations_)
    for duration_, duration in zip(durations_, durations):
        multiplier = duration_ / duration
        multiplier = abjad.Multiplier(multiplier)
        multiplier = multiplier.with_denominator(2**10)
        multipliers.append(multiplier)
    multipliers = [_.pair for _ in multipliers]
    return multipliers


def _make_figure_music(
    affix,
    talea,
    spelling,
    treatments,
    acciaccatura,
    collections,
    next_attack,
    next_segment,
    collection_index=None,
    total_collections=None,
) -> tuple[list[abjad.Tuplet], int, int]:
    segment_count = len(collections)
    tuplets = []
    if collection_index is None:
        for i, segment in enumerate(collections):
            if affix is not None:
                result = affix(i, segment_count)
                rest_prefix, rest_suffix = result
                affix_skips_instead_of_rests = affix.skips_instead_of_rests
            else:
                rest_prefix, rest_suffix = None, None
                affix_skips_instead_of_rests = None
            tuplet, next_attack, next_segment = _make_figure_tuplet(
                talea,
                spelling,
                treatments,
                acciaccatura,
                segment,
                next_attack,
                next_segment,
                rest_prefix=rest_prefix,
                rest_suffix=rest_suffix,
                affix_skips_instead_of_rests=affix_skips_instead_of_rests,
            )
            tuplets.append(tuplet)
    else:
        assert len(collections) == 1, repr(collections)
        segment = collections[0]
        if affix is not None:
            result = affix(collection_index, total_collections)
            rest_prefix, rest_suffix = result
            affix_skips_instead_of_rests = affix.skips_instead_of_rests
        else:
            rest_prefix, rest_suffix = None, None
            affix_skips_instead_of_rests = None
        tuplet, next_attack, next_segment = _make_figure_tuplet(
            talea,
            spelling,
            treatments,
            acciaccatura,
            segment,
            next_attack,
            next_segment,
            rest_prefix=rest_prefix,
            rest_suffix=rest_suffix,
            affix_skips_instead_of_rests=affix_skips_instead_of_rests,
        )
        tuplets.append(tuplet)
    assert all(isinstance(_, abjad.Tuplet) for _ in tuplets)
    return tuplets, next_attack, next_segment


def _make_figure_tuplet(
    talea,
    spelling,
    treatments,
    acciaccatura,
    segment,
    next_attack,
    next_segment,
    rest_prefix=None,
    rest_suffix=None,
    affix_skips_instead_of_rests=None,
) -> tuple[abjad.Tuplet, int, int]:
    spelling = spelling or rmakers.Spelling()
    next_segment += 1
    leaves = []
    current_selection = next_segment - 1
    if treatments:
        treatment = abjad.CyclicTuple(treatments)[current_selection]
    else:
        treatment = 0
    before_grace_containers = None
    if acciaccatura is not None:
        if isinstance(segment, set | frozenset):
            raise Exception("decide how to model chords with acciaccatura.")
        before_grace_containers, segment = acciaccatura(segment)
        assert len(before_grace_containers) == len(segment)
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
        while talea[count] < 0:
            next_attack += 1
            this_one = talea[count]
            duration = -this_one
            leaves_ = abjad.makers.make_leaves(
                [None], [duration], increase_monotonic=spelling.increase_monotonic
            )
            leaves.extend(leaves_)
            count = next_attack
        next_attack += 1
        this_one = talea[count]
        duration = this_one
        assert 0 < duration, repr(duration)
        skips_instead_of_rests = False
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
            if pitch_expression[-1] == "skip":
                skips_instead_of_rests = True
            pitch_expression = None
        if is_chord:
            leaves_ = abjad.makers.make_leaves(
                [tuple(pitch_expression)],
                [duration],
                increase_monotonic=spelling.increase_monotonic,
                skips_instead_of_rests=skips_instead_of_rests,
            )
        else:
            leaves_ = abjad.makers.make_leaves(
                [pitch_expression],
                [duration],
                increase_monotonic=spelling.increase_monotonic,
                skips_instead_of_rests=skips_instead_of_rests,
            )
        leaves.extend(leaves_)
        count = next_attack
        while talea[count] < 0 and not count % len(talea) == 0:
            next_attack += 1
            this_one = talea[count]
            duration = -this_one
            leaves_ = abjad.makers.make_leaves(
                [None], [duration], increase_monotonic=spelling.increase_monotonic
            )
            leaves.extend(leaves_)
            count = next_attack
    leaves = _add_rest_affixes(
        leaves,
        talea,
        rest_prefix,
        rest_suffix,
        affix_skips_instead_of_rests,
        spelling.increase_monotonic,
    )
    leaf_selection = list(leaves)
    if isinstance(treatment, int):
        tuplet = _make_tuplet_with_extra_count(
            leaf_selection, treatment, talea.denominator
        )
    elif treatment in ("accel", "rit"):
        tuplet = _make_accelerando(leaf_selection, treatment)
    elif isinstance(treatment, abjad.Ratio):
        numerator, denominator = treatment.numbers
        tuplet = abjad.Tuplet(f"{denominator}:{numerator}", leaf_selection)
    elif isinstance(treatment, str) and ":" in treatment:
        numerator_str, denominator_str = treatment.split(":")
        numerator, denominator = int(numerator_str), int(denominator_str)
        tuplet = abjad.Tuplet((denominator, numerator), leaf_selection)
    elif isinstance(treatment, abjad.Multiplier):
        tuplet = abjad.Tuplet(treatment, leaf_selection)
    elif treatment.__class__ is abjad.Duration:
        tuplet_duration = treatment
        contents_duration = abjad.get.duration(leaf_selection)
        multiplier = tuplet_duration / contents_duration
        tuplet = abjad.Tuplet(multiplier, leaf_selection)
        if not abjad.Multiplier(tuplet.multiplier).normalized():
            tuplet.normalize_multiplier()
    elif isinstance(treatment, tuple) and len(treatment) == 2:
        tuplet_duration = abjad.Duration(treatment)
        contents_duration = abjad.get.duration(leaf_selection)
        multiplier = tuplet_duration / contents_duration
        pair = multiplier.pair
        tuplet = abjad.Tuplet(pair, leaf_selection)
        if not abjad.Multiplier(tuplet.multiplier).normalized():
            tuplet.normalize_multiplier()
    else:
        raise Exception(f"bad time treatment: {treatment!r}.")
    assert isinstance(tuplet, abjad.Tuplet)
    tag = abjad.Tag("baca._make_figure_tuplet()")
    if before_grace_containers is not None:
        logical_ties = abjad.iterate.logical_ties(tuplet)
        pairs = zip(before_grace_containers, logical_ties)
        for before_grace_container, logical_tie in pairs:
            if before_grace_container is None:
                continue
            abjad.attach(before_grace_container, logical_tie.head, tag=tag)
    if tuplet.trivial():
        tuplet.hide = True
    assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
    return tuplet, next_attack, next_segment


def _make_tuplet_with_extra_count(leaf_selection, extra_count, denominator):
    contents_duration = abjad.get.duration(leaf_selection)
    contents_duration = contents_duration.with_denominator(denominator)
    contents_count = contents_duration.numerator
    if 0 < extra_count:
        extra_count %= contents_count
    elif extra_count < 0:
        extra_count = abs(extra_count)
        extra_count %= python_math.ceil(contents_count / 2.0)
        extra_count *= -1
    new_contents_count = contents_count + extra_count
    tuplet_multiplier = abjad.Multiplier(new_contents_count, contents_count)
    if not tuplet_multiplier.normalized():
        message = f"{leaf_selection!r} gives {tuplet_multiplier}"
        message += " with {contents_count} and {new_contents_count}."
        raise Exception(message)
    pair = tuplet_multiplier.pair
    tuplet = abjad.Tuplet(pair, leaf_selection)
    return tuplet


def _matches_pitch(pitched_leaf, pitch_object):
    if isinstance(pitch_object, Coat):
        pitch_object = pitch_object.argument
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
class Acciaccatura:

    durations: typing.Sequence[abjad.Duration] = (abjad.Duration(1, 16),)
    lmr: LMR = LMR()

    def __post_init__(self):
        assert all(isinstance(_, abjad.Duration) for _ in self.durations), repr(
            self.durations
        )
        assert isinstance(self.lmr, LMR), repr(self.lmr)

    def __call__(
        self, collection: list | None = None
    ) -> tuple[list[abjad.BeforeGraceContainer | None], list]:
        assert isinstance(collection, list), repr(collection)
        segment_parts = self.lmr(collection)
        segment_parts = [_ for _ in segment_parts if _]
        collection = [_[-1] for _ in segment_parts]
        durations = self.durations
        acciaccatura_containers: list[abjad.BeforeGraceContainer | None] = []
        for segment_part in segment_parts:
            if len(segment_part) <= 1:
                acciaccatura_containers.append(None)
                continue
            grace_token = list(segment_part[:-1])
            grace_leaves = abjad.makers.make_leaves(grace_token, durations)
            acciaccatura_container = abjad.BeforeGraceContainer(
                grace_leaves, command=r"\acciaccatura"
            )
            if 1 < len(acciaccatura_container):
                abjad.beam(
                    acciaccatura_container[:],
                    tag=_tags.function_name(_frame(), self),
                )
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        assert isinstance(collection, list), repr(collection)
        return acciaccatura_containers, collection


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Anchor:
    """
    Anchor.

    ``use_remote_stop_offset`` is true when contribution anchors to remote selection stop
    offset; otherwise anchors to remote selection start offset.
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
class Coat:

    argument: int | str | abjad.Pitch | None = None


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Contribution:

    voice_name_to_selection: dict[str, list]
    anchor: Anchor | None = None
    figure_name: str | None = None
    hide_time_signature: bool | None = None
    time_signature: abjad.TimeSignature | None = None

    def __post_init__(self):
        assert isinstance(self.voice_name_to_selection, dict), repr(
            self.voice_name_to_selection
        )
        for value in self.voice_name_to_selection.values():
            assert isinstance(value, list), repr(value)
            assert len(value) == 1, repr(value)
            assert isinstance(value[0], abjad.Container), repr(value)
        if self.anchor is not None:
            assert isinstance(self.anchor, Anchor), repr(self.anchor)
        if self.figure_name is not None:
            assert isinstance(self.figure_name, str), repr(self.figure_name)
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
        "figure_names",
        "floating_selections",
        "music_maker",
        "score_stop_offset",
        "voice_names",
        "score",
        "time_signatures",
        "voice_abbreviations",
    )

    def __init__(self, score: abjad.Score, voice_abbreviations=None):
        assert isinstance(score, abjad.Score), repr(score)
        self.score = score
        self.voice_abbreviations = dict(voice_abbreviations or {})
        voice_names = []
        for voice in abjad.iterate.components(score, abjad.Voice):
            voice_names.append(voice.name)
        self.voice_names = voice_names
        self.current_offset = abjad.Offset(0)
        self.figure_number = 1
        self.figure_names: list[str] = []
        self.floating_selections: dict = dict([(_, []) for _ in self.voice_names])
        self.score_stop_offset = abjad.Offset(0)
        self.time_signatures: list[abjad.TimeSignature] = []

    def __call__(
        self,
        voice_name: str,
        collections: typing.Sequence,
        *commands,
        anchor: Anchor | None = None,
        do_not_label: bool = False,
        figure_name: str = "",
        figure_label_direction: int | None = None,
        hide_time_signature: bool | None = None,
        tsd: int | None = None,
    ) -> None:
        make_figures(
            self,
            voice_name,
            collections,
            *commands,
            anchor=anchor,
            do_not_label=do_not_label,
            figure_name=figure_name,
            figure_label_direction=figure_label_direction,
            hide_time_signature=hide_time_signature,
            tsd=tsd,
        )

    def assemble(self, voice_name) -> list | None:
        floating_selections = self.floating_selections[voice_name]
        total_duration = sum([_.duration for _ in self.time_signatures])
        for floating_selection in floating_selections:
            assert isinstance(floating_selection, abjad.Timespan)
        floating_selections = list(floating_selections)
        floating_selections.sort()
        try:
            first_start_offset = floating_selections[0].start_offset
        except Exception:
            first_start_offset = abjad.Offset(0)
        timespans = abjad.TimespanList(floating_selections)
        if timespans:
            gaps = ~timespans
        else:
            sectionwide_gap = abjad.Timespan(0, total_duration)
            gaps = abjad.TimespanList([sectionwide_gap])
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        if floating_selections:
            final_stop_offset = floating_selections[-1].stop_offset
        else:
            final_stop_offset = total_duration
        if final_stop_offset < total_duration:
            final_gap = abjad.Timespan(final_stop_offset, total_duration)
            gaps.append(final_gap)
        selections = floating_selections + list(gaps)
        selections.sort()
        fused_selection = []
        for selection in selections:
            if (
                isinstance(selection, abjad.Timespan)
                and selection.annotation is not None
            ):
                fused_selection.extend(selection.annotation)
            else:
                assert isinstance(selection, abjad.Timespan)
                skip = abjad.Skip(1, multiplier=selection.duration.pair)
                fused_selection.append(skip)
        return fused_selection

    def populate_commands(self, score):
        for voice_name in sorted(self.floating_selections):
            selection = self.assemble(voice_name)
            if not selection:
                continue
            voice = score[voice_name]
            voice.extend(selection)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class FigureMaker:

    talea: rmakers.Talea
    acciaccatura: Acciaccatura | None = None
    affix: typing.Optional["RestAffix"] = None
    restart_talea: bool = False
    tsd: int | None = None
    spelling: rmakers.Spelling | None = None
    treatments: typing.Sequence = ()

    def __post_init__(self):
        if self.acciaccatura is not None:
            assert isinstance(self.acciaccatura, Acciaccatura), repr(self.acciaccatura)
        if self.affix is not None:
            assert isinstance(self.affix, RestAffix), repr(self.affix)
        assert isinstance(self.restart_talea, bool), repr(self.restart_talea)
        if self.tsd is not None:
            assert isinstance(self.tsd, int), repr(self.tsd)
        if self.spelling is not None:
            assert isinstance(self.spelling, rmakers.Spelling), repr(self.spelling)
        assert isinstance(self.talea, rmakers.Talea), repr(self.talea)
        if self.treatments is not None:
            for treatment in self.treatments:
                assert _is_treatment(treatment)

    def __call__(
        self,
        collections: typing.Sequence,
        collection_index: int | None = None,
        total_collections: int | None = None,
    ) -> list[abjad.Tuplet]:
        return _call_figure_maker(
            self.affix,
            self.talea,
            self.spelling,
            self.treatments,
            self.acciaccatura,
            collections=collections,
            restart_talea=self.restart_talea,
        )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Imbrication:

    voice_name: str
    segment: list[int]
    commands: tuple = ()
    allow_unused_pitches: bool = False
    by_pitch_class: bool = False
    hocket: bool = False
    truncate_ties: bool = False

    def __post_init__(self) -> None:
        assert isinstance(self.voice_name, str), repr(self.voice_name)
        assert isinstance(self.segment, list), repr(self.segment)
        assert isinstance(self.allow_unused_pitches, bool)
        assert isinstance(self.by_pitch_class, bool), repr(self.by_pitch_class)
        assert isinstance(self.hocket, bool), repr(self.hocket)
        assert isinstance(self.truncate_ties, bool), repr(self.truncate_ties)

    def __call__(self, container: abjad.Container) -> dict[str, list]:
        return _do_imbrication(
            container,
            self.segment,
            self.voice_name,
            *self.commands,
            allow_unused_pitches=self.allow_unused_pitches,
            by_pitch_class=self.by_pitch_class,
            hocket=self.hocket,
            truncate_ties=self.truncate_ties,
        )


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Nest:

    treatments: typing.Sequence[int | str]
    lmr: LMR | None = None

    def __post_init__(self):
        assert isinstance(self.treatments, list | tuple)
        for treatment in self.treatments:
            assert _is_treatment(treatment), repr(treatment)
        if self.lmr is not None:
            assert isinstance(self.lmr, LMR), repr(self.lmr)

    def __call__(self, selection) -> list[abjad.Tuplet]:
        return _do_nest_command(selection, lmr=self.lmr, treatments=self.treatments)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class RestAffix:

    pattern: abjad.Pattern | None = None
    prefix: typing.Sequence[int] = ()
    skips_instead_of_rests: bool = False
    suffix: typing.Sequence[int] = ()

    def __post_init__(self):
        if self.pattern is not None:
            assert isinstance(self.pattern, abjad.Pattern)
        if self.prefix is not None:
            assert all(isinstance(_, int) for _ in self.prefix)
        assert isinstance(self.skips_instead_of_rests, bool), repr(
            self.skips_instead_of_rests
        )
        if self.suffix is not None:
            assert all(isinstance(_, int) for _ in self.suffix)

    def __call__(
        self, collection_index: int, total_collections: int
    ) -> tuple[typing.Sequence[int] | None, typing.Sequence[int] | None]:
        if self.pattern is None:
            if collection_index == 0 and collection_index == total_collections - 1:
                return self.prefix, self.suffix
            if collection_index == 0:
                return self.prefix, None
            if collection_index == total_collections - 1:
                return None, self.suffix
        elif self.pattern.matches_index(collection_index, total_collections):
            return self.prefix, self.suffix
        return None, None


class Stack:

    __slots__ = ("commands",)

    def __init__(self, *commands) -> None:
        commands = commands or ()
        self.commands = tuple(commands)

    def __call__(self, argument: typing.Any, **keywords) -> typing.Any:
        if not self.commands:
            return argument
        try:
            result: typing.Any = self.commands[0](argument, **keywords)
        except Exception:
            message = "exception while calling:\n"
            message += f"   {self.commands[0]}"
            raise Exception(message)
        for command in self.commands[1:]:
            try:
                result_ = command(result)
            except Exception:
                message = "exception while calling:\n"
                message += f"   {command}"
                raise Exception(message)
            if result_ not in (True, False, None):
                result = result_
        if result not in (True, False, None):
            return result


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


def coat(pitch: int | str | abjad.Pitch) -> Coat:
    return Coat(pitch)


def figure(
    collections,
    counts: typing.Sequence[int],
    denominator: int,
    *,
    acciaccatura: bool | Acciaccatura | LMR | None = None,
    affix: RestAffix | None = None,
    restart_talea: bool = False,
    tsd: int | None = None,
    spelling: rmakers.Spelling | None = None,
    treatments: typing.Sequence = (),
) -> abjad.Container:
    if acciaccatura is True:
        acciaccatura = Acciaccatura()
    elif isinstance(acciaccatura, LMR):
        acciaccatura = Acciaccatura(lmr=acciaccatura)
    if acciaccatura is not None:
        assert isinstance(acciaccatura, Acciaccatura), repr(acciaccatura)
    tuplets = _call_figure_maker(
        affix,
        rmakers.Talea(counts=counts, denominator=denominator),
        spelling,
        treatments,
        acciaccatura,
        collections=collections,
        restart_talea=restart_talea,
    )
    container = abjad.Container(tuplets)
    return container


def imbricate(
    container: abjad.Container,
    voice_name: str,
    segment: list,
    *specifiers: typing.Any,
    allow_unused_pitches: bool = False,
    by_pitch_class: bool = False,
    hocket: bool = False,
    truncate_ties: bool = False,
) -> dict[str, list]:
    return _do_imbrication(
        container,
        segment,
        voice_name,
        *specifiers,
        allow_unused_pitches=allow_unused_pitches,
        by_pitch_class=by_pitch_class,
        hocket=hocket,
        truncate_ties=truncate_ties,
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


def make_figures(
    accumulator: "Accumulator",
    voice_name: str,
    collections: typing.Sequence | None,
    *commands,
    anchor: typing.Optional["Anchor"] = None,
    container: abjad.Container | None = None,
    do_not_label: bool = False,
    figure_name: str = "",
    figure_label_direction: int | None = None,
    hide_time_signature: bool | None = None,
    imbrications: dict[str, list[abjad.Container]] | None = None,
    tsd: int | None = None,
    tuplets: list[abjad.Tuplet] | None = None,
):
    assert isinstance(figure_name, str), repr(figure_name)
    voice_name = accumulator.voice_abbreviations.get(voice_name, voice_name)
    if container is not None:
        assert collections is None
        assert tuplets is None
        imbrications = imbrications or {}
    elif tuplets is not None:
        assert collections is None
        container = abjad.Container(tuplets)
        imbrications = imbrications or {}
    else:
        assert collections is not None
        container, imbrications, tsd = _collections_to_container(
            accumulator, voice_name, collections, *commands, tsd=tsd
        )
    duration = abjad.get.duration(container)
    if tsd is not None:
        pair = duration.with_denominator(tsd).pair
    else:
        pair = duration.pair
    time_signature = abjad.TimeSignature(pair)
    leaf = abjad.select.leaf(container, 0)
    abjad.annotate(leaf, "figure_name", figure_name)
    if not do_not_label:
        _label_figure(
            container, figure_name, figure_label_direction, accumulator.figure_number
        )
    selection = [container]
    voice_name_to_selection = {voice_name: selection}
    assert isinstance(imbrications, dict)
    for voice_name, selection in imbrications.items():
        voice_name_to_selection[voice_name] = selection
    if anchor is not None:
        voice_name_ = accumulator.voice_abbreviations.get(
            anchor.remote_voice_name, anchor.remote_voice_name
        )
        anchor = dataclasses.replace(anchor, remote_voice_name=voice_name_)
    contribution = Contribution(
        voice_name_to_selection,
        anchor=anchor,
        figure_name=figure_name,
        hide_time_signature=hide_time_signature,
        time_signature=time_signature,
    )
    if contribution.figure_name:
        if contribution.figure_name in accumulator.figure_names:
            raise Exception(f"duplicate figure name: {contribution.figure_name!r}.")
        accumulator.figure_names.append(contribution.figure_name)
    for voice_name, selection in contribution.voice_name_to_selection.items():
        start_offset = _get_start_offset(
            selection,
            contribution,
            accumulator.floating_selections,
            accumulator.current_offset,
            accumulator.score_stop_offset,
        )
        stop_offset = start_offset + abjad.get.duration(selection)
        timespan = abjad.Timespan(start_offset, stop_offset)
        floating_selection = abjad.Timespan(
            timespan.start_offset,
            timespan.stop_offset,
            annotation=selection,
        )
        if voice_name not in accumulator.floating_selections:
            voice_name = accumulator.voice_abbreviations.get(voice_name, voice_name)
        accumulator.floating_selections[voice_name].append(floating_selection)
    accumulator.current_offset = stop_offset
    accumulator.score_stop_offset = max(accumulator.score_stop_offset, stop_offset)
    if not contribution.hide_time_signature:
        if (
            contribution.anchor is None
            or contribution.hide_time_signature is False
            or (contribution.anchor and contribution.anchor.remote_voice_name is None)
        ):
            assert isinstance(contribution.time_signature, abjad.TimeSignature)
            accumulator.time_signatures.append(contribution.time_signature)
    if not do_not_label:
        accumulator.figure_number += 1


def nest(
    argument, treatments: typing.Sequence, *, lmr: LMR | None = None
) -> list[abjad.Tuplet]:
    assert treatments is not None
    if not isinstance(treatments, list):
        treatments = [treatments]
    return _do_nest_command(argument, lmr=lmr, treatments=treatments)


def rests_after(counts: typing.Sequence[int]) -> RestAffix:
    return RestAffix(suffix=counts)


def rests_around(prefix: list[int], suffix: list[int]) -> RestAffix:
    return RestAffix(prefix=prefix, suffix=suffix)


def rests_before(counts: list[int]) -> RestAffix:
    return RestAffix(prefix=counts)


def resume() -> Anchor:
    """
    Resumes music at next offset across all voices in score.
    """
    return Anchor()


def resume_after(remote_voice_name) -> Anchor:
    """
    Resumes music after remote selection.
    """
    return Anchor(
        remote_selector=lambda _: abjad.select.leaf(_, -1),
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
    )


def skips_after(counts: list[int]) -> RestAffix:
    return RestAffix(skips_instead_of_rests=True, suffix=counts)


def skips_around(prefix: list[int], suffix: list[int]) -> RestAffix:
    return RestAffix(prefix=prefix, skips_instead_of_rests=True, suffix=suffix)


def skips_before(counts: list[int]) -> RestAffix:
    return RestAffix(prefix=counts, skips_instead_of_rests=True)


def stack(*commands) -> Stack:
    return Stack(*commands)
