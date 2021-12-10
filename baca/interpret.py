import copy
import functools
import importlib
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import const as _const
from . import indicators as _indicators
from . import layout as _layout
from . import memento as _memento
from . import overrides as _overrides
from . import parts as _parts
from . import piecewise as _piecewise
from . import pitchclasses as _pitchclasses
from . import pitchcommands as _pitchcommands
from . import rhythmcommands as _rhythmcommands
from . import scoping as _scoping
from . import selection as _selection
from . import selectors as _selectors
from . import tags as _tags

nonfirst_preamble = r"""\header { composer = ##f poet = ##f title = ##f }
\layout { indent = 0 }
\paper { print-first-page-number = ##t }"""


def _activate_tags(score, tags):
    if not tags:
        return
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    for leaf in abjad.iterate.leaves(score):
        if not isinstance(leaf, abjad.Skip):
            continue
        wrappers = abjad.get.wrappers(leaf)
        for wrapper in wrappers:
            if wrapper.tag is None:
                continue
            for tag in tags:
                if tag in wrapper.tag:
                    wrapper.deactivate = False
                    break


def _add_container_identifiers(score, segment_number):
    if segment_number is not None:
        assert segment_number, repr(segment_number)
        segment_number = f"segment.{segment_number}"
    else:
        segment_number = ""
    contexts = []
    try:
        context = score["Global_Skips"]
        contexts.append(context)
    except ValueError:
        pass
    try:
        context = score["Global_Rests"]
        contexts.append(context)
    except ValueError:
        pass
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice._has_indicator(_const.INTERMITTENT):
            continue
        contexts.append(voice)
    container_to_part_assignment = {}
    context_name_counts = {}
    for context in contexts:
        assert context.name is not None, repr(context)
        count = context_name_counts.get(context.name, 0)
        if count == 0:
            suffixed_context_name = context.name
        else:
            suffixed_context_name = f"{context.name}.count.{count}"
        context_name_counts[context.name] = count + 1
        if segment_number:
            context_identifier = f"{segment_number}.{suffixed_context_name}"
        else:
            context_identifier = suffixed_context_name
        context_identifier = context_identifier.replace("_", ".")
        context.identifier = f"%*% {context_identifier}"
        part_container_count = 0
        for container in abjad.iterate.components(context, abjad.Container):
            if not container.identifier:
                continue
            if container.identifier.startswith("%*% Part"):
                part_container_count += 1
                part = container.identifier.strip("%*% ")
                globals_ = globals()
                globals_["PartAssignment"] = _parts.PartAssignment
                part = eval(part, globals_)
                container_identifier = (
                    f"{context_identifier}.part.{part_container_count}"
                )
                container_identifier = abjad.String(container_identifier)
                assert "_" not in container_identifier, repr(container_identifier)
                assert container_identifier not in container_to_part_assignment
                timespan = container._get_timespan()
                pair = (part, timespan)
                container_to_part_assignment[container_identifier] = pair
                container.identifier = f"%*% {container_identifier}"
    for staff in abjad.iterate.components(score, abjad.Staff):
        if segment_number:
            context_identifier = f"{segment_number}.{staff.name}"
        else:
            context_identifier = staff.name
        context_identifier = context_identifier.replace("_", ".")
        staff.identifier = f"%*% {context_identifier}"
    return container_to_part_assignment


def _adjust_first_measure_number(first_measure_number, previous_metadata):
    if first_measure_number is not None:
        return first_measure_number
    if not previous_metadata:
        return 1
    string = "first_measure_number"
    first_measure_number = previous_metadata.get(string)
    time_signatures = previous_metadata.get("time_signatures")
    if first_measure_number is None or time_signatures is None:
        return 1
    first_measure_number += len(time_signatures)
    return first_measure_number


def _alive_during_previous_segment(previous_persist, context):
    assert isinstance(context, abjad.Context), repr(context)
    names = previous_persist.get("alive_during_segment", [])
    return context.name in names


def _analyze_memento(score, dictionary, context, memento):
    previous_indicator = _memento_to_indicator(dictionary, memento)
    if previous_indicator is None:
        return
    if isinstance(previous_indicator, _indicators.SpacingSection):
        return
    if memento.context in score:
        for context in abjad.iterate.components(score, abjad.Context):
            if context.name == memento.context:
                memento_context = context
                break
    else:
        # context alive in previous segment doesn't exist in this segment
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
    elif not _scoping.compare_persistent_indicators(previous_indicator, indicator):
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
        if isinstance(wrapper.indicator, abjad.LilyPondLiteral):
            if wrapper.indicator.argument == "":
                continue
        tag_ = wrapper.tag.append(tag)
        wrapper.tag = tag_


def _apply_breaks(score, spacing):
    if spacing is None:
        return
    if spacing.breaks is None:
        return
    global_skips = score["Global_Skips"]
    skips = _selection.Selection(global_skips).skips()
    measure_count = len(skips)
    literal = abjad.LilyPondLiteral(r"\autoPageBreaksOff", "before")
    abjad.attach(
        literal,
        skips[0],
        tag=_tags.BREAK.append(_scoping.site(_frame(), n=1)),
    )
    for skip in skips[:measure_count]:
        if not abjad.get.has_indicator(skip, _layout.LBSD):
            literal = abjad.LilyPondLiteral(r"\noBreak", "before")
            abjad.attach(
                literal,
                skip,
                tag=_tags.BREAK.append(_scoping.site(_frame(), n=2)),
            )
    assert spacing.breaks.commands is not None
    for measure_number, commands in spacing.breaks.commands.items():
        if measure_count < measure_number:
            message = f"score ends at measure {measure_count}"
            message += f" (not {measure_number})."
            raise Exception(message)
        for command in commands:
            command(global_skips)


def _apply_spacing(page_layout_profile, score, spacing):
    with abjad.Timer() as timer:
        spacing(score, page_layout_profile)
    count = int(timer.elapsed_time)
    return count


def _assert_nonoverlapping_rhythms(rhythms, voice):
    previous_stop_offset = 0
    for rhythm in rhythms:
        start_offset = rhythm.start_offset
        if start_offset < previous_stop_offset:
            raise Exception(f"{voice} has overlapping rhythms.")
        duration = abjad.get.duration(rhythm.annotation)
        stop_offset = start_offset + duration
        previous_stop_offset = stop_offset


def _attach_default_indicators(argument):
    """
    Attaches defaults to all staff and staff group contexts in ``argument`` when
    ``argument`` is a score.

    Attaches defaults to ``argument`` (without iterating ``argument``) when ``argument``
    is a staff or staff group.

    Returns list of one wrapper for every indicator attached.
    """
    prototype = (abjad.Score, abjad.Staff, abjad.StaffGroup)
    assert isinstance(argument, prototype), repr(argument)
    wrappers = []
    tag = _const.REMOVE_ALL_EMPTY_STAVES
    empty_prototype = (abjad.MultimeasureRest, abjad.Skip)
    prototype = (abjad.Staff, abjad.StaffGroup)
    if isinstance(argument, abjad.Score):
        staff__groups = list(abjad.Selection(argument).components(prototype))
        staves = list(abjad.Selection(argument).components(abjad.Staff))
    elif isinstance(argument, abjad.Staff):
        staff__groups = [argument]
        staves = [argument]
    else:
        assert isinstance(argument, abjad.StaffGroup), repr(argument)
        staff__groups = [argument]
        staves = []
    for staff__group in staff__groups:
        leaf = None
        voices = abjad.Selection(staff__group).components(abjad.Voice)
        assert isinstance(voices, abjad.Selection), repr(voices)
        # find leaf 0 in first nonempty voice
        for voice in voices:
            leaves = []
            for leaf_ in abjad.iterate.leaves(voice):
                if abjad.get.has_indicator(leaf_, _const.HIDDEN):
                    leaves.append(leaf_)
            if not all(isinstance(_, empty_prototype) for _ in leaves):
                leaf = abjad.get.leaf(voice, 0)
                break
        # otherwise, find first leaf in voice in non-removable staff
        if leaf is None:
            for voice in voices:
                voice_might_vanish = False
                for component in abjad.get.parentage(voice):
                    if abjad.get.annotation(component, tag) is True:
                        voice_might_vanish = True
                if not voice_might_vanish:
                    leaf = abjad.get.leaf(voice, 0)
                    if leaf is not None:
                        break
        # otherwise, as last resort find first leaf in first voice
        if leaf is None:
            leaf = abjad.get.leaf(voices[0], 0)
        if leaf is None:
            continue
        instrument = abjad.get.indicator(leaf, abjad.Instrument)
        if instrument is None:
            string = "default_instrument"
            instrument = abjad.get.annotation(staff__group, string)
            if instrument is not None:
                wrapper = abjad.attach(
                    instrument,
                    leaf,
                    context=staff__group.lilypond_type,
                    tag=_scoping.site(_frame(), n=1),
                    wrapper=True,
                )
                wrappers.append(wrapper)
        margin_markup = abjad.get.indicator(leaf, abjad.MarginMarkup)
        if margin_markup is None:
            string = "default_margin_markup"
            margin_markup = abjad.get.annotation(staff__group, string)
            if margin_markup is not None:
                wrapper = abjad.attach(
                    margin_markup,
                    leaf,
                    tag=_tags.NOT_PARTS.append(_scoping.site(_frame(), n=2)),
                    wrapper=True,
                )
                wrappers.append(wrapper)
    for staff in staves:
        leaf = abjad.get.leaf(staff, 0)
        clef = abjad.get.indicator(leaf, abjad.Clef)
        if clef is not None:
            continue
        clef = abjad.get.annotation(staff, "default_clef")
        if clef is not None:
            wrapper = abjad.attach(
                clef,
                leaf,
                tag=_scoping.site(_frame(), n=3),
                wrapper=True,
            )
            wrappers.append(wrapper)
    return wrappers


def _attach_fermatas(
    always_make_global_rests,
    append_phantom_measure,
    score,
    time_signatures,
):
    if not always_make_global_rests:
        del score["Global_Rests"]
        return
    has_fermata = False
    if not has_fermata and not always_make_global_rests:
        del score["Global_Rests"]
        return
    context = score["Global_Rests"]
    rests = _make_global_rests(
        append_phantom_measure,
        time_signatures,
    )
    context.extend(rests)


def _attach_first_appearance_default_indicators(
    manifests,
    previous_persistent_indicators,
    score,
):
    staff_or_staff_group = (abjad.Staff, abjad.StaffGroup)
    for staff_or_staff_group in abjad.iterate.components(score, staff_or_staff_group):
        if staff_or_staff_group.name in previous_persistent_indicators:
            continue
        for wrapper in _attach_default_indicators(staff_or_staff_group):
            _scoping.treat_persistent_wrapper(manifests, wrapper, "default")


