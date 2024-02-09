"""
Piecewise.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import piecewise as _piecewise
from . import tags as _tags
from . import typings as _typings


def bow_speed(
    argument,
    items: str | list,
    *tweaks: _typings.IndexedTweak,
    bookend: bool = False,
    left_broken: bool = False,
    left_broken_text: str | None = None,
    right_broken: bool = False,
    staff_padding: int | float | None = None,
) -> list[abjad.Wrapper]:
    tag = _helpers.function_name(_frame())
    tag = tag.append(_tags.BOW_SPEED_SPANNER)
    wrappers = _piecewise.text(
        argument,
        items,
        *tweaks,
        bookend=bookend,
        iterate_argument_when_multiple_specifiers=True,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="BowSpeed",
        right_broken=right_broken,
        staff_padding=staff_padding,
    )
    _tags.wrappers(wrappers, tag)
    return wrappers
