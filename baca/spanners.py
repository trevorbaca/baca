"""
Spanners.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import indicators as _indicators
from . import piecewise as _piecewise
from . import select as _select
from . import tags as _tags
from . import tweaks as _tweaks
from . import typings as _typings


def _attach_spanner_start(
    argument,
    spanner_start,
    *tweaks: _typings.IndexedTweak,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    staff_padding: int | float | None = None,
) -> abjad.Wrapper:
    unbundled_indicator = _indicators._unbundle_indicator(spanner_start)
    assert unbundled_indicator.spanner_start is True
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    spanner_start = _tweaks.bundle_tweaks(spanner_start, tweaks)
    tag = _helpers.function_name(_frame())
    # TODO: maybe move into _indicators._attach_persistent_indicator()?
    tag = tag.append(_tags.SPANNER_START)
    if left_broken:
        tag = tag.append(_tags.LEFT_BROKEN)
    first_leaf = abjad.select.leaf(argument, 0)
    return _indicators._attach_persistent_indicator(
        first_leaf,
        spanner_start,
        direction=direction,
        tag=tag,
    )


def _attach_spanner_stop(
    argument,
    spanner_stop,
    *,
    right_broken: bool = False,
) -> abjad.Wrapper:
    assert spanner_stop.spanner_stop is True, repr(spanner_stop)
    tag = _helpers.function_name(_frame())
    # TODO: maybe move into _indicators._attach_persistent_indicator()?
    tag = tag.append(_tags.SPANNER_STOP)
    if right_broken:
        tag = tag.append(_tags.RIGHT_BROKEN)
    final_leaf = abjad.select.leaf(argument, -1)
    return _indicators._attach_persistent_indicator(
        final_leaf,
        spanner_stop,
        tag=tag,
    )


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
    wrappers = []
    if start_beam is not None:
        wrapper = _attach_spanner_start(
            argument,
            start_beam,
            *tweaks,
            direction=direction,
        )
        wrappers.append(wrapper)
    if stop_beam is not None:
        wrapper = _attach_spanner_stop(
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
        if isinstance(second.indicator, abjad.Dynamic):
            stop_dynamic = second.indicator
        else:
            assert isinstance(second.indicator, abjad.StopHairpin)
            stop_hairpin = second.indicator
        if second.spanner_start:
            raise Exception(descriptor)
        if second.spanner_stop:
            raise Exception(descriptor)
    else:
        raise NotImplementedError(descriptor)
    if start_dynamic is not None:
        assert _indicators._is_maybe_bundled(start_dynamic, abjad.Dynamic), repr(
            start_dynamic
        )
        if left_broken is True:
            message = f"left-broken must begin with hairpin: {descriptor!r}"
            raise Exception(message)
    if start_hairpin is not None:
        assert _indicators._is_maybe_bundled(start_hairpin, abjad.StartHairpin), repr(
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
        wrapper = _attach_spanner_start(
            argument,
            start_hairpin,
            *tweaks,
            left_broken=left_broken,
        )
        wrappers.append(wrapper)
    if stop_hairpin is not None:
        wrapper = _attach_spanner_stop(
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
        wrapper = _attach_spanner_start(
            argument,
            start_slur_,
            *tweaks,
        )
        wrappers.append(wrapper)
    if stop_slur_ is not None:
        wrapper = _attach_spanner_stop(
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
        wrapper = _attach_spanner_start(
            argument,
            start_piano_pedal,
            *tweaks,
        )
        wrappers.append(wrapper)
    if stop_piano_pedal is not None:
        wrapper = _attach_spanner_stop(
            argument,
            stop_piano_pedal,
        )
        wrappers.append(wrapper)
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
