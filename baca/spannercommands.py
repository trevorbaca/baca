"""
Spanners.
"""
import dataclasses
from inspect import currentframe as _frame

import abjad

from . import tags as _tags
from . import tweaks as _tweaks


def _do_spanner_indicator_command(
    argument,
    start_indicator,
    stop_indicator,
    *tweaks,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
) -> list[abjad.Wrapper]:
    wrappers = []
    if start_indicator is not None:
        start_indicator = _tweaks.bundle_tweaks(start_indicator, tweaks)
        tag = _tags.function_name(_frame(), n=1)
        tag = tag.append(_tags.SPANNER_START)
        if left_broken:
            tag = tag.append(_tags.LEFT_BROKEN)
        first_leaf = abjad.select.leaf(argument, 0)
        wrapper = abjad.attach(
            start_indicator,
            first_leaf,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    if stop_indicator is not None:
        tag = _tags.function_name(_frame(), n=2)
        tag = tag.append(_tags.SPANNER_STOP)
        if right_broken:
            tag = tag.append(_tags.RIGHT_BROKEN)
        final_leaf = abjad.select.leaf(argument, -1)
        wrapper = abjad.attach(
            stop_indicator,
            final_leaf,
            direction=direction,
            tag=tag,
            wrapper=True,
        )
        wrappers.append(wrapper)
    return wrappers


def _prepare_start_trill_span(
    *,
    alteration,
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
    start_trill_span_: abjad.StartTrillSpan | abjad.Bundle
    start_trill_span_ = start_trill_span
    if pitch is not None or interval is not None:
        start_trill_span_ = dataclasses.replace(
            start_trill_span_, interval=interval, pitch=pitch
        )
    if harmonic is True:
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        string = rf"- \tweak TrillPitchHead.stencil {string}"
        start_trill_span_ = abjad.bundle(start_trill_span_, string)
    return start_trill_span_


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
    wrappers = _do_spanner_indicator_command(
        argument,
        start_beam,
        stop_beam,
        *tweaks,
        direction=direction,
    )
    tag = _tags.function_name(_frame())
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
    return _do_spanner_indicator_command(
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
    wrappers = _do_spanner_indicator_command(
        argument,
        start_ottava,
        stop_ottava,
        right_broken=right_broken,
    )
    tag = _tags.function_name(_frame())
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
    wrappers = _do_spanner_indicator_command(
        argument,
        start_slur_,
        stop_slur_,
        *tweaks,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def sustain_pedal(
    argument,
    *,
    start_piano_pedal: abjad.StartPianoPedal = abjad.StartPianoPedal(),
    stop_piano_pedal: abjad.StopPianoPedal = abjad.StopPianoPedal(),
) -> list[abjad.Wrapper]:
    assert isinstance(start_piano_pedal, abjad.StartPianoPedal), repr(start_piano_pedal)
    assert isinstance(stop_piano_pedal, abjad.StopPianoPedal), repr(stop_piano_pedal)
    wrappers = _do_spanner_indicator_command(
        argument,
        start_piano_pedal,
        stop_piano_pedal,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers


def trill_spanner(
    argument,
    *tweaks: abjad.Tweak,
    alteration: str | None = None,
    harmonic: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    start_trill_span: abjad.StartTrillSpan = abjad.StartTrillSpan(),
    stop_trill_span: abjad.StopTrillSpan = abjad.StopTrillSpan(),
) -> list[abjad.Wrapper]:
    start_trill_span_ = _prepare_start_trill_span(
        alteration=alteration,
        harmonic=harmonic,
        start_trill_span=start_trill_span,
    )
    wrappers = _do_spanner_indicator_command(
        argument,
        start_trill_span_,
        stop_trill_span,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
    )
    tag = _tags.function_name(_frame())
    _tags.wrappers(wrappers, tag)
    return wrappers
