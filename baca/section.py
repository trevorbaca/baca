"""
Interpret.
"""
import copy
import dataclasses
import importlib
import inspect
import os
import pathlib
import pprint
import sys
import types
import typing
from inspect import currentframe as _frame

import abjad

from . import build as _build
from . import docs as _docs
from . import indicatorclasses as _indicatorclasses
from . import layout as _layout
from . import lilypond as _lilypond
from . import memento as _memento
from . import overridecommands as _overridecommands
from . import parts as _parts
from . import path as _path
from . import pcollections as _pcollections
from . import piecewisecommands as _piecewisecommands
from . import pitchcommands as _pitchcommands
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from .enums import enums as _enums


def _add_container_identifiers(score, section_number):
    if section_number is not None:
        assert section_number, repr(section_number)
        section_number = f"number.{int(section_number)}"
    else:
        section_number = ""
    contexts = []
    try:
        context = score["Skips"]
        contexts.append(context)
    except ValueError:
        pass
    try:
        context = score["Rests"]
        contexts.append(context)
    except ValueError:
        pass
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice._has_indicator(_enums.INTERMITTENT):
            continue
        contexts.append(voice)
    container_to_part_assignment = {}
    context_name_to_count = {}
    for context in contexts:
        assert context.name is not None, repr(context)
        count = context_name_to_count.get(context.name, 0)
        if count == 0:
            suffixed_context_name = context.name
        else:
            suffixed_context_name = f"{context.name}.item.{count}"
        context_name_to_count[context.name] = count + 1
        if section_number:
            context_identifier = f"{section_number}.{suffixed_context_name}"
        else:
            context_identifier = suffixed_context_name
        context.identifier = f"%*% {context_identifier}"
        part_container_count = 0
        total_part_containers = 0
        for container in abjad.iterate.components(context, abjad.Container):
            if not container.identifier:
                continue
            if container.identifier.startswith("%*% Part"):
                total_part_containers += 1
        for container in abjad.iterate.components(context, abjad.Container):
            if not container.identifier:
                continue
            if container.identifier.startswith("%*% Part"):
                part_container_count += 1
                part = container.identifier.strip("%*% ")
                globals_ = globals()
                globals_["PartAssignment"] = _parts.PartAssignment
                part = eval(part, globals_)
                container_identifier = f"{context_identifier}.container"
                if 1 < total_part_containers:
                    container_identifier += f".{part_container_count}"
                assert abjad.string.is_lilypond_identifier(container_identifier), repr(
                    container_identifier
                )
                assert container_identifier not in container_to_part_assignment
                timespan = container._get_timespan()
                pair = (part, timespan)
                container_to_part_assignment[container_identifier] = pair
                container.identifier = f"%*% {container_identifier}"
    for staff in abjad.iterate.components(score, abjad.Staff):
        if section_number:
            context_identifier = f"{section_number}.{staff.name}"
        else:
            context_identifier = staff.name
        staff.identifier = f"%*% {context_identifier}"
    return container_to_part_assignment


def _alive_during_previous_section(previous_metadata, context):
    assert isinstance(context, abjad.Context), repr(context)
    names = previous_metadata.get("alive_during_section", [])
    return context.name in names


def _analyze_memento(score, dictionary, context, memento):
    previous_indicator = _memento_to_indicator(dictionary, memento)
    if previous_indicator is None:
        return
    if isinstance(previous_indicator, _indicatorclasses.SpacingSection):
        return
    if memento.context in score:
        for context in abjad.iterate.components(score, abjad.Context):
            if context.name == memento.context:
                memento_context = context
                break
    else:
        # context alive in previous section doesn't exist in this section
        return
    leaf = abjad.get.leaf(memento_context, 0)
    if isinstance(previous_indicator, abjad.Instrument):
        prototype = abjad.Instrument
    else:
        prototype = type(previous_indicator)
    indicator = abjad.get.indicator(leaf, prototype)
    status = None
    if indicator is None:
        status = "reapplied"
    elif not _treat.compare_persistent_indicators(previous_indicator, indicator):
        status = "explicit"
    elif isinstance(previous_indicator, abjad.TimeSignature):
        status = "reapplied"
    else:
        status = "redundant"
    edition = memento.edition or abjad.Tag()
    if memento.synthetic_offset is None:
        synthetic_offset = None
    else:
        assert 0 < memento.synthetic_offset, repr(memento)
        synthetic_offset = -memento.synthetic_offset
    return leaf, previous_indicator, status, edition, synthetic_offset


def _append_tag_to_wrappers(leaf, tag):
    assert isinstance(tag, abjad.Tag), repr(tag)
    for wrapper in abjad.get.wrappers(leaf):
        if isinstance(wrapper.unbundle_indicator(), abjad.LilyPondLiteral):
            if wrapper.unbundle_indicator().argument == "":
                continue
        if tag.string not in wrapper.tag.string:
            tag_ = wrapper.tag.append(tag)
            wrapper.tag = tag_


def _assert_nonoverlapping_rhythms(rhythms, voice):
    previous_stop_offset = 0
    for rhythm in rhythms:
        start_offset = rhythm.start_offset
        if start_offset < previous_stop_offset:
            raise Exception(f"{voice} has overlapping rhythms.")
        duration = abjad.get.duration(rhythm.annotation)
        stop_offset = start_offset + duration
        previous_stop_offset = stop_offset


def _attach_nonfirst_empty_start_bar(global_skips):
    # empty start bar allows LilyPond to print bar numbers at start of nonfirst sections
    first_skip = _select.skip(global_skips, 0)
    literal = abjad.LilyPondLiteral(r'\bar ""')
    tag = _tags.EMPTY_START_BAR
    tag = tag.append(_tags.ONLY_SECTION)
    abjad.attach(
        literal,
        first_skip,
        tag=tag.append(_tags.function_name(_frame())),
    )


def _attach_metronome_marks(global_skips, parts_metric_modulation_multiplier):
    indicator_count = 0
    skips = _select.skips(global_skips)
    final_leaf_metronome_mark = abjad.get.indicator(skips[-1], abjad.MetronomeMark)
    add_right_text_to_me = None
    if final_leaf_metronome_mark:
        tempo_prototype = (
            abjad.MetronomeMark,
            _indicatorclasses.Accelerando,
            _indicatorclasses.Ritardando,
        )
        for skip in reversed(skips[:-1]):
            if abjad.get.has_indicator(skip, tempo_prototype):
                add_right_text_to_me = skip
                break
    for i, skip in enumerate(skips):
        metronome_mark = abjad.get.indicator(skip, abjad.MetronomeMark)
        metric_modulation = abjad.get.indicator(skip, abjad.MetricModulation)
        accelerando = abjad.get.indicator(skip, _indicatorclasses.Accelerando)
        ritardando = abjad.get.indicator(skip, _indicatorclasses.Ritardando)
        if (
            metronome_mark is None
            and metric_modulation is None
            and accelerando is None
            and ritardando is None
        ):
            continue
        if metronome_mark is not None:
            # metronome_mark._hide = True
            metronome_mark.hide = True
            wrapper = abjad.get.wrapper(skip, abjad.MetronomeMark)
        if metric_modulation is not None:
            # TODO: public hide:
            # TODO: detach / reattach frozen object:
            metric_modulation._hide = True
        if accelerando is not None:
            # TODO: detach / reattach frozen object:
            accelerando.hide = True
        if ritardando is not None:
            # TODO: detach / reattach frozen object:
            ritardando.hide = True
        if skip is skips[-1]:
            break
        if metronome_mark is None and metric_modulation is not None:
            wrapper = abjad.get.wrapper(skip, abjad.MetricModulation)
        if metronome_mark is None and accelerando is not None:
            wrapper = abjad.get.wrapper(skip, _indicatorclasses.Accelerando)
        if metronome_mark is None and ritardando is not None:
            wrapper = abjad.get.wrapper(skip, _indicatorclasses.Ritardando)
        has_trend = accelerando is not None or ritardando is not None
        indicator_count += 1
        tag = wrapper.tag
        stripped_left_text = None
        if metronome_mark is not None:
            if metric_modulation is not None:
                if metronome_mark.custom_markup is not None:
                    left_text = metronome_mark._get_markup().string
                    left_text = left_text.removeprefix(r"\markup").strip()
                    modulation = metric_modulation._get_markup().string
                    modulation = modulation.removeprefix(r"\markup").strip()
                    string = rf"\concat {{ {left_text} \hspace #2 \upright ["
                    string += rf" \line {{ {modulation} }} \hspace #0.5"
                    string += r" \upright ] }"
                    left_text = abjad.Markup(string)
                else:
                    left_text = _bracket_metric_modulation(
                        metronome_mark, metric_modulation
                    )
                if metronome_mark.custom_markup is not None:
                    stripped_left_text = r"- \baca-metronome-mark-spanner-left-markup"
                    string = abjad.lilypond(metronome_mark.custom_markup)
                    assert string.startswith("\\")
                    stripped_left_text += f" {string}"
                # mixed number
                elif metronome_mark.decimal is True:
                    arguments = metronome_mark._get_markup_arguments()
                    log, dots, stem, base, n, d = arguments
                    stripped_left_text = (
                        r"- \baca-metronome-mark-spanner-left-text-mixed-number"
                    )
                    stripped_left_text += f' {log} {dots} {stem} "{base}" "{n}" "{d}"'
                else:
                    arguments = metronome_mark._get_markup_arguments()
                    log, dots, stem, value = arguments
                    stripped_left_text = r"- \baca-metronome-mark-spanner-left-text"
                    stripped_left_text += f' {log} {dots} {stem} "{value}"'
            elif metronome_mark.custom_markup is not None:
                left_text = r"- \baca-metronome-mark-spanner-left-markup"
                string = abjad.lilypond(metronome_mark.custom_markup)
                assert string.startswith("\\")
                left_text += f" {string}"
            # mixed number
            elif metronome_mark.decimal is True:
                arguments = metronome_mark._get_markup_arguments()
                log, dots, stem, base, n, d = arguments
                left_text = r"- \baca-metronome-mark-spanner-left-text-mixed-number"
                left_text += f' {log} {dots} {stem} "{base}" "{n}" "{d}"'
            else:
                arguments = metronome_mark._get_markup_arguments()
                log, dots, stem, value = arguments
                left_text = r"- \baca-metronome-mark-spanner-left-text"
                left_text += f' {log} {dots} {stem} "{value}"'
        elif accelerando is not None:
            left_text = accelerando._get_markup()
            string = left_text.string.removeprefix(r"\markup").strip()
            left_text = abjad.Markup(string)
        elif ritardando is not None:
            left_text = ritardando._get_markup()
            string = left_text.string.removeprefix(r"\markup").strip()
            left_text = abjad.Markup(string)
        if has_trend:
            style = "dashed-line-with-arrow"
        else:
            style = "invisible-line"
        if 0 < i:
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMM")
            abjad.attach(
                stop_text_span,
                skip,
                tag=_tags.function_name(_frame(), n=1),
            )
        if add_right_text_to_me is skip:
            right_text = final_leaf_metronome_mark._get_markup()
        else:
            right_text = None
        start_text_span = abjad.StartTextSpan(
            command=r"\bacaStartTextSpanMM",
            left_text=left_text,
            right_text=right_text,
            style=style,
        )
        if not tag:
            continue
        assert "METRONOME_MARK" in tag.string, repr(tag)
        if (
            isinstance(wrapper.unbundle_indicator(), abjad.MetronomeMark)
            and has_trend
            and "EXPLICIT" not in tag.string
        ):
            words = []
            for word in tag.string.split(":"):
                if "METRONOME_MARK" in word:
                    word = word.replace("REAPPLIED", "EXPLICIT")
                    word = word.replace("REDUNDANT", "EXPLICIT")
                words.append(word)
            string = ":".join(words)
            new_tag = abjad.Tag(string)
            indicator = wrapper.unbundle_indicator()
            abjad.detach(wrapper, skip)
            abjad.attach(
                indicator,
                skip,
                tag=new_tag.append(_tags.function_name(_frame(), n=5)),
            )
            tag = new_tag
        if not (
            isinstance(start_text_span.left_text, str)
            and start_text_span.left_text.endswith("(1 . 1)")
            and parts_metric_modulation_multiplier is not None
        ):
            abjad.attach(
                start_text_span,
                skip,
                deactivate=True,
                tag=tag.append(_tags.function_name(_frame(), n=2)),
            )
        else:
            abjad.attach(
                start_text_span,
                skip,
                deactivate=True,
                tag=tag.append(_tags.function_name(_frame(), n=2.1)).append(
                    _tags.METRIC_MODULATION_IS_NOT_SCALED,
                ),
            )
            left_text_ = start_text_span.left_text
            assert left_text_.endswith("(1 . 1)")
            n, d = parts_metric_modulation_multiplier
            left_text_ = left_text_[:-7] + f"({n} . {d})"
            start_text_span_ = dataclasses.replace(
                start_text_span, left_text=left_text_
            )
            abjad.attach(
                start_text_span_,
                skip,
                deactivate=True,
                tag=tag.append(_tags.function_name(_frame(), n=2.2)).append(
                    _tags.METRIC_MODULATION_IS_SCALED,
                ),
            )
        if stripped_left_text is not None:
            start_text_span_ = dataclasses.replace(
                start_text_span, left_text=stripped_left_text
            )
            abjad.attach(
                start_text_span_,
                skip,
                deactivate=True,
                tag=tag.append(_tags.function_name(_frame(), n=2.2)).append(
                    _tags.METRIC_MODULATION_IS_STRIPPED,
                ),
            )
        string = tag.string
        if "EXPLICIT" in string:
            status = "explicit"
        elif "REAPPLIED" in string:
            status = "reapplied"
        elif "REDUNDANT" in string:
            status = "redundant"
        else:
            status = None
        assert status is not None
        color = _treat._status_to_color[status]
        string = f"{status.upper()}_METRONOME_MARK_WITH_COLOR"
        tag = abjad.Tag(string)
        if isinstance(left_text, str):
            string = left_text.replace(
                "baca-metronome-mark-spanner-left-markup",
                "baca-metronome-mark-spanner-colored-left-markup",
            )
            string = string.replace(
                "baca-metronome-mark-spanner-left-text",
                "baca-metronome-mark-spanner-colored-left-text",
            )
            string = string.replace(
                "baca-bracketed-metric-modulation",
                "baca-colored-bracketed-metric-modulation",
            )
            string = string.replace(
                "baca-bracketed-mixed-number-metric-modulation",
                "baca-colored-bracketed-mixed-number-metric-modulation",
            )
            left_text_with_color = f"{string} #'{color}"
        else:
            color = f"(x11-color '{color})"
            left_text_with_color = abjad.Markup(
                rf"\with-color #{color} {left_text.string}"
            )
        if right_text:
            wrapper = abjad.get.wrapper(skips[-1], abjad.MetronomeMark)
            tag = wrapper.tag
            string = tag.string
            if "EXPLICIT" in string:
                status = "explicit"
            elif "REAPPLIED" in tag.string:
                status = "reapplied"
            elif "REDUNDANT" in tag.string:
                status = "redundant"
            else:
                status = None
            assert status is not None
            color = _treat._status_to_color[status]
            color = f"(x11-color '{color})"
            right_text_with_color = abjad.Markup(
                rf"\with-color #{color} {right_text.string}"
            )
        else:
            right_text_with_color = None
        start_text_span = abjad.StartTextSpan(
            command=r"\bacaStartTextSpanMM",
            left_text=left_text_with_color,
            right_text=right_text_with_color,
            style=style,
        )
        abjad.attach(
            start_text_span,
            skip,
            deactivate=False,
            tag=tag.append(_tags.function_name(_frame(), n=3)),
        )
    if indicator_count:
        final_skip = skip
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMM")
        tag_ = _tags.EOS_STOP_MM_SPANNER
        tag_ = tag_.append(_tags.function_name(_frame(), n=4))
        abjad.attach(stop_text_span, final_skip, tag=tag_)