def _attach_first_segment_default_indicators(manifests, score):
    for wrapper in _attach_default_indicators(score):
        _scoping.treat_persistent_wrapper(manifests, wrapper, "default")


def _attach_nonfirst_empty_start_bar(global_skips):
    # empty start bar allows LilyPond to print bar numbers at start of nonfirst segments
    first_skip = _selection.Selection(global_skips).skip(0)
    literal = abjad.LilyPondLiteral(r'\bar ""')
    tag = _tags.EMPTY_START_BAR
    tag = tag.append(_tags.ONLY_SEGMENT)
    abjad.attach(
        literal,
        first_skip,
        tag=tag.append(_scoping.site(_frame())),
    )


def _attach_metronome_marks(global_skips, parts_metric_modulation_multiplier):
    indicator_count = 0
    skips = _selection.Selection(global_skips).skips()
    final_leaf_metronome_mark = abjad.get.indicator(skips[-1], abjad.MetronomeMark)
    add_right_text_to_me = None
    if final_leaf_metronome_mark:
        tempo_prototype = (
            abjad.MetronomeMark,
            _indicators.Accelerando,
            _indicators.Ritardando,
        )
        for skip in reversed(skips[:-1]):
            if abjad.get.has_indicator(skip, tempo_prototype):
                add_right_text_to_me = skip
                break
    for i, skip in enumerate(skips):
        metronome_mark = abjad.get.indicator(skip, abjad.MetronomeMark)
        metric_modulation = abjad.get.indicator(skip, abjad.MetricModulation)
        accelerando = abjad.get.indicator(skip, _indicators.Accelerando)
        ritardando = abjad.get.indicator(skip, _indicators.Ritardando)
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
            # TODO: public hide
            metric_modulation._hide = True
        if accelerando is not None:
            # TODO: public hide
            accelerando._hide = True
        if ritardando is not None:
            # TODO: public hide
            ritardando._hide = True
        if skip is skips[-1]:
            break
        if metronome_mark is None and metric_modulation is not None:
            wrapper = abjad.get.wrapper(skip, abjad.MetricModulation)
        if metronome_mark is None and accelerando is not None:
            wrapper = abjad.get.wrapper(skip, _indicators.Accelerando)
        if metronome_mark is None and ritardando is not None:
            wrapper = abjad.get.wrapper(skip, _indicators.Ritardando)
        has_trend = accelerando is not None or ritardando is not None
        indicator_count += 1
        tag = wrapper.tag
        stripped_left_text = None
        if metronome_mark is not None:
            if metric_modulation is not None:
                if metronome_mark.custom_markup is not None:
                    left_text = str(metronome_mark._get_markup())
                    left_text = left_text.removeprefix(r"\markup").strip()
                    modulation = str(metric_modulation._get_markup())
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
            string = str(left_text).removeprefix(r"\markup").strip()
            left_text = abjad.Markup(string)
        elif ritardando is not None:
            left_text = ritardando._get_markup()
            string = str(left_text).removeprefix(r"\markup").strip()
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
                tag=_scoping.site(_frame(), n=1),
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
        assert "METRONOME_MARK" in str(tag), repr(tag)
        if (
            isinstance(wrapper.indicator, abjad.MetronomeMark)
            and has_trend
            and "EXPLICIT" not in str(tag)
        ):
            words = []
            for word in str(tag).split(":"):
                if "METRONOME_MARK" in word:
                    word = word.replace("DEFAULT", "EXPLICIT")
                    word = word.replace("REAPPLIED", "EXPLICIT")
                    word = word.replace("REDUNDANT", "EXPLICIT")
                words.append(word)
            string = ":".join(words)
            new_tag = abjad.Tag(string)
            indicator = wrapper.indicator
            abjad.detach(wrapper, skip)
            abjad.attach(
                indicator,
                skip,
                tag=new_tag.append(_scoping.site(_frame(), n=5)),
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
                tag=tag.append(_scoping.site(_frame(), n=2)),
            )
        else:
            abjad.attach(
                start_text_span,
                skip,
                deactivate=True,
                tag=tag.append(_scoping.site(_frame(), n=2.1)).append(
                    _tags.METRIC_MODULATION_IS_NOT_SCALED,
                ),
            )
            left_text_ = start_text_span.left_text
            assert left_text_.endswith("(1 . 1)")
            n, d = parts_metric_modulation_multiplier
            left_text_ = left_text_[:-7] + f"({n} . {d})"
            start_text_span_ = abjad.new(start_text_span, left_text=left_text_)
            abjad.attach(
                start_text_span_,
                skip,
                deactivate=True,
                tag=tag.append(_scoping.site(_frame(), n=2.2)).append(
                    _tags.METRIC_MODULATION_IS_SCALED,
                ),
            )
        if stripped_left_text is not None:
            start_text_span_ = abjad.new(start_text_span, left_text=stripped_left_text)
            abjad.attach(
                start_text_span_,
                skip,
                deactivate=True,
                tag=tag.append(_scoping.site(_frame(), n=2.2)).append(
                    _tags.METRIC_MODULATION_IS_STRIPPED,
                ),
            )
        string = str(tag)
        if "DEFAULT" in string:
            status = "default"
        elif "EXPLICIT" in string:
            status = "explicit"
        elif "REAPPLIED" in string:
            status = "reapplied"
        elif "REDUNDANT" in string:
            status = "redundant"
        else:
            status = None
        assert status is not None
        color = _scoping._status_to_color[status]
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
            string = str(tag)
            if "DEFAULT" in string:
                status = "default"
            elif "EXPLICIT" in string:
                status = "explicit"
            elif "REAPPLIED" in str(tag):
                status = "reapplied"
            elif "REDUNDANT" in str(tag):
                status = "redundant"
            else:
                status = None
            assert status is not None
            color = _scoping._status_to_color[status]
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
            tag=tag.append(_scoping.site(_frame(), n=3)),
        )
    if indicator_count:
        final_skip = skip
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMM")
        tag_ = _tags.EOS_STOP_MM_SPANNER
        tag_ = tag_.append(_scoping.site(_frame(), n=4))
        abjad.attach(stop_text_span, final_skip, tag=tag_)


def _attach_rhythm_annotation_spanner(command, selection):
    if selection is None:
        return
    if not command.annotation_spanner_text and not command.frame:
        return
    leaves = []
    for leaf in abjad.iterate.leaves(selection):
        if abjad.get.parentage(leaf).get(abjad.OnBeatGraceContainer):
            continue
        leaves.append(leaf)
    container = abjad.get.before_grace_container(leaves[0])
    if container is not None:
        leaves_ = abjad.select(container).leaves()
        leaves[0:0] = leaves_
    container = abjad.get.after_grace_container(leaves[-1])
    if container is not None:
        leaves_ = abjad.select(container).leaves()
        leaves.extend(leaves_)
    string = command.annotation_spanner_text
    if string is None:
        string = command._make_rhythm_annotation_string()
    color = command.annotation_spanner_color or "#darkyellow"
    command_ = _piecewise.rhythm_annotation_spanner(
        string,
        abjad.tweak(color).color,
        abjad.tweak(8).staff_padding,
        leak_spanner_stop=True,
        selector=_selectors.leaves(),
    )
    command_(leaves)


# This exists because of an incompletely implemented behavior in LilyPond;
# LilyPond doesn't understand repeat-tied notes to be tied;
# because of this LilyPond incorrectly prints accidentals in front of some
# repeat-tied notes; this function works around LilyPond's behavior
def _attach_shadow_tie_indicators(score):
    tag = _scoping.site(_frame())
    for plt in _selection.Selection(score).plts():
        if len(plt) == 1:
            continue
        for pleaf in plt[:-1]:
            if abjad.get.has_indicator(pleaf, abjad.Tie):
                continue
            tie = abjad.Tie()
            abjad.tweak(tie).stencil = False
            abjad.attach(tie, pleaf, tag=tag)


def _attach_sounds_during(score):
    for voice in abjad.iterate.components(score, abjad.Voice):
        pleaves = []
        for pleaf in _selection.Selection(voice).pleaves():
            if abjad.get.has_indicator(pleaf, _const.PHANTOM):
                continue
            pleaves.append(pleaf)
        if bool(pleaves):
            abjad.attach(_const.SOUNDS_DURING_SEGMENT, voice)


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


def _bundle_runtime(
    allows_instrument=None,
    instruments=None,
    manifests=None,
    margin_markups=None,
    metronome_marks=None,
    offset_to_measure_number=None,
    previous_segment_voice_metadata=None,
):
    runtime = {}
    runtime["allows_instrument"] = allows_instrument
    runtime["instruments"] = instruments
    runtime["manifests"] = manifests
    runtime["margin_markups"] = margin_markups
    runtime["metronome_marks"] = metronome_marks
    runtime["offset_to_measure_number"] = offset_to_measure_number or {}
    runtime["previous_segment_voice_metadata"] = previous_segment_voice_metadata
    return runtime


def _cache_leaves(score, measure_count):
    measure_timespans = []
    for measure_index in range(measure_count):
        measure_number = measure_index + 1
        measure_timespan = _get_measure_timespan(score, measure_number)
        measure_timespans.append(measure_timespan)
    cache = {}
    for leaf in abjad.select(score).leaves():
        parentage = abjad.get.parentage(leaf)
        context = parentage.get(abjad.Context)
        leaves_by_measure_number = cache.setdefault(context.name, {})
        leaf_timespan = abjad.get.timespan(leaf)
        # TODO: replace loop with bisection:
        for i, measure_timespan in enumerate(measure_timespans):
            measure_number = i + 1
            if leaf_timespan.starts_during_timespan(measure_timespan):
                cached_leaves = leaves_by_measure_number.setdefault(measure_number, [])
                cached_leaves.append(leaf)
    return cache


def _calculate_clock_times(
    score,
    clock_time_override,
    fermata_measure_numbers,
    first_measure_number,
    previous_stop_clock_time,
):
    skips = _selection.Selection(score["Global_Skips"]).skips()
    if "Global_Rests" not in score:
        return None, None, None, None
    for context in abjad.iterate.components(score, abjad.Context):
        if context.name == "Global_Rests":
            break
    rests = _selection.Selection(context).rests()
    assert len(skips) == len(rests)
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
            fermata_duration = abjad.get.annotation(rest, _const.FERMATA_DURATION)
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


