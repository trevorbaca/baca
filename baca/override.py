"""
Overrides.
"""
from inspect import currentframe as _frame

import abjad

from . import helpers as _helpers
from . import tags as _tags


def _do_override_command(
    leaves,
    grob,
    attribute,
    value,
    first_tag,
    final_tag,
    *,
    after=False,
    allowlist=None,
    blocklist=None,
    context=None,
    deactivate=False,
) -> list[abjad.Wrapper]:
    if blocklist:
        for leaf in leaves:
            if isinstance(leaf, blocklist):
                raise Exception(f"{type(leaf).__name__} is forbidden.")
    if allowlist:
        for leaf in leaves:
            if not isinstance(leaf, allowlist):
                names = ",".join(_.__name__ for _ in allowlist)
                violator = type(leaf).__name__
                raise Exception(f"only {names} (not {violator}) allowed.")
    lilypond_type = context
    if lilypond_type is not None:
        assert isinstance(lilypond_type, str), repr(lilypond_type)
    if lilypond_type in dir(abjad):
        context = getattr(abjad, lilypond_type)
        assert issubclass(context, abjad.Context), repr(context)
        context = abjad.get.parentage(leaves[0]).get(context) or context()
        lilypond_type = context.lilypond_type
        assert isinstance(lilypond_type, str), repr(lilypond_type)
    assert isinstance(grob, str)
    assert isinstance(attribute, str)
    once = bool(len(leaves) == 1)
    override = abjad.LilyPondOverride(
        lilypond_type=lilypond_type,
        grob_name=grob,
        once=once,
        property_path=attribute,
        value=value,
    )
    string = override.override_string
    site = "before"
    if after is True:
        site = "after"
    literal = abjad.LilyPondLiteral(string, site=site)
    wrapper_1 = abjad.attach(
        literal, leaves[0], deactivate=deactivate, tag=first_tag, wrapper=True
    )
    if once:
        return [wrapper_1]
    override = abjad.LilyPondOverride(
        lilypond_type=lilypond_type,
        grob_name=grob,
        is_revert=True,
        property_path=attribute,
    )
    string = override.revert_string
    literal = abjad.LilyPondLiteral(string, site="after")
    wrapper_2 = abjad.attach(
        literal, leaves[-1], deactivate=deactivate, tag=final_tag, wrapper=True
    )
    return [wrapper_1, wrapper_2]


def _do_override(
    frame,
    argument,
    grob,
    attribute,
    value,
    *,
    after=False,
    context=None,
) -> list[abjad.Wrapper]:
    leaves = abjad.select.leaves(argument)
    first_tag = _helpers.function_name(frame, n=1)
    final_tag = _helpers.function_name(frame, n=2)
    return _do_override_command(
        leaves,
        grob,
        attribute,
        value,
        first_tag,
        final_tag,
        after=after,
        context=context,
    )


def accidental_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="extra_offset",
        grob="Accidental",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def accidental_font_size(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="font_size",
        grob="Accidental",
        value=n,
    )


def accidental_outside_staff_priority(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Accidental",
        attribute="outside_staff_priority",
        value=n,
    )


def accidental_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="stencil",
        grob="Accidental",
        value=False,
    )


def accidental_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="transparent",
        value=True,
        grob="Accidental",
    )


def accidental_x_extent_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="X_extent",
        grob="Accidental",
        value=False,
    )


def accidental_x_offset(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="X_offset",
        grob="Accidental",
        value=n,
    )


def accidental_y_offset(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="Y_offset",
        grob="Accidental",
        value=n,
    )


def bar_line_color(
    argument, color: str, *, after: bool = False, context: str = "Score"
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="BarLine",
        attribute="color",
        value=color,
        after=after,
        context=context,
    )


def bar_line_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="BarLine",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        after=after,
        context=context,
    )


def bar_line_hair_thickness(
    argument, number: int | float, *, after: bool = False, context: str = "Score"
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="BarLine",
        attribute="hair_thickness",
        value=number,
        after=after,
        context=context,
    )