def _attach_rhythm_annotation_spanner(command, selection):
    if selection is None:
        return
    if not command.annotation_spanner_text:
        return
    leaves = []
    for leaf in abjad.iterate.leaves(selection):
        if abjad.get.parentage(leaf).get(abjad.OnBeatGraceContainer):
            continue
        leaves.append(leaf)
    container = abjad.get.before_grace_container(leaves[0])
    if container is not None:
        leaves_ = abjad.select.leaves(container)
        leaves[0:0] = leaves_
    container = abjad.get.after_grace_container(leaves[-1])
    if container is not None:
        leaves_ = abjad.select.leaves(container)
        leaves.extend(leaves_)
    string = command.annotation_spanner_text
    if string is None:
        string = command._make_rhythm_annotation_string()
    color = command.annotation_spanner_color or "#darkyellow"
    command_ = _piecewisecommands.rhythm_annotation_spanner(
        string,
        abjad.Tweak(rf"- \tweak color {color}"),
        abjad.Tweak(r"- \tweak staff-padding 8"),
        leak_spanner_stop=True,
        selector=lambda _: _select.leaves(_),
    )
    command_(leaves)


# This exists because of an incompletely implemented behavior in LilyPond;
# LilyPond doesn't understand repeat-tied notes to be tied;
# because of this LilyPond incorrectly prints accidentals in front of some
# repeat-tied notes; this function works around LilyPond's behavior
def _attach_shadow_tie_indicators(score):
    tag = _tags.function_name(_frame())
    for plt in _select.plts(score):
        if len(plt) == 1:
            continue
        for pleaf in plt[:-1]:
            if abjad.get.has_indicator(pleaf, abjad.Tie):
                continue
            tie = abjad.Tie()
            bundle = abjad.bundle(tie, r"- \tweak stencil ##f")
            abjad.attach(bundle, pleaf, tag=tag)


def _attach_sounds_during(score):
    for voice in abjad.iterate.components(score, abjad.Voice):
        pleaves = _select.pleaves(voice)
        if bool(pleaves):
            abjad.attach(_enums.SOUNDS_DURING_SECTION, voice)


def _bracket_metric_modulation(metronome_mark, metric_modulation):
    if metronome_mark.decimal is not True:
        # TODO: refactor _get_markup_arguments() to return dict
        arguments = metronome_mark._get_markup_arguments()
        mm_length, mm_dots, mm_stem, mm_value = arguments
        arguments = metric_modulation._get_markup_arguments()
        if metric_modulation._note_to_note():
            command = r"- \baca-bracketed-metric-modulation"
            lhs_length, lhs_dots, rhs_length, rhs_dots = arguments
            command += f' #{mm_length} #{mm_dots} #{mm_stem} #"{mm_value}"'
            command += f" #{lhs_length} #{lhs_dots}"
            command += f" #{rhs_length} #{rhs_dots}"
        elif metric_modulation._lhs_tuplet():
            command = r"- \baca-bracketed-metric-modulation-tuplet-lhs"
            tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[:4]
            note_length, note_dots = arguments[4:]
            command += f' #{mm_length} #{mm_dots} #{mm_stem} #"{mm_value}"'
            command += f" #{tuplet_length} #{tuplet_dots}"
            command += f" #{tuplet_n} #{tuplet_d}"
            command += f" #{note_length} #{note_dots}"
        elif metric_modulation._rhs_tuplet():
            command = r"- \baca-bracketed-metric-modulation-tuplet-rhs"
            note_length, note_dots = arguments[:2]
            tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[2:]
            command += f' #{mm_length} #{mm_dots} #{mm_stem} #"{mm_value}"'
            command += f" #{note_length} #{note_dots}"
            command += f" #{tuplet_length} #{tuplet_dots}"
            command += f" #{tuplet_n} #{tuplet_d}"
        else:
            raise Exception("implement tied note values in metric modulation.")
    else:
        arguments = metronome_mark._get_markup_arguments()
        mm_length, mm_dots, mm_stem, mm_base, mm_n, mm_d = arguments
        # TODO: refactor _get_markup_arguments() to return dict
        arguments = metric_modulation._get_markup_arguments()
        if metric_modulation._note_to_note():
            command = r"- \baca-bracketed-mixed-number-metric-modulation"
            lhs_length, lhs_dots, rhs_length, rhs_dots = arguments
            command += f" #{mm_length} #{mm_dots} #{mm_stem}"
            command += f' #"{mm_base}" #"{mm_n}" #"{mm_d}"'
            command += f" #{lhs_length} #{lhs_dots}"
            command += f" #{rhs_length} #{rhs_dots}"
        elif metric_modulation._lhs_tuplet():
            command = r"- \baca-bracketed-mixed-number-metric-modulation-tuplet-lhs"
            tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[:4]
            note_length, note_dots = arguments[4:]
            command += f" #{mm_length} #{mm_dots} #{mm_stem}"
            command += f' #"{mm_base}" #"{mm_n}" #"{mm_d}"'
            command += f" #{tuplet_length} #{tuplet_dots}"
            command += f" #{tuplet_n} #{tuplet_d}"
            command += f" #{note_length} #{note_dots}"
        elif metric_modulation._rhs_tuplet():
            command = r"- \baca-bracketed-mixed-number-metric-modulation-tuplet-rhs"
            note_length, note_dots = arguments[:2]
            tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[2:]
            command += f" #{mm_length} #{mm_dots} #{mm_stem}"
            command += f' #"{mm_base}" #"{mm_n}" #"{mm_d}"'
            command += f" #{note_length} #{note_dots}"
            command += f" #{tuplet_length} #{tuplet_dots}"
            command += f" #{tuplet_n} #{tuplet_d}"
        else:
            raise Exception("implement tied note values in metric modulation.")
    scale = metric_modulation.scale
    command += f" #'({scale[0]} . {scale[1]})"
    return command


def _calculate_clock_times(
    score,
    clock_time_override,
    fermata_measure_numbers,
    first_measure_number,
    previous_stop_clock_time,
):
    skips = _select.skips(score["Skips"])
    if "Rests" not in score:
        return None, None, None, None
    for context in abjad.iterate.components(score, abjad.Context):
        if context.name == "Rests":
            break
    rests = abjad.select.rests(context)
    assert (len(skips) == len(rests)) or (len(skips) == len(rests) + 1)
    start_clock_time = previous_stop_clock_time
    start_clock_time = start_clock_time or "0'00''"
    start_offset = abjad.Duration.from_clock_string(start_clock_time)
    if clock_time_override:
        metronome_mark = clock_time_override
        abjad.attach(metronome_mark, skips[0])
    if abjad.get.effective(skips[0], abjad.MetronomeMark) is None:
        return None, None, start_clock_time, None
    clock_times = []
    for local_measure_index, skip in enumerate(skips):
        measure_number = first_measure_number + local_measure_index
        if measure_number not in fermata_measure_numbers:
            clock_times.append(start_offset)
            duration = abjad.get.duration(skip, in_seconds=True)
        else:
            rest = rests[local_measure_index]
            fermata_duration = abjad.get.annotation(rest, _enums.FERMATA_DURATION)
            duration = abjad.Duration(fermata_duration)
            clock_times.append(duration)
        start_offset += duration
    clock_times.append(start_offset)
    assert len(skips) == len(clock_times) - 1
    if clock_time_override:
        metronome_mark = clock_time_override
        abjad.detach(metronome_mark, skips[0])
    stop_clock_time = clock_times[-1].to_clock_string()
    duration = clock_times[-1] - clock_times[0]
    duration_clock_string = duration.to_clock_string()
    return duration_clock_string, clock_times, start_clock_time, stop_clock_time


def _check_all_music_in_part_containers(score):
    indicator = _enums.MULTIMEASURE_REST_CONTAINER
    for voice in abjad.iterate.components(score, abjad.Voice):
        for component in voice:
            if isinstance(component, abjad.MultimeasureRest | abjad.Skip):
                continue
            if abjad.get.has_indicator(component, _enums.HIDDEN):
                continue
            if abjad.get.has_indicator(component, indicator):
                continue
            if (
                type(component) is abjad.Container
                and component.identifier
                and component.identifier.startswith("%*% ")
            ):
                continue
            message = f"{voice.name} contains {component!r} outside part container."
            raise Exception(message)


def _check_anchors_are_final(score):
    anchor_count, violators = 0, []
    for leaf in abjad.iterate.leaves(score):
        if abjad.get.has_indicator(leaf, (_enums.ANCHOR_NOTE, _enums.ANCHOR_SKIP)):
            anchor_count += 1
            next_leaf = abjad.get.leaf(leaf, 1)
            if next_leaf is not None:
                violators.append(leaf)
    if violators:
        message = f"{len(violators)} / {anchor_count} anchor leaves"
        message += " are not section-final."
        raise Exception(message)


def _check_doubled_dynamics(score):
    for leaf in abjad.iterate.leaves(score):
        dynamics = abjad.get.indicators(leaf, abjad.Dynamic)
        if 1 < len(dynamics):
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            message = f"leaf {str(leaf)} in {voice.name} has"
            message += f" {len(dynamics)} dynamics attached:"
            for dynamic in dynamics:
                message += f"\n   {dynamic!s}"
            raise Exception(message)


def _check_duplicate_part_assignments(dictionary, part_manifest):
    if not dictionary:
        return
    if not part_manifest:
        return
    part_to_timespans = {}
    for identifier, (part_assignment, timespan) in dictionary.items():
        for part in part_assignment.make_parts():
            if part.identifier() not in part_to_timespans:
                part_to_timespans[part.identifier()] = []
            part_to_timespans[part.identifier()].append(timespan)
    messages = []
    for part_name, timespans in part_to_timespans.items():
        if len(timespans) <= 1:
            continue
        timespan_list = abjad.TimespanList(timespans)
        if timespan_list.compute_logical_and():
            message = f"  Part {part_name!r} is assigned to overlapping containers ..."
            messages.append(message)
    if messages:
        message = "\n" + "\n".join(messages)
        raise Exception(message)


def _check_persistent_indicators(do_not_require_short_instrument_names, score):
    indicator = _enums.SOUNDS_DURING_SECTION
    for voice in abjad.iterate.components(score, abjad.Voice):
        if not abjad.get.has_indicator(voice, indicator):
            continue
        for i, leaf in enumerate(abjad.iterate.leaves(voice)):
            _check_persistent_indicators_for_leaf(
                do_not_require_short_instrument_names, leaf, i, voice.name
            )


def _check_persistent_indicators_for_leaf(
    do_not_require_short_instrument_names, leaf, i, voice_name
):
    prototype = (
        _indicatorclasses.Accelerando,
        abjad.MetronomeMark,
        _indicatorclasses.Ritardando,
    )
    mark = abjad.get.effective(leaf, prototype)
    if mark is None:
        message = f"{voice_name} leaf {i} ({leaf!s}) missing metronome mark."
        raise Exception(message)
    instrument = abjad.get.effective(leaf, abjad.Instrument)
    if instrument is None:
        message = f"{voice_name} leaf {i} ({leaf!s}) missing instrument."
        raise Exception(message)
    if not do_not_require_short_instrument_names:
        name = abjad.get.effective(leaf, abjad.ShortInstrumentName)
        if name is None:
            message = f"{voice_name} leaf {i} ({leaf!s}) missing short instrument name."
            raise Exception(message)
    clef = abjad.get.effective(leaf, abjad.Clef)
    if clef is None:
        raise Exception(f"{voice_name} leaf {i} ({leaf!s}) missing clef.")