def _call_commands(
    allow_empty_selections,
    allows_instrument,
    cache,
    commands,
    measure_count,
    offset_to_measure_number,
    manifests,
    previous_persist,
    score,
    voice_metadata,
):
    command_count = 0
    for command in commands:
        assert isinstance(command, _scoping.Command)
        if isinstance(command, _rhythmcommands.RhythmCommand):
            continue
        command_count += 1
        selection, cache = _scope_to_leaf_selection(
            score,
            allow_empty_selections,
            cache,
            command,
            measure_count,
        )
        voice_name = command.scope.voice_name
        previous_segment_voice_metadata = _get_previous_segment_voice_metadata(
            previous_persist, voice_name
        )
        runtime = _bundle_runtime(
            allows_instrument=allows_instrument,
            manifests=manifests,
            offset_to_measure_number=offset_to_measure_number,
            previous_segment_voice_metadata=previous_segment_voice_metadata,
        )
        try:
            command(selection, runtime)
        except Exception:
            print(f"Interpreting ...\n\n{abjad.storage(command)}\n")
            raise
        cache = _handle_mutator(score, cache, command)
        if getattr(command, "persist", None):
            parameter = command.parameter
            state = command.state
            assert "name" not in state
            state["name"] = command.persist
            if voice_name not in voice_metadata:
                voice_metadata[voice_name] = {}
            voice_metadata[voice_name][parameter] = state
    return cache, command_count


def _call_rhythm_commands(
    always_make_global_rests,
    attach_rhythm_annotation_spanners,
    commands,
    append_phantom_measure,
    manifests,
    measure_count,
    previous_persist,
    score,
    skips_instead_of_rests,
    time_signatures,
    voice_metadata,
):
    _attach_fermatas(
        always_make_global_rests,
        append_phantom_measure,
        score,
        time_signatures,
    )
    command_count = 0
    tag = _scoping.site(_frame())
    if skips_instead_of_rests:
        prototype = abjad.Skip
    else:
        prototype = abjad.MultimeasureRest
    silence_maker = rmakers.multiplied_duration(prototype, tag=tag)
    segment_duration = None
    for voice in abjad.select(score).components(abjad.Voice):
        assert not len(voice), repr(voice)
        voice_metadata_ = voice_metadata.get(voice.name, {})
        commands_ = _voice_to_rhythm_commands(commands, voice)
        if not commands_:
            selection = silence_maker(time_signatures)
            assert isinstance(selection, abjad.Selection), repr(selection)
            voice.extend(selection)
            if append_phantom_measure:
                container = _make_multimeasure_rest_container(
                    voice.name,
                    (1, 4),
                    skips_instead_of_rests,
                    phantom=True,
                    suppress_note=True,
                )
                voice.append(container)
            continue
        timespans = []
        for command in commands_:
            if command.scope.measures is None:
                raise Exception(abjad.storage(command))
            measures = command.scope.measures
            result = _get_measure_time_signatures(
                measure_count,
                score,
                time_signatures,
                *measures,
            )
            start_offset, time_signatures_ = result
            previous_segment_voice_metadata = _get_previous_segment_voice_metadata(
                previous_persist, voice.name
            )
            runtime = _bundle_runtime(
                manifests=manifests,
                previous_segment_voice_metadata=previous_segment_voice_metadata,
            )
            selection = None
            try:
                selection = command._make_selection(time_signatures_, runtime)
            except Exception:
                print(f"Interpreting ...\n\n{abjad.storage(command)}\n")
                raise
            if attach_rhythm_annotation_spanners:
                _attach_rhythm_annotation_spanner(command, selection)
            timespan = abjad.Timespan(start_offset=start_offset, annotation=selection)
            timespans.append(timespan)
            if command.persist and command.state:
                state = command.state
                assert "name" not in state
                state["name"] = command.persist
                voice_metadata_[command.parameter] = command.state
            command_count += 1
        if bool(voice_metadata_):
            voice_metadata[voice.name] = voice_metadata_
        timespans.sort()
        _assert_nonoverlapping_rhythms(timespans, voice.name)
        selections, segment_duration = _intercalate_silences(
            skips_instead_of_rests,
            time_signatures,
            timespans,
            voice.name,
        )
        if append_phantom_measure:
            suppress_note = False
            final_leaf = abjad.get.leaf(selections, -1)
            if isinstance(final_leaf, abjad.MultimeasureRest):
                suppress_note = True
            container = _make_multimeasure_rest_container(
                voice.name,
                (1, 4),
                skips_instead_of_rests,
                phantom=True,
                suppress_note=suppress_note,
            )
            selection = abjad.select(container)
            selections.append(selection)
        voice.extend(selections)
    return command_count, segment_duration


def _check_all_music_in_part_containers(score):
    indicator = _const.MULTIMEASURE_REST_CONTAINER
    for voice in abjad.iterate.components(score, abjad.Voice):
        for component in voice:
            if isinstance(component, (abjad.MultimeasureRest, abjad.Skip)):
                continue
            if abjad.get.has_indicator(component, _const.HIDDEN):
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
        for part in part_manifest.expand(part_assignment):
            if part.name not in part_to_timespans:
                part_to_timespans[part.name] = []
            part_to_timespans[part.name].append(timespan)
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


def _check_persistent_indicators(do_not_require_margin_markup, score):
    indicator = _const.SOUNDS_DURING_SEGMENT
    for voice in abjad.iterate.components(score, abjad.Voice):
        if not abjad.get.has_indicator(voice, indicator):
            continue
        for i, leaf in enumerate(abjad.iterate.leaves(voice)):
            _check_persistent_indicators_for_leaf(
                do_not_require_margin_markup, leaf, i, voice.name
            )


def _check_persistent_indicators_for_leaf(
    do_not_require_margin_markup, leaf, i, voice_name
):
    prototype = (
        _indicators.Accelerando,
        abjad.MetronomeMark,
        _indicators.Ritardando,
    )
    mark = abjad.get.effective(leaf, prototype)
    if mark is None:
        message = f"{voice_name} leaf {i} ({leaf!s}) missing metronome mark."
        raise Exception(message)
    instrument = abjad.get.effective(leaf, abjad.Instrument)
    if instrument is None:
        message = f"{voice_name} leaf {i} ({leaf!s}) missing instrument."
        raise Exception(message)
    if not do_not_require_margin_markup:
        markup = abjad.get.effective(leaf, abjad.MarginMarkup)
        if markup is None:
            message = f"{voice_name} leaf {i} ({leaf!s}) missing margin markup."
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
        staff_position = abjad.StaffPosition.from_pitch_and_clef(
            note.written_pitch,
            clef,
        )
        if staff_position == abjad.StaffPosition(0):
            abjad.override(note).laissez_vibrer_tie.direction = abjad.Up


def _clean_up_on_beat_grace_containers(score):
    for container in abjad.select(score).components(abjad.OnBeatGraceContainer):
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
            staff_position = abjad.StaffPosition.from_pitch_and_clef(
                note_head.written_pitch, clef
            )
            if staff_position.number == 0:
                repeat_tie = abjad.get.indicator(leaf, abjad.RepeatTie)
                abjad.tweak(repeat_tie).direction = abjad.Up
                break


def _clean_up_rhythm_maker_voice_names(score):
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice.name == "Rhythm_Maker_Music_Voice":
            outer = abjad.get.parentage(voice).get(abjad.Voice, 1)
            voice.name = outer.name


def _clone_segment_initial_short_instrument_name(score):
    prototype = abjad.MarginMarkup
    for context in abjad.iterate.components(score, abjad.Context):
        first_leaf = abjad.get.leaf(context, 0)
        if abjad.get.has_indicator(first_leaf, abjad.StartMarkup):
            continue
        margin_markup = abjad.get.indicator(first_leaf, prototype)
        if margin_markup is None:
            continue
        if isinstance(margin_markup.markup, str):
            markup = margin_markup.markup
        else:
            markup = abjad.new(margin_markup.markup)
        start_markup = abjad.StartMarkup(
            context=margin_markup.context,
            format_slot=margin_markup.format_slot,
            markup=markup,
        )
        abjad.attach(
            start_markup,
            first_leaf,
            tag=_scoping.site(_frame()),
        )


def _collect_alive_during_segment(score):
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
    metadata,
    persist,
    persistent_indicators,
    score,
    start_clock_time,
    stop_clock_time,
    time_signatures,
    voice_metadata,
):
    metadata_, persist_ = {}, {}
    persist_["alive_during_segment"] = _collect_alive_during_segment(score)
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
    dictionary = metadata.get("first_appearance_margin_markup")
    if dictionary:
        metadata_["first_appearance_margin_markup"] = dictionary
    metadata_["first_measure_number"] = first_measure_number
    metadata_["final_measure_number"] = final_measure_number
    if final_measure_is_fermata is True:
        metadata_["final_measure_is_fermata"] = True
    if first_metronome_mark is False:
        metadata_["first_metronome_mark"] = first_metronome_mark
    if persistent_indicators:
        persist_["persistent_indicators"] = persistent_indicators
    if start_clock_time is not None:
        metadata_["start_clock_time"] = start_clock_time
    if stop_clock_time is not None:
        metadata_["stop_clock_time"] = stop_clock_time
    metadata_["time_signatures"] = time_signatures
    if voice_metadata:
        persist_["voice_metadata"] = voice_metadata
    metadata.clear()
    metadata.update(metadata_)
    metadata = dict(metadata)
    _sort_dictionary(metadata)
    metadata = dict(metadata)
    for key, value in metadata.items():
        if value in (True, False):
            continue
        if not bool(value):
            raise Exception(f"{key} metadata should be nonempty (not {value!r}).")
    persist.clear()
    persist.update(persist_)
    persist = dict(persist)
    _sort_dictionary(persist)
    persist = dict(persist)
    for key, value in persist.items():
        if not bool(value):
            raise Exception(f"{key} persist should be nonempty (not {value!r}).")


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
    do_not_persist_on_phantom_measure = (
        abjad.Instrument,
        abjad.MetronomeMark,
        abjad.MarginMarkup,
        abjad.TimeSignature,
    )
    for name, dependent_wrappers in name_to_wrappers.items():
        mementos = []
        wrappers = []
        dictionary = abjad._inspect._get_persistent_wrappers(
            dependent_wrappers=dependent_wrappers,
            omit_with_indicator=_const.PHANTOM,
        )
        for wrapper in dictionary.values():
            if isinstance(wrapper.indicator, do_not_persist_on_phantom_measure):
                wrappers.append(wrapper)
        dictionary = abjad._inspect._get_persistent_wrappers(
            dependent_wrappers=dependent_wrappers
        )
        for wrapper in dictionary.values():
            if not isinstance(wrapper.indicator, do_not_persist_on_phantom_measure):
                wrappers.append(wrapper)
        for wrapper in wrappers:
            leaf = wrapper.component
            parentage = abjad.get.parentage(leaf)
            first_context = parentage.get(abjad.Context)
            indicator = wrapper.indicator
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
            elif isinstance(indicator, abjad.MarginMarkup):
                manifest = "margin_markups"
            else:
                prototype = type(indicator)
                prototype = _prototype_string(prototype)
            value = _scoping._indicator_to_key(indicator, manifests)
            if value is None:
                raise Exception(f"can not find in manifest:\n\n  {indicator}")
            editions = wrapper.tag.editions()
            if editions:
                words = [str(_) for _ in editions]
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
            mementos.sort(key=lambda _: abjad.storage(_))
            result[name] = mementos
    if previous_persistent_indicators:
        for context_name, mementos in previous_persistent_indicators.items():
            if context_name not in result:
                result[context_name] = mementos
    return result


