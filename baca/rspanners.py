"""
Spanners.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import indicators as _indicators
from . import select as _select
from . import spannerlib as _spannerlib
from . import tags as _tags
from . import textspannerlib as _textspannerlib


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
    _tags.tag(wrappers, tag)
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def pizzicato(
    argument,
    *tweaks: abjad.Tweak,
    descriptor: str = r"\baca-pizz-markup =|",
    do_not_rleak: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    left_broken_text: str = r"\baca-parenthesized-pizz-markup",
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if do_not_rleak is False:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers


def string_number(
    argument,
    string_number: int,
    *tweaks: abjad.Tweak,
    invisible_line: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
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
    _tags.tag(wrappers, _helpers.function_name(_frame()))
    return wrappers
