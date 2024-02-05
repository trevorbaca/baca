"""
Spanners.
"""

import dataclasses
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import piecewise as _piecewise
from . import spanners as _spanners
from . import tags as _tags


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


def clb(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
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
    wrappers = _spanners._attach_spanner_indicators(
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
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=left_broken_text,
        lilypond_id="Covered",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        r"\baca-damp-markup =|",
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-damp-markup",
        lilypond_id="Damp",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=left_broken_text,
        lilypond_id="HalfCLT",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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


def material_annotation(
    argument,
    items: str | list,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=None,
        lilypond_id="MaterialAnnotation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        "MM =|",
        boxed=False,
        direction=None,
        left_broken_text=None,
        lilypond_id="MetricModulation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    return _spanners._attach_spanner_indicators(
        argument,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )


def ottava_bassa(
    argument,
    *,
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0),
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    assert isinstance(start_ottava, abjad.Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, abjad.Ottava), repr(stop_ottava)
    wrappers = _spanners._attach_spanner_indicators(
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
        argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-pizz-markup",
        lilypond_id="Pizzicato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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


def spazzolato(
    argument,
    *tweaks: abjad.Tweak,
    items: str | list = r"\baca-spazzolato-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        items,
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-spazz-markup",
        lilypond_id="Spazzolato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
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
    wrappers = _spanners._attach_spanner_indicators(
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


def tasto(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        "T =|",
        boxed=False,
        direction=None,
        left_broken_text=r"\baca-left-broken-t-markup",
        lilypond_id="SCP",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
    argument = _spanners._with_next_nonobgc_leaf(argument)
    start_trill_span_ = _prepare_start_trill_span(
        alteration=alteration,
        force_trill_pitch_head_accidental=force_trill_pitch_head_accidental,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
    )
    wrappers = _spanners._attach_spanner_indicators(
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
) -> list[abjad.Wrapper]:
    argument = _spanners._with_next_nonobgc_leaf(argument)
    specifiers = _piecewise._prepare_text_spanner_arguments(
        "XFB =|",
        left_broken_text=r"\baca-left-broken-xfb-markup",
        lilypond_id="BowSpeed",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = _spanners._attach_spanner_indicators(
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