def _color_mock_pitch(score):
    indicator = _const.MOCK
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.MOCK_COLORING)
    leaves = []
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, indicator):
            continue
        string = r"\baca-mock-coloring"
        literal = abjad.LilyPondLiteral(string, format_slot="before")
        abjad.attach(literal, pleaf, tag=tag)
        leaves.append(pleaf)


def _color_not_yet_pitched(score):
    indicator = _const.NOT_YET_PITCHED
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.NOT_YET_PITCHED_COLORING)
    leaves = []
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, indicator):
            continue
        string = r"\baca-not-yet-pitched-coloring"
        literal = abjad.LilyPondLiteral(string, format_slot="before")
        tag_ = tag
        if abjad.get.has_indicator(pleaf, _const.HIDDEN):
            tag_ = tag_.append(_tags.HIDDEN)
        if abjad.get.has_indicator(pleaf, _const.NOTE):
            tag_ = tag_.append(_tags.NOTE)
        abjad.attach(literal, pleaf, tag=tag_)
        leaves.append(pleaf)


def _color_not_yet_registered(score):
    indicator = _const.NOT_YET_REGISTERED
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.NOT_YET_REGISTERED_COLORING)
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, indicator):
            continue
        string = r"\baca-not-yet-registered-coloring"
        literal = abjad.LilyPondLiteral(string, format_slot="before")
        abjad.attach(literal, pleaf, tag=tag)


def _color_octaves(score):
    vertical_moments = abjad.iterate_vertical_moments(score)
    markup = abjad.Markup(r"\markup OCTAVE", direction=abjad.Up)
    abjad.tweak(markup).color = "#red"
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.OCTAVE_COLORING)
    for vertical_moment in vertical_moments:
        pleaves, pitches = [], []
        for leaf in vertical_moment.leaves:
            if abjad.get.has_indicator(leaf, _const.HIDDEN):
                continue
            if abjad.get.has_indicator(leaf, _const.STAFF_POSITION):
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
        if _pitchclasses.PitchClassSegment(pitch_classes).has_duplicates():
            color = True
            for pleaf in pleaves:
                if abjad.get.has_indicator(pleaf, _const.ALLOW_OCTAVE):
                    color = False
            if not color:
                continue
            for pleaf in pleaves:
                abjad.attach(markup, pleaf, tag=tag)
                string = r"\baca-octave-coloring"
                literal = abjad.LilyPondLiteral(string, format_slot="before")
                abjad.attach(literal, pleaf, tag=tag)


def _comment_measure_numbers(first_measure_number, offset_to_measure_number, score):
    for leaf in abjad.iterate.leaves(score):
        offset = abjad.get.timespan(leaf).start_offset
        measure_number = offset_to_measure_number.get(offset, None)
        if measure_number is None:
            continue
        local_measure_number = measure_number - first_measure_number
        local_measure_number += 1
        context = abjad.get.parentage(leaf).get(abjad.Context)
        string = f"% [{context.name} measure {local_measure_number}]"
        literal = abjad.LilyPondLiteral(string, format_slot="absolute_before")
        abjad.attach(literal, leaf, tag=_scoping.site(_frame()))


def _deactivate_tags(deactivate, score):
    if not deactivate:
        return
    tags = deactivate
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    for leaf in abjad.iterate.leaves(score):
        wrappers = abjad.get.wrappers(leaf)
        for wrapper in wrappers:
            if wrapper.tag is None:
                continue
            for tag in tags:
                if tag in wrapper.tag:
                    wrapper.deactivate = True
                    break


def _error_on_not_yet_pitched(score):
    violators = []
    for voice in abjad.iterate.components(score, abjad.Voice):
        for leaf in abjad.iterate.leaves(voice):
            if abjad.get.has_indicator(leaf, _const.NOT_YET_PITCHED):
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


def _extend_beams(score):
    for leaf in abjad.iterate.leaves(score):
        if abjad.get.indicator(leaf, _const.RIGHT_BROKEN_BEAM):
            _extend_beam(leaf)


def _find_repeat_pitch_classes(argument):
    violators = []
    for voice in abjad.iterate.components(argument, abjad.Voice):
        if abjad.get.has_indicator(voice, _const.INTERMITTENT):
            continue
        previous_lt, previous_pcs = None, []
        for lt in abjad.iterate.logical_ties(voice):
            if abjad.get.has_indicator(lt.head, _const.HIDDEN):
                written_pitches = []
            elif isinstance(lt.head, abjad.Note):
                written_pitches = [lt.head.written_pitch]
            elif isinstance(lt.head, abjad.Chord):
                written_pitches = lt.head.written_pitches
            else:
                written_pitches = []
            pcs = _pitchclasses.PitchClassSet(written_pitches)
            if abjad.get.has_indicator(
                lt.head, _const.NOT_YET_PITCHED
            ) or abjad.get.has_indicator(lt.head, _const.ALLOW_REPEAT_PITCH):
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
    for plt in _selection.Selection(score).plts():
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
    if "Global_Rests" in score:
        context = score["Global_Rests"]
        rests = abjad.select(context).leaves(abjad.MultimeasureRest)
        final_measure_index = len(rests) - 1
        final_measure_index -= 1
        indicator = _const.FERMATA_MEASURE
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


def _get_global_spanner_extra_offsets(
    clock_time_extra_offset,
    local_measure_number_extra_offset,
    measure_number_extra_offset,
    spacing_extra_offset,
    stage_number_extra_offset,
):
    strings = []
    if clock_time_extra_offset is not None:
        value = clock_time_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"clock-time-extra-offset = {string}"
        strings.append(string)
    if local_measure_number_extra_offset is not None:
        value = local_measure_number_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"local-measure-number-extra-offset = {string}"
        strings.append(string)
    if measure_number_extra_offset is not None:
        value = measure_number_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"measure-number-extra-offset = {string}"
        strings.append(string)
    if spacing_extra_offset is not None:
        value = spacing_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"spacing-extra-offset = {string}"
        strings.append(string)
    if stage_number_extra_offset is not None:
        value = stage_number_extra_offset
        assert isinstance(value, tuple)
        string = f"#'({value[0]} . {value[1]})"
        string = f"stage-number-extra-offset = {string}"
        strings.append(string)
    return strings


def _get_measure_number_tag(leaf, offset_to_measure_number):
    start_offset = abjad.get.timespan(leaf).start_offset
    measure_number = offset_to_measure_number.get(start_offset)
    if measure_number is not None:
        return abjad.Tag(f"MEASURE_{measure_number}")


def _get_measure_offsets(score, start_measure, stop_measure):
    skips = _selection.Selection(score["Global_Skips"]).skips()
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


def _get_previous_segment_voice_metadata(previous_persist, voice_name):
    if not previous_persist:
        return
    voice_metadata = previous_persist.get("voice_metadata")
    if not voice_metadata:
        return
    return voice_metadata.get(voice_name, {})


def _handle_mutator(score, cache, command):
    if hasattr(command, "_mutates_score") and command._mutates_score():
        cache = None
        _update_score_one_time(score)
    return cache


def _intercalate_silences(
    skips_instead_of_rests,
    time_signatures,
    timespans,
    voice_name,
):
    selections = []
    durations = [_.duration for _ in time_signatures]
    measure_start_offsets = abjad.math.cumulative_sums(durations)
    segment_duration = measure_start_offsets[-1]
    previous_stop_offset = abjad.Offset(0)
    for timespan in timespans:
        start_offset = timespan.start_offset
        if start_offset < previous_stop_offset:
            raise Exception("overlapping offsets: {timespan!r}.")
        if previous_stop_offset < start_offset:
            selection = _make_measure_silences(
                measure_start_offsets,
                skips_instead_of_rests,
                previous_stop_offset,
                start_offset,
                voice_name,
            )
            selections.append(selection)
        selection = timespan.annotation
        assert isinstance(selection, abjad.Selection), repr(selection)
        selections.append(selection)
        duration = abjad.get.duration(selection)
        previous_stop_offset = start_offset + duration
    if previous_stop_offset < segment_duration:
        selection = _make_measure_silences(
            measure_start_offsets,
            skips_instead_of_rests,
            previous_stop_offset,
            segment_duration,
            voice_name,
        )
        assert isinstance(selection, abjad.Selection)
        selections.append(selection)
    assert all(isinstance(_, abjad.Selection) for _ in selections)
    return selections, segment_duration


def _label_clock_time(
    clock_time_override,
    fermata_measure_numbers,
    first_measure_number,
    previous_metadata,
    score,
):
    skips = _selection.Selection(score["Global_Skips"]).skips()
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
                tag=tag.append(_scoping.site(_frame())),
            )
        if 0 < measure_index:
            tag = _tags.CLOCK_TIME
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanCT")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag.append(_scoping.site(_frame())),
            )
    return duration, start_clock_time, stop_clock_time


def _label_duration_multipliers(score):
    tag = _scoping.site(_frame())
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
            markup = abjad.Markup(string, direction=abjad.Up)
            tag_ = tag
            if abjad.get.has_indicator(leaf, _const.HIDDEN):
                tag_ = tag_.append(_tags.HIDDEN)
            if abjad.get.has_indicator(leaf, _const.MULTIMEASURE_REST):
                tag_ = tag_.append(_tags.MULTIMEASURE_REST)
            if abjad.get.has_indicator(leaf, _const.NOTE):
                tag_ = tag_.append(_tags.NOTE)
            if abjad.get.has_indicator(leaf, _const.PHANTOM):
                tag_ = tag_.append(_tags.PHANTOM)
            if abjad.get.has_indicator(leaf, _const.REST_VOICE):
                tag_ = tag_.append(_tags.REST_VOICE)
            abjad.attach(markup, leaf, deactivate=True, tag=tag_)
            already_labeled.add(leaf)


def _label_measure_numbers(first_measure_number, global_skips):
    skips = _selection.Selection(global_skips).skips()
    total = len(skips)
    for measure_index, skip in enumerate(skips):
        local_measure_number = measure_index + 1
        measure_number = first_measure_number + measure_index
        if measure_index < total - 1:
            tag = _tags.LOCAL_MEASURE_NUMBER
            tag = tag.append(_scoping.site(_frame()))
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
            tag = tag.append(_scoping.site(_frame()))
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
            tag = tag.append(_scoping.site(_frame()))
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanLMN")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
            tag = _tags.MEASURE_NUMBER
            tag = tag.append(_scoping.site(_frame()))
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMN")
            abjad.attach(
                stop_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )


def _label_moment_numbers(global_skips, moment_markup):
    if not moment_markup:
        return
    skips = _selection.Selection(global_skips).skips()
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
        tag = tag.append(_scoping.site(_frame()))
        if color is not None:
            string = r"- \baca-start-xnm-colored-left-only"
            string += f' "{value}" {color}'
        else:
            string = r"- \baca-start-xnm-left-only"
            string += f' "{value}"'
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
            tag = tag.append(_scoping.site(_frame()))
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
    tag = tag.append(_scoping.site(_frame()))
    stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanXNM")
    abjad.attach(
        stop_text_span,
        skip,
        context="GlobalSkips",
        deactivate=True,
        tag=tag,
    )


def _label_stage_numbers(global_skips, stage_markup):
    if not stage_markup:
        return
    skips = _selection.Selection(global_skips).skips()
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
        tag = tag.append(_scoping.site(_frame()))
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
            tag = tag.append(_scoping.site(_frame()))
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
    tag = tag.append(_scoping.site(_frame()))
    stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSNM")
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
    tag = tag.append(_scoping.site(_frame()))
    for staff in abjad.iterate.components(score, abjad.Staff):
        first_leaf = abjad.get.leaf(staff, 0)
        assert first_leaf is not None
        literal = abjad.LilyPondLiteral(string)
        abjad.attach(literal, first_leaf, tag=tag)


def _make_global_context():
    global_rests = abjad.Context(lilypond_type="GlobalRests", name="Global_Rests")
    global_skips = abjad.Context(lilypond_type="GlobalSkips", name="Global_Skips")
    global_context = abjad.Context(
        [global_rests, global_skips],
        lilypond_type="GlobalContext",
        simultaneous=True,
        name="Global_Context",
    )
    return global_context


def _make_global_rests(append_phantom_measure, time_signatures):
    rests = []
    for time_signature in time_signatures:
        rest = abjad.MultimeasureRest(
            abjad.Duration(1),
            multiplier=time_signature.duration,
            tag=_scoping.site(_frame(), n=1),
        )
        rests.append(rest)
    if append_phantom_measure:
        tag = _scoping.site(_frame(), n=2).append(_tags.PHANTOM)
        rest = abjad.MultimeasureRest(abjad.Duration(1), multiplier=(1, 4), tag=tag)
        abjad.attach(_const.PHANTOM, rest)
        rests.append(rest)
    return rests


def _make_global_skips(
    append_phantom_measure,
    global_skips,
    time_signatures,
):
    for time_signature in time_signatures:
        skip = abjad.Skip(
            1,
            multiplier=time_signature.duration,
            tag=_scoping.site(_frame(), n=1),
        )
        abjad.attach(
            time_signature,
            skip,
            context="Score",
            tag=_scoping.site(_frame(), n=2),
        )
        global_skips.append(skip)
    if append_phantom_measure:
        tag = _scoping.site(_frame(), n=3)
        tag = tag.append(_tags.PHANTOM)
        skip = abjad.Skip(1, multiplier=(1, 4), tag=tag)
        abjad.attach(_const.PHANTOM, skip)
        global_skips.append(skip)
        if time_signature != abjad.TimeSignature((1, 4)):
            time_signature = abjad.TimeSignature((1, 4))
            abjad.attach(time_signature, skip, context="Score", tag=tag)


def _make_lilypond_file(
    include_layout_ly,
    includes,
    midi,
    preamble,
    score,
):
    tag = _scoping.site(_frame())
    items = []
    items.extend(includes)
    items.append("")
    if preamble:
        string = "\n".join(preamble)
        items.append(string)
    block = abjad.Block("score")
    block.items.append(score)
    items.append(block)
    lilypond_file = abjad.LilyPondFile(
        items=items,
        lilypond_language_token=False,
        tag=tag,
    )
    if include_layout_ly:
        assert len(lilypond_file["score"].items) == 1
        score = lilypond_file["Score"]
        assert isinstance(score, abjad.Score)
        include = abjad.Container(tag=tag)
        literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
        abjad.attach(literal, include, tag=None)
        string = r'\include "layout.ly"'
        literal = abjad.LilyPondLiteral(string, format_slot="opening")
        abjad.attach(literal, include, tag=tag)
        container = abjad.Container([include, score], simultaneous=True, tag=tag)
        literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
        abjad.attach(literal, container, tag=None)
        literal = abjad.LilyPondLiteral("", format_slot="closing")
        abjad.attach(literal, container, tag=None)
        lilypond_file["score"].items[:] = [container]
        lilypond_file["score"].items.append("")
    if midi:
        block = abjad.Block("midi")
        lilypond_file["score"].items.append(block)
    return lilypond_file


def _make_measure_silences(
    measure_start_offsets,
    skips_instead_of_rests,
    start,
    stop,
    voice_name,
):
    tag = _scoping.site(_frame())
    offsets = [start]
    for measure_start_offset in measure_start_offsets:
        if start < measure_start_offset < stop:
            offsets.append(measure_start_offset)
    offsets.append(stop)
    silences = []
    durations = abjad.math.difference_series(offsets)
    for i, duration in enumerate(durations):
        if i == 0:
            silence = _make_multimeasure_rest_container(
                voice_name, duration, skips_instead_of_rests
            )
        else:
            if skips_instead_of_rests:
                silence = abjad.Skip(1, multiplier=duration, tag=tag)
            else:
                silence = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
        silences.append(silence)
    assert all(isinstance(_, abjad.Component) for _ in silences)
    selection = abjad.select(silences)
    return selection


def _make_multimeasure_rest_container(
    voice_name,
    duration,
    skips_instead_of_rests,
    phantom=False,
    suppress_note=False,
):
    if suppress_note is True:
        assert phantom is True
    if phantom is True:
        phantom_tag = _tags.PHANTOM
    else:
        phantom_tag = abjad.Tag()
    tag = _scoping.site(_frame(), n=1)
    tag = tag.append(phantom_tag)
    tag = tag.append(_tags.HIDDEN)
    if suppress_note is not True:
        note_or_rest = _tags.NOTE
        tag = tag.append(_tags.NOTE)
        note = abjad.Note("c'1", multiplier=duration, tag=tag)
        abjad.attach(_const.NOTE, note)
        abjad.attach(_const.NOT_YET_PITCHED, note)
    else:
        note_or_rest = _tags.MULTIMEASURE_REST
        tag = tag.append(_tags.MULTIMEASURE_REST)
        note = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
        abjad.attach(_const.MULTIMEASURE_REST, note)
    abjad.attach(_const.HIDDEN, note)
    tag = _scoping.site(_frame(), n=2)
    tag = tag.append(phantom_tag)
    tag = tag.append(note_or_rest)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
    literal = abjad.LilyPondLiteral(
        r"\abjad-invisible-music-coloring", format_slot="before"
    )
    abjad.attach(literal, note, tag=tag)
    tag = _scoping.site(_frame(), n=3)
    tag = tag.append(phantom_tag)
    tag = tag.append(note_or_rest)
    tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
    literal = abjad.LilyPondLiteral(r"\abjad-invisible-music", format_slot="before")
    abjad.attach(literal, note, deactivate=True, tag=tag)
    abjad.attach(_const.HIDDEN, note)
    tag = _scoping.site(_frame(), n=4)
    tag = tag.append(phantom_tag)
    hidden_note_voice = abjad.Voice([note], name=voice_name, tag=tag)
    abjad.attach(_const.INTERMITTENT, hidden_note_voice)
    tag = _scoping.site(_frame(), n=5)
    tag = tag.append(phantom_tag)
    tag = tag.append(_tags.REST_VOICE)
    if skips_instead_of_rests:
        tag = tag.append(_tags.SKIP)
        rest = abjad.Skip(1, multiplier=duration, tag=tag)
        abjad.attach(_const.SKIP, rest)
    else:
        tag = tag.append(_tags.MULTIMEASURE_REST)
        rest = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
        abjad.attach(_const.MULTIMEASURE_REST, rest)
    abjad.attach(_const.REST_VOICE, rest)
    if "Music_Voice" in voice_name:
        name = voice_name.replace("Music_Voice", "Rest_Voice")
    else:
        name = voice_name.replace("Voice", "Rest_Voice")
    tag = _scoping.site(_frame(), n=6)
    tag = tag.append(phantom_tag)
    multimeasure_rest_voice = abjad.Voice([rest], name=name, tag=tag)
    abjad.attach(_const.INTERMITTENT, multimeasure_rest_voice)
    tag = _scoping.site(_frame(), n=7)
    tag = tag.append(phantom_tag)
    container = abjad.Container(
        [hidden_note_voice, multimeasure_rest_voice],
        simultaneous=True,
        tag=tag,
    )
    abjad.attach(_const.MULTIMEASURE_REST_CONTAINER, container)
    if phantom is True:
        for component in abjad.iterate.components(container):
            abjad.attach(_const.PHANTOM, component)
    return container


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
    elif class_ is _indicators.StaffLines:
        indicator = class_(line_count=memento.value)
    elif memento.value is None:
        indicator = class_()
    elif isinstance(memento.value, dict):
        indicator = class_(**memento.value)
    else:
        try:
            indicator = class_(memento.value)
        except Exception:
            raise Exception(abjad.storage(memento))
    return indicator


def _move_global_context(score):
    assert "Global_Rests" not in score
    global_skips = score["Global_Skips"]
    global_skips.lilypond_type = "Voice"
    music_context = score["Music_Context"]
    for component in abjad.iterate.components(music_context):
        if isinstance(component, abjad.Staff):
            first_music_staff = component
            break
    first_music_staff.simultaneous = True
    first_music_staff.insert(0, global_skips)
    score["Global_Context"][:] = []
    del score["Global_Context"]
    assert len(score) == 1, repr(score)
    score[:] = music_context[:]
    if len(score) == 1:
        score.simultaneous = False