def bar_line_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "BarLine",
        "transparent",
        True,
        context="Score",
    )


def bar_line_x_extent(
    leaves,
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    # TODO: use _do_override()
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    first_tag = _helpers.function_name(_frame(), n=1)
    final_tag = _helpers.function_name(_frame(), n=2)
    return _do_override_command(
        leaves,
        "BarLine",
        "X_extent",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
        after=after,
        allowlist=None,
        blocklist=None,
        context=context,
        deactivate=False,
    )


def beam_positions(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Beam",
        "positions",
        f"#'({n} . {n})",
    )


def beam_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Beam",
        attribute="stencil",
        value=False,
    )


def beam_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Beam",
        attribute="transparent",
        value=True,
    )


def clef_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Clef",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        context="Staff",
    )


def clef_shift(
    argument,
    clef: str | abjad.Clef,
    first_measure_number: int,
) -> list[abjad.Wrapper]:
    leaf = abjad.select.leaf(argument, 0)
    measure_number = abjad.get.measure_number(leaf)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    wrappers = []
    wrappers_ = clef_x_extent_false(argument)
    _tags.wrappers(wrappers_, _tags.SHIFTED_CLEF, measure_number_tag)
    wrappers.extend(wrappers_)
    extra_offset_x: int | float
    if isinstance(clef, str):
        clef = abjad.Clef(clef)
    if isinstance(clef, int | float):
        extra_offset_x = clef
    else:
        assert isinstance(clef, abjad.Clef)
        width = clef._to_width[clef.name]
        extra_offset_x = -width
    pair = (extra_offset_x, 0)
    wrappers_ = clef_extra_offset(argument, pair)
    _tags.wrappers(wrappers_, _tags.SHIFTED_CLEF, measure_number_tag)
    wrappers.extend(wrappers_)
    return wrappers


def clef_whiteout(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Clef",
        attribute="whiteout",
        value=n,
        context="Staff",
    )


def clef_x_extent_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Clef",
        "X_extent",
        False,
        context="Staff",
    )


def dls_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "DynamicLineSpanner",
        "padding",
        n,
    )


def dls_staff_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "DynamicLineSpanner",
        "staff_padding",
        n,
    )


def dls_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicLineSpanner",
        attribute="direction",
        value=abjad.UP,
    )


def dots_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Dots",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def dots_font_size(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Dots",
        attribute="font_size",
        value=n,
    )


def dots_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Dots",
        attribute="stencil",
        value=False,
    )


def dots_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Dots",
        attribute="transparent",
        value=True,
    )


def dots_x_extent_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Dots",
        attribute="X_extent",
        value=False,
    )


def dynamic_text_color(argument, color: str = "#red") -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicText",
        attribute="color",
        value=color,
    )


def dynamic_text_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "DynamicText",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
    )


def dynamic_text_parent_alignment_x(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicText",
        attribute="parent_alignment_X",
        value=n,
    )


def dynamic_text_self_alignment_x(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "DynamicText",
        "self_alignment_X",
        n,
    )


def dynamic_text_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicText",
        attribute="stencil",
        value=False,
    )


def dynamic_text_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicText",
        attribute="transparent",
        value=True,
    )


def dynamic_text_x_extent_zero(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "DynamicText",
        "X_extent",
        (0, 0),
    )


def dynamic_text_x_offset(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicText",
        attribute="X_offset",
        value=n,
    )


def dynamic_text_y_offset(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="DynamicText",
        attribute="Y_offset",
        value=n,
    )


def flag_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Flag",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def flag_font_size(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="font_size",
        grob="Flag",
        value=n,
    )


def flag_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Flag",
        attribute="stencil",
        value=False,
    )


def flag_stencil(argument, stencil: str) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Flag",
        attribute="stencil",
        value=stencil,
    )


def flag_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Flag",
        attribute="transparent",
        value=True,
    )


def glissando_thickness(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Glissando",
        attribute="thickness",
        value=str(n),
    )


