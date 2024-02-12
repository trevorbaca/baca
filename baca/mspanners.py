"""
Piecewise.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import piecewise as _piecewise
from . import spanners as _spanners
from . import tags as _tags
from . import typings as _typings


def bow_speed(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool | None = None,
    do_not_rleak: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert do_not_bookend is not False, repr(do_not_bookend)
    lilypond_id = "BowSpeed"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
        assert do_not_bookend is None, repr(do_not_bookend)
        if rleak is True:
            argument = _piecewise._rleak_next_nonobgc_leaf(argument)
        specifier = specifiers[0]
        wrappers = []
        wrapper = _spanners._attach_spanner_start(
            argument,
            specifier.spanner_start,
            *tweaks,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _spanners._attach_spanner_stop(
            argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        if do_not_bookend is None:
            do_not_bookend = False
        if rleak is True:
            argument[-1] = _piecewise._rleak_next_nonobgc_leaf(argument[-1])
        wrappers = _piecewise._iterate_pieces(
            argument,
            *tweaks,
            do_not_bookend=do_not_bookend,
            left_broken=left_broken,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def circle_bow(
    argument,
    *tweaks: _typings.IndexedTweak,
    left_broken: bool = False,
    left_broken_text: str | None = r"\baca-left-broken-circle-bowing-markup",
    qualifier: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if qualifier is None:
        descriptor = r"\baca-circle-markup =|"
    else:
        assert isinstance(qualifier, str), repr(qualifier)
        descriptor = rf"\baca-circle-{qualifier}-markup =|"
    lilypond_id = "CircleBow"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
        if rleak is True:
            argument = _piecewise._rleak_next_nonobgc_leaf(argument)
        specifier = specifiers[0]
        wrappers = []
        wrapper = _spanners._attach_spanner_start(
            argument,
            specifier.spanner_start,
            *tweaks,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _spanners._attach_spanner_stop(
            argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        if rleak is True:
            argument[-1] = _piecewise._rleak_next_nonobgc_leaf(argument[-1])
        wrappers = _piecewise._iterate_pieces(
            argument,
            *tweaks,
            left_broken=left_broken,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def scp(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool | None = None,
    bound_details_right_padding: int | float | None = None,
    do_not_rleak: bool = False,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert do_not_bookend is not False, repr(do_not_bookend)
    lilypond_id = "SCP"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
        assert do_not_bookend is None, repr(do_not_bookend)
        if rleak is True:
            argument = _piecewise._rleak_next_nonobgc_leaf(argument)
        specifier = specifiers[0]
        wrappers = []
        wrapper = _spanners._attach_spanner_start(
            argument,
            specifier.spanner_start,
            *tweaks,
            bound_details_right_padding=bound_details_right_padding,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _spanners._attach_spanner_stop(
            argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        if do_not_bookend is None:
            do_not_bookend = False
        if rleak is True:
            argument[-1] = _piecewise._rleak_next_nonobgc_leaf(argument[-1])
        wrappers = _piecewise._iterate_pieces(
            argument,
            *tweaks,
            do_not_bookend=do_not_bookend,
            bound_details_right_padding=bound_details_right_padding,
            left_broken=left_broken,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def text(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool | None = None,
    debug: bool = False,
    direction: int | None = None,
    do_not_rleak: bool = False,
    do_not_start_spanner_on_final_piece: bool = False,
    leak_spanner_stop: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    lilypond_id: int | str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert isinstance(descriptor, str), repr(descriptor)
    assert do_not_bookend is not False, repr(do_not_bookend)
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        direction=direction,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if debug is True:
        breakpoint()
    if len(specifiers) == 1:
        assert do_not_bookend is None, repr(do_not_bookend)
        if rleak is True:
            argument = _piecewise._rleak_next_nonobgc_leaf(argument)
        specifier = specifiers[0]
        wrappers = []
        wrapper = _spanners._attach_spanner_start(
            argument,
            specifier.spanner_start,
            *tweaks,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _spanners._attach_spanner_stop(
            argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        if do_not_bookend is None:
            do_not_bookend = False
        if rleak is True:
            argument[-1] = _piecewise._rleak_next_nonobgc_leaf(argument[-1])
        wrappers = _piecewise._iterate_pieces(
            argument,
            *tweaks,
            do_not_bookend=do_not_bookend,
            do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
            leak_spanner_stop=leak_spanner_stop,
            left_broken=left_broken,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers


def vibrato(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool | None = None,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    rleak: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    assert do_not_bookend is not False, repr(do_not_bookend)
    lilypond_id = "Vibrato"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
        assert do_not_bookend is None, repr(do_not_bookend)
        if rleak is True:
            argument = _piecewise._rleak_next_nonobgc_leaf(argument)
        specifier = specifiers[0]
        wrappers = []
        wrapper = _spanners._attach_spanner_start(
            argument,
            specifier.spanner_start,
            *tweaks,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _spanners._attach_spanner_stop(
            argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        if do_not_bookend is None:
            do_not_bookend = False
        if rleak is True:
            argument[-1] = _piecewise._rleak_next_nonobgc_leaf(argument[-1])
        wrappers = _piecewise._iterate_pieces(
            argument,
            *tweaks,
            do_not_bookend=do_not_bookend,
            left_broken=left_broken,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