def _move_global_rests(
    global_rests_in_every_staff,
    global_rests_in_topmost_staff,
    score,
):
    if not global_rests_in_topmost_staff and not global_rests_in_every_staff:
        return
    if "Global_Rests" not in score:
        return
    global_rests = score["Global_Rests"]
    score["Global_Context"].remove(global_rests)
    music_context = score["Music_Context"]
    if global_rests_in_topmost_staff is True:
        for staff in abjad.iterate.components(music_context, abjad.Staff):
            break
        staff.simultaneous = True
        staff.insert(0, global_rests)
        return
    if global_rests_in_every_staff is True:
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
    for skip in _selection.Selection(global_skips).skips():
        offset = abjad.get.timespan(skip).start_offset
        offset_to_measure_number[offset] = measure_number
        measure_number += 1
    return offset_to_measure_number


def _print_timing(title, timer, *, print_timing=False, suffix=None):
    if not print_timing:
        return
    count = int(timer.elapsed_time)
    counter = abjad.String("second").pluralize(count)
    count = str(count)
    if suffix is not None:
        suffix = f" [{suffix}]"
    else:
        suffix = ""
    string = f"{_const.colors.cyan}{title}{suffix} in {count} {counter}"
    string += f" ...{_const.colors.end}"
    print(string)


def _prototype_string(class_):
    parts = class_.__module__.split(".")
    if parts[-1] != class_.__name__:
        parts.append(class_.__name__)
    return f"{parts[0]}.{parts[-1]}"


def _reapply_persistent_indicators(
    manifests,
    previous_persistent_indicators,
    score,
):
    for context in abjad.iterate.components(score, abjad.Context):
        mementos = previous_persistent_indicators.get(context.name)
        if not mementos:
            continue
        for memento in mementos:
            if memento.manifest is not None:
                if memento.manifest == "instruments":
                    dictionary = manifests["abjad.Instrument"]
                elif memento.manifest == "margin_markups":
                    dictionary = manifests["abjad.MarginMarkup"]
                elif memento.manifest == "metronome_marks":
                    dictionary = manifests["abjad.MetronomeMark"]
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
                site = _scoping.site(_frame(), n=1)
                edition = edition.append(site)
                wrapper.tag = wrapper.tag.append(edition)
                _scoping.treat_persistent_wrapper(manifests, wrapper, status)
                continue
            # TODO: change to parameter comparison
            prototype = (
                _indicators.Accelerando,
                abjad.MetronomeMark,
                _indicators.Ritardando,
            )
            if isinstance(previous_indicator, prototype):
                site = _scoping.site(_frame(), n=2)
                if status == "reapplied":
                    wrapper = abjad.attach(
                        previous_indicator,
                        leaf,
                        synthetic_offset=synthetic_offset,
                        tag=edition.append(site),
                        wrapper=True,
                    )
                    _scoping.treat_persistent_wrapper(manifests, wrapper, status)
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
                    _scoping.treat_persistent_wrapper(manifests, wrapper, status)
                continue
            attached = False
            site = _scoping.site(_frame(), n=3)
            tag = edition.append(site)
            if isinstance(previous_indicator, abjad.MarginMarkup):
                tag = tag.append(_tags.NOT_PARTS)
            try:
                wrapper = abjad.attach(
                    previous_indicator,
                    leaf,
                    synthetic_offset=synthetic_offset,
                    tag=tag,
                    wrapper=True,
                )
                attached = True
            except abjad.PersistentIndicatorError:
                pass
            if attached:
                _scoping.treat_persistent_wrapper(manifests, wrapper, status)


def _reanalyze_reapplied_synthetic_wrappers(score):
    site = _scoping.site(_frame())
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if wrapper.synthetic_offset is None:
                continue
            if 0 <= wrapper.synthetic_offset:
                continue
            if "REAPPLIED" in str(wrapper.tag):
                string = str(wrapper.tag)
                string = string.replace("REAPPLIED", "EXPLICIT")
                tag_ = abjad.Tag(string).append(site)
                wrapper._tag = tag_
                wrapper._synthetic_offset = None


def _reanalyze_trending_dynamics(manifests, score):
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if isinstance(wrapper.indicator, abjad.Dynamic) and abjad.get.indicators(
                leaf, abjad.StartHairpin
            ):
                _scoping.treat_persistent_wrapper(manifests, wrapper, "explicit")


def _remove_redundant_time_signatures(append_phantom_measure, global_skips):
    previous_time_signature = None
    cached_time_signatures = []
    skips = _selection.Selection(global_skips).skips()
    if append_phantom_measure:
        skips = skips[:-1]
    for skip in skips:
        time_signature = abjad.get.indicator(skip, abjad.TimeSignature)
        cached_time_signatures.append(str(time_signature))
        if time_signature == previous_time_signature:
            abjad.detach(time_signature, skip)
        else:
            previous_time_signature = time_signature
    return cached_time_signatures


def _remove_tags(remove_tags, score):
    assert all(isinstance(_, abjad.Tag) for _ in remove_tags), repr(remove_tags)
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if wrapper.tag is None:
                continue
            for word in wrapper.tag:
                if abjad.Tag(word) in remove_tags:
                    abjad.detach(wrapper, leaf)
                    break


def _scope_to_leaf_selection(
    score,
    allow_empty_selections,
    cache,
    command,
    measure_count,
):
    leaves = []
    selections, cache = _scope_to_leaf_selections(
        score,
        cache,
        measure_count,
        command.scope,
    )
    for selection in selections:
        leaves.extend(selection)
    selection = abjad.select(leaves)
    if not selection:
        message = f"EMPTY SELECTION:\n\n{abjad.storage(command)}"
        if allow_empty_selections:
            print(message)
        else:
            raise Exception(message)
    assert selection.are_leaves(), repr(selection)
    if isinstance(command.scope, _scoping.TimelineScope):
        selection = _sort_by_timeline(selection)
    return selection, cache


def _scope_to_leaf_selections(score, cache, measure_count, scope):
    if cache is None:
        cache = _cache_leaves(score, measure_count)
    if isinstance(scope, _scoping.Scope):
        scopes = [scope]
    else:
        assert isinstance(scope, _scoping.TimelineScope)
        scopes = list(scope.scopes)
    leaf_selections = []
    for scope in scopes:
        leaves = []
        try:
            leaves_by_measure_number = cache[scope.voice_name]
        except KeyError:
            print(f"Unknown voice {scope.voice_name} ...\n")
            raise
        start = scope.measures[0]
        if scope.measures[1] == -1:
            stop = measure_count + 1
        else:
            stop = scope.measures[1] + 1
        if start < 0:
            start = measure_count - abs(start) + 1
        if stop < 0:
            stop = measure_count - abs(stop) + 1
        for measure_number in range(start, stop):
            leaves_ = leaves_by_measure_number.get(measure_number, [])
            leaves.extend(leaves_)
        leaf_selections.append(abjad.select(leaves))
    return leaf_selections, cache


def _set_intermittent_to_staff_position_zero(score):
    pleaves = []
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice._has_indicator(_const.INTERMITTENT):
            for pleaf in abjad.iterate.leaves(voice, pitched=True):
                if abjad.get.has_indicator(pleaf, _const.NOT_YET_PITCHED):
                    pleaves.append(pleaf)
    command = _pitchcommands.staff_position(
        0,
        _selectors.plts(),
        set_chord_pitches_equal=True,
    )
    command(pleaves)


def _set_not_yet_pitched_to_staff_position_zero(score):
    pleaves = []
    for pleaf in abjad.iterate.leaves(score, pitched=True):
        if not abjad.get.has_indicator(pleaf, _const.NOT_YET_PITCHED):
            continue
        pleaves.append(pleaf)
    command = _pitchcommands.staff_position(
        0,
        _selectors.plts(),
        set_chord_pitches_equal=True,
    )
    command(pleaves)


def _shift_measure_initial_clefs(
    offset_to_measure_number,
    previous_persist,
    score,
):
    for staff in abjad.iterate.components(score, abjad.Staff):
        for leaf in abjad.iterate.leaves(staff):
            start_offset = abjad.get.timespan(leaf).start_offset
            wrapper = abjad.get.wrapper(leaf, abjad.Clef)
            if wrapper is None or not wrapper.tag:
                continue
            if _tags.EXPLICIT_CLEF not in wrapper.tag:
                continue
            measure_number = offset_to_measure_number.get(start_offset)
            if measure_number is None:
                continue
            clef = wrapper.indicator
            suite = _overrides.clef_shift(clef, selector=_selectors.leaf(0))
            runtime = _bundle_runtime(
                offset_to_measure_number=offset_to_measure_number,
            )
            suite(leaf, runtime=runtime)


def _sort_dictionary(dictionary):
    items = list(dictionary.items())
    items.sort()
    dictionary.clear()
    for key, value in items:
        if isinstance(value, dict):
            _sort_dictionary(value)
        dictionary[key] = value


def _sort_by_timeline(leaves):
    assert leaves.are_leaves(), repr(leaves)

    def compare(leaf_1, leaf_2):
        start_offset_1 = abjad.get.timespan(leaf_1).start_offset
        start_offset_2 = abjad.get.timespan(leaf_2).start_offset
        if start_offset_1 < start_offset_2:
            return -1
        if start_offset_2 < start_offset_1:
            return 1
        index_1 = abjad.get.parentage(leaf_1).score_index()
        index_2 = abjad.get.parentage(leaf_2).score_index()
        if index_1 < index_2:
            return -1
        if index_2 < index_1:
            return 1
        return 0

    leaves = list(leaves)
    leaves.sort(key=functools.cmp_to_key(compare))
    return abjad.select(leaves)


