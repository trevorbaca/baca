"""
Spanners.
"""

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
    context: str | None = None,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    wrappers = []
    if start_indicator is not None:
        unbundled_indicator = _piecewise._unbundle_indicator(start_indicator)
        start_indicator = _tweaks.bundle_tweaks(start_indicator, tweaks)
        tag = _helpers.function_name(_frame(), n=1)
        if getattr(unbundled_indicator, "spanner_stop", False) is True:
            tag = tag.append(_tags.SPANNER_STOP)
        else:
            assert getattr(unbundled_indicator, "spanner_start", False) is True
            tag = tag.append(_tags.SPANNER_START)
        if left_broken:
            tag = tag.append(_tags.LEFT_BROKEN)
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
        assert stop_indicator.spanner_stop is True, repr(stop_indicator)
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
    return wrappers


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


def hairpin(
    argument,
    descriptor: str,
    *tweaks: abjad.Tweak,
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
    start_dynamic, start_hairpin, stop_indicator = None, None, None
    if len(specifiers) == 1:
        specifier = specifiers[0]
        start_dynamic = specifier.indicator
        start_hairpin = specifier.spanner_start
    elif len(specifiers) == 2:
        first, second = specifiers
        start_dynamic = first.indicator
        start_hairpin = first.spanner_start
        stop_indicator = second.indicator
        if second.spanner_start:
            raise Exception(descriptor)
        if second.spanner_stop:
            raise Exception(descriptor)
    else:
        raise NotImplementedError(descriptor)
    if start_dynamic is not None:
        assert _piecewise._is_maybe_bundled(start_dynamic, abjad.Dynamic), repr(
            start_dynamic
        )
    if start_hairpin is not None:
        assert _piecewise._is_maybe_bundled(start_hairpin, abjad.StartHairpin), repr(
            start_hairpin
        )
    if stop_indicator is not None:
        assert _piecewise._is_maybe_bundled(
            stop_indicator, abjad.Dynamic | abjad.StopHairpin
        ), repr(stop_indicator)
    if right_broken is True:
        assert start_hairpin is not None, repr(start_hairpin)
        assert stop_indicator is None, repr(stop_indicator)
        stop_indicator = abjad.StopHairpin()
    if start_dynamic is not None:
        wrappers_ = _attach_spanner_indicators(
            argument,
            start_dynamic,
            left_broken=left_broken,
            right_broken=right_broken,
        )
        wrappers.extend(wrappers_)
    wrappers_ = _attach_spanner_indicators(
        argument,
        start_hairpin,
        stop_indicator,
        *tweaks,
        left_broken=left_broken,
        right_broken=right_broken,
    )
    wrappers.extend(wrappers_)
    tag = _helpers.function_name(_frame())
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