def _clean_up_laissez_vibrer_tie_direction(score):
    default = abjad.Clef("treble")
    for note in abjad.iterate.leaves(score, abjad.Note):
        if note.written_duration < 1:
            continue
        if not abjad.get.has_indicator(note, abjad.LaissezVibrer):
            continue
        clef = abjad.get.effective(note, abjad.Clef, default=default)
        staff_position = clef.to_staff_position(note.written_pitch)
        if staff_position == abjad.StaffPosition(0):
            abjad.override(note).LaissezVibrerTie.direction = abjad.UP


def _clean_up_on_beat_grace_containers(score):
    for container in abjad.select.components(score, abjad.OnBeatGraceContainer):
        container._match_anchor_leaf()
        container._set_leaf_durations()
        container._attach_lilypond_one_voice()


def _clean_up_repeat_tie_direction(score):
    default = abjad.Clef("treble")
    for leaf in abjad.iterate.leaves(score, pitched=True):
        if leaf.written_duration < 1:
            continue
        if not abjad.get.has_indicator(leaf, abjad.RepeatTie):
            continue
        clef = abjad.get.effective(leaf, abjad.Clef, default=default)
        if hasattr(leaf, "written_pitch"):
            note_heads = [leaf.note_head]
        else:
            note_heads = leaf.note_heads
        for note_head in note_heads:
            staff_position = clef.to_staff_position(note_head.written_pitch)
            if staff_position.number == 0:
                wrapper = abjad.get.indicator(leaf, abjad.RepeatTie, unwrap=False)
                abjad.detach(wrapper, leaf)
                bundle = abjad.bundle(wrapper.get_item(), r"- \tweak direction #up")
                abjad.attach(bundle, leaf, tag=wrapper.tag)
                break


def _clone_section_initial_short_instrument_name(score):
    prototype = abjad.ShortInstrumentName
    for context in abjad.iterate.components(score, abjad.Context):
        first_leaf = abjad.get.leaf(context, 0)
        if abjad.get.has_indicator(first_leaf, abjad.InstrumentName):
            continue
        short_instrument_name = abjad.get.indicator(first_leaf, prototype)
        if short_instrument_name is None:
            continue
        if isinstance(short_instrument_name.markup, str):
            markup = short_instrument_name.markup
        else:
            markup = dataclasses.replace(short_instrument_name.markup)
        instrument_name = abjad.InstrumentName(
            markup,
            context=short_instrument_name.context,
            site=short_instrument_name.site,
        )
        abjad.attach(
            instrument_name,
            first_leaf,
            tag=_tags.function_name(_frame()),
        )


def _collect_alive_during_section(score):
    result = []
    for context in abjad.iterate.components(score, abjad.Context):
        if context.name not in result:
            result.append(context.name)
    return result


def _collect_metadata(
    container_to_part_assignment,
    duration,
    fermata_measure_numbers,
    final_measure_is_fermata,
    final_measure_number,
    first_measure_number,
    first_metronome_mark,
    has_anchor_skip,
    metadata,
    persist,
    persistent_indicators,
    score,
    start_clock_time,
    stop_clock_time,
    time_signatures,
    voice_name_to_parameter_to_state,
) -> tuple[types.MappingProxyType, types.MappingProxyType]:
    metadata_, persist_ = {}, {}
    persist_["alive_during_section"] = _collect_alive_during_section(score)
    # make-layout-ly scripts adds bol measure numbers to metadata
    bol_measure_numbers = metadata.get("bol_measure_numbers")
    if bol_measure_numbers:
        metadata_["bol_measure_numbers"] = bol_measure_numbers
    if container_to_part_assignment:
        persist_["container_to_part_assignment"] = container_to_part_assignment
    if duration is not None:
        metadata_["duration"] = duration
    if fermata_measure_numbers:
        metadata_["fermata_measure_numbers"] = fermata_measure_numbers
    dictionary = metadata.get("first_appearance_short_instrument_names")
    if dictionary:
        metadata_["first_appearance_short_instrument_names"] = dictionary
    metadata_["first_measure_number"] = first_measure_number
    metadata_["final_measure_number"] = final_measure_number
    if final_measure_is_fermata is True:
        metadata_["final_measure_is_fermata"] = True
    if first_metronome_mark is False:
        metadata_["first_metronome_mark"] = first_metronome_mark
    if has_anchor_skip is True:
        metadata_["has_anchor_skip"] = has_anchor_skip
    if persistent_indicators:
        persist_["persistent_indicators"] = persistent_indicators
    if start_clock_time is not None:
        metadata_["start_clock_time"] = start_clock_time
    if stop_clock_time is not None:
        metadata_["stop_clock_time"] = stop_clock_time
    metadata_["time_signatures"] = time_signatures
    if voice_name_to_parameter_to_state:
        persist_["voice_name_to_parameter_to_state"] = voice_name_to_parameter_to_state
    new_metadata = {}
    new_metadata.update(metadata_)
    _sort_dictionary(new_metadata)
    new_metadata_proxy = types.MappingProxyType(new_metadata)
    for key, value in new_metadata_proxy.items():
        if value in (True, False):
            continue
        if not bool(value):
            raise Exception(f"{key} metadata should be nonempty (not {value!r}).")
    new_persist = {}
    new_persist.update(persist_)
    _sort_dictionary(new_persist)
    new_persist_proxy = types.MappingProxyType(new_persist)
    for key, value in new_persist_proxy.items():
        if not bool(value):
            raise Exception(f"{key} persist should be nonempty (not {value!r}).")
    return new_metadata_proxy, new_persist_proxy


def _collect_persistent_indicators(
    manifests,
    previous_persistent_indicators,
    score,
):
    result = {}
    contexts = abjad.iterate.components(score, abjad.Context)
    contexts = list(contexts)
    contexts.sort(key=lambda _: _.name)
    name_to_wrappers = {}
    for context in contexts:
        if context.name not in name_to_wrappers:
            name_to_wrappers[context.name] = []
        wrappers = context._dependent_wrappers[:]
        name_to_wrappers[context.name].extend(wrappers)
    do_not_persist_on_anchor_leaf = (
        abjad.Instrument,
        abjad.MetronomeMark,
        abjad.ShortInstrumentName,
        abjad.TimeSignature,
    )
    for name, dependent_wrappers in name_to_wrappers.items():
        mementos = []
        wrappers = []
        dictionary = abjad._getlib._get_persistent_wrappers(
            dependent_wrappers=dependent_wrappers,
            omit_with_indicator=(_enums.ANCHOR_NOTE, _enums.ANCHOR_SKIP),
        )
        for wrapper in dictionary.values():
            if isinstance(wrapper.unbundle_indicator(), do_not_persist_on_anchor_leaf):
                wrappers.append(wrapper)
        dictionary = abjad._getlib._get_persistent_wrappers(
            dependent_wrappers=dependent_wrappers
        )
        for wrapper in dictionary.values():
            if not isinstance(
                wrapper.unbundle_indicator(), do_not_persist_on_anchor_leaf
            ):
                wrappers.append(wrapper)
        for wrapper in wrappers:
            leaf = wrapper.component
            parentage = abjad.get.parentage(leaf)
            first_context = parentage.get(abjad.Context)
            indicator = wrapper.unbundle_indicator()
            if isinstance(indicator, abjad.Glissando):
                continue
            if isinstance(indicator, abjad.RepeatTie):
                continue
            if isinstance(indicator, abjad.StopBeam):
                continue
            if isinstance(indicator, abjad.StopPhrasingSlur):
                continue
            if isinstance(indicator, abjad.StopPianoPedal):
                continue
            if isinstance(indicator, abjad.StopSlur):
                continue
            if isinstance(indicator, abjad.StopTextSpan):
                continue
            if isinstance(indicator, abjad.StopTrillSpan):
                continue
            if isinstance(indicator, abjad.Tie):
                continue
            prototype, manifest = None, None
            if isinstance(indicator, abjad.Instrument):
                manifest = "instruments"
            elif isinstance(indicator, abjad.MetronomeMark):
                manifest = "metronome_marks"
            elif isinstance(indicator, abjad.ShortInstrumentName):
                manifest = "short_instrument_names"
            else:
                prototype = type(indicator)
                prototype = _prototype_string(prototype)
            value = _treat._indicator_to_key(indicator, manifests)
            if value is None:
                raise Exception(f"can not find in manifest:\n\n  {indicator}")
            editions = wrapper.tag.editions()
            if editions:
                words = [_.string for _ in editions]
                string = ":".join(words)
                editions = abjad.Tag(string)
            else:
                editions = None
            memento = _memento.Memento(
                context=first_context.name,
                edition=editions,
                manifest=manifest,
                prototype=prototype,
                synthetic_offset=wrapper.synthetic_offset,
                value=value,
            )
            mementos.append(memento)
        if mementos:
            mementos.sort(key=lambda _: repr(_))
            result[name] = mementos
    if previous_persistent_indicators:
        for context_name, mementos in previous_persistent_indicators.items():
            if context_name not in result:
                result[context_name] = mementos
    return result


def _color_mock_pitch(score):
    indicator = _enums.MOCK
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.MOCK_COLORING)
    leaves = []
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, indicator):
            continue
        string = r"\baca-mock-coloring"
        literal = abjad.LilyPondLiteral(string, site="before")
        abjad.attach(literal, pleaf, tag=tag)
        leaves.append(pleaf)


def _color_not_yet_pitched(score):
    indicator = _enums.NOT_YET_PITCHED
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_YET_PITCHED_COLORING)
    leaves = []
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, indicator):
            continue
        string = r"\baca-not-yet-pitched-coloring"
        literal = abjad.LilyPondLiteral(string, site="before")
        tag_ = tag
        if abjad.get.has_indicator(pleaf, _enums.HIDDEN):
            tag_ = tag_.append(_tags.HIDDEN)
        if abjad.get.has_indicator(pleaf, _enums.NOTE):
            tag_ = tag_.append(_tags.NOTE)
        abjad.attach(literal, pleaf, tag=tag_)
        leaves.append(pleaf)


def _color_not_yet_registered(score):
    indicator = _enums.NOT_YET_REGISTERED
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.NOT_YET_REGISTERED_COLORING)
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, indicator):
            continue
        string = r"\baca-not-yet-registered-coloring"
        literal = abjad.LilyPondLiteral(string, site="before")
        abjad.attach(literal, pleaf, tag=tag)


def _comment_measure_numbers(first_measure_number, offset_to_measure_number, score):
    for leaf in abjad.iterate.leaves(score):
        offset = abjad.get.timespan(leaf).start_offset
        measure_number = offset_to_measure_number.get(offset, None)
        if measure_number is None:
            continue
        context = abjad.get.parentage(leaf).get(abjad.Context)
        if abjad.get.has_indicator(leaf, _enums.ANCHOR_SKIP):
            string = "% [anchor skip]"
        elif abjad.get.has_indicator(leaf, _enums.ANCHOR_NOTE):
            string = f"% [{context.name} anchor note]"
        else:
            local_measure_number = measure_number - first_measure_number
            local_measure_number += 1
            string = f"% [{context.name} measure {local_measure_number}]"
        literal = abjad.LilyPondLiteral(string, site="absolute_before")
        abjad.attach(literal, leaf, tag=_tags.function_name(_frame()))


def _error_on_not_yet_pitched(score):
    violators = []
    for voice in abjad.iterate.components(score, abjad.Voice):
        for leaf in abjad.iterate.leaves(voice):
            if abjad.get.has_indicator(leaf, _enums.NOT_YET_PITCHED):
                violators.append((voice.name, leaf))
    if violators:
        strings = [f"{len(violators)} leaves not yet pitched ..."]
        strings.extend([f"    {_[0]} {repr(_[1])}" for _ in violators])
        message = "\n".join(strings)
        raise Exception(message)


def _extend_beam(leaf):
    if not abjad.get.has_indicator(leaf, abjad.StopBeam):
        parentage = abjad.get.parentage(leaf)
        voice = parentage.get(abjad.Voice)
        message = f"{leaf!s} in {voice.name} has no StopBeam."
        raise Exception(message)
    abjad.detach(abjad.StopBeam, leaf)
    if not abjad.get.has_indicator(leaf, abjad.StartBeam):
        abjad.detach(abjad.BeamCount, leaf)
        left = leaf.written_duration.flag_count
        beam_count = abjad.BeamCount(left, 1)
        abjad.attach(beam_count, leaf, "_extend_beam")
    current_leaf = leaf
    while True:
        next_leaf = abjad.get.leaf(current_leaf, 1)
        if next_leaf is None:
            parentage = abjad.get.parentage(current_leaf)
            voice = parentage.get(abjad.Voice)
            message = f"no leaf follows {current_leaf!s} in {voice.name};"
            message += "\n\tDo not set extend_beam=True on last figure."
            raise Exception(message)
            return
        if abjad.get.has_indicator(next_leaf, abjad.StartBeam):
            abjad.detach(abjad.StartBeam, next_leaf)
            if not abjad.get.has_indicator(next_leaf, abjad.StopBeam):
                abjad.detach(abjad.BeamCount, next_leaf)
                right = next_leaf.written_duration.flag_count
                beam_count = abjad.BeamCount(1, right)
                abjad.attach(beam_count, next_leaf, "_extend_beam")
            return
        current_leaf = next_leaf


def _find_first_measure_number(previous_metadata):
    assert previous_metadata, repr(previous_metadata)
    previous_final_measure_number = previous_metadata.get("final_measure_number")
    if previous_final_measure_number is None:
        return 1
    first_measure_number = previous_final_measure_number + 1
    return first_measure_number


