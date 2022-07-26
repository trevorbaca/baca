"""
Overrides.
"""
import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import select as _select
from . import tags as _tags
from . import typings


def _do_override_command(
    leaves,
    grob,
    attribute,
    value,
    first_tag,
    final_tag,
    after=False,
    allowlist=None,
    blocklist=None,
    context=None,
    deactivate=False,
):
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
        return wrapper_1
    override = abjad.LilyPondOverride(
        lilypond_type=lilypond_type,
        grob_name=grob,
        is_revert=True,
        property_path=attribute,
    )
    string = override.revert_string
    literal = abjad.LilyPondLiteral(string, "after")
    wrapper_2 = abjad.attach(
        literal, leaves[-1], deactivate=deactivate, tag=final_tag, wrapper=True
    )
    return wrapper_1, wrapper_2


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OverrideCommand(_command.Command):

    after: bool = False
    allowlist: tuple[type, ...] = ()
    attribute: str | None = None
    blocklist: tuple[type, ...] = ()
    context: str | None = None
    grob: str | None = None
    selector: typing.Callable = lambda _: _select.leaves(_)
    value: typing.Any = None

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert isinstance(self.after, bool), repr(self.after)
        if self.allowlist is not None:
            assert isinstance(self.allowlist, tuple), repr(self.allowlist)
            assert all(issubclass(_, abjad.Leaf) for _ in self.allowlist)
        if self.attribute is not None:
            assert isinstance(self.attribute, str), repr(self.attribute)
        if self.blocklist is not None:
            assert isinstance(self.blocklist, tuple), repr(self.blocklist)
            assert all(issubclass(_, abjad.Leaf) for _ in self.blocklist)
        if self.context is not None:
            assert isinstance(self.context, str), repr(self.context)
        if self.grob is not None:
            assert isinstance(self.grob, str), repr(self.grob)

    __repr__ = _command.Command.__repr__

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        leaves = abjad.select.leaves(argument)
        first_tag = self.get_tag(leaves[0], runtime=runtime)
        function_name = _tags.function_name(_frame(), self, n=1)
        if first_tag:
            first_tag = first_tag.append(function_name)
        else:
            first_tag = function_name
        final_tag = self.get_tag(leaves[-1], runtime=runtime)
        function_name = _tags.function_name(_frame(), self, n=2)
        if final_tag:
            final_tag = final_tag.append(function_name)
        else:
            final_tag = function_name
        _do_override_command(
            leaves,
            self.grob,
            self.attribute,
            self.value,
            first_tag,
            final_tag,
            after=self.after,
            allowlist=self.allowlist,
            blocklist=self.blocklist,
            context=self.context,
            deactivate=self.deactivate,
        )
        return False


def accidental_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def accidental_font_size(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="font_size",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def accidental_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def accidental_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
):
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def accidental_x_extent_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def accidental_x_offset(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_offset",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def accidental_y_offset(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="Y_offset",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def bar_line_color(
    color: str,
    *,
    after: bool = False,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        after=after,
        attribute="color",
        value=color,
        context=context,
        grob="BarLine",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        after=after,
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        context=context,
        grob="BarLine",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="BarLine",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_transparent_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "BarLine",
        "transparent",
        True,
        first_tag,
        final_tag,
        context="Score",
    )


def bar_line_x_extent_command(
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
    measures: typings.Slice = None,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        after=after,
        attribute="X_extent",
        value=f"#'({pair[0]} . {pair[1]})",
        context=context,
        measures=measures,
        grob="BarLine",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_x_extent(
    leaves,
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
    tags: list[abjad.Tag] = None,
) -> None:
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
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


def beam_positions(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    if not isinstance(n, int | float):
        message = f"beam position must be number (not {n})."
        raise Exception(message)
    return OverrideCommand(
        attribute="positions",
        value=f"#'({n} . {n})",
        grob="Beam",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def beam_positions_function(
    argument, n: int | float, *, tags: list[abjad.Tag] = None
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Beam",
        "positions",
        f"#'({n} . {n})",
        first_tag,
        final_tag,
    )


def beam_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="Beam",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def beam_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Beam",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def clef_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def clef_extra_offset_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Clef",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
        context="Staff",
    )


def clef_shift(
    clef: str | abjad.Clef,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> _command.Suite:
    extra_offset_x: int | float
    if isinstance(clef, str):
        clef = abjad.Clef(clef)
    if isinstance(clef, int | float):
        extra_offset_x = clef
    else:
        assert isinstance(clef, abjad.Clef)
        width = clef._to_width[clef.name]
        extra_offset_x = -width
    suite = _command.suite(
        clef_x_extent_false(), clef_extra_offset((extra_offset_x, 0))
    )
    _command.tag(_tags.function_name(_frame()), suite)
    _command.tag(_tags.SHIFTED_CLEF, suite, tag_measure_number=True)
    return suite


def clef_shift_function(
    leaf,
    clef: str | abjad.Clef,
    first_measure_number: int,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    measure_number = abjad.get.measure_number(leaf)
    measure_number += first_measure_number - 1
    measure_number_tag = abjad.Tag(f"MEASURE_{measure_number}")
    clef_x_extent_false_function(leaf, tags=[_tags.SHIFTED_CLEF, measure_number_tag])
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
    clef_extra_offset_function(
        leaf, pair, tags=[_tags.SHIFTED_CLEF, measure_number_tag]
    )


def clef_whiteout(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="whiteout",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def clef_x_extent_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def clef_x_extent_false_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Clef",
        "X_extent",
        False,
        first_tag,
        final_tag,
        context="Staff",
    )


def dls_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dls_padding_function(
    argument,
    n: int | float,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "DynamicLineSpanner",
        "padding",
        n,
        first_tag,
        final_tag,
    )


def dls_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dls_staff_padding_function(
    argument,
    n: int | float,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "DynamicLineSpanner",
        "staff_padding",
        n,
        first_tag,
        final_tag,
    )


def dls_up(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dots_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def dots_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def dots_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dots_x_extent_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def dynamic_text_color(
    color: str = "#red",
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    if not isinstance(pair, tuple):
        raise Exception(f"dynamic text extra offset must be pair (not {pair}).")
    if len(pair) != 2:
        raise Exception(f"dynamic text extra offset must be pair (not {pair}).")
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_extra_offset_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "DynamicText",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
    )


def dynamic_text_parent_alignment_x(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_self_alignment_x(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_x_extent_zero(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_x_extent_zero_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "DynamicText",
        "X_extent",
        (0, 0),
        first_tag,
        final_tag,
    )


def dynamic_text_x_offset(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_y_offset(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flag_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="Flag",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def flag_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="Flag",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def flag_transparent(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Flag",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def glissando_thickness(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="thickness",
        value=str(n),
        grob="Glissando",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_shorten_pair(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="shorten_pair",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_shorten_pair_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Hairpin",
        "shorten_pair",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
    )


def hairpin_start_shift(
    dynamic: str | abjad.Dynamic,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> _command.Suite:
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[str(dynamic.name)]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    suite = _command.suite(
        dynamic_text_extra_offset((extra_offset_x, 0)),
        dynamic_text_x_extent_zero(),
        hairpin_shorten_pair((hairpin_shorten_left, 0)),
    )
    _command.tag(_tags.function_name(_frame()), suite)
    return suite


def hairpin_start_shift_function(
    argument,
    dynamic: str | abjad.Dynamic,
) -> None:
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[str(dynamic.name)]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    leaf = abjad.select.leaf(argument, 0)
    dynamic_text_extra_offset_function(leaf, (extra_offset_x, 0))
    dynamic_text_x_extent_zero_function(leaf)
    hairpin_shorten_pair_function(argument, (hairpin_shorten_left, 0))


def hairpin_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_to_barline(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="to_barline",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_to_barline_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Hairpin",
        "to_barline",
        True,
        first_tag,
        final_tag,
    )


def hairpin_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer_tie_down(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer_tie_up(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def mmrest_color(
    color: str = "#red",
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_transparent(
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_transparent_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    mmrests = _select.mmrests(leaves)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        mmrests,
        "MultiMeasureRest",
        "transparent",
        True,
        first_tag,
        final_tag,
    )


def mmrest_text_color(
    color: str = "#red",
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_extra_offset_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "MultiMeasureRestText",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
    )


def mmrest_text_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_parent_center(
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=0,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_transparent(
    *,
    selector: typing.Callable = lambda _: _select.mmrests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def no_ledgers(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="no_ledgers",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_column_shift(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="force_hshift",
        value=n,
        grob="NoteColumn",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_color(
    color: str,
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=color,
    )


def note_head_duration_log(
    n: int,
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="duration_log",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def note_head_duration_log_function(
    argument, n: int, *, allow_rests: bool = False, tags: list[abjad.Tag] = None
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    elif allow_rests:
        leaves = abjad.select.leaves(argument)
    else:
        leaves = _select.pleaves(argument)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "NoteHead",
        "duration_log",
        n,
        first_tag,
        final_tag,
    )


def note_head_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def note_head_font_size(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="font_size",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def note_head_no_ledgers(
    value: bool,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="no_ledgers",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=value,
    )


def note_head_no_ledgers_function(
    argument, value: bool, *, allow_rests: bool = False, tags: list[abjad.Tag] = None
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    elif allow_rests:
        leaves = abjad.select.leaves(argument)
    else:
        leaves = _select.pleaves(argument)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "NoteHead",
        "no_ledgers",
        value,
        first_tag,
        final_tag,
    )


def note_head_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def note_head_style(
    string: str,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="style",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=string,
    )


def note_head_style_function(
    argument, string: str, *, allow_rests: bool = False, tags: list[abjad.Tag] = None
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    elif allow_rests:
        leaves = abjad.select.leaves(argument)
    else:
        leaves = _select.pleaves(argument)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "NoteHead",
        "style",
        string,
        first_tag,
        final_tag,
    )


def note_head_style_cross(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="style",
        value="#'cross",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_style_harmonic(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="style",
        value="#'harmonic",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_style_harmonic_function(
    argument, *, allow_rests: bool = False, tags: list[abjad.Tag] = None
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    elif allow_rests:
        leaves = abjad.select.leaves(argument)
    else:
        leaves = _select.pleaves(argument)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "NoteHead",
        "style",
        "#'harmonic",
        first_tag,
        final_tag,
    )


def note_head_style_harmonic_black(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="style",
        value="#'harmonic-black",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_transparent(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
):
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_x_extent_zero(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=(0, 0),
    )


def ottava_bracket_shorten_pair(
    pair: tuple[int | float, int | float] = (-0.8, -0.6),
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="shorten_pair",
        context="Staff",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="OttavaBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def ottava_bracket_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        context="Staff",
        value=n,
        grob="OttavaBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def ottava_bracket_staff_padding_function(
    argument,
    n: int | float,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "OttavaBracket",
        "staff_padding",
        n,
        first_tag,
        final_tag,
        context="Staff",
    )


def rehearsal_mark_down(
    *,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark_down_function(
    argument,
    *,
    context: str = "Score",
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "RehearsalMark",
        "direction",
        abjad.DOWN,
        first_tag,
        final_tag,
        context=context,
    )


def rehearsal_mark_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark_extra_offset_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    context: str = "Score",
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "RehearsalMark",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
        context=context,
    )


def rehearsal_mark_padding(
    n: int | float,
    *,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="padding",
        value=n,
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark_padding_function(
    argument,
    n: int | float,
    *,
    context: str = "Score",
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "RehearsalMark",
        "padding",
        n,
        first_tag,
        final_tag,
        context=context,
    )


def rehearsal_mark_self_alignment_x(
    n: int,
    *,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rehearsal_mark_self_alignment_x_function(
    argument,
    n: int,
    *,
    context: str = "Score",
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "RehearsalMark",
        "self_alignment_X",
        n,
        first_tag,
        final_tag,
        context=context,
    )


def rehearsal_mark_y_offset(
    n: int | float,
    *,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_down(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def repeat_tie_extra_offset_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "RepeatTie",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
    )


def repeat_tie_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def repeat_tie_transparent(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
):
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_up(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_color(
    color: str,
    *,
    selector: typing.Callable = lambda _: _select.rest(_, 0),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_down(
    *,
    selector: typing.Callable = lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.rest(_, 0),
) -> OverrideCommand:
    if not isinstance(pair, tuple):
        raise Exception(f"rest extra offset must be pair (not {pair!r}).")
    if len(pair) != 2:
        raise Exception(f"rest extra offset must be pair (not {pair!r}).")
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_position(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_position",
        value=n,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_staff_position_function(
    argument,
    n: int | float,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Rest",
        "staff_position",
        n,
        first_tag,
        final_tag,
    )


def rest_transparent(
    *,
    selector: typing.Callable = lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_up(
    *,
    selector: typing.Callable = lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_x_extent_zero(
    *,
    selector: typing.Callable = lambda _: _select.rest(_, 0),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=(0, 0),
    )


def script_color(
    color: str = "#red",
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_down(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_padding(
    number: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="padding",
        value=number,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_staff_padding_function(
    argument,
    n: int | float,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Script",
        "staff_padding",
        n,
        first_tag,
        final_tag,
    )


def script_up(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_x_extent_zero(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def slur_down(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Slur",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def slur_up(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Slur",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def span_bar_color(
    color: str,
    *,
    after: bool = False,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        after=after,
        attribute="color",
        value=color,
        context=context,
        grob="SpanBar",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def span_bar_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    after: bool = False,
    context: str = "Score",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        after=after,
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        context=context,
        grob="SpanBar",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def span_bar_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="SpanBar",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def span_bar_transparent_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "SpanBar",
        "transparent",
        True,
        first_tag,
        final_tag,
        context="Score",
    )


def stem_color(
    color: str = "#red",
    *,
    context: str = None,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="color",
        value=color,
        context=context,
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_down(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_down_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Stem",
        "direction",
        abjad.DOWN,
        first_tag,
        final_tag,
    )


def stem_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def stem_transparent(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_tremolo_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="StemTremolo",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_up(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_up_function(
    argument,
    *,
    allow_rests: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    elif allow_rests:
        leaves = abjad.select.leaves(argument)
    else:
        leaves = _select.pleaves(argument)
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "Stem",
        "direction",
        abjad.UP,
        first_tag,
        final_tag,
    )


def strict_note_spacing_off(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="strict_note_spacing",
        value=False,
        context="Score",
        grob="SpacingSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def sustain_pedal_staff_padding(
    n: int | float,
    *,
    context: str = "Staff",
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        context=context,
        grob="SustainPedalLineSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tacet(
    color="#green",
    *,
    measures=None,
    selector: typing.Callable = lambda _: _select.mmrests(_),
):
    command = mmrest_color(color, selector=selector)
    _command.tag(_tags.TACET_COLORING, command)
    _command.tag(_tags.function_name(_frame()), command)
    command_ = _command.new(command, measures=measures)
    assert isinstance(command_, OverrideCommand)
    return command_


def text_script_color(
    color: str = "#red",
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="color",
        blocklist=tuple(blocklist),
        value=color,
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_script_down(
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="direction",
        blocklist=tuple(blocklist),
        value=abjad.DOWN,
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_script_extra_offset_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    allow_mmrests: bool = False,
    tags: list[abjad.Tag] = None,
) -> abjad.Wrapper:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return _do_override_command(
        leaves,
        "TextScript",
        "extra_offset",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
        # after=after,
        # allowlist=None,
        blocklist=tuple(blocklist),
        # context=context,
        # deactivate=False,
    )


def text_script_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="extra_offset",
        blocklist=tuple(blocklist),
        value=f"#'({pair[0]} . {pair[1]})",
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_script_font_size(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="font_size",
        blocklist=tuple(blocklist),
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_script_padding(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="padding",
        blocklist=tuple(blocklist),
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_script_padding_function(
    argument,
    n: int | float,
    *,
    allow_mmrests: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    _do_override_command(
        leaves,
        "TextScript",
        "padding",
        str(n),
        first_tag,
        final_tag,
        # after=after,
        # allowlist=None,
        blocklist=tuple(blocklist),
        # context=context,
        # deactivate=False,
    )


def text_script_parent_alignment_x(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="parent_alignment_X",
        blocklist=tuple(blocklist),
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_script_parent_alignment_x_function(
    argument,
    n: int | float,
    *,
    allow_mmrests: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    _do_override_command(
        leaves,
        "TextScript",
        "parent_alignment_X",
        n,
        first_tag,
        final_tag,
        # after=after,
        # allowlist=None,
        blocklist=tuple(blocklist),
        # context=context,
        # deactivate=False,
    )


def text_script_self_alignment_x(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="self_alignment_X",
        blocklist=tuple(blocklist),
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_script_self_alignment_x_function(
    argument,
    n: int | float,
    *,
    allow_mmrests: bool = False,
    tags: list[abjad.Tag] = None,
) -> abjad.Wrapper:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return _do_override_command(
        leaves,
        "TextScript",
        "self_alignment_X",
        n,
        first_tag,
        final_tag,
        # after=after,
        # allowlist=None,
        blocklist=tuple(blocklist),
        # context=context,
        # deactivate=False,
    )


def text_script_staff_padding(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="staff_padding",
        blocklist=tuple(blocklist),
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_script_staff_padding_function(
    argument,
    n: int | float,
    *,
    allow_mmrests: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    _do_override_command(
        leaves,
        "TextScript",
        "staff_padding",
        n,
        first_tag,
        final_tag,
        # after=after,
        # allowlist=None,
        blocklist=tuple(blocklist),
        # context=context,
        # deactivate=False,
    )


def text_script_up(
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="direction",
        blocklist=tuple(blocklist),
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.UP,
    )


def text_script_x_offset(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="X_offset",
        blocklist=tuple(blocklist),
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_script_y_offset(
    n: int | float,
    *,
    allow_mmrests: bool = False,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    blocklist = []
    if allow_mmrests is not True:
        blocklist.append(abjad.MultimeasureRest)
    return OverrideCommand(
        attribute="Y_offset",
        blocklist=tuple(blocklist),
        grob="TextScript",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_spanner_left_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="bound_details__left__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_spanner_left_padding_function(
    argument,
    n: int | float,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TextSpanner",
        "bound_details__left__padding",
        n,
        first_tag,
        final_tag,
    )


def text_spanner_right_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="bound_details__right__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_spanner_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def text_spanner_staff_padding_function(
    argument,
    n: int | float,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TextSpanner",
        "staff_padding",
        n,
        first_tag,
        final_tag,
    )


def text_spanner_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def text_spanner_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )


def text_spanner_y_offset(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="Y_offset",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_spanner_y_offset_function(
    argument,
    n: int | float,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TextSpanner",
        "Y_offset",
        n,
        first_tag,
        final_tag,
    )


def tie_down(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        grob="Tie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.DOWN,
    )


def tie_up(
    *,
    selector: typing.Callable = lambda _: _select.pleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        grob="Tie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.UP,
    )


def time_signature_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.hleaf(_, 0),
) -> OverrideCommand:
    assert isinstance(pair, tuple), repr(pair)
    return OverrideCommand(
        attribute="extra_offset",
        context="Score",
        grob="TimeSignature",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def time_signature_stencil_false(
    *,
    selector: typing.Callable = lambda _: _select.hleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="stencil",
        context="Score",
        grob="TimeSignature",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def time_signature_stencil_false_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TimeSignature",
        "stencil",
        False,
        first_tag,
        final_tag,
        context="Score",
    )


def time_signature_transparent(
    *,
    selector: typing.Callable = lambda _: _select.hleaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        context="Score",
        grob="TimeSignature",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )


def trill_spanner_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        grob="TrillSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def tuplet_bracket_down(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.DOWN,
    )


def tuplet_bracket_down_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TupletBracket",
        "direction",
        abjad.DOWN,
        first_tag,
        final_tag,
    )


def tuplet_bracket_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_outside_staff_priority(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="outside_staff_priority",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def tuplet_bracket_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="padding",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def tuplet_bracket_padding_function(
    argument,
    n: int | float,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TupletBracket",
        "padding",
        n,
        first_tag,
        final_tag,
    )


def tuplet_bracket_shorten_pair(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="shorten_pair",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_shorten_pair_function(
    argument,
    pair: tuple[int | float, int | float],
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TupletBracket",
        "shorten_pair",
        f"#'({pair[0]} . {pair[1]})",
        first_tag,
        final_tag,
    )


def tuplet_bracket_staff_padding(
    n: int | float,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="staff_padding",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def tuplet_bracket_staff_padding_function(
    argument,
    n: int | float,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    if isinstance(argument, abjad.Leaf):
        leaves = [argument]
    else:
        assert all(isinstance(_, abjad.Leaf) for _ in argument), repr(argument)
        leaves = argument
    first_tag = _tags.function_name(_frame(), n=1)
    for tag in tags or []:
        first_tag = first_tag.append(tag)
    final_tag = _tags.function_name(_frame(), n=2)
    for tag in tags or []:
        final_tag = final_tag.append(tag)
    _do_override_command(
        leaves,
        "TupletBracket",
        "staff_padding",
        n,
        first_tag,
        final_tag,
    )


def tuplet_bracket_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )


def tuplet_bracket_up(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="direction",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.UP,
    )


def tuplet_number_denominator(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value="#tuplet-number::calc-denominator-text",
    )


def tuplet_number_extra_offset(
    pair: tuple[int | float, int | float],
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="extra_offset",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_number_text(
    string: str,
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    assert isinstance(string, str), repr(string)
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=string,
    )


def tuplet_number_transparent(
    *,
    selector: typing.Callable = lambda _: _select.leaves(_),
) -> OverrideCommand:
    return OverrideCommand(
        attribute="transparent",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )
