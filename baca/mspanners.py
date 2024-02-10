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