def _find_repeat_pitch_classes(argument):
    violators = []
    for voice in abjad.iterate.components(argument, abjad.Voice):
        if abjad.get.has_indicator(voice, _enums.INTERMITTENT):
            continue
        previous_lt, previous_pcs = None, set()
        for lt in abjad.iterate.logical_ties(voice):
            if abjad.get.has_indicator(lt.head, _enums.HIDDEN):
                written_pitches = set()
            elif isinstance(lt.head, abjad.Note):
                written_pitches = set([lt.head.written_pitch])
            elif isinstance(lt.head, abjad.Chord):
                written_pitches = set(lt.head.written_pitches)
            else:
                written_pitches = set()
            pcs = set(abjad.NamedPitchClass(_) for _ in written_pitches)
            if abjad.get.has_indicator(
                lt.head, _enums.NOT_YET_PITCHED
            ) or abjad.get.has_indicator(lt.head, _enums.ALLOW_REPEAT_PITCH):
                pass
            elif pcs & previous_pcs:
                if previous_lt not in violators:
                    violators.append(previous_lt)
                if lt not in violators:
                    violators.append(lt)
            previous_lt = lt
            previous_pcs = pcs
    return violators


def _force_nonnatural_accidentals(score):
    natural = abjad.Accidental("natural")
    for plt in _select.plts(score):
        if isinstance(plt[0], abjad.Note):
            note_heads = [plt[0].note_head]
        else:
            note_heads = plt[0].note_heads
        for note_head in note_heads:
            if note_head.written_pitch.accidental != natural:
                note_head.is_forced = True


def _get_fermata_measure_numbers(first_measure_number, score):
    fermata_start_offsets, fermata_measure_numbers = [], []
    final_measure_is_fermata = False
    if "Rests" in score:
        context = score["Rests"]
        rests = abjad.select.leaves(context, abjad.MultimeasureRest)
        final_measure_index = len(rests)
        final_measure_index -= 1
        indicator = _enums.FERMATA_MEASURE
        for measure_index, rest in enumerate(rests):
            if not abjad.get.has_indicator(rest, indicator):
                continue
            if measure_index == final_measure_index:
                final_measure_is_fermata = True
            measure_number = first_measure_number + measure_index
            timespan = abjad.get.timespan(rest)
            fermata_start_offsets.append(timespan.start_offset)
            fermata_measure_numbers.append(measure_number)
    return (
        fermata_start_offsets,
        fermata_measure_numbers,
        final_measure_is_fermata,
    )


def _get_measure_number_tag(leaf, offset_to_measure_number):
    start_offset = abjad.get.timespan(leaf).start_offset
    measure_number = offset_to_measure_number.get(start_offset)
    if measure_number is not None:
        return abjad.Tag(f"MEASURE_{measure_number}")


def _get_measure_offsets(score, start_measure, stop_measure):
    skips = _select.skips(score["Skips"])
    start_skip = skips[start_measure - 1]
    assert isinstance(start_skip, abjad.Skip), start_skip
    start_offset = abjad.get.timespan(start_skip).start_offset
    stop_skip = skips[stop_measure - 1]
    assert isinstance(stop_skip, abjad.Skip), stop_skip
    stop_offset = abjad.get.timespan(stop_skip).stop_offset
    return start_offset, stop_offset


def _get_measure_time_signatures(
    measure_count,
    score,
    time_signatures,
    start_measure=None,
    stop_measure=None,
):
    assert stop_measure is not None
    start_index = start_measure - 1
    if stop_measure is None:
        time_signatures = [time_signatures[start_index]]
    else:
        if stop_measure == -1:
            stop_measure = measure_count
        stop_index = stop_measure
        time_signatures = time_signatures[start_index:stop_index]
    measure_timespan = _get_measure_timespan(score, start_measure)
    return measure_timespan.start_offset, time_signatures


def _get_measure_timespan(score, measure_number):
    start_offset, stop_offset = _get_measure_offsets(
        score,
        measure_number,
        measure_number,
    )
    return abjad.Timespan(start_offset, stop_offset)


def _label_clock_time(
    clock_time_override,
    fermata_measure_numbers,
    first_measure_number,
    previous_metadata,
    score,
):
    skips = _select.skips(score["Skips"])
    previous_stop_clock_time = previous_metadata.get("stop_clock_time")
    result = _calculate_clock_times(
        score,
        clock_time_override,
        fermata_measure_numbers,
        first_measure_number,
        previous_stop_clock_time,
    )
    duration = result[0]
    clock_times = result[1]
    start_clock_time = result[2]
    stop_clock_time = result[3]
    if clock_times is None:
        return None, start_clock_time, None
    total = len(skips)
    clock_times = clock_times[:total]
    final_clock_time = clock_times[-1]
    final_clock_string = final_clock_time.to_clock_string()
    final_seconds = int(final_clock_time)
    final_fermata_string = f"{final_seconds}''"
    final_measure_number = first_measure_number + total - 1
    final_is_fermata = False
    if final_measure_number in fermata_measure_numbers:
        final_is_fermata = True
    for measure_index in range(len(skips)):
        measure_number = first_measure_number + measure_index
        is_fermata = False
        if measure_number in fermata_measure_numbers:
            is_fermata = True
        skip = skips[measure_index]
        clock_time = clock_times[measure_index]
        clock_string = clock_time.to_clock_string()
        seconds = int(clock_time)
        fermata_string = f"{seconds}''"
        if measure_index < total - 1:
            tag = _tags.CLOCK_TIME
            if measure_index == total - 2:
                if is_fermata and final_is_fermata:
                    string = r"- \baca-start-ct-both-fermata"
                    string += f' "{fermata_string}" "{final_fermata_string}"'
                elif is_fermata and not final_is_fermata:
                    string = r"- \baca-start-ct-both-left-fermata"
                    string += f' "{fermata_string}" "[{final_clock_string}]"'
                elif not is_fermata and final_is_fermata:
                    string = r"- \baca-start-ct-both-right-fermata"
                    string += f' "[{clock_string}]" "{final_fermata_string}"'
                else:
                    string = r"- \baca-start-ct-both"
                    string += f' "[{clock_string}]" "[{final_clock_string}]"'
            else:
                if not is_fermata:
                    string = r"- \baca-start-ct-left-only"
                    string += f' "[{clock_string}]"'
                else:
                    seconds = int(clock_time)
                    string = r"- \baca-start-ct-left-only-fermata"
                    string += f' "{fermata_string}"'
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanCT", left_text=string
            )
            abjad.attach(
                start_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag.append(_tags.function_name(_frame())),
            )
        if 0 < measure_index:
            tag = _tags.CLOCK_TIME
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanCT")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag.append(_tags.function_name(_frame())),
            )
    return duration, start_clock_time, stop_clock_time


def _label_duration_multipliers(score):
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.DURATION_MULTIPLIER)
    already_labeled = set()
    for voice in abjad.iterate.components(score, abjad.Voice):
        for leaf in abjad.iterate.leaves(voice):
            if isinstance(leaf, abjad.Skip):
                continue
            if leaf.multiplier is None:
                continue
            if leaf in already_labeled:
                continue
            n, d = leaf.multiplier.pair
            string = r"\baca-duration-multiplier-markup"
            string += f' #"{n}" #"{d}"'
            markup = abjad.Markup(string)
            tag_ = tag
            if abjad.get.has_indicator(leaf, _enums.HIDDEN):
                tag_ = tag_.append(_tags.HIDDEN)
            if abjad.get.has_indicator(leaf, _enums.MULTIMEASURE_REST):
                tag_ = tag_.append(_tags.MULTIMEASURE_REST)
            if abjad.get.has_indicator(leaf, _enums.NOTE):
                tag_ = tag_.append(_tags.NOTE)
            if abjad.get.has_indicator(leaf, _enums.REST_VOICE):
                tag_ = tag_.append(_tags.REST_VOICE)
            abjad.attach(markup, leaf, deactivate=True, direction=abjad.UP, tag=tag_)
            already_labeled.add(leaf)


def _label_measure_numbers(first_measure_number, global_skips):
    skips = _select.skips(global_skips)
    total = len(skips)
    for measure_index, skip in enumerate(skips):
        local_measure_number = measure_index + 1
        measure_number = first_measure_number + measure_index
        if measure_index < total - 1:
            tag = _tags.LOCAL_MEASURE_NUMBER
            tag = tag.append(_tags.function_name(_frame()))
            string = r"- \baca-start-lmn-left-only"
            string += f' "{local_measure_number}"'
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanLMN", left_text=string
            )
            abjad.attach(
                start_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
            tag = _tags.MEASURE_NUMBER
            tag = tag.append(_tags.function_name(_frame()))
            string = r"- \baca-start-mn-left-only"
            string += f' "{measure_number}"'
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanMN", left_text=string
            )
            abjad.attach(
                start_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
        if 0 < measure_index:
            tag = _tags.LOCAL_MEASURE_NUMBER
            tag = tag.append(_tags.function_name(_frame()))
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanLMN")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
            tag = _tags.MEASURE_NUMBER
            tag = tag.append(_tags.function_name(_frame()))
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMN")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )


def _magnify_staves(magnify_staves, score):
    if magnify_staves is None:
        return
    if isinstance(magnify_staves, tuple):
        multiplier, tag = magnify_staves
    else:
        multiplier, tag = magnify_staves, None
    multiplier = abjad.Multiplier(multiplier)
    numerator, denominator = multiplier.pair
    string = rf"\magnifyStaff #{numerator}/{denominator}"
    tag = abjad.Tag(tag)
    tag = tag.append(_tags.function_name(_frame()))
    for staff in abjad.iterate.components(score, abjad.Staff):
        first_leaf = abjad.get.leaf(staff, 0)
        assert first_leaf is not None
        literal = abjad.LilyPondLiteral(string)
        abjad.attach(literal, first_leaf, tag=tag)


def _make_global_context():
    global_rests = abjad.Context(lilypond_type="GlobalRests", name="Rests")
    global_skips = abjad.Context(lilypond_type="GlobalSkips", name="Skips")
    global_context = abjad.Context(
        [global_rests, global_skips],
        lilypond_type="GlobalContext",
        simultaneous=True,
        name="GlobalContext",
    )
    return global_context


def _make_global_rests(global_rests, time_signatures):
    rests = []
    for time_signature in time_signatures:
        rest = abjad.MultimeasureRest(
            abjad.Duration(1),
            multiplier=abjad.NonreducedFraction(time_signature.pair),
            tag=_tags.function_name(_frame(), n=1),
        )
        rests.append(rest)
    global_rests.extend(rests)


def _make_global_skips(
    global_skips,
    time_signatures,
    *,
    append_anchor_skip=False,
):
    for time_signature in time_signatures:
        skip = abjad.Skip(
            1,
            multiplier=abjad.NonreducedFraction(time_signature.pair),
            tag=_tags.function_name(_frame(), n=1),
        )
        abjad.attach(
            time_signature,
            skip,
            context="Score",
            tag=_tags.function_name(_frame(), n=2),
        )
        global_skips.append(skip)
    if append_anchor_skip:
        tag = _tags.function_name(_frame(), n=3)
        tag = tag.append(_tags.ANCHOR_SKIP)
        skip = abjad.Skip(1, multiplier=(1, 4), tag=tag)
        abjad.attach(_enums.ANCHOR_SKIP, skip)
        global_skips.append(skip)
        if time_signature != abjad.TimeSignature((1, 4)):
            time_signature = abjad.TimeSignature((1, 4))
            # abjad.attach(time_signature, skip, context="Score", tag=tag)
            abjad.attach(time_signature, skip, context="Score", tag=None)


def _memento_to_indicator(dictionary, memento):
    if memento.manifest is not None:
        if dictionary is None:
            raise Exception(f"can not find {memento.manifest!r} manifest.")
        return dictionary.get(memento.value)
    baca = importlib.import_module("baca")
    globals_ = globals()
    globals_["baca"] = baca
    class_ = eval(memento.prototype, globals_)
    if hasattr(class_, "from_string"):
        indicator = class_.from_string(memento.value)
    elif class_ is abjad.Dynamic and memento.value.startswith("\\"):
        indicator = class_(name="", command=memento.value)
    elif isinstance(memento.value, class_):
        indicator = memento.value
    elif class_ is _indicatorclasses.StaffLines:
        indicator = class_(line_count=memento.value)
    elif memento.value is None:
        indicator = class_()
    elif isinstance(memento.value, dict):
        indicator = class_(**memento.value)
    else:
        try:
            indicator = class_(memento.value)
        except Exception:
            raise Exception(repr(memento))
    return indicator


def _move_global_rests(
    global_rests_in_every_staff,
    global_rests_in_topmost_staff,
    score,
):
    if not (global_rests_in_topmost_staff or global_rests_in_every_staff):
        return
    if "Rests" not in score:
        return
    global_rests = score["Rests"]
    score["GlobalContext"].remove(global_rests)
    music_context = score["MusicContext"]
    if global_rests_in_topmost_staff is True:
        for staff in abjad.iterate.components(music_context, abjad.Staff):
            break
        staff.simultaneous = True
        staff.insert(0, global_rests)
    elif global_rests_in_every_staff is True:
        topmost_staff = True
        tag = global_rests.tag or abjad.Tag()
        for staff in abjad.iterate.components(music_context, abjad.Staff):
            staff.simultaneous = True
            global_rests_ = copy.deepcopy(global_rests)
            if not topmost_staff:
                global_rests_._tag = tag.append(_tags.NOT_TOPMOST)
            staff.insert(0, global_rests_)
            topmost_staff = False


def _populate_offset_to_measure_number(first_measure_number, global_skips):
    measure_number = first_measure_number
    offset_to_measure_number = {}
    for skip in _select.skips(global_skips):
        offset = abjad.get.timespan(skip).start_offset
        offset_to_measure_number[offset] = measure_number
        measure_number += 1
    return offset_to_measure_number


def _prototype_string(class_):
    parts = class_.__module__.split(".")
    if parts[-1] != class_.__name__:
        parts.append(class_.__name__)
    return f"{parts[0]}.{parts[-1]}"


def _reapply_persistent_indicators(
    manifests,
    previous_persistent_indicators,
    score,
    *,
    already_reapplied_contexts=None,
    do_not_iterate=None,
):
    if already_reapplied_contexts is None:
        already_reapplied_contexts = set()
    if do_not_iterate is not None:
        contexts = [do_not_iterate]
    else:
        contexts = abjad.select.components(score, abjad.Context)
    for context in contexts:
        if context.name in already_reapplied_contexts:
            continue
        already_reapplied_contexts.add(context.name)
        mementos = previous_persistent_indicators.get(context.name)
        if not mementos:
            continue
        for memento in mementos:
            if memento.manifest is not None:
                if memento.manifest == "instruments":
                    dictionary = manifests["abjad.Instrument"]
                elif memento.manifest == "metronome_marks":
                    dictionary = manifests.get("abjad.MetronomeMark")
                elif memento.manifest == "short_instrument_names":
                    dictionary = manifests["abjad.ShortInstrumentName"]
                else:
                    raise Exception(memento.manifest)
            else:
                dictionary = None
            result = _analyze_memento(score, dictionary, context, memento)
            if result is None:
                continue
            leaf, previous_indicator, status, edition, synthetic_offset = result
            if isinstance(previous_indicator, abjad.TimeSignature):
                if status in (None, "explicit"):
                    continue
                assert status == "reapplied", repr(status)
                wrapper = abjad.get.wrapper(leaf, abjad.TimeSignature)
                function_name = _tags.function_name(_frame(), n=1)
                edition = edition.append(function_name)
                wrapper.tag = wrapper.tag.append(edition)
                _treat.treat_persistent_wrapper(manifests, wrapper, status)
                continue
            # TODO: change to parameter comparison
            prototype = (
                _indicatorclasses.Accelerando,
                abjad.MetronomeMark,
                _indicatorclasses.Ritardando,
            )
            if isinstance(previous_indicator, prototype):
                function_name = _tags.function_name(_frame(), n=2)
                if status == "reapplied":
                    wrapper = abjad.attach(
                        previous_indicator,
                        leaf,
                        synthetic_offset=synthetic_offset,
                        tag=edition.append(function_name),
                        wrapper=True,
                    )
                    _treat.treat_persistent_wrapper(manifests, wrapper, status)
                else:
                    assert status in ("redundant", None), repr(status)
                    if status is None:
                        status = "explicit"
                    wrappers = abjad.get.wrappers(leaf, prototype)
                    # lone metronome mark or lone tempo trend:
                    if len(wrappers) == 1:
                        wrapper = wrappers[0]
                    # metronome mark + tempo trend:
                    else:
                        assert 1 < len(wrappers), repr(wrappers)
                        prototype = abjad.MetronomeMark
                        wrapper = abjad.get.wrapper(leaf, prototype)
                    wrapper.tag = wrapper.tag.append(edition)
                    _treat.treat_persistent_wrapper(manifests, wrapper, status)
                continue
            attached = False
            function_name = _tags.function_name(_frame(), n=3)
            tag = edition.append(function_name)
            if isinstance(previous_indicator, abjad.ShortInstrumentName):
                if _tags.NOT_PARTS.string not in tag.string:
                    tag = tag.append(_tags.NOT_PARTS)
            try:
                wrapper = abjad.attach(
                    previous_indicator,
                    leaf,
                    check_duplicate_indicator=True,
                    synthetic_offset=synthetic_offset,
                    tag=tag,
                    wrapper=True,
                )
                attached = True
            except abjad.PersistentIndicatorError:
                pass
            if attached:
                _treat.treat_persistent_wrapper(manifests, wrapper, status)


def _reanalyze_reapplied_synthetic_wrappers(score):
    function_name = _tags.function_name(_frame())
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if wrapper.synthetic_offset is None:
                continue
            if 0 <= wrapper.synthetic_offset:
                continue
            if "REAPPLIED" in wrapper.tag.string:
                string = wrapper.tag.string
                string = string.replace("REAPPLIED", "EXPLICIT")
                words = string.split(":")
                if abjad.sequence.has_duplicates(words):
                    words_ = []
                    for word in words:
                        if word not in words_:
                            words_.append(word)
                    words = words_
                string = ":".join(words)
                tag_ = abjad.Tag(string)
                tag_ = tag_.append(function_name)
                wrapper._tag = tag_
                wrapper._synthetic_offset = None


def _reanalyze_trending_dynamics(manifests, score):
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if isinstance(
                wrapper.unbundle_indicator(), abjad.Dynamic
            ) and abjad.get.indicators(leaf, abjad.StartHairpin):
                _treat.treat_persistent_wrapper(manifests, wrapper, "explicit")


def _remove_layout_tags(score):
    layout_removal_tags = _tags.layout_removal_tags()
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if wrapper.tag is None:
                continue
            for word in wrapper.tag.words():
                if abjad.Tag(word) in layout_removal_tags:
                    abjad.detach(wrapper, leaf)
                    break


def _set_intermittent_to_staff_position_zero(score):
    pleaves = []
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice._has_indicator(_enums.INTERMITTENT):
            for pleaf in abjad.iterate.leaves(voice, pitched=True):
                if abjad.get.has_indicator(pleaf, _enums.NOT_YET_PITCHED):
                    pleaves.append(pleaf)
    _pitchcommands.staff_position(
        pleaves,
        0,
        allow_hidden=True,
        set_chord_pitches_equal=True,
    )


def _set_not_yet_pitched_to_staff_position_zero(score):
    pleaves = []
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, _enums.NOT_YET_PITCHED):
            continue
        pleaves.append(pleaf)
    _pitchcommands.staff_position(
        pleaves,
        0,
        allow_hidden=True,
        set_chord_pitches_equal=True,
    )