def _style_fermata_measures(
    fermata_extra_offset_y,
    fermata_measure_empty_overrides,
    fermata_start_offsets,
    final_segment,
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
            if abjad.get.has_indicator(leaf, _const.PHANTOM):
                continue
            start_offset = abjad.get.timespan(leaf).start_offset
            if start_offset not in fermata_start_offsets:
                continue
            voice = abjad.get.parentage(leaf).get(abjad.Voice)
            if "Rest_Voice" in voice.name:
                continue
            if start_offset not in empty_fermata_measure_start_offsets:
                continue
            empty_staff_lines = _indicators.StaffLines(0)
            empty_bar_extent = _indicators.BarExtent(0)
            previous_staff_lines = abjad.get.effective(leaf, _indicators.StaffLines)
            previous_bar_extent = abjad.get.effective(leaf, _indicators.BarExtent)
            next_leaf = abjad.get.leaf(leaf, 1)
            if abjad.get.has_indicator(next_leaf, _const.PHANTOM):
                next_leaf = None
            next_staff_lines = None
            if next_leaf is not None:
                next_staff_lines = abjad.get.effective(
                    next_leaf, _indicators.StaffLines
                )
                next_bar_extent = abjad.get.effective(next_leaf, _indicators.BarExtent)
            if (
                previous_staff_lines != empty_staff_lines
            ) and not abjad.get.has_indicator(leaf, _indicators.StaffLines):
                abjad.attach(
                    empty_staff_lines,
                    leaf,
                    tag=_scoping.site(_frame(), n=1),
                )
                if not final_segment:
                    abjad.attach(
                        empty_bar_extent,
                        leaf,
                        tag=_scoping.site(_frame(), n=2).append(
                            _tags.FERMATA_MEASURE_EMPTY_BAR_EXTENT
                        ),
                    )
            if next_leaf is not None and empty_staff_lines != next_staff_lines:
                if next_staff_lines is None:
                    next_staff_lines_ = _indicators.StaffLines(5)
                else:
                    next_staff_lines_ = next_staff_lines
                if next_bar_extent is None:
                    next_bar_extent_ = _indicators.StaffLines(5)
                else:
                    next_bar_extent_ = next_bar_extent
                wrapper = abjad.get.effective_wrapper(next_leaf, _indicators.StaffLines)
                next_leaf_start_offset = abjad.get.timespan(next_leaf).start_offset
                if wrapper is None or (wrapper.start_offset != next_leaf_start_offset):
                    abjad.attach(
                        next_staff_lines_,
                        next_leaf,
                        tag=_scoping.site(_frame(), n=3),
                    )
                    abjad.attach(
                        next_bar_extent_,
                        next_leaf,
                        tag=_scoping.site(_frame(), n=4).append(
                            _tags.FERMATA_MEASURE_NEXT_BAR_EXTENT
                        ),
                    )
            if next_leaf is None and previous_staff_lines != empty_staff_lines:
                previous_line_count = 5
                if previous_staff_lines is not None:
                    previous_line_count = previous_staff_lines.line_count
                resume_staff_lines = _indicators.StaffLines(
                    previous_line_count, hide=True
                )
                abjad.attach(
                    resume_staff_lines,
                    leaf,
                    synthetic_offset=99,
                    tag=_scoping.site(_frame(), n=5),
                )
                previous_line_count = 5
                if previous_bar_extent is not None:
                    previous_line_count = previous_bar_extent.line_count
                resume_bar_extent = _indicators.BarExtent(
                    previous_line_count, hide=True
                )
                abjad.attach(
                    resume_bar_extent,
                    leaf,
                    synthetic_offset=99,
                    tag=_scoping.site(_frame(), n=6).append(
                        _tags.FERMATA_MEASURE_RESUME_BAR_EXTENT
                    ),
                )
            if start_offset in bar_lines_already_styled:
                continue
            if not (next_leaf is None and final_segment):
                # TODO: replace literal with override
                strings = []
                string = r"Score.BarLine.transparent = ##t"
                string = r"\once \override " + string
                strings.append(string)
                string = r"Score.SpanBar.transparent = ##t"
                string = r"\once \override " + string
                strings.append(string)
                literal = abjad.LilyPondLiteral(strings)
                tag = _tags.FERMATA_MEASURE
                measure_number_tag = _get_measure_number_tag(
                    leaf,
                    offset_to_measure_number,
                )
                if measure_number_tag is not None:
                    tag = tag.append(measure_number_tag)
                next_leaf_ = abjad.get.leaf(leaf, 1)
                assert next_leaf_ is not None, repr(next_leaf_)
                abjad.attach(
                    literal,
                    next_leaf_,
                    tag=tag.append(_scoping.site(_frame(), n=7)),
                )
            bar_lines_already_styled.append(start_offset)
    rests = _selection.Selection(score["Global_Rests"]).leaves(abjad.MultimeasureRest)
    for measure_number in fermata_measure_empty_overrides:
        measure_index = measure_number - 1
        rest = rests[measure_index]
        grob = abjad.override(rest).multi_measure_rest_text
        grob.extra_offset = (0, fermata_extra_offset_y)


def _style_phantom_measures(score):
    skip = abjad.get.leaf(score["Global_Skips"], -1)
    for literal in abjad.get.indicators(skip, abjad.LilyPondLiteral):
        if r"\baca-time-signature-color" in literal.argument:
            abjad.detach(literal, skip)
    _append_tag_to_wrappers(
        skip,
        _scoping.site(_frame(), n=1).append(_tags.PHANTOM),
    )
    string = r"\baca-time-signature-transparent"
    literal = abjad.LilyPondLiteral(string)
    abjad.attach(
        literal,
        skip,
        tag=_scoping.site(_frame(), n=2).append(_tags.PHANTOM),
    )
    strings = [
        r"\once \override Score.BarLine.transparent = ##t",
        r"\once \override Score.SpanBar.transparent = ##t",
    ]
    literal = abjad.LilyPondLiteral(strings, format_slot="after")
    abjad.attach(
        literal,
        skip,
        tag=_scoping.site(_frame(), n=3).append(_tags.PHANTOM),
    )
    if "Global_Rests" in score:
        for context in abjad.iterate.components(score, abjad.Context):
            if context.name == "Global_Rests":
                rest = context[-1]
                break
        _append_tag_to_wrappers(
            rest,
            _scoping.site(_frame(), n=4).append(_tags.PHANTOM),
        )
    start_offset = abjad.get.timespan(skip).start_offset
    enumeration = _const.MULTIMEASURE_REST_CONTAINER
    containers = []
    for container in abjad.select(score).components(abjad.Container):
        if not abjad.get.has_indicator(container, enumeration):
            continue
        leaf = abjad.get.leaf(container, 0)
        if abjad.get.timespan(leaf).start_offset != start_offset:
            continue
        containers.append(container)
    string_1 = r"\once \override Score.TimeSignature.X-extent = ##f"
    string_2 = r"\once \override MultiMeasureRest.transparent = ##t"
    strings = [
        r"\stopStaff",
        r"\once \override Staff.StaffSymbol.transparent = ##t",
        r"\startStaff",
    ]
    for container in containers:
        for leaf in abjad.select(container).leaves():
            _append_tag_to_wrappers(
                leaf,
                _scoping.site(_frame(), n=5).append(_tags.PHANTOM),
            )
            if not isinstance(leaf, abjad.MultimeasureRest):
                continue
            if abjad.get.has_indicator(leaf, _const.HIDDEN):
                continue
            literal = abjad.LilyPondLiteral(string_1)
            abjad.attach(
                literal,
                leaf,
                tag=_scoping.site(_frame(), n=6).append(_tags.PHANTOM),
            )
            literal = abjad.LilyPondLiteral(string_2)
            abjad.attach(
                literal,
                leaf,
                tag=_scoping.site(_frame(), n=7).append(_tags.PHANTOM),
            )
            literal = abjad.LilyPondLiteral(strings)
            abjad.attach(
                literal,
                leaf,
                tag=_scoping.site(_frame(), n=8).append(_tags.PHANTOM),
            )


def _transpose_score(score):
    for pleaf in _selection.Selection(score).pleaves():
        if abjad.get.has_indicator(pleaf, _const.DO_NOT_TRANSPOSE):
            continue
        if abjad.get.has_indicator(pleaf, _const.STAFF_POSITION):
            continue
        abjad.iterpitches.transpose_from_sounding_pitch(pleaf)


def _treat_untreated_persistent_wrappers(
    manifests,
    score,
):
    dynamic_prototype = (abjad.Dynamic, abjad.StartHairpin)
    tempo_prototype = (
        _indicators.Accelerando,
        abjad.MetronomeMark,
        _indicators.Ritardando,
    )
    for leaf in abjad.iterate.leaves(score):
        for wrapper in abjad.get.wrappers(leaf):
            if not getattr(wrapper.indicator, "persistent", False):
                continue
            if wrapper.tag and _tags.has_persistence_tag(wrapper.tag):
                continue
            if isinstance(wrapper.indicator, abjad.Instrument):
                prototype = abjad.Instrument
            elif isinstance(wrapper.indicator, dynamic_prototype):
                prototype = dynamic_prototype
            elif isinstance(wrapper.indicator, tempo_prototype):
                prototype = tempo_prototype
            else:
                prototype = type(wrapper.indicator)
            # TODO: optimize
            previous_indicator = abjad.get.effective(leaf, prototype, n=-1)
            if _scoping.compare_persistent_indicators(
                previous_indicator, wrapper.indicator
            ):
                status = "redundant"
            else:
                status = "explicit"
            _scoping.treat_persistent_wrapper(manifests, wrapper, status)


def _update_score_one_time(score):
    is_forbidden_to_update = score._is_forbidden_to_update
    score._is_forbidden_to_update = False
    score._update_now(offsets=True)
    score._is_forbidden_to_update = is_forbidden_to_update


def _voice_to_rhythm_commands(commands, voice):
    commands_ = []
    for command in commands:
        if not isinstance(command, _rhythmcommands.RhythmCommand):
            continue
        if command.scope.voice_name == voice.name:
            commands_.append(command)
    return commands_


def _whitespace_leaves(score):
    for leaf in abjad.iterate.leaves(score):
        literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
        abjad.attach(literal, leaf, tag=None)
    for container in abjad.iterate.components(score, abjad.Container):
        if hasattr(container, "_main_leaf"):
            literal = abjad.LilyPondLiteral("", format_slot="absolute_after")
            abjad.attach(literal, container, tag=None)
        else:
            literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
            abjad.attach(literal, container, tag=None)
        literal = abjad.LilyPondLiteral("", format_slot="closing")
        abjad.attach(literal, container, tag=None)


def color_out_of_range_pitches(score):
    indicator = _const.ALLOW_OUT_OF_RANGE
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.OUT_OF_RANGE_COLORING)
    for voice in abjad.iterate.components(score, abjad.Voice):
        for pleaf in abjad.iterate.leaves(voice, pitched=True):
            if abjad.get.has_indicator(pleaf, _const.HIDDEN):
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
                literal = abjad.LilyPondLiteral(string, format_slot="before")
                abjad.attach(literal, pleaf, tag=tag)


def color_repeat_pitch_classes(score):
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.REPEAT_PITCH_CLASS_COLORING)
    lts = _find_repeat_pitch_classes(score)
    for lt in lts:
        for leaf in lt:
            string = r"\baca-repeat-pitch-class-coloring"
            literal = abjad.LilyPondLiteral(string, format_slot="before")
            abjad.attach(literal, leaf, tag=tag)