def hairpin_shorten_pair(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Hairpin",
        "shorten_pair",
        f"#'({pair[0]} . {pair[1]})",
    )


def hairpin_start_shift(argument, dynamic: str | abjad.Dynamic) -> list[abjad.Wrapper]:
    wrappers = []
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[str(dynamic.name)]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    wrappers_ = dynamic_text_extra_offset(argument, (extra_offset_x, 0))
    wrappers.extend(wrappers_)
    wrappers_ = dynamic_text_x_extent_zero(argument)
    wrappers.extend(wrappers_)
    wrappers_ = hairpin_shorten_pair(argument, (hairpin_shorten_left, 0))
    wrappers.extend(wrappers_)
    return wrappers


def hairpin_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Hairpin",
        attribute="stencil",
        value=False,
    )


def hairpin_to_barline(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Hairpin",
        "to_barline",
        True,
    )


def hairpin_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Hairpin",
        attribute="transparent",
        value=True,
    )


def laissez_vibrer_tie_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="LaissezVibrerTie",
        attribute="direction",
        value=abjad.DOWN,
    )


def laissez_vibrer_tie_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="LaissezVibrerTie",
        attribute="direction",
        value=abjad.UP,
    )


def mmrest_color(argument, color: str = "#red") -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="MultiMeasureRest",
        attribute="color",
        value=color,
    )


def mmrest_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "MultiMeasureRest",
        "transparent",
        True,
    )


def mmrest_text_color(argument, color: str = "#red") -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="MultiMeasureRestText",
        attribute="color",
        value=color,
    )


def mmrest_text_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "MultiMeasureRestText",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
    )


def mmrest_text_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="MultiMeasureRestText",
        attribute="padding",
        value=n,
    )


def mmrest_text_parent_center(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="MultiMeasureRestText",
        attribute="parent_alignment_X",
        value=0,
    )


def mmrest_text_staff_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="MultiMeasureRestText",
        attribute="staff_padding",
        value=n,
    )


def mmrest_text_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="MultiMeasureRestText",
        attribute="transparent",
        value=True,
    )


def note_column_shift(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteColumn",
        attribute="force_hshift",
        value=n,
    )


def note_head_color(argument, color: str) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="color",
        value=color,
    )


def note_head_duration_log(argument, n: int) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "NoteHead",
        "duration_log",
        n,
    )


def note_head_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def note_head_font_size(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="font_size",
        value=n,
    )


def note_head_no_ledgers(argument, value: bool) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "NoteHead",
        "no_ledgers",
        value,
    )


def note_head_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="stencil",
        value=False,
    )


def note_head_style(argument, string: str) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "NoteHead",
        "style",
        string,
    )


def note_head_style_cross(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "NoteHead",
        "style",
        "#'cross",
    )


def note_head_style_harmonic(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "NoteHead",
        "style",
        "#'harmonic",
    )


def note_head_style_harmonic_black(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="style",
        value="#'harmonic-black",
    )


def note_head_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="transparent",
        value=True,
    )


def note_head_transparent_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="transparent",
        value=False,
    )


def note_head_x_extent_zero(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="NoteHead",
        attribute="X_extent",
        value=(0, 0),
    )


def ottava_bracket_shorten_pair(
    argument, pair: tuple[int | float, int | float] = (-0.8, -0.6)
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="OttavaBracket",
        attribute="shorten_pair",
        value=f"#'({pair[0]} . {pair[1]})",
        context="Staff",
    )


def ottava_bracket_staff_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "OttavaBracket",
        "staff_padding",
        n,
        context="Staff",
    )


def parentheses_font_size(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="font_size",
        grob="Parentheses",
        value=n,
    )


def rehearsal_mark_down(
    argument,
    *,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "RehearsalMark",
        "direction",
        abjad.DOWN,
        context=context,
    )


def rehearsal_mark_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
    *,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "RehearsalMark",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        context=context,
    )