def _shift_measure_initial_clefs(
    first_measure_number,
    offset_to_measure_number,
    score,
):
    for staff in abjad.iterate.components(score, abjad.Staff):
        for leaf in abjad.iterate.leaves(staff):
            start_offset = abjad.get.timespan(leaf).start_offset
            wrapper = abjad.get.wrapper(leaf, abjad.Clef)
            if wrapper is None or not wrapper.tag:
                continue
            if _tags.EXPLICIT_CLEF.string not in wrapper.tag.words():
                continue
            measure_number = offset_to_measure_number.get(start_offset)
            if measure_number is None:
                continue
            clef = wrapper.unbundle_indicator()
            _overridecommands.clef_shift(leaf, clef, first_measure_number)


# TODO: make public
def _sort_dictionary(dictionary):
    items = list(dictionary.items())
    items.sort()
    dictionary.clear()
    for key, value in items:
        if isinstance(value, dict):
            _sort_dictionary(value)
        dictionary[key] = value


def _style_anchor_notes(score):
    for note in abjad.select.components(score, abjad.Note):
        if not abjad.get.has_indicator(note, _enums.ANCHOR_NOTE):
            continue
        _append_tag_to_wrappers(note, _tags.function_name(_frame()))
        _append_tag_to_wrappers(note, _tags.ANCHOR_NOTE)


def _style_anchor_skip(score):
    global_skips = score["Skips"]
    skip = abjad.get.leaf(global_skips, -1)
    if not abjad.get.has_indicator(skip, _enums.ANCHOR_SKIP):
        return
    for literal in abjad.get.indicators(skip, abjad.LilyPondLiteral):
        if r"\baca-time-signature-color" in literal.argument:
            abjad.detach(literal, skip)
    tag = _tags.function_name(_frame(), n=1)
    tag = tag.append(_tags.ANCHOR_SKIP)
    _append_tag_to_wrappers(skip, tag)
    if abjad.get.has_indicator(skip, abjad.TimeSignature):
        tag = _tags.function_name(_frame(), n=2)
        tag = tag.append(_tags.ANCHOR_SKIP)
        abjad.attach(
            abjad.LilyPondLiteral(r"\baca-time-signature-transparent"), skip, tag=tag
        )
    tag = _tags.function_name(_frame(), n=3)
    tag = tag.append(_tags.ANCHOR_SKIP)
    abjad.attach(
        abjad.LilyPondLiteral(
            [
                r"\once \override Score.BarLine.transparent = ##t",
                r"\once \override Score.SpanBar.transparent = ##t",
            ],
            site="after",
        ),
        skip,
        tag=tag,
    )


def _style_fermata_measures(
    fermata_extra_offset_y,
    fermata_measure_empty_overrides,
    fermata_start_offsets,
    final_section,
    offset_to_measure_number,
    score,
):
    if not fermata_measure_empty_overrides:
        return
    if not fermata_start_offsets:
        return
    bar_lines_already_styled = []
    empty_fermata_measure_start_offsets = []
    for measure_number in fermata_measure_empty_overrides or []:
        timespan = _get_measure_timespan(score, measure_number)
        empty_fermata_measure_start_offsets.append(timespan.start_offset)
    for staff in abjad.iterate.components(score, abjad.Staff):
        for leaf in abjad.iterate.leaves(staff):
            if abjad.get.has_indicator(leaf, (_enums.ANCHOR_NOTE, _enums.ANCHOR_SKIP)):
                continue
            start_offset = abjad.get.timespan(leaf).start_offset
            if start_offset not in fermata_start_offsets:
                continue
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            if "Rests" in voice.name:
                continue
            if start_offset not in empty_fermata_measure_start_offsets:
                continue
            empty_staff_lines = _indicatorclasses.StaffLines(0)
            empty_bar_extent = _indicatorclasses.BarExtent(0)
            previous_staff_lines = abjad.get.effective(
                leaf, _indicatorclasses.StaffLines
            )
            previous_bar_extent = abjad.get.effective(leaf, _indicatorclasses.BarExtent)
            next_leaf = abjad.get.leaf(leaf, 1)
            anchors = (_enums.ANCHOR_NOTE, _enums.ANCHOR_SKIP)
            if next_leaf is not None:
                if abjad.get.has_indicator(next_leaf, anchors):
                    next_leaf = None
            next_staff_lines = None
            if next_leaf is not None:
                next_staff_lines = abjad.get.effective(
                    next_leaf, _indicatorclasses.StaffLines
                )
                next_bar_extent = abjad.get.effective(
                    next_leaf, _indicatorclasses.BarExtent
                )
            if (
                previous_staff_lines != empty_staff_lines
            ) and not abjad.get.has_indicator(leaf, _indicatorclasses.StaffLines):
                abjad.attach(
                    empty_staff_lines,
                    leaf,
                    tag=_tags.function_name(_frame(), n=1),
                )
                if not final_section:
                    abjad.attach(
                        empty_bar_extent,
                        leaf,
                        tag=_tags.function_name(_frame(), n=2).append(
                            _tags.FERMATA_MEASURE_EMPTY_BAR_EXTENT
                        ),
                    )
            if next_leaf is not None and empty_staff_lines != next_staff_lines:
                if next_staff_lines is None:
                    next_staff_lines_ = _indicatorclasses.StaffLines(5)
                else:
                    next_staff_lines_ = next_staff_lines
                if next_bar_extent is None:
                    next_bar_extent_ = _indicatorclasses.StaffLines(5)
                else:
                    next_bar_extent_ = next_bar_extent
                wrapper = abjad.get.effective_wrapper(
                    next_leaf, _indicatorclasses.StaffLines
                )
                next_leaf_start_offset = abjad.get.timespan(next_leaf).start_offset
                if wrapper is None or (wrapper.start_offset != next_leaf_start_offset):
                    abjad.attach(
                        next_staff_lines_,
                        next_leaf,
                        tag=_tags.function_name(_frame(), n=3),
                    )
                    abjad.attach(
                        next_bar_extent_,
                        next_leaf,
                        tag=_tags.function_name(_frame(), n=4).append(
                            _tags.FERMATA_MEASURE_NEXT_BAR_EXTENT
                        ),
                    )
            if next_leaf is None and previous_staff_lines != empty_staff_lines:
                previous_line_count = 5
                if previous_staff_lines is not None:
                    previous_line_count = previous_staff_lines.line_count
                resume_staff_lines = _indicatorclasses.StaffLines(
                    previous_line_count, hide=True
                )
                abjad.attach(
                    resume_staff_lines,
                    leaf,
                    synthetic_offset=99,
                    tag=_tags.function_name(_frame(), n=5),
                )
                previous_line_count = 5
                if previous_bar_extent is not None:
                    previous_line_count = previous_bar_extent.line_count
                resume_bar_extent = _indicatorclasses.BarExtent(
                    previous_line_count, hide=True
                )
                abjad.attach(
                    resume_bar_extent,
                    leaf,
                    synthetic_offset=99,
                    tag=_tags.function_name(_frame(), n=6).append(
                        _tags.FERMATA_MEASURE_RESUME_BAR_EXTENT
                    ),
                )
            if start_offset in bar_lines_already_styled:
                continue
            bar_lines_already_styled.append(start_offset)
    rests = abjad.select.leaves(score["Rests"], abjad.MultimeasureRest)
    for measure_number in fermata_measure_empty_overrides:
        measure_index = measure_number - 1
        rest = rests[measure_index]
        grob = abjad.override(rest).MultiMeasureRestText
        grob.extra_offset = (0, fermata_extra_offset_y)
        next_leaf = abjad.get.leaf(rest, 1)
        if not (next_leaf is None and final_section):
            # TODO: replace literal with override
            strings = []
            string = r"Score.BarLine.transparent = ##t"
            string = r"\once \override " + string
            strings.append(string)
            string = r"Score.SpanBar.transparent = ##t"
            string = r"\once \override " + string
            strings.append(string)
            literal = abjad.LilyPondLiteral(strings, site="after")
            tag = _tags.FERMATA_MEASURE
            measure_number_tag = _get_measure_number_tag(
                rest,
                offset_to_measure_number,
            )
            if measure_number_tag is not None:
                tag = tag.append(measure_number_tag)
            abjad.attach(
                literal,
                rest,
                tag=tag.append(_tags.function_name(_frame(), n=7)),
            )


