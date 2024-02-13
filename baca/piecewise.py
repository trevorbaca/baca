"""
Piecewise.
"""

from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import spannerlib as _spannerlib
from . import spanners as _spanners
from . import tags as _tags
from . import typings as _typings


def hairpin(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    do_not_bookend: bool | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    forbid_al_niente_to_bar_line: bool = False,
    left_broken: bool = False,
    right_broken: bool = False,
    rleak: bool = False,
) -> list[abjad.Wrapper]:
    assert isinstance(descriptor, str), repr(descriptor)
    assert do_not_bookend is not False, repr(do_not_bookend)
    assert isinstance(do_not_start_spanner_on_final_piece, bool)
    assert isinstance(left_broken, bool), repr(left_broken)
    assert isinstance(right_broken, bool), repr(right_broken)
    if left_broken is True:
        assert descriptor[0] in ("o", "<", ">"), repr(descriptor)
    if right_broken is True:
        assert descriptor[-1] == "!", repr(descriptor)
    specifiers = _spannerlib.parse_hairpin_descriptor(
        descriptor,
        forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
    )
    if rleak is True:
        argument[-1] = _spanners.rleak_next_nonobgc_leaf(argument[-1])
    if do_not_bookend is None:
        do_not_bookend = False
    wrappers = _spannerlib.iterate_pieces(
        argument,
        *tweaks,
        attach_stop_hairpin_on_right_broken_final_piece=True,
        do_not_bookend=do_not_bookend,
        do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
        left_broken=left_broken,
        right_broken=right_broken,
        specifiers=specifiers,
    )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