def rehearsal_mark_padding(
    argument,
    n: int | float,
    *,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "RehearsalMark",
        "padding",
        n,
        context=context,
    )


def rehearsal_mark_self_alignment_x(
    argument,
    n: int,
    *,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "RehearsalMark",
        "self_alignment_X",
        n,
        context=context,
    )


def rehearsal_mark_y_offset(
    argument,
    n: int | float,
    *,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="RehearsalMark",
        attribute="Y_offset",
        value=n,
        context=context,
    )


def repeat_tie_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="RepeatTie",
        attribute="direction",
        value=abjad.DOWN,
    )


def repeat_tie_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "RepeatTie",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
    )


def repeat_tie_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="RepeatTie",
        attribute="stencil",
        value=False,
    )


def repeat_tie_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="RepeatTie",
        attribute="transparent",
        value=True,
    )


def repeat_tie_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="RepeatTie",
        attribute="direction",
        value=abjad.UP,
    )


def rest_color(argument, color: str) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Rest",
        attribute="color",
        value=color,
    )


def rest_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Rest",
        attribute="direction",
        value=abjad.DOWN,
    )


def rest_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Rest",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def rest_staff_position(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Rest",
        "staff_position",
        n,
    )


def rest_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Rest",
        attribute="transparent",
        value=True,
    )


def rest_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Rest",
        attribute="direction",
        value=abjad.UP,
    )


def rest_x_extent_zero(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Rest",
        attribute="X_extent",
        value=(0, 0),
    )


def script_color(argument, color: str = "#red") -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Script",
        attribute="color",
        value=color,
    )


def script_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Script",
        attribute="direction",
        value=abjad.DOWN,
    )


def script_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Script",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def script_padding(argument, number: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Script",
        attribute="padding",
        value=number,
    )


def script_staff_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Script",
        "staff_padding",
        n,
    )


def script_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Script",
        attribute="direction",
        value=abjad.UP,
    )


def script_x_extent_zero(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Script",
        attribute="X_extent",
        value=(0, 0),
    )


def slur_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Slur",
        attribute="direction",
        value=abjad.DOWN,
    )


def slur_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Slur",
        attribute="direction",
        value=abjad.UP,
    )


def span_bar_color(
    argument,
    color: str,
    *,
    after: bool = False,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        after=after,
        grob="SpanBar",
        attribute="color",
        value=color,
        context=context,
    )


def span_bar_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="SpanBar",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        after=after,
        context=context,
    )


def span_bar_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "SpanBar",
        "transparent",
        True,
        context="Score",
    )


def stem_color(
    argument,
    color: str = "#red",
    *,
    context: str | None = None,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Stem",
        attribute="color",
        value=color,
        context=context,
    )


def stem_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Stem",
        "direction",
        abjad.DOWN,
    )


def stem_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Stem",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_length(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Stem",
        attribute="length",
        value=n,
    )


def stem_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Stem",
        attribute="stencil",
        value=False,
    )


def stem_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Stem",
        attribute="transparent",
        value=True,
    )


def stem_tremolo_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="StemTremolo",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "Stem",
        "direction",
        abjad.UP,
    )


def strict_note_spacing_off(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="SpacingSpanner",
        attribute="strict_note_spacing",
        value=False,
        context="Score",
    )


def sustain_pedal_staff_padding(
    argument,
    n: int | float,
    *,
    context: str = "Staff",
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="SustainPedalLineSpanner",
        attribute="staff_padding",
        value=n,
        context=context,
    )


def tacet(argument, color="#green") -> list[abjad.Wrapper]:
    wrappers = mmrest_color(argument, color)
    _tags.wrappers(wrappers, _tags.TACET_COLORING, _helpers.function_name(_frame()))
    return wrappers


def text_script_color(argument, color: str = "#red") -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextScript",
        attribute="color",
        value=color,
    )


def text_script_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextScript",
        attribute="direction",
        value=abjad.DOWN,
    )


def text_script_extra_offset(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextScript",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
    )


def text_script_font_size(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextScript",
        attribute="font_size",
        value=n,
    )


def text_script_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextScript",
        "padding",
        str(n),
    )


def text_script_parent_alignment_x(
    argument,
    n: int | float,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextScript",
        "parent_alignment_X",
        n,
    )


def text_script_self_alignment_x(
    argument,
    n: int | float,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextScript",
        "self_alignment_X",
        n,
    )


def text_script_staff_padding(
    argument,
    n: int | float,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextScript",
        "staff_padding",
        n,
    )


def text_script_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextScript",
        attribute="direction",
        value=abjad.UP,
    )


def text_script_x_offset(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextScript",
        attribute="X_offset",
        value=n,
    )


def text_script_y_offset(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextScript",
        attribute="Y_offset",
        value=n,
    )


def text_spanner_left_padding(
    argument,
    n: int | float,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextSpanner",
        "bound_details__left__padding",
        n,
    )


def text_spanner_right_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextSpanner",
        attribute="bound_details__right__padding",
        value=n,
    )


def text_spanner_staff_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextSpanner",
        "staff_padding",
        n,
    )


def text_spanner_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextSpanner",
        attribute="stencil",
        value=False,
    )


def text_spanner_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TextSpanner",
        attribute="transparent",
        value=True,
    )


def text_spanner_y_offset(
    argument,
    n: int | float,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TextSpanner",
        "Y_offset",
        n,
    )


def tie_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Tie",
        attribute="direction",
        value=abjad.DOWN,
    )


def tie_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="Tie",
        attribute="direction",
        value=abjad.UP,
    )


def time_signature_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TimeSignature",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        context="Score",
    )


def time_signature_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TimeSignature",
        "stencil",
        False,
        context="Score",
    )


def time_signature_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TimeSignature",
        attribute="transparent",
        value=True,
        context="Score",
    )


def trill_spanner_dash_period(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TrillSpanner",
        attribute="dash_period",
        value=n,
    )


def trill_spanner_staff_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TrillSpanner",
        attribute="staff_padding",
        value=n,
    )


def trill_spanner_style(argument, style: str) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TrillSpanner",
        attribute="style",
        value=style,
    )


def tuplet_bracket_after_line_breaking_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TupletBracket",
        "after-line-breaking",
        False,
    )


def tuplet_bracket_down(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TupletBracket",
        "direction",
        abjad.DOWN,
    )


def tuplet_bracket_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletBracket",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_outside_staff_priority(
    argument, n: int | float
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletBracket",
        attribute="outside_staff_priority",
        value=n,
    )


def tuplet_bracket_padding(argument, n: int | float) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TupletBracket",
        "padding",
        n,
    )


def tuplet_bracket_positions(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TupletBracket",
        "positions",
        f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_shorten_pair(
    argument,
    pair: tuple[int | float, int | float],
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TupletBracket",
        "shorten_pair",
        f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_staff_padding(
    argument,
    n: int | float,
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        "TupletBracket",
        "staff_padding",
        n,
    )


def tuplet_bracket_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="stencil",
        grob="TupletBracket",
        value=False,
    )


def tuplet_bracket_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletBracket",
        attribute="transparent",
        value=True,
    )


def tuplet_bracket_up(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletBracket",
        attribute="direction",
        value=abjad.UP,
    )


def tuplet_number_denominator(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletNumber",
        attribute="text",
        value="#tuplet-number::calc-denominator-text",
    )


def tuplet_number_extra_offset(
    argument, pair: tuple[int | float, int | float]
) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletNumber",
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_number_stencil_false(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        attribute="stencil",
        grob="TupletNumber",
        value=False,
    )


def tuplet_number_text(argument, string: str) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletNumber",
        attribute="text",
        value=string,
    )


def tuplet_number_transparent(argument) -> list[abjad.Wrapper]:
    return _do_override(
        _frame(),
        argument,
        grob="TupletNumber",
        attribute="transparent",
        value=True,
    )
