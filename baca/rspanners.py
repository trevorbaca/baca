"""
Spanners.
"""

import dataclasses
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import indicators as _indicators
from . import select as _select
from . import spannerlib as _spannerlib
from . import tags as _tags
from . import textspannerlib as _textspannerlib


def clb(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
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
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        f"{markup} =|",
        left_broken_text=r"\baca-left-broken-clb-markup",
        lilypond_id="CLB",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def covered(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-covered-markup =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-covered-markup",
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id="Covered",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def damp(
    argument,
    *tweaks: abjad.Tweak,
    bound_details_right_padding: int | float | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        r"\baca-damp-markup =|",
        left_broken_text=r"\baca-left-broken-damp-markup",
        lilypond_id="Damp",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        bound_details_right_padding=bound_details_right_padding,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def half_clt(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = "½ clt =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-half-clt-markup",
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id="HalfCLT",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def material_annotation(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=None,
        lilypond_id="MaterialAnnotation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
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
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        "MM =|",
        left_broken_text=None,
        lilypond_id="MetricModulation",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.METRIC_MODULATION_SPANNER)
    _tags.wrappers(wrappers, tag)
    return wrappers


def ottava(
    argument,
    n: int = 1,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(n, int), repr(n)
    wrappers = []
    leaf = abjad.select.leaf(argument, 0)
    wrappers_ = _indicators.ottava(leaf, n)
    wrappers.extend(wrappers_)
    leaf = abjad.select.leaf(argument, -1)
    wrappers_ = _indicators.ottava(leaf, 0)
    wrappers.extend(wrappers_)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def pizzicato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-pizz-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
    without_next_leaf: bool = False,
) -> list[abjad.Wrapper]:
    if without_next_leaf is False:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=r"\baca-left-broken-pizz-markup",
        lilypond_id="Pizzicato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def spazzolato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-spazzolato-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=r"\baca-left-broken-spazz-markup",
        lilypond_id="Spazzolato",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
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
    argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(string_number, str), repr(string_number)
    assert string_number in ("I", "II", "III", "IV"), repr(string_number)
    if invisible_line is True:
        descriptor = f"{string_number} ||"
    else:
        descriptor = f"{string_number} =|"
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=f"{(string_number)}",
        lilypond_id="StringNumber",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def tasto(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = "T =|",
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=r"\baca-left-broken-t-markup",
        lilypond_id="SCP",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
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
    argument = _select.rleak_next_nonobgc_leaf(argument)
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
    if pitch is not None or interval is not None:
        start_trill_span = dataclasses.replace(
            start_trill_span, interval=interval, pitch=pitch
        )
    if force_trill_pitch_head_accidental is True:
        start_trill_span = dataclasses.replace(
            start_trill_span,
            force_trill_pitch_head_accidental=force_trill_pitch_head_accidental,
        )
    start_trill_span_: abjad.StartTrillSpan | abjad.Bundle = start_trill_span
    start_trill_span_ = start_trill_span
    if harmonic is True:
        # TODO: replace this with a (one-word) predefined function
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        string = rf"- \tweak TrillPitchHead.stencil {string}"
        start_trill_span_ = abjad.bundle(start_trill_span_, string)
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        start_trill_span_,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        stop_trill_span,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def xfb(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        "XFB =|",
        left_broken_text=r"\baca-left-broken-xfb-markup",
        lilypond_id="BowSpeed",
    )
    assert len(specifiers) == 1
    specifier = specifiers[0]
    wrappers = []
    wrapper = _spannerlib.attach_spanner_start(
        argument,
        specifier.spanner_start,
        *tweaks,
        left_broken=left_broken,
        staff_padding=staff_padding,
    )
    wrappers.append(wrapper)
    wrapper = _spannerlib.attach_spanner_stop(
        argument,
        specifier.spanner_stop,
        right_broken=right_broken,
    )
    wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