def transpose_score(score):
    for pleaf in _select.pleaves(score):
        if abjad.get.has_indicator(pleaf, _enums.DO_NOT_TRANSPOSE):
            continue
        if abjad.get.has_indicator(pleaf, _enums.STAFF_POSITION):
            continue
        abjad.iterpitches.transpose_from_sounding_pitch(pleaf)


_transpose_score_alias = transpose_score


def treat_untreated_persistent_wrappers(score, *, manifests=None):
    manifests = manifests or {}
    dynamic_prototype = (abjad.Dynamic, abjad.StartHairpin)
    tempo_prototype = (
        _indicatorclasses.Accelerando,
        abjad.MetronomeMark,
        _indicatorclasses.Ritardando,
    )
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if not getattr(wrapper.unbundle_indicator(), "persistent", False):
                continue
            if wrapper.tag and _tags.has_persistence_tag(wrapper.tag):
                continue
            if isinstance(wrapper.unbundle_indicator(), abjad.Instrument):
                prototype = abjad.Instrument
            elif isinstance(wrapper.unbundle_indicator(), dynamic_prototype):
                prototype = dynamic_prototype
            elif isinstance(wrapper.unbundle_indicator(), tempo_prototype):
                prototype = tempo_prototype
            else:
                prototype = type(wrapper.unbundle_indicator())
            # TODO: optimize
            previous_indicator = abjad.get.effective(leaf, prototype, n=-1)
            if _treat.compare_persistent_indicators(
                previous_indicator, wrapper.unbundle_indicator()
            ):
                status = "redundant"
            else:
                status = "explicit"
            _treat.treat_persistent_wrapper(manifests, wrapper, status)


_treat_untreated_persistent_wrappers_alias = treat_untreated_persistent_wrappers


def _update_score_one_time(score):
    is_forbidden_to_update = score._is_forbidden_to_update
    score._is_forbidden_to_update = False
    abjad._updatelib._update_now(score, offsets=True)
    score._is_forbidden_to_update = is_forbidden_to_update


def _whitespace_leaves(score):
    for leaf in abjad.iterate.leaves(score):
        literal = abjad.LilyPondLiteral("", site="absolute_before")
        abjad.attach(literal, leaf, tag=None)
    for container in abjad.iterate.components(score, abjad.Container):
        if hasattr(container, "_main_leaf"):
            literal = abjad.LilyPondLiteral("", site="absolute_after")
            abjad.attach(literal, container, tag=None)
        else:
            literal = abjad.LilyPondLiteral("", site="absolute_before")
            abjad.attach(literal, container, tag=None)
        literal = abjad.LilyPondLiteral("", site="closing")
        abjad.attach(literal, container, tag=None)


class CacheGetItemWrapper:
    def __init__(self, voice_name_to_leaves_by_measure, voice_abbreviations):
        self.voice_name_to_leaves_by_measure = voice_name_to_leaves_by_measure
        self.abbreviation_to_voice_name = {}
        for abbreviation, voice_name in voice_abbreviations.items():
            self.abbreviation_to_voice_name[abbreviation] = voice_name

    def __getattr__(self, string):
        return self.__getitem__(string)

    def __getitem__(self, argument):
        try:
            measure_number_to_leaves = self.voice_name_to_leaves_by_measure[argument]
        except KeyError:
            voice_name = self.abbreviation_to_voice_name[argument]
            measure_number_to_leaves = self.voice_name_to_leaves_by_measure[voice_name]
        return DictionaryGetItemWrapper(measure_number_to_leaves)

    @staticmethod
    def _get_for_voice(result, voice, argument):
        if isinstance(argument, int):
            assert 1 <= argument, repr(argument)
            result_ = voice[argument]
            result.append(result_)
        elif isinstance(argument, tuple):
            assert len(argument) == 2, repr(argument)
            result_ = voice[argument]
            result.append(result_)
        else:
            assert isinstance(argument, list), repr(argument)
            for pair in argument:
                assert isinstance(pair, tuple), repr(pair)
                assert len(pair) == 2, repr(pair)
                result_ = voice[pair]
                result.append(result_)

    def get(self, *items):
        result = []
        for item in items:
            if isinstance(item, str):
                voice = self[item]
                result.append(voice)
            elif isinstance(item, tuple):
                assert len(item) == 2, repr(item)
                if isinstance(item[0], str):
                    voice = self[item[0]]
                    self._get_for_voice(result, voice, item[1])
                else:
                    assert isinstance(item[0], list), repr(item[0])
                    for abbreviation in item[0]:
                        assert isinstance(abbreviation, str), repr(abbreviation)
                        voice = self[abbreviation]
                        self._get_for_voice(result, voice, item[1])
            else:
                assert isinstance(item, list), repr(item)
                for item_ in item:
                    result_ = self.get(item_)
                    result.append(result_)
        return result

    def rebuild(self):
        cache = cache_leaves(
            self._score, self._measure_count, self._voice_abbreviations
        )
        self.voice_name_to_leaves_by_measure = cache.voice_name_to_leaves_by_measure


class DictionaryGetItemWrapper:
    def __init__(self, measure_number_to_leaves):
        self.measure_number_to_leaves = measure_number_to_leaves

    def __getitem__(self, argument):
        if isinstance(argument, int):
            result = self.measure_number_to_leaves[argument]
        else:
            result = []
            assert isinstance(argument, tuple), repr(argument)
            start, stop = argument
            assert 0 < start, repr(start)
            assert 0 < stop, repr(stop)
            for number in range(start, stop + 1):
                try:
                    leaves = self.measure_number_to_leaves[number]
                except KeyError:
                    leaves = []
                result.extend(leaves)
        return result

    def get(self, start, stop=None):
        if stop is not None:
            return self.__getitem__((start, stop))
        else:
            return self.__getitem__(start)

    def leaves(self):
        result = []
        for measure_number, leaves in self.measure_number_to_leaves.items():
            result.extend(leaves)
        return result


