"""
Spanners.
"""

from inspect import currentframe as _frame

import abjad

from . import hairpinlib as _hairpinlib
from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import indicators as _indicators
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
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def hairpin(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
    debug=False,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
) -> list[abjad.Wrapper]:
    if rleak is True:
        argument = _select.rleak_next_nonobgc_leaf(argument)
    specifiers = _hairpinlib.parse_hairpin_descriptor(descriptor)
    start_dynamic, start_hairpin, stop_dynamic, stop_hairpin = None, None, None, None
    if len(specifiers) == 1:
        specifier = specifiers[0]
        start_dynamic = specifier.indicator
        start_hairpin = specifier.spanner_start
        stop_hairpin = specifier.spanner_stop
    elif len(specifiers) == 2:
        first, second = specifiers
        start_dynamic = first.indicator
        start_hairpin = first.spanner_start
        stop_dynamic = second.indicator
        stop_hairpin = second.spanner_stop
    else:
        raise NotImplementedError(descriptor)
    if start_dynamic is not None:
        assert _indicatorlib.is_maybe_bundled(start_dynamic, abjad.Dynamic), repr(
            start_dynamic
        )
        if left_broken is True:
            message = f"left-broken must begin with hairpin: {descriptor!r}"
            raise Exception(message)
    if start_hairpin is not None:
        assert _indicatorlib.is_maybe_bundled(start_hairpin, abjad.StartHairpin), repr(
            start_hairpin
        )
    if stop_dynamic is not None:
        assert isinstance(stop_dynamic, abjad.Dynamic), repr(stop_dynamic)
    if stop_hairpin is not None:
        assert isinstance(stop_hairpin, abjad.StopHairpin), repr(stop_hairpin)
    if right_broken is True:
        assert start_hairpin is not None, repr(start_hairpin)
        if not isinstance(stop_hairpin, abjad.StopHairpin):
            message = f"right-broken must have stop-hairpin: {descriptor!r}"
            raise Exception(message)
    wrappers = []
    first_leaf = abjad.select.leaf(argument, 0)
    final_leaf = abjad.select.leaf(argument, -1)
    if start_dynamic is not None:
        assert isinstance(start_dynamic, abjad.Dynamic), repr(start_dynamic)
        wrappers_ = _indicators.dynamic(
            first_leaf,
            start_dynamic,
        )
        wrappers.extend(wrappers_)
    if stop_dynamic is not None:
        wrappers_ = _indicators.dynamic(
            final_leaf,
            stop_dynamic,
        )
        wrappers.extend(wrappers_)
    if start_hairpin is not None:
        wrapper = _spannerlib.attach_spanner_start(
            argument,
            start_hairpin,
            *tweaks,
            left_broken=left_broken,
        )
        wrappers.append(wrapper)
    if stop_hairpin is not None:
        wrapper = _spannerlib.attach_spanner_stop(
            argument,
            stop_hairpin,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
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
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
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
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
