"""
indicatorlib.py.
"""

import typing
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import tags as _tags
from . import treat as _treat


def attach_persistent_indicator(
    leaf: abjad.Leaf,
    indicator: typing.Any,
    *,
    context: str | None = None,
    deactivate: bool = False,
    direction: abjad.Vertical | None = None,
    left_broken: bool = False,
    manifests: dict | None = None,
    right_broken: bool = False,
    tag: abjad.Tag | None = None,
) -> abjad.wrapper.Wrapper:
    unbundled_indicator = unbundle_indicator(indicator)
    assert unbundled_indicator.persistent is True, repr(indicator)
    if context is not None:
        assert isinstance(context, str), repr(context)
    assert isinstance(deactivate, bool), repr(deactivate)
    manifests = manifests or {}
    assert isinstance(manifests, dict), repr(manifests)
    tag = tag or abjad.Tag()
    tag = tag.append(_helpers.function_name(_frame()))
    if getattr(unbundled_indicator, "spanner_start", False) is True:
        tag = tag.append(_tags.SPANNER_START)
    if getattr(unbundled_indicator, "spanner_stop", False) is True:
        tag = tag.append(_tags.SPANNER_STOP)
    if left_broken is True:
        tag = tag.append(_tags.LEFT_BROKEN)
    if right_broken is True:
        tag = tag.append(_tags.RIGHT_BROKEN)
    reapplied_indicator = _treat.remove_reapplied_wrappers(leaf, indicator)
    assert not isinstance(reapplied_indicator, abjad.wrapper.Wrapper)
    abjad.attach(
        indicator,
        leaf,
        context=context,
        deactivate=deactivate,
        direction=direction,
        tag=tag,
    )
    retrieved_wrappers = abjad.get.wrappers(leaf, unbundled_indicator)
    wrapper = retrieved_wrappers[-1]
    if _treat.compare_persistent_indicators(indicator, reapplied_indicator):
        result = _treat.treat_persistent_wrapper(manifests, wrapper, "redundant")
        if result is not None:
            assert isinstance(result, abjad.wrapper.Wrapper)
            wrapper = result
    return wrapper


def is_maybe_bundled(argument, prototype):
    if isinstance(argument, prototype):
        return True
    if isinstance(argument, abjad.Bundle):
        if isinstance(argument.indicator, prototype):
            return True
    return False


def unbundle_indicator(argument):
    if isinstance(argument, abjad.Bundle):
        return argument.indicator
    return argument