class DynamicScope:
    def __init__(self, argument):
        self.argument = argument

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self.argument

    def __getitem__(self, i):
        return self.argument.__getitem__(i)

    def __iter__(self):
        try:
            return iter(self.argument)
        except TypeError:
            return iter([self.argument])

    def __len__(self):
        try:
            return len(self.argument)
        except TypeError:
            return 1

    def leaf(self, n, *, grace=None):
        return abjad.select.leaf(self.argument, n, exclude=_enums.HIDDEN, grace=grace)

    def leaves(self, *, grace=None):
        return abjad.select.leaves(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def lleaf(self, n):
        return _select.lleaf(self.argument, n, exclude=_enums.HIDDEN)

    def lleaves(self, *, count=None):
        return _select.lleaves(self.argument, count=count, exclude=_enums.HIDDEN)

    def ltleaves(self):
        return _select.ltleaves(self.argument, exclude=_enums.HIDDEN)

    def mmrest(self, n):
        return _select.mmrest(self.argument, n, exclude=_enums.HIDDEN)

    def mmrests(self):
        return _select.mmrests(self.argument, exclude=_enums.HIDDEN)

    def phead(self, n):
        return _select.phead(self.argument, n, exclude=_enums.HIDDEN)

    def pheads(self, *, grace=None):
        return _select.pheads(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def pleaf(self, n, *, grace=None):
        return _select.pleaf(self.argument, n, exclude=_enums.HIDDEN, grace=grace)

    def pleaves(self, *, grace=None):
        return _select.pleaves(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def plt(self, n):
        return _select.plt(self.argument, n, exclude=_enums.HIDDEN)

    def plts(self, *, grace=None):
        return _select.plts(self.argument, exclude=_enums.HIDDEN, grace=grace)

    def ptail(self, n):
        return _select.ptail(self.argument, n, exclude=_enums.HIDDEN)

    def ptails(self):
        return _select.ptails(self.argument, exclude=_enums.HIDDEN)

    def rest(self, n):
        return abjad.select.rest(self.argument, n, exclude=_enums.HIDDEN)

    def rests(self):
        return abjad.select.rests(self.argument)

    def rleaf(self, n):
        return _select.rleaf(self.argument, n)

    def rleak(self):
        return _select.rleak(self.argument)

    def rleaves(self, *, count=1):
        return _select.rleaves(self.argument, count=count, exclude=_enums.HIDDEN)

    def run(self, n):
        return abjad.select.run(self.argument, n, exclude=_enums.HIDDEN)

    def runs(self):
        return _select.runs(self.argument, exclude=_enums.HIDDEN)

    def tleaves(self, *, grace=None):
        return _select.tleaves(self.argument, grace=grace)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Measures:

    time_signatures: list[abjad.TimeSignature]

    def __call__(self, start=None, stop=None):
        if start is None and stop is None:
            return self.time_signatures
        assert 0 < start, start
        if stop is None:
            stop = start
        assert 0 < stop, stop
        return self.time_signatures[start - 1 : stop]


class VoiceCache:
    def __init__(self, score, voice_abbreviations=None):
        voices = []
        for voice in abjad.select.components(score, abjad.Voice):
            if hasattr(self, voice.name):
                continue
            voices.append(voice)
            setattr(self, voice.name, voice)
            if voice_abbreviations:
                for abbreviation, voice_name in voice_abbreviations.items():
                    if voice_name == voice.name:
                        setattr(self, abbreviation, voice)
        self._voices = voices

    def __call__(self, abbreviation):
        voice = getattr(self, abbreviation)
        return voice

    def __iter__(self):
        return iter(self._voices)


def append_anchor_note(argument, *, runtime=None):
    leaf = abjad.get.leaf(argument, 0)
    parentage = abjad.get.parentage(leaf)
    voice = parentage.get(abjad.Voice, n=-1)
    tag = abjad.Tag("baca.append_anchor_note(1)")
    tag = tag.append(_tags.ANCHOR_NOTE)
    tag = tag.append(_tags.HIDDEN)
    tag = tag.append(_tags.NOTE)
    note = abjad.Note("c'1", multiplier=(1, 4), tag=tag)
    abjad.attach(_enums.ANCHOR_NOTE, note)
    abjad.attach(_enums.HIDDEN, note)
    abjad.attach(_enums.NOT_YET_PITCHED, note)
    abjad.attach(_enums.NOTE, note)
    #
    tag = abjad.Tag("baca.append_anchor_note(2)")
    tag = tag.append(_tags.ANCHOR_NOTE)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
    tag = tag.append(_tags.NOTE)
    abjad.attach(
        abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring", site="before"),
        note,
        tag=tag,
    )
    #
    tag = abjad.Tag("baca.append_anchor_note(3)")
    tag = tag.append(_tags.ANCHOR_NOTE)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
    tag = tag.append(_tags.NOTE)
    abjad.attach(
        abjad.LilyPondLiteral(r"\abjad-invisible-music", site="before"),
        note,
        deactivate=True,
        tag=tag,
    )
    #
    abjad.attach(
        abjad.LilyPondLiteral(
            [
                r"\stopStaff",
                r"\once \override Staff.StaffSymbol.transparent = ##t",
                r"\startStaff",
            ]
        ),
        note,
        tag=abjad.Tag("baca.append_anchor_note(4)"),
    )
    #
    abjad.attach(
        # TODO: use override object once they exist and can be tagged
        abjad.LilyPondLiteral(r"\once \override Accidental.stencil = ##f"),
        note,
        tag=abjad.Tag("baca.append_anchor_note(5)"),
    )
    #
    voice.append(note)


def apply_breaks(score, breaks) -> None:
    if breaks is None:
        return
    global_skips = score["Skips"]
    skips = _select.skips(global_skips)
    measure_count = len(skips)
    literal = abjad.LilyPondLiteral(r"\autoPageBreaksOff", "before")
    abjad.attach(
        literal,
        skips[0],
        tag=_tags.BREAK.append(_tags.function_name(_frame(), n=1)),
    )
    for skip in skips[:measure_count]:
        if not abjad.get.has_indicator(skip, _layout.LBSD):
            literal = abjad.LilyPondLiteral(r"\noBreak", "before")
            abjad.attach(
                literal,
                skip,
                tag=_tags.BREAK.append(_tags.function_name(_frame(), n=2)),
            )
    tag = _tags.function_name(inspect.currentframe())
    tag = tag.append(_tags.BREAK)
    for skip_index, indicators in breaks.skip_index_to_indicators.items():
        measure_number = skip_index + 1
        if measure_count < measure_number:
            message = f"score ends at measure {measure_count}"
            message += f" (not {measure_number})."
            raise Exception(message)
        skip = global_skips[skip_index]
        for indicator in indicators:
            abjad.attach(
                indicator,
                skip,
                tag=tag,
            )


def cache_leaves(score, measure_count, voice_abbreviations=None):
    measure_timespans = []
    for measure_index in range(measure_count):
        measure_number = measure_index + 1
        measure_timespan = _get_measure_timespan(score, measure_number)
        measure_timespans.append(measure_timespan)
    voice_name_to_leaves_by_measure = {}
    for leaf in abjad.select.leaves(score):
        parentage = abjad.get.parentage(leaf)
        context = parentage.get(abjad.Context)
        measure_number_to_leaves = voice_name_to_leaves_by_measure.setdefault(
            context.name, {}
        )
        leaf_timespan = abjad.get.timespan(leaf)
        # TODO: replace loop with bisection:
        for i, measure_timespan in enumerate(measure_timespans):
            measure_number = i + 1
            if leaf_timespan.starts_during_timespan(measure_timespan):
                cached_leaves = measure_number_to_leaves.setdefault(measure_number, [])
                cached_leaves.append(leaf)
    if voice_abbreviations:
        voice_name_to_leaves_by_measure = CacheGetItemWrapper(
            voice_name_to_leaves_by_measure, voice_abbreviations
        )
        voice_name_to_leaves_by_measure._score = score
        voice_name_to_leaves_by_measure._measure_count = measure_count
        voice_name_to_leaves_by_measure._voice_abbreviations = voice_abbreviations
    return voice_name_to_leaves_by_measure


def cache_voices(score, voice_abbreviations=None):
    return VoiceCache(score, voice_abbreviations)


def color_octaves(score):
    vertical_moments = abjad.iterate_vertical_moments(score)
    markup = abjad.Markup(r"\markup OCTAVE")
    bundle = abjad.bundle(markup, r"- \tweak color #red")
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.OCTAVE_COLORING)
    for vertical_moment in vertical_moments:
        pleaves, pitches = [], []
        for leaf in vertical_moment.leaves:
            if abjad.get.has_indicator(leaf, _enums.HIDDEN):
                continue
            if abjad.get.has_indicator(leaf, _enums.STAFF_POSITION):
                continue
            if isinstance(leaf, abjad.Note):
                pleaves.append(leaf)
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pleaves.append(leaf)
                pitches.extend(leaf.written_pitches)
        if not pitches:
            continue
        pitch_classes = [_.pitch_class for _ in pitches]
        if _pcollections.has_duplicates([pitch_classes]):
            color = True
            for pleaf in pleaves:
                if abjad.get.has_indicator(pleaf, _enums.ALLOW_OCTAVE):
                    color = False
            if not color:
                continue
            for pleaf in pleaves:
                abjad.attach(bundle, pleaf, direction=abjad.UP, tag=tag)
                string = r"\baca-octave-coloring"
                literal = abjad.LilyPondLiteral(string, site="before")
                abjad.attach(literal, pleaf, tag=tag)


_color_octaves_alias = color_octaves


def color_out_of_range_pitches(score):
    indicator = _enums.ALLOW_OUT_OF_RANGE
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.OUT_OF_RANGE_COLORING)
    for voice in abjad.iterate.components(score, abjad.Voice):
        for pleaf in abjad.iterate.leaves(voice, pitched=True):
            if abjad.get.has_indicator(pleaf, _enums.HIDDEN):
                continue
            if abjad.get.has_indicator(pleaf, indicator):
                continue
            instrument = abjad.get.effective(pleaf, abjad.Instrument)
            if instrument is None:
                continue
            if not abjad.iterpitches.sounding_pitches_are_in_range(
                pleaf, instrument.pitch_range
            ):
                string = r"\baca-out-of-range-coloring"
                literal = abjad.LilyPondLiteral(string, site="before")
                abjad.attach(literal, pleaf, tag=tag)


def color_repeat_pitch_classes(score):
    tag = _tags.function_name(_frame())
    tag = tag.append(_tags.REPEAT_PITCH_CLASS_COLORING)
    lts = _find_repeat_pitch_classes(score)
    for lt in lts:
        for leaf in lt:
            string = r"\baca-repeat-pitch-class-coloring"
            literal = abjad.LilyPondLiteral(string, site="before")
            abjad.attach(literal, leaf, tag=tag)


def extend_beams(score):
    for leaf in abjad.iterate.leaves(score):
        if abjad.get.indicator(leaf, _enums.RIGHT_BROKEN_BEAM):
            _extend_beam(leaf)


def get_voice_names(score):
    voice_names = ["Skips", "Rests"]
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice.name is not None:
            voice_names.append(voice.name)
            words = voice.name.split(".")
            if "Music" in words:
                rest_voice_name = voice.name.replace("Music", "Rests")
                voice_names.append(rest_voice_name)
            elif "Voice" in words:
                rest_voice_name = f"{voice.name}.Rests"
                voice_names.append(rest_voice_name)
    return tuple(voice_names)


def label_moment_numbers(global_skips, moment_markup):
    if not moment_markup:
        return
    skips = _select.skips(global_skips)
    for i, item in enumerate(moment_markup):
        if len(item) == 2:
            value, lmn = item
            color = None
        elif len(item) == 3:
            value, lmn, color = item
        else:
            raise Exception(item)
        measure_index = lmn - 1
        skip = skips[measure_index]
        tag = _tags.MOMENT_NUMBER
        tag = tag.append(_tags.MOMENT_ANNOTATION_SPANNER)
        tag = tag.append(_tags.function_name(_frame()))
        if color is not None:
            string = rf'- \baca-start-xnm-colored-left-only "{value}" {color}'
        else:
            string = rf'- \baca-start-xnm-left-only "{value}"'
        start_text_span = abjad.StartTextSpan(
            command=r"\bacaStartTextSpanXNM", left_text=string
        )
        abjad.attach(
            start_text_span,
            skip,
            context="GlobalSkips",
            deactivate=True,
            tag=tag,
        )
        if 0 < i:
            tag = _tags.MOMENT_NUMBER
            tag = tag.append(_tags.MOMENT_ANNOTATION_SPANNER)
            tag = tag.append(_tags.function_name(_frame()))
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanXNM")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
    skip = skips[-1]
    tag = _tags.MOMENT_NUMBER
    tag = tag.append(_tags.MOMENT_ANNOTATION_SPANNER)
    tag = tag.append(_tags.function_name(_frame()))
    stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanXNM")
    abjad.attach(
        stop_text_span,
        skip,
        context="GlobalSkips",
        deactivate=True,
        tag=tag,
    )


def label_stage_numbers(global_skips, stage_markup):
    if not stage_markup:
        return
    skips = _select.skips(global_skips)
    for i, item in enumerate(stage_markup):
        if len(item) == 2:
            value, lmn = item
            color = None
        elif len(item) == 3:
            value, lmn, color = item
        else:
            raise Exception(item)
        measure_index = lmn - 1
        skip = skips[measure_index]
        tag = _tags.STAGE_NUMBER
        tag = tag.append(_tags.function_name(_frame()))
        if color is not None:
            string = r"- \baca-start-snm-colored-left-only"
            string += f' "{value}" {color}'
        else:
            string = r"- \baca-start-snm-left-only"
            string += f' "{value}"'
        start_text_span = abjad.StartTextSpan(
            command=r"\bacaStartTextSpanSNM", left_text=string
        )
        abjad.attach(
            start_text_span,
            skip,
            context="GlobalSkips",
            deactivate=True,
            tag=tag,
        )
        if 0 < i:
            tag = _tags.STAGE_NUMBER
            tag = tag.append(_tags.function_name(_frame()))
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSNM")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
    skip = skips[-1]
    tag = _tags.STAGE_NUMBER
    tag = tag.append(_tags.function_name(_frame()))
    stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSNM")
    abjad.attach(
        stop_text_span,
        skip,
        context="GlobalSkips",
        deactivate=True,
        tag=tag,
    )


def make_layout_ly(
    spacing,
    *,
    curtail_measure_count=None,
    do_not_tag=False,
    do_not_write_metadata=False,
    file_name="layout.ly",
    page_layout_context_only=False,
    time_signatures=None,
):
    layout_directory = pathlib.Path(os.getcwd())
    _build._print_main_task("Making layout ...")
    assert isinstance(spacing, _layout.SpacingSpecifier), repr(spacing)
    layout_py = layout_directory / "layout.py"
    layout_ly = layout_directory / file_name
    if spacing.overrides is not None:
        assert spacing.fallback_duration is not None
    if spacing.fallback_duration is None:
        eol_measure_numbers = None
        fermata_measure_numbers = None
        measure_count = None
    else:
        tuple_ = _path.get_measure_profile_metadata(layout_py)
        first_measure_number = tuple_[0]
        measure_count = tuple_[1]
        fermata_measure_numbers = tuple_[2] or []
        first_measure_number = first_measure_number or 1
        fermata_measure_numbers = [
            _ - (first_measure_number - 1) for _ in fermata_measure_numbers
        ]
        eol_measure_numbers = []
        for bol_measure_number in spacing.breaks.bol_measure_numbers[1:]:
            eol_measure_number = bol_measure_number - 1
            eol_measure_numbers.append(eol_measure_number)
    page_layout_profile = {
        "eol_measure_numbers": eol_measure_numbers,
        "fermata_measure_numbers": fermata_measure_numbers,
        "measure_count": measure_count,
    }
    has_anchor_skip = _path.get_metadatum(
        layout_directory,
        "has_anchor_skip",
    )
    document_name = abjad.string.to_shout_case(layout_directory.name)
    if time_signatures is not None:
        first_measure_number = 1
    elif layout_directory.parent.name == "sections":
        string = "first_measure_number"
        first_measure_number = _path.get_metadatum(layout_directory, string, default=1)
        if not bool(first_measure_number):
            _build._print_file_handling("Can not find first measure number ...")
            first_measure_number = False
        assert isinstance(first_measure_number, int)
        time_signatures = _path.get_metadatum(layout_directory, "time_signatures")
    else:
        first_measure_number = 1
        time_signatures = []
        contents_directory = _path.get_contents_directory(layout_directory)
        sections_directory = contents_directory / "sections"
        for section_directory in sorted(sections_directory.glob("*")):
            if not section_directory.is_dir():
                continue
            time_signatures_ = _path.get_metadatum(
                section_directory,
                "time_signatures",
            )
            time_signatures.extend(time_signatures_)
    if first_measure_number is False:
        raise Exception("first_measure_number should not be false")
        _build._print_file_handling(f"Skipping {_path.trim(layout_py)} ...")
        sys.exit(1)
    assert abjad.string.is_shout_case(document_name)
    score = _docs.make_empty_score(1, do_not_move_global_context=True)
    time_signatures_ = [abjad.TimeSignature.from_string(_) for _ in time_signatures]
    set_up_score(
        score,
        time_signatures_,
        append_anchor_skip=has_anchor_skip,
        do_not_reapply_persistent_indicators=True,
        layout=True,
    )
    spacing(score, page_layout_profile, has_anchor_skip=has_anchor_skip)
    # TODO: separate 'breaks' from SpacingSpecifier:
    apply_breaks(score, spacing.breaks)
    _ = postprocess_score(
        score,
        append_anchor_skip=has_anchor_skip,
        add_container_identifiers=True,
        comment_measure_numbers=True,
        do_not_check_wellformedness=True,
        environment=_build.Environment(
            first_measure_number=first_measure_number,
        ),
        first_section=True,
        whitespace_leaves=True,
    )
    _remove_layout_tags(score)
    lilypond_file = _lilypond.file(score)
    context = lilypond_file["Skips"]
    if curtail_measure_count is not None:
        del context[curtail_measure_count:]
    context.lilypond_type = "PageLayout"
    context.name = "PageLayout"
    skips = _select.skips(context)
    for skip in skips:
        abjad.detach(abjad.TimeSignature, skip)
    score = lilypond_file["Score"]
    del score["MusicContext"]
    score = lilypond_file["Score"]
    tags = not do_not_tag
    if page_layout_context_only:
        page_layout_context = score["PageLayout"]
        text = abjad.lilypond(page_layout_context, tags=tags)
    else:
        text = abjad.lilypond(score, tags=tags)
    text = text.replace("Skips", "PageLayout")
    text = text.replace("GlobalSkips", "PageLayout")
    # TODO: remove following line?
    text = text.replace("Global.Skips", "Page.Layout")
    text = abjad.tag.left_shift_tags(text)
    layout_ly = layout_directory / file_name
    lines = []
    # TODO: remove first_page_number embedding
    if layout_directory.parent.name == "sections":
        if layout_directory.name != "01":
            previous_section_number = str(int(layout_directory.name) - 1).zfill(2)
            previous_section_directory = (
                layout_directory.parent / previous_section_number
            )
            previous_layout_ly = previous_section_directory / "layout.ly"
            if previous_layout_ly.is_file():
                result = _build._get_preamble_page_count_overview(previous_layout_ly)
                if result is not None:
                    _, _, final_page_number = result
                    first_page_number = final_page_number + 1
                    line = f"% first_page_number = {first_page_number}"
                    lines.append(line)
    page_count = spacing.breaks.page_count
    lines.append(f"% page_count = {page_count}")
    time_signatures = [str(_) for _ in time_signatures]
    measure_count = len(time_signatures)
    lines.append(f"% measure_count = {measure_count} + 1")
    string = pprint.pformat(time_signatures, compact=True, width=80 - 3)
    lines_ = string.split("\n")
    lines_ = [_.strip("[").strip("]") for _ in lines_]
    lines_ = ["% " + _ for _ in lines_]
    lines_.insert(0, "% time_signatures = [")
    lines_.append("%  ]")
    lines.extend(lines_)
    header = "\n".join(lines) + "\n\n"
    layout_ly.write_text(header + text + "\n")
    counter = abjad.string.pluralize("measure", measure_count)
    message = f"Writing {measure_count} + 1 {counter} to"
    message += f" {_path.trim(layout_ly)} ..."
    _build._print_file_handling(message)
    bol_measure_numbers = []
    skips = abjad.iterate.leaves(score["PageLayout"], abjad.Skip)
    for i, skip in enumerate(skips):
        for literal in abjad.get.indicators(skip, abjad.LilyPondLiteral):
            if literal.argument in (r"\break", r"\pageBreak"):
                measure_number = first_measure_number + i
                bol_measure_numbers.append(measure_number)
                continue
    count = len(bol_measure_numbers)
    numbers = abjad.string.pluralize("number", count)
    items = ", ".join([str(_) for _ in bol_measure_numbers])
    if not do_not_write_metadata:
        metadata = layout_directory / ".metadata"
        string = _path.trim(metadata)
        message = f"Writing BOL measure {numbers} {items} to {string} ..."
        _build._print_file_handling(message)
        if layout_directory.name.endswith("-parts"):
            if document_name is not None:
                part_dictionary = _path.get_metadatum(
                    layout_directory,
                    document_name,
                    {},
                )
            else:
                part_dictionary = {}
            part_dictionary["bol_measure_numbers"] = bol_measure_numbers
            assert abjad.string.is_shout_case(document_name)
            _path.add_metadatum(layout_directory, document_name, part_dictionary)
        else:
            _path.add_metadatum(
                layout_directory,
                "bol_measure_numbers",
                bol_measure_numbers,
            )


def measures(items):
    time_signatures = [abjad.TimeSignature(_) for _ in items]
    return Measures(time_signatures)


@_build.timed("postprocess_score")
def postprocess_score(
    score,
    *,
    add_container_identifiers=False,
    all_music_in_part_containers=False,
    allow_empty_selections=False,
    always_make_global_rests=False,
    append_anchor_skip=False,
    attach_instruments_by_hand=False,
    check_persistent_indicators=False,
    clock_time_extra_offset=None,
    clock_time_override=None,
    color_not_yet_pitched=False,
    color_octaves=False,
    comment_measure_numbers=False,
    do_not_check_wellformedness=False,
    do_not_require_short_instrument_names=False,
    empty_fermata_measures=False,
    environment: _build.Environment = None,
    error_on_not_yet_pitched=False,
    fermata_extra_offset_y=2.5,
    fermata_measure_empty_overrides=(),
    final_section=False,
    first_section=False,
    force_nonnatural_accidentals=False,
    global_rests_in_every_staff=False,
    global_rests_in_topmost_staff=False,
    label_clock_time=False,
    magnify_staves=None,
    manifests=None,
    part_manifest=None,
    parts_metric_modulation_multiplier=None,
    section_number=None,
    shift_measure_initial_clefs=False,
    tags: _tags.Tags = None,
    transpose_score=False,
    treat_untreated_persistent_wrappers=False,
    whitespace_leaves=False,
):
    skips = score["Skips"]
    if append_anchor_skip:
        skips = skips[:-1]
    time_signatures = []
    for skip in skips:
        time_signature = abjad.get.effective(skip, abjad.TimeSignature)
        time_signatures.append(time_signature)
    assert isinstance(score, abjad.Score), repr(score)
    activate, deactivate = None, None
    if tags is not None:
        assert isinstance(tags, _tags.Tags), repr(tags)
        activate = tags.activate
        deactivate = tags.deactivate
    if activate is not None:
        assert isinstance(activate, list), repr(activate)
        assert all(isinstance(_, abjad.Tag) for _ in activate)
    assert isinstance(all_music_in_part_containers, bool)
    assert isinstance(allow_empty_selections, bool)
    if clock_time_override is not None:
        assert isinstance(clock_time_override, abjad.MetronomeMark)
    assert isinstance(color_octaves, bool)
    assert isinstance(do_not_check_wellformedness, bool)
    if deactivate is not None:
        assert isinstance(deactivate, list), repr(deactivate)
        assert all(isinstance(_, abjad.Tag) for _ in deactivate)
    assert isinstance(do_not_require_short_instrument_names, bool)
    assert isinstance(empty_fermata_measures, bool)
    environment = environment or _build.Environment()
    first_measure_number = environment.first_measure_number
    metadata = environment.metadata
    persist = environment.persist
    previous_metadata = environment.previous_metadata
    section_number = environment.section_number
    assert all(0 < _ for _ in fermata_measure_empty_overrides)
    assert isinstance(final_section, bool)
    assert isinstance(first_measure_number, int)
    assert isinstance(first_section, bool)
    assert isinstance(force_nonnatural_accidentals, bool)
    global_skips = score["Skips"]
    manifests = manifests or {}
    measure_count = len(time_signatures)
    if parts_metric_modulation_multiplier is not None:
        assert isinstance(parts_metric_modulation_multiplier, tuple)
        assert len(parts_metric_modulation_multiplier) == 2
    previous_persistent_indicators = previous_metadata.get("persistent_indicators", {})
    assert isinstance(transpose_score, bool)
    assert isinstance(treat_untreated_persistent_wrappers, bool)
    voice_name_to_parameter_to_state: dict[str, dict] = {}
    with abjad.ForbidUpdate(component=score, update_on_exit=True):
        offset_to_measure_number = _populate_offset_to_measure_number(
            first_measure_number,
            global_skips,
        )
        extend_beams(score)
        _attach_sounds_during(score)
        if not first_section:
            _clone_section_initial_short_instrument_name(score)
        cached_time_signatures = remove_redundant_time_signatures(
            global_skips,
            append_anchor_skip=append_anchor_skip,
        )
        result = _get_fermata_measure_numbers(first_measure_number, score)
        fermata_start_offsets = result[0]
        fermata_measure_numbers = result[1]
        final_measure_is_fermata = result[2]
        if empty_fermata_measures and not fermata_measure_empty_overrides:
            fermata_measure_empty_overrides = [
                _ - first_measure_number + 1 for _ in fermata_measure_numbers
            ]
        if treat_untreated_persistent_wrappers:
            _treat_untreated_persistent_wrappers_alias(score, manifests=manifests)
        _attach_metronome_marks(global_skips, parts_metric_modulation_multiplier)
        _reanalyze_trending_dynamics(manifests, score)
        _reanalyze_reapplied_synthetic_wrappers(score)
        if transpose_score:
            _transpose_score_alias(score)
        _color_not_yet_registered(score)
        _color_mock_pitch(score)
        _set_intermittent_to_staff_position_zero(score)
        if color_not_yet_pitched:
            _color_not_yet_pitched(score)
        _set_not_yet_pitched_to_staff_position_zero(score)
        _clean_up_repeat_tie_direction(score)
        _clean_up_laissez_vibrer_tie_direction(score)
        if error_on_not_yet_pitched:
            _error_on_not_yet_pitched(score)
        _check_doubled_dynamics(score)
        color_out_of_range_pitches(score)
        if check_persistent_indicators:
            _check_persistent_indicators(
                do_not_require_short_instrument_names,
                score,
            )
        color_repeat_pitch_classes(score)
        if color_octaves:
            _color_octaves_alias(score)
        _attach_shadow_tie_indicators(score)
        if force_nonnatural_accidentals:
            _force_nonnatural_accidentals(score)
        _label_duration_multipliers(score)
        _magnify_staves(magnify_staves, score)
        if whitespace_leaves:
            _whitespace_leaves(score)
        if comment_measure_numbers:
            _comment_measure_numbers(
                first_measure_number,
                offset_to_measure_number,
                score,
            )
        _style_fermata_measures(
            fermata_extra_offset_y,
            fermata_measure_empty_overrides,
            fermata_start_offsets,
            final_section,
            offset_to_measure_number,
            score,
        )
        if shift_measure_initial_clefs:
            _shift_measure_initial_clefs(
                first_measure_number,
                offset_to_measure_number,
                score,
            )
        container_to_part_assignment = None
        if add_container_identifiers:
            container_to_part_assignment = _add_container_identifiers(
                score,
                section_number,
            )
            if all_music_in_part_containers:
                _check_all_music_in_part_containers(score)
            _check_duplicate_part_assignments(
                container_to_part_assignment,
                part_manifest,
            )
    _move_global_rests(
        global_rests_in_every_staff,
        global_rests_in_topmost_staff,
        score,
    )
    _clean_up_on_beat_grace_containers(score)
    if not do_not_check_wellformedness:
        count, message = abjad.wf.tabulate_wellformedness(
            score, check_out_of_range_pitches=False
        )
        if count:
            raise Exception("\n" + message)
        violators, total = abjad.wf.check_out_of_range_pitches(
            score, allow_indicators=(_enums.ALLOW_OUT_OF_RANGE, _enums.HIDDEN)
        )
        if violators:
            raise Exception(f"{len(violators)} /    {total} out of range pitches")
    clock_time_duration = None
    start_clock_time = None
    stop_clock_time = None
    if label_clock_time:
        result = _label_clock_time(
            clock_time_override,
            fermata_measure_numbers,
            first_measure_number,
            previous_metadata,
            score,
        )
        clock_time_duration = result[0]
        start_clock_time = result[1]
        stop_clock_time = result[2]
    final_measure_number = first_measure_number + measure_count - 1
    persistent_indicators = _collect_persistent_indicators(
        manifests,
        previous_persistent_indicators,
        score,
    )
    first_metronome_mark = True
    skip = abjad.select.leaf(score["Skips"], 0)
    metronome_mark = abjad.get.effective(skip, abjad.MetronomeMark)
    if metronome_mark is None:
        first_metronome_mark = False
    new_metadata, new_persist = _collect_metadata(
        container_to_part_assignment,
        clock_time_duration,
        fermata_measure_numbers,
        final_measure_is_fermata,
        final_measure_number,
        first_measure_number,
        first_metronome_mark,
        append_anchor_skip,
        metadata,
        persist,
        persistent_indicators,
        score,
        start_clock_time,
        stop_clock_time,
        cached_time_signatures,
        voice_name_to_parameter_to_state,
    )
    new_metadata = proxy(new_metadata | new_persist)
    _style_anchor_skip(score)
    _style_anchor_notes(score)
    _check_anchors_are_final(score)
    return new_metadata


def proxy(mapping):
    return types.MappingProxyType(mapping)


def reapply(voices, manifests, previous_persistent_indicators):
    runtime = {
        "already_reapplied_contexts": {"Score"},
        "manifests": manifests,
        "previous_persistent_indicators": previous_persistent_indicators,
    }
    for voice in voices:
        reapply_persistent_indicators(voice, runtime=runtime)


def reapply_persistent_indicators(argument, *, runtime=None):
    already_reapplied_contexts = runtime["already_reapplied_contexts"]
    manifests = runtime["manifests"]
    previous_persistent_indicators = runtime["previous_persistent_indicators"]
    leaf = abjad.select.leaf(argument, 0)
    parentage = abjad.get.parentage(leaf)
    contexts = []
    score = None
    for component in parentage:
        if isinstance(component, abjad.Score):
            score = component
        elif isinstance(component, abjad.Context):
            contexts.append(component)
    assert isinstance(score, abjad.Score)
    for context in contexts:
        _reapply_persistent_indicators(
            manifests,
            previous_persistent_indicators,
            score,
            already_reapplied_contexts=already_reapplied_contexts,
            do_not_iterate=context,
        )


def remove_redundant_time_signatures(global_skips, *, append_anchor_skip=False):
    previous_time_signature = None
    cached_time_signatures = []
    skips = _select.skips(global_skips)
    if append_anchor_skip:
        assert abjad.get.has_indicator(skips[-1], _enums.ANCHOR_SKIP)
        skips = skips[:-1]
    for skip in skips:
        time_signature = abjad.get.indicator(skip, abjad.TimeSignature)
        string = f"{time_signature.numerator}/{time_signature.denominator}"
        cached_time_signatures.append(string)
        if time_signature == previous_time_signature:
            abjad.detach(time_signature, skip)
        else:
            previous_time_signature = time_signature
    return cached_time_signatures


def scope(cache):
    return DynamicScope(cache)


def section_defaults():
    return {
        "add_container_identifiers": True,
        "append_anchor_skip": True,
        "check_persistent_indicators": True,
        "color_not_yet_pitched": True,
        "comment_measure_numbers": True,
        "force_nonnatural_accidentals": True,
        "label_clock_time": True,
        "shift_measure_initial_clefs": True,
        "treat_untreated_persistent_wrappers": True,
        "whitespace_leaves": True,
    }


def set_up_score(
    score: abjad.Score,
    time_signatures: typing.Sequence[abjad.TimeSignature],
    *,
    always_make_global_rests: bool = False,
    append_anchor_skip: bool = False,
    do_not_reapply_persistent_indicators: bool = False,
    docs: bool = False,
    first_measure_number: int = 1,
    first_section: bool = False,
    layout: bool = False,
    manifests: dict = None,
    previous_persistent_indicators: dict = None,
) -> None:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    manifests = manifests or {}
    assert isinstance(manifests, dict), repr(manifests)
    if docs:
        first_section = True
    skips = score["Skips"]
    _make_global_skips(skips, time_signatures, append_anchor_skip=append_anchor_skip)
    if not first_section:
        _attach_nonfirst_empty_start_bar(skips)
    _label_measure_numbers(first_measure_number, skips)
    if always_make_global_rests:
        _make_global_rests(score["Rests"], time_signatures)
    elif "Rests" in score:
        del score["Rests"]
    if previous_persistent_indicators and not do_not_reapply_persistent_indicators:
        _reapply_persistent_indicators(
            manifests,
            previous_persistent_indicators,
            score,
            do_not_iterate=score,
        )


def time_signatures(pairs):
    return [abjad.TimeSignature(_) for _ in pairs]


def update_voice_name_to_parameter_to_state(
    voice_name_to_parameter_to_state: dict,
    voice_name: str,
    parameter: str,
    name: str,
    state: dict,
):
    assert isinstance(voice_name_to_parameter_to_state, dict), repr(
        voice_name_to_parameter_to_state
    )
    assert isinstance(voice_name, str), repr(voice_name)
    assert isinstance(parameter, str), repr(parameter)
    assert isinstance(name, str), repr(name)
    assert isinstance(state, dict), repr(state)
    assert "name" not in state, repr(state)
    state["name"] = name
    state = dict(sorted(state.items()))
    voice_name_to_parameter_to_state_ = voice_name_to_parameter_to_state.get(
        voice_name, {}
    )
    voice_name_to_parameter_to_state_[parameter] = state
    voice_name_to_parameter_to_state[voice_name] = voice_name_to_parameter_to_state_