def interpreter(
    score,
    commands,
    time_signatures,
    *,
    activate=None,
    add_container_identifiers=False,
    all_music_in_part_containers=False,
    allow_empty_selections=False,
    allows_instrument=None,
    always_make_global_rests=False,
    append_phantom_measure=False,
    attach_nonfirst_empty_start_bar=False,
    attach_rhythm_annotation_spanners=False,
    check_persistent_indicators=False,
    check_wellformedness=False,
    clock_time_extra_offset=None,
    clock_time_override=None,
    color_not_yet_pitched=False,
    color_octaves=False,
    comment_measure_numbers=False,
    deactivate=None,
    do_not_require_margin_markup=False,
    error_on_not_yet_pitched=False,
    fermata_extra_offset_y=2.5,
    fermata_measure_empty_overrides=None,
    final_segment=False,
    first_measure_number=None,
    first_segment=False,
    force_nonnatural_accidentals=False,
    global_rests_in_every_staff=False,
    global_rests_in_topmost_staff=False,
    instruments=None,
    label_clock_time=False,
    magnify_staves=None,
    margin_markups=None,
    metadata=None,
    metronome_marks=None,
    # TODO: remove midi keyword because unused?
    midi=False,
    moment_markup=None,
    move_global_context=False,
    page_layout_profile=None,
    part_manifest=None,
    parts_metric_modulation_multiplier=None,
    persist=None,
    previous_metadata=None,
    previous_persist=None,
    print_timing=False,
    remove_tags=None,
    segment_number=None,
    shift_measure_initial_clefs=False,
    skips_instead_of_rests=False,
    spacing=None,
    stage_markup=None,
    transpose_score=False,
    treat_untreated_persistent_wrappers=False,
    whitespace_leaves=False,
):
    assert isinstance(score, abjad.Score), repr(score)
    if activate is not None:
        assert all(isinstance(_, abjad.Tag) for _ in activate)
    assert all_music_in_part_containers in (True, False)
    assert allow_empty_selections in (True, False)
    if clock_time_override is not None:
        assert isinstance(clock_time_override, abjad.MetronomeMark)
    assert color_octaves in (True, False)
    assert check_wellformedness in (True, False)
    if deactivate is not None:
        assert all(isinstance(_, abjad.Tag) for _ in deactivate)
    assert do_not_require_margin_markup in (True, False)
    assert final_segment in (True, False)
    first_measure_number = _adjust_first_measure_number(
        first_measure_number,
        previous_metadata,
    )
    assert first_segment in (True, False)
    assert force_nonnatural_accidentals in (True, False)
    manifests = {
        "abjad.Instrument": instruments,
        "abjad.MarginMarkup": margin_markups,
        "abjad.MetronomeMark": metronome_marks,
    }
    metadata = dict(metadata or {})
    if parts_metric_modulation_multiplier is not None:
        assert isinstance(parts_metric_modulation_multiplier, tuple)
        assert len(parts_metric_modulation_multiplier) == 2
    persist = dict(persist or {})
    previous_metadata = dict(previous_metadata or {})
    previous_persist = dict(previous_persist or {})
    assert transpose_score in (True, False)
    assert treat_untreated_persistent_wrappers in (True, False)
    voice_metadata = {}
    global_skips = score["Global_Skips"]
    with abjad.Timer() as timer:
        # temporary hack to make baca.selectors.mleaves() work
        dummy_container = abjad.Container([score], name="Dummy_Container")
        _make_global_skips(append_phantom_measure, global_skips, time_signatures)
        if attach_nonfirst_empty_start_bar and not first_segment:
            _attach_nonfirst_empty_start_bar(global_skips)
        _label_measure_numbers(first_measure_number, global_skips)
        _label_stage_numbers(global_skips, stage_markup)
        _label_moment_numbers(global_skips, moment_markup)
    # _print_timing("Initialization", timer, print_timing=print_timing)
    with abjad.Timer() as timer:
        measure_count = len(time_signatures)
        with abjad.ForbidUpdate(component=score, update_on_exit=True):
            command_count, segment_duration = _call_rhythm_commands(
                always_make_global_rests,
                attach_rhythm_annotation_spanners,
                commands,
                append_phantom_measure,
                manifests,
                measure_count,
                previous_persist,
                score,
                skips_instead_of_rests,
                time_signatures,
                voice_metadata,
            )
            _clean_up_rhythm_maker_voice_names(score)
    _print_timing(
        "Rhythm commands", timer, print_timing=print_timing, suffix=command_count
    )
    with abjad.Timer() as timer:
        offset_to_measure_number = _populate_offset_to_measure_number(
            first_measure_number,
            global_skips,
        )
        _extend_beams(score)
        _attach_sounds_during(score)
        if first_segment:
            _attach_first_segment_default_indicators(
                manifests,
                score,
            )
        previous_persistent_indicators = previous_persist.get("persistent_indicators")
        if previous_persistent_indicators and not first_segment:
            _reapply_persistent_indicators(
                manifests,
                previous_persistent_indicators,
                score,
            )
            _attach_first_appearance_default_indicators(
                manifests,
                previous_persistent_indicators,
                score,
            )
        if spacing is not None:
            _apply_spacing(page_layout_profile, score, spacing)
    # _print_timing("Cleanup", timer, print_timing=print_timing)
    with abjad.Timer() as timer:
        with abjad.ForbidUpdate(component=score, update_on_exit=True):
            cache = None
            cache, command_count = _call_commands(
                allow_empty_selections,
                allows_instrument,
                cache,
                commands,
                measure_count,
                offset_to_measure_number,
                manifests,
                previous_persist,
                score,
                voice_metadata,
            )
    _print_timing(
        "Other commands", timer, print_timing=print_timing, suffix=command_count
    )
    with abjad.Timer() as timer:
        with abjad.ForbidUpdate(component=score, update_on_exit=True):
            if not first_segment:
                _clone_segment_initial_short_instrument_name(score)
            cached_time_signatures = _remove_redundant_time_signatures(
                append_phantom_measure,
                global_skips,
            )
            result = _get_fermata_measure_numbers(first_measure_number, score)
            fermata_start_offsets = result[0]
            fermata_measure_numbers = result[1]
            final_measure_is_fermata = result[2]
            if treat_untreated_persistent_wrappers:
                _treat_untreated_persistent_wrappers(manifests, score)
            _attach_metronome_marks(global_skips, parts_metric_modulation_multiplier)
            _reanalyze_trending_dynamics(manifests, score)
            _reanalyze_reapplied_synthetic_wrappers(score)
            if transpose_score:
                _transpose_score(score)
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
                    do_not_require_margin_markup,
                    score,
                )
            color_repeat_pitch_classes(score)
            if color_octaves:
                _color_octaves(score)
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
            _apply_breaks(score, spacing)
            _style_fermata_measures(
                fermata_extra_offset_y,
                fermata_measure_empty_overrides,
                fermata_start_offsets,
                final_segment,
                offset_to_measure_number,
                score,
            )
            if shift_measure_initial_clefs:
                _shift_measure_initial_clefs(
                    offset_to_measure_number,
                    previous_persist,
                    score,
                )
            _deactivate_tags(deactivate, score)
            _remove_tags(remove_tags or [], score)
            container_to_part_assignment = None
            if add_container_identifiers:
                container_to_part_assignment = _add_container_identifiers(
                    score,
                    segment_number,
                )
                if all_music_in_part_containers:
                    _check_all_music_in_part_containers(score)
                _check_duplicate_part_assignments(
                    container_to_part_assignment,
                    part_manifest,
                )
    _print_timing("Postprocessing", timer, print_timing=print_timing)
    with abjad.Timer() as timer:
        _move_global_rests(
            global_rests_in_every_staff,
            global_rests_in_topmost_staff,
            score,
        )
        if move_global_context:
            _move_global_context(score)
        _clean_up_on_beat_grace_containers(score)
        if check_wellformedness:
            count, message = abjad.wf.tabulate_wellformedness(score)
            if count:
                raise Exception("\n" + message)
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
        _activate_tags(score, activate)
        final_measure_number = first_measure_number + measure_count - 1
        persistent_indicators = _collect_persistent_indicators(
            manifests,
            previous_persistent_indicators,
            score,
        )
        first_metronome_mark = True
        skip = abjad.select(score["Global_Skips"]).leaf(0)
        metronome_mark = abjad.get.effective(skip, abjad.MetronomeMark)
        if metronome_mark is None:
            first_metronome_mark = False
        _collect_metadata(
            container_to_part_assignment,
            clock_time_duration,
            fermata_measure_numbers,
            final_measure_is_fermata,
            final_measure_number,
            first_measure_number,
            first_metronome_mark,
            metadata,
            persist,
            persistent_indicators,
            score,
            start_clock_time,
            stop_clock_time,
            cached_time_signatures,
            voice_metadata,
        )
        if append_phantom_measure:
            _style_phantom_measures(score)
    # _print_timing("Cleanup", timer, print_timing=print_timing)
    dummy_container[:] = []
    return metadata, persist


def make_lilypond_file(
    score,
    clock_time_extra_offset=None,
    include_layout_ly=False,
    includes=None,
    local_measure_number_extra_offset=None,
    measure_number_extra_offset=None,
    midi=False,
    preamble=None,
    spacing_extra_offset=None,
    stage_number_extra_offset=None,
):
    assert isinstance(score, abjad.Score), repr(score)
    if clock_time_extra_offset not in (False, None):
        assert isinstance(clock_time_extra_offset, tuple)
        assert len(clock_time_extra_offset) == 2
    includes = list(includes or [])
    includes = [rf'\include "{_}"' for _ in includes]
    preamble = list(preamble or [])
    if preamble:
        assert all(isinstance(_, str) for _ in preamble), repr(preamble)
    strings = _get_global_spanner_extra_offsets(
        clock_time_extra_offset,
        local_measure_number_extra_offset,
        measure_number_extra_offset,
        spacing_extra_offset,
        stage_number_extra_offset,
    )
    preamble.extend(strings)
    lilypond_file = _make_lilypond_file(
        include_layout_ly,
        includes,
        midi,
        preamble,
        score,
    )
    return lilypond_file


def score_interpretation_defaults():
    return {
        "add_container_identifiers": True,
        "attach_nonfirst_empty_start_bar": True,
        "attach_rhythm_annotation_spanners": True,
        "check_persistent_indicators": True,
        "check_wellformedness": True,
        "color_not_yet_pitched": True,
        "comment_measure_numbers": True,
        "force_nonnatural_accidentals": True,
        "label_clock_time": True,
        "print_timing": True,
        "shift_measure_initial_clefs": True,
        "treat_untreated_persistent_wrappers": True,
        "whitespace_leaves": True,
    }
