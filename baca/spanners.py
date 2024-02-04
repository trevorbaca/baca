"""
Spanners.
"""

import dataclasses
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import piecewise as _piecewise
from . import select as _select
from . import tags as _tags
from . import treat as _treat
from . import tweaks as _tweaks


def _attach_spanner_indicators(
    argument,
    start_indicator=None,
    stop_indicator=None,
    *tweaks,
    attach_right_broken_hairpin_stop_literal: bool = False,
    context: str | None = None,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    tag_start_dynamic_as_spanner_stop: bool = False,
    tag_start_indicator_as_right_broken: bool = False,
) -> list[abjad.Wrapper]:
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    wrappers = []
    if start_indicator is not None:
        start_indicator = _tweaks.bundle_tweaks(start_indicator, tweaks)
        tag = _helpers.function_name(_frame(), n=1)
        if tag_start_dynamic_as_spanner_stop:
            tag = tag.append(_tags.SPANNER_STOP)
        else:
            tag = tag.append(_tags.SPANNER_START)
        if left_broken:
            tag = tag.append(_tags.LEFT_BROKEN)
        if right_broken and tag_start_indicator_as_right_broken:
            tag = tag.append(_tags.RIGHT_BROKEN)
        first_leaf = abjad.select.leaf(argument, 0)
        reapplied = _treat.remove_reapplied_wrappers(first_leaf, start_indicator)
        wrapper = abjad.attach(
            start_indicator,
            first_leaf,
            context=context,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        if _treat.compare_persistent_indicators(start_indicator, reapplied):
            _treat.treat_persistent_wrapper({}, wrapper, "redundant")
        wrappers.append(wrapper)
    if stop_indicator is not None:
        tag = _helpers.function_name(_frame(), n=2)
        tag = tag.append(_tags.SPANNER_STOP)
        if right_broken:
            tag = tag.append(_tags.RIGHT_BROKEN)
        final_leaf = abjad.select.leaf(argument, -1)
        reapplied = _treat.remove_reapplied_wrappers(final_leaf, stop_indicator)
        wrapper = abjad.attach(
            stop_indicator,
            final_leaf,
            context=context,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        if _treat.compare_persistent_indicators(stop_indicator, reapplied):
            _treat.treat_persistent_wrapper({}, wrapper, "redundant")
        wrappers.append(wrapper)
    if start_indicator is not None:
        if right_broken is True:
            if attach_right_broken_hairpin_stop_literal is True:
                tag = _helpers.function_name(_frame(), n=3)
                tag = tag.append(_tags.RIGHT_BROKEN)
                # TODO: can this be replaced by an abjad.Dynamic?
                literal = abjad.LilyPondLiteral(r"\!", site="after")
                final_leaf = abjad.select.leaf(argument, -1)
                wrapper = abjad.attach(
                    literal,
                    final_leaf,
                    context=context,
                    direction=direction,
                    tag=tag,
                    wrapper=True,
                )
                wrappers.append(wrapper)
    return wrappers


def _prepare_start_trill_span(
    *,
    alteration,
    force_trill_pitch_head_accidental,
    harmonic,
    start_trill_span,
):
    assert isinstance(start_trill_span, abjad.StartTrillSpan), repr(start_trill_span)
    interval = pitch = None
    if alteration is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        assert isinstance(alteration, prototype), repr(alteration)
        try:
            pitch = abjad.NamedPitch(alteration)
        except Exception:
            pass
        try:
            interval = abjad.NamedInterval(alteration)
        except Exception:
            pass
    start_trill_span_ = start_trill_span
    assert isinstance(start_trill_span_, (abjad.StartTrillSpan, abjad.Bundle))
    if pitch is not None or interval is not None:
        start_trill_span_ = dataclasses.replace(
            start_trill_span_, interval=interval, pitch=pitch
        )
    if force_trill_pitch_head_accidental is True:
        start_trill_span_ = dataclasses.replace(
            start_trill_span_,
            force_trill_pitch_head_accidental=force_trill_pitch_head_accidental,
        )
    if harmonic is True:
        # TODO: replace this with a (one-word) predefined function
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        string = rf"- \tweak TrillPitchHead.stencil {string}"
        start_trill_span_ = abjad.bundle(start_trill_span_, string)
    return start_trill_span_


def _with_next_nonobgc_leaf(argument):
    result = _select.rleak(argument)
    if abjad.get.parentage(result[-1]).get(abjad.OnBeatGraceContainer):
        result = _select.rleak(argument, grace=False)
    return result


def beam(
    argument,
    *tweaks: abjad.Tweak,
    direction: abjad.Vertical | None = None,
    start_beam: abjad.StartBeam = abjad.StartBeam(),
    stop_beam: abjad.StopBeam = abjad.StopBeam(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_beam, abjad.StartBeam), repr(start_beam)
    assert isinstance(stop_beam, abjad.StopBeam), repr(stop_beam)
    for leaf in abjad.iterate.leaves(argument, grace=False):
        abjad.detach(abjad.StartBeam, leaf)
        abjad.detach(abjad.StopBeam, leaf)
    wrappers = _attach_spanner_indicators(
        argument,
        start_beam,
        stop_beam,
        *tweaks,
        direction=direction,
    )
    tag = _helpers.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def clb(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.CLB_SPANNER)
    assert string_number in (1, 2, 3, 4), repr(string_number)
    if string_number == 1:
        markup = r"\baca-damp-clb-one-markup"
    elif string_number == 2:
        markup = r"\baca-damp-clb-two-markup"
    elif string_number == 3:
        markup = r"\baca-damp-clb-three-markup"
    elif string_number == 4:
        markup = r"\baca-damp-clb-four-markup"
    else:
        raise Exception(string_number)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        f"{markup} =|",
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-clb-markup",
        lilypond_id="CLB",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.CLB_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def covered(
    argument,
    *tweaks: abjad.Tweak,
    items: str = r"\baca-covered-markup =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-covered-markup",
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=left_broken_text,
        lilypond_id="Covered",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.COVERED_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def damp(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        r"\baca-damp-markup =|",
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-damp-markup",
        lilypond_id="Damp",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.DAMP_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def half_clt(
    argument,
    *tweaks: abjad.Tweak,
    items: str = "½ clt =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-half-clt-markup",
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=left_broken_text,
        lilypond_id="HalfCLT",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.HALF_CLT_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def hairpin(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    debug: bool = False,
    forbid_al_niente_to_bar_line: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    with_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    if with_next_leaf is True:
        argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise.parse_hairpin_descriptor(
        descriptor,
        forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
    )
    wrappers = []
    start_dynamic, hairpin_start, stop_dynamic = None, None, None
    if len(specifiers) == 1:
        specifier = specifiers[0]
        start_dynamic = specifier.indicator
        hairpin_start = specifier.spanner_start
    elif len(specifiers) == 2:
        first, second = specifiers
        start_dynamic = first.indicator
        hairpin_start = first.spanner_start
        stop_dynamic = second.indicator
        if second.spanner_start:
            raise Exception(descriptor)
        if second.spanner_stop:
            raise Exception(descriptor)
    else:
        raise NotImplementedError(descriptor)
    if start_dynamic is not None:
        wrappers_ = _attach_spanner_indicators(
            argument,
            start_dynamic,
            left_broken=left_broken,
            right_broken=right_broken,
            tag_start_dynamic_as_spanner_stop=True,
            tag_start_indicator_as_right_broken=True,
        )
        wrappers.extend(wrappers_)
    wrappers_ = _attach_spanner_indicators(
        argument,
        hairpin_start,
        stop_dynamic,
        *tweaks,
        attach_right_broken_hairpin_stop_literal=True,
        left_broken=left_broken,
        right_broken=right_broken,
        tag_start_indicator_as_right_broken=True,
    )
    wrappers.extend(wrappers_)
    tag = _helpers.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def material_annotation(
    argument,
    items: str | list,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    with_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    if with_next_leaf is True:
        argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=None,
        lilypond_id="MaterialAnnotation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.MATERIAL_ANNOTATION_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def metric_modulation(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    with_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    if with_next_leaf is True:
        argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        "MM =|",
        boxed=False,
        direction=None,
        left_broken_text=None,
        lilypond_id="MetricModulation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.METRIC_MODULATION_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def ottava(
    argument,
    *,
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    return _attach_spanner_indicators(
        argument,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )


def ottava_bassa(
    argument,
    *,
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, site="after"),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    wrappers = _attach_spanner_indicators(
        argument,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )
    tag = _helpers.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def pizzicato(
    argument,
    *tweaks: abjad.Tweak,
    items: str = r"\baca-pizz-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    without_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    if without_next_leaf is False:
        argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-pizz-markup",
        lilypond_id="Pizzicato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.PIZZICATO_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def slur(
    argument,
    *tweaks: abjad.Tweak,
    phrasing_slur: bool = False,
    start_slur: abjad.StartSlur | None = None,
    stop_slur: abjad.StopSlur | None = None,
) -> list[abjad.Wrapper]:
    if phrasing_slur is True:
        start_slur_ = start_slur or abjad.StartPhrasingSlur()
        stop_slur_ = stop_slur or abjad.StopPhrasingSlur()
    else:
        start_slur_ = start_slur or abjad.StartSlur()
        stop_slur_ = stop_slur or abjad.StopSlur()
    wrappers = _attach_spanner_indicators(
        argument,
        start_slur_,
        stop_slur_,
        *tweaks,
    )
    tag = _helpers.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def spazzolato(
    argument,
    *tweaks: abjad.Tweak,
    items: str | list = r"\baca-spazzolato-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-spazz-markup",
        lilypond_id="Spazzolato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.SPAZZOLATO_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def string_number(
    argument,
    string_number: str,
    *tweaks: abjad.Tweak,
    invisible_line: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    with_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    assert with_next_leaf is True, repr(with_next_leaf)
    argument = _select.next(argument)
    assert isinstance(string_number, str), repr(string_number)
    assert string_number in ("I", "II", "III", "IV"), repr(string_number)
    if invisible_line is True:
        items = f"{string_number} ||"
    else:
        items = f"{string_number} =|"
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        left_broken_text=f"{(string_number)}",
        lilypond_id="StringNumber",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.STRING_NUMBER_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def sustain_pedal(
    argument,
    *,
    context: str | None = None,
    start_piano_pedal: abjad.StartPianoPedal = abjad.StartPianoPedal(),
    stop_piano_pedal: abjad.StopPianoPedal = abjad.StopPianoPedal(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_piano_pedal, abjad.StartPianoPedal), repr(start_piano_pedal)
    assert isinstance(stop_piano_pedal, abjad.StopPianoPedal), repr(stop_piano_pedal)
    wrappers = _attach_spanner_indicators(
        argument,
        start_piano_pedal,
        stop_piano_pedal,
        context=context,
    )
    tag = _helpers.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def tasto(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        "T =|",
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-t-markup",
        lilypond_id="SCP",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.TASTO_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def trill(
    argument,
    *tweaks: abjad.Tweak,
    alteration: str | None = None,
    force_trill_pitch_head_accidental: bool = False,
    harmonic: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    start_trill_span: abjad.StartTrillSpan = abjad.StartTrillSpan(),
    stop_trill_span: abjad.StopTrillSpan = abjad.StopTrillSpan(),
) -> list[abjad.Wrapper]:
    argument = _with_next_nonobgc_leaf(argument)
    start_trill_span_ = _prepare_start_trill_span(
        alteration=alteration,
        force_trill_pitch_head_accidental=force_trill_pitch_head_accidental,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
    )
    wrappers = _attach_spanner_indicators(
        argument,
        start_trill_span_,
        stop_trill_span,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def xfb(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    with_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    assert with_next_leaf is True, repr(with_next_leaf)
    argument = _select.next(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        "XFB =|",
        left_broken_text=r"\baca-left-broken-xfb-markup",
        lilypond_id="BowSpeed",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _attach_spanner_indicators(
        argument,
        specifier.spanner_start,
        specifier.spanner_stop,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.BOW_SPEED_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers
