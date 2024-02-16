"""
Piecewise.
"""

from inspect import currentframe as _frame

import abjad

from . import hairpinlib as _hairpinlib
from . import helpers as _helpers
from . import spanners as _spanners
from . import tags as _tags
from . import typings as _typings


def hairpin(
    argument,
    descriptor: str,
    *tweaks: _typings.IndexedTweak,
    debug: bool = False,
    cyclic: bool = False,
    do_not_bookend: bool | None = None,
    do_not_start_spanner_on_final_piece: bool = False,
    glue: bool = False,
    left_broken: bool = False,
    match: bool = False,
    # match: bool = True,
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
    specifiers = _hairpinlib.parse_hairpin_descriptor(descriptor)
    if rleak is True:
        argument[-1] = _spanners.rleak_next_nonobgc_leaf(argument[-1])
    if do_not_bookend is None:
        do_not_bookend = False
    if cyclic is False and match is True and len(specifiers) != len(argument):
        message = f"\n{len(specifiers)} specifiers ...."
        for specifier in specifiers:
            message += "\n\t" + str(specifier)
        message += f"\n{len(argument)} argument pieces ..."
        for piece in argument:
            message += "\n\t" + str(piece)
        raise Exception(message)
    wrappers = _hairpinlib.iterate_hairpin_pieces(
        argument,
        *tweaks,
        cyclic=cyclic,
        debug=debug,
        do_not_bookend=do_not_bookend,
        do_not_start_spanner_on_final_piece=do_not_start_spanner_on_final_piece,
        glue=glue,
        left_broken=left_broken,
        right_broken=right_broken,
        specifiers=specifiers,
    )
    _tags.wrappers(wrappers, _helpers.function_name(_frame()))
    return wrappers
