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
    bookend: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    lilypond_id = "BowSpeed"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
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
        wrappers = _piecewise._iterate_pieces(
            (),
            *tweaks,
            bookend=bookend,
            left_broken=left_broken,
            pieces=argument,
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
        wrappers = _piecewise._iterate_pieces(
            (),
            *tweaks,
            left_broken=left_broken,
            pieces=argument,
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
    bookend: bool = False,
    bound_details_right_padding: int | float | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    lilypond_id = "SCP"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
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
        wrappers = _piecewise._iterate_pieces(
            (),
            *tweaks,
            bookend=bookend,
            bound_details_right_padding=bound_details_right_padding,
            left_broken=left_broken,
            pieces=argument,
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
    bookend: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    lilypond_id = "Vibrato"
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
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
        wrappers = _piecewise._iterate_pieces(
            (),
            *tweaks,
            bookend=bookend,
            left_broken=left_broken,
            pieces=argument,
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
    bookend: bool = True,
    direction: int | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    leak_spanner_stop: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    lilypond_id: int | str | None = None,
    pieces: list[list[abjad.Leaf]] | None = None,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    if not argument:
        assert pieces, repr(pieces)
        the_argument = pieces
    if not pieces:
        assert argument, repr(argument)
        the_argument = argument
    assert isinstance(descriptor, str), repr(descriptor)
    specifiers = _piecewise.parse_text_spanner_descriptor(
        descriptor,
        direction=direction,
        left_broken_text=left_broken_text,
        lilypond_id=lilypond_id,
    )
    if len(specifiers) == 1:
        specifier = specifiers[0]
        wrappers = []
        wrapper = _spanners._attach_spanner_start(
            the_argument,
            specifier.spanner_start,
            *tweaks,
            left_broken=left_broken,
            staff_padding=staff_padding,
        )
        wrappers.append(wrapper)
        wrapper = _spanners._attach_spanner_stop(
            the_argument,
            specifier.spanner_stop,
            right_broken=right_broken,
        )
        wrappers.append(wrapper)
    else:
        wrappers = _piecewise._iterate_pieces(
            argument,
            *tweaks,
            bookend=bookend,
            do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
            leak_spanner_stop=leak_spanner_stop,
            left_broken=left_broken,
            pieces=pieces,
            right_broken=right_broken,
            specifiers=specifiers,
            staff_padding=staff_padding,
        )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
