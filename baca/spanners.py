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
    wrappers = []
    if start_beam is not None:
        wrapper = _spannerlib.attach_spanner_start(
            argument,
            start_beam,
            *tweaks,
            direction=direction,
        )
        wrappers.append(wrapper)
    if stop_beam is not None:
        wrapper = _spannerlib.attach_spanner_stop(
            argument,
            stop_beam,
        )
        wrappers.append(wrapper)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def clb(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def covered(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-covered-markup =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-parenthesized-cov-markup",
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def damp(
    argument,
    *tweaks: abjad.Tweak,
    bound_details_right_padding: int | float | None = None,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def half_clt(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = "½ clt =|",
    left_broken: bool = False,
    left_broken_text: str = r"\baca-left-broken-half-clt-markup",
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def material_annotation(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, tag)
    return wrappers


def metric_modulation(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, tag)
    return wrappers


def ottava(
    argument,
    n: int = 1,
    *,
    rleak: bool = False,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(n, int), repr(n)
    wrappers = []
    leaf = abjad.select.leaf(argument, 0)
    wrappers_ = _indicators.ottava(leaf, n)
    wrappers.extend(wrappers_)
    leaf = abjad.select.leaf(argument, -1)
    wrappers_ = _indicators.ottava(leaf, 0)
    wrappers.extend(wrappers_)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def pizzicato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-pizz-markup =|",
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    left_broken_text: str = r"\baca-parenthesized-pizz-markup",
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
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
    wrappers = []
    if start_slur_ is not None:
        wrapper = _spannerlib.attach_spanner_start(
            argument,
            start_slur_,
            *tweaks,
        )
        wrappers.append(wrapper)
    if stop_slur_ is not None:
        wrapper = _spannerlib.attach_spanner_stop(
            argument,
            stop_slur_,
        )
        wrappers.append(wrapper)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def spazzolato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-spazzolato-markup =|",
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def string_number(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    invisible_line: bool = False,
    left_broken: bool = False,
    rleak: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    assert isinstance(string_number, int), repr(string_number)
    assert string_number in (1, 2, 3, 4), repr(string_number)
    if string_number == 1:
        string_number_markup = r"\baca-string-i-markup"
        left_broken_text = r"\baca-parenthesized-string-i-markup"
    elif string_number == 2:
        string_number_markup = r"\baca-string-ii-markup"
        left_broken_text = r"\baca-parenthesized-string-ii-markup"
    elif string_number == 3:
        string_number_markup = r"\baca-string-iii-markup"
        left_broken_text = r"\baca-parenthesized-string-iii-markup"
    else:
        assert string_number == 4, repr(string_number)
        string_number_markup = r"\baca-string-iv-markup"
        left_broken_text = r"\baca-parenthesized-string-iv-markup"
    if invisible_line is True:
        descriptor = f"{string_number_markup} ||"
    else:
        descriptor = f"{string_number_markup} =|"
    specifiers = _textspannerlib.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def sustain_pedal(
    argument,
    *tweaks: abjad.Tweak,
    start_piano_pedal: abjad.StartPianoPedal = abjad.StartPianoPedal(),
    stop_piano_pedal: abjad.StopPianoPedal = abjad.StopPianoPedal(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_piano_pedal, abjad.StartPianoPedal), repr(start_piano_pedal)
    assert isinstance(stop_piano_pedal, abjad.StopPianoPedal), repr(stop_piano_pedal)
    wrappers = []
    if start_piano_pedal is not None:
        wrapper = _spannerlib.attach_spanner_start(
            argument,
            start_piano_pedal,
            *tweaks,
        )
        wrappers.append(wrapper)
    if stop_piano_pedal is not None:
        wrapper = _spannerlib.attach_spanner_stop(
            argument,
            stop_piano_pedal,
        )
        wrappers.append(wrapper)
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def tasto(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = "T =|",
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def trill(
    argument,
    *tweaks: abjad.Tweak,
    alteration: str | None = None,
    force_trill_pitch_head_accidental: bool = False,
    harmonic: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
    start_trill_span: abjad.StartTrillSpan = abjad.StartTrillSpan(),
    stop_trill_span: abjad.StopTrillSpan = abjad.StopTrillSpan(),
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def xfb(
    argument,
    *tweaks: abjad.Tweak,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if rleak is True:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers
