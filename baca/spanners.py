"""
Spanners.
"""

import dataclasses
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import select as _select
from . import spannerlib as _spannerlib
from . import tags as _tags


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
