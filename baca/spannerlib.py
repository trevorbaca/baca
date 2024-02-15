"""
spannerlib.py.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import indicatorlib as _indicatorlib
from . import tags as _tags
from . import tweaks as _tweaks
from . import typings as _typings


def attach_spanner_start(
    argument,
    spanner_start,
    *tweaks: _typings.IndexedTweak,
    bound_details_right_padding: int | float | None = None,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    staff_padding: int | float | None = None,
) -> abjad.Wrapper:
    unbundled_indicator = _indicatorlib.unbundle_indicator(spanner_start)
    assert unbundled_indicator.spanner_start is True
    if bound_details_right_padding is not None:
        string = rf"- \tweak bound-details.right.padding {bound_details_right_padding}"
        tweaks = tweaks + (abjad.Tweak(string),)
    if staff_padding is not None:
        tweaks = tweaks + (abjad.Tweak(rf"- \tweak staff-padding {staff_padding}"),)
    spanner_start = _tweaks.bundle_tweaks(spanner_start, tweaks)
    first_leaf = abjad.select.leaf(argument, 0)
    wrapper = _indicatorlib.attach_persistent_indicator(
        first_leaf,
        spanner_start,
        direction=direction,
    )
    tag = _helpers.function_name(_frame())
    if left_broken:
        tag = tag.append(_tags.LEFT_BROKEN)
    _tags.wrappers([wrapper], tag)
    return wrapper


def attach_spanner_stop(
    argument,
    spanner_stop,
    *,
    right_broken: bool = False,
) -> abjad.Wrapper:
    assert spanner_stop.spanner_stop is True, repr(spanner_stop)
    final_leaf = abjad.select.leaf(argument, -1)
    wrapper = _indicatorlib.attach_persistent_indicator(
        final_leaf,
        spanner_stop,
    )
    tag = _helpers.function_name(_frame())
    if right_broken:
        tag = tag.append(_tags.RIGHT_BROKEN)
    _tags.wrappers([wrapper], tag)
    return wrapper
