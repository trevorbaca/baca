"""
Spanners.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
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
