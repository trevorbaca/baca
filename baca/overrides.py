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
    abjad.attach(literal, leaves[0], deactivate=deactivate, tag=first_tag)
    if once:
        return
    override = abjad.LilyPondOverride(
        lilypond_type=lilypond_type,
        grob_name=grob,
        is_revert=True,
        property_path=attribute,
    )
    string = override.revert_string
    literal = abjad.LilyPondLiteral(string, "after")
    abjad.attach(literal, leaves[-1], deactivate=deactivate, tag=final_tag)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OverrideCommand(_command.Command):
    """
    Override command.
    """

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
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides accidental extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def accidental_font_size(
    n: int | float,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides accidental font size.
    """
    return OverrideCommand(
        attribute="font_size",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def accidental_stencil_false(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides accidental stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def accidental_transparent(
    selector=lambda _: _select.leaves(_),
):
    """
    Overrides accidental transparency on.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def accidental_x_extent_false(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides accidental X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def accidental_x_offset(
    n: int | float,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides accidental X-offset.
    """
    return OverrideCommand(
        attribute="X_offset",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def accidental_y_offset(
    n: int | float,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides accidental Y-offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        grob="Accidental",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def bar_line_color(
    color: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    after: bool = False,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides bar line color.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    after: bool = False,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides bar line extra offset.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    r"""
    Overrides bar line transparency.

    ..  container:: example

        Makes bar line before measure 1 transparent:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> stack = rmakers.stack(
        ...     rmakers.talea([1, 1, 1, -1], 8),
        ...     rmakers.beam(),
        ...     rmakers.extract_trivial(),
        ... )
        >>> music = stack(accumulator.get())
        >>> score["Music"].extend(music)

        >>> accumulator(
        ...     "Music",
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.bar_line_transparent(
        ...         selector=lambda _: abjad.select.group_by_measure(_)[1]
        ...     ),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'8
                        [
                        d''8
                        f'8
                        ]
                        r8
                        \override Score.BarLine.transparent = ##t
                        e''8
                        [
                        g'8
                        f''8
                        ]
                        \revert Score.BarLine.transparent
                        r8
                        e'8
                        [
                        d''8
                        f'8
                        ]
                        r8
                        e''8
                        [
                        g'8
                        ]
                    }
                >>
            }

    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="BarLine",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def bar_line_x_extent_command(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    after: bool = False,
    context: str = "Score",
    measures: typings.Slice = None,
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides beam positions.

    ..  container:: example

        Overrides beam positions on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         treatments=[-1],
        ...     ),
        ...     baca.stem_up(),
        ...     rmakers.beam(),
        ...     baca.beam_positions(6),
        ...     baca.tuplet_bracket_staff_padding(4),
        ... )
        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> selections = stack(collections)

        >>> lilypond_file = abjad.illustrators.selection(selections)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \times 4/5
                    {
                        \override Beam.positions = #'(6 . 6)
                        \override TupletBracket.staff-padding = 4
                        \time 3/4
                        r8
                        \override Stem.direction = #up
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \times 4/5
                    {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert Stem.direction
                        r4
                        \revert Beam.positions
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides beam stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Beam",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def beam_transparent(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides beam transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Beam",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def clef_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
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
    selector=lambda _: abjad.select.leaf(_, 0),
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
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides clef whiteout.
    """
    return OverrideCommand(
        attribute="whiteout",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def clef_x_extent_false(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides clef x-extent.
    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides dynamic line spanner padding.
    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides dynamic line spanner staff padding

    ..  container:: example

        Overrides dynamic line spanner staff padding on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dls_staff_padding(4),
        ...     baca.new(
        ...         baca.hairpin(
        ...             "p < f",
        ...             remove_length_1_spanner_start=True,
        ...             selector=lambda _: baca.select.tleaves(_),
        ...             ),
        ...         map=lambda _: abjad.select.tuplets(_),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override DynamicLineSpanner.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        \p
                        [
                        \<
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        \f
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        \p
                        [
                        \<
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        \f
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \p
                        r4
                        \revert DynamicLineSpanner.staff-padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides dynamic line spanner direction.

    ..  container:: example

        Up-overrides dynamic line spanner direction on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dls_up(),
        ...     baca.new(
        ...         baca.hairpin(
        ...             "p < f",
        ...             remove_length_1_spanner_start=True,
        ...             selector=lambda _: baca.select.tleaves(_),
        ...             ),
        ...         map=lambda _: abjad.select.tuplets(_),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override DynamicLineSpanner.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        \p
                        [
                        \<
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        \f
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        \p
                        [
                        \<
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        \f
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \p
                        r4
                        \revert DynamicLineSpanner.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dots_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides dots extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def dots_stencil_false(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides dots stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def dots_transparent(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides dots transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dots_x_extent_false(
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dots X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Dots",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def dynamic_text_color(
    color: str = "#red",
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text color.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    r"""
    Overrides dynamic text extra offset.

    ..  container:: example

        Overrides dynamic text extra offset on pitched leaf 0:

        >>> def selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("f", selector=selector),
        ...     baca.dynamic_text_extra_offset((-3, 0)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \once \override DynamicText.extra-offset = #'(-3 . 0)
                        c'16
                        \p
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        \f
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raise exception on nonpair input:

        >>> baca.dynamic_text_extra_offset(2)
        Traceback (most recent call last):
            ...
        Exception: dynamic text extra offset must be pair (not 2).

    """
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


def dynamic_text_parent_alignment_x(
    n: int | float,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text parent alignment X to ``n``.
    """
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_self_alignment_x(
    n: int | float,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text self-alignment-X to ``n``.
    """
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_stencil_false(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_transparent(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_x_extent_zero(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_x_offset(
    n: int | float,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def dynamic_text_y_offset(
    n: int | float,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides dynamic text Y-extent.
    """
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flag_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides flag extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Flag",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def flag_stencil_false(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides flag stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Flag",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def flag_transparent(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    """
    Overrides flag transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Flag",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def glissando_thickness(
    n: int | float,
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    """
    Overrides glissando thickness.
    """
    return OverrideCommand(
        attribute="thickness",
        value=str(n),
        grob="Glissando",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_shorten_pair(
    pair: tuple[int | float, int | float],
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides hairpin shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_start_shift(
    dynamic: str | abjad.Dynamic,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> _command.Suite:
    """
    Shifts hairpin start dynamic to left by width of dynamic.
    """
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


def hairpin_stencil_false(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides hairpin stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_to_barline(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides hairpin to-barline to true.
    """
    return OverrideCommand(
        attribute="to_barline",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def hairpin_transparent(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides hairpin transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer_tie_down(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer_tie_up(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def mmrest_color(
    color: str = "#red",
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest color.


    ..  container:: example

        REGRESSION. Coerces X11 color names:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.mmrest_color("#(x11-color 'DarkOrchid)"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                b'1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                        >>
                        \override MultiMeasureRest.color = #(x11-color 'DarkOrchid)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \revert MultiMeasureRest.color
                    }
                >>
            }

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_transparent(
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_color(
    color: str = "#red",
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text color.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: baca.select.mmrest(_, 1),
        ...     ),
        ...     baca.mmrest_text_color("#red"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                b'1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                        >>
                        \override MultiMeasureRestText.color = #red
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \revert MultiMeasureRestText.color
                    }
                >>
            }

    ..  container:: example exception

        Raises exception when called on leaves other than multimeasure
        rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(accumulator.get())
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.mmrest_text_color(
        ...         "#red",
        ...         selector=lambda _: baca.select.leaves(_),
        ...     ),
        ...     baca.pitches([2, 4]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: only MultimeasureRest (not Note) allowed.

    """
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
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text extra offset.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: baca.select.mmrest(_, 1),
        ...     ),
        ...     baca.mmrest_text_extra_offset((0, 2)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                b'1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                        >>
                        \override MultiMeasureRestText.extra-offset = #'(0 . 2)
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \revert MultiMeasureRestText.extra-offset
                    }
                >>
            }

    """
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
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text padding.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: baca.select.mmrest(_, 1),
        ...     ),
        ...     baca.mmrest_text_padding(2),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                b'1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                        >>
                        \override MultiMeasureRestText.padding = 2
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \revert MultiMeasureRestText.padding
                    }
                >>
            }

    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_parent_center(
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text parent alignment X to center.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: baca.select.mmrest(_, 1),
        ...     ),
        ...     baca.mmrest_text_parent_center(),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                b'1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                        >>
                        \override MultiMeasureRestText.parent-alignment-X = 0
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \revert MultiMeasureRestText.parent-alignment-X
                    }
                >>
            }

    """
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
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text staff padding.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: baca.select.mmrest(_, 1),
        ...     ),
        ...     baca.mmrest_text_staff_padding(2),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        <<
                            \context Voice = "Music"
                            {
                                %@% \abjad-invisible-music
                                \abjad-invisible-music-coloring
                                \once \override Accidental.stencil = ##f
                                \once \override NoteColumn.ignore-collision = ##t
                                b'1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                            \context Voice = "Rests"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                            }
                        >>
                        \override MultiMeasureRestText.staff-padding = 2
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        \revert MultiMeasureRestText.staff-padding
                    }
                >>
            }

    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_transparent(
    selector=lambda _: _select.mmrests(_),
) -> OverrideCommand:
    """
    Overrides script transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def no_ledgers(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_column_shift(
    n: int | float,
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note column force hshift.
    """
    return OverrideCommand(
        attribute="force_hshift",
        value=n,
        grob="NoteColumn",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_color(
    color: str,
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="color",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=color,
    )


def note_head_duration_log(
    n: int,
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    """
    Overrides note-head duration-log property.
    """
    return OverrideCommand(
        attribute="duration_log",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def note_head_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def note_head_font_size(
    n: int | float,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note-head font size.
    """
    return OverrideCommand(
        attribute="font_size",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def note_head_no_ledgers(
    value: bool,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers property.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=value,
    )


def note_head_stencil_false(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note-head stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def note_head_style(
    string: str,
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note-head style property.
    """
    return OverrideCommand(
        attribute="style",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=string,
    )


def note_head_style_cross(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides note-head style.

    ..  container:: example

        Overrides note-head style on all pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.note_head_style_cross(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \override NoteHead.style = #'cross
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert NoteHead.style
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="style",
        value="#'cross",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_style_harmonic(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides note-head style for ``selector`` output.

    ..  container:: example

        Overrides note-head style on all PLTs:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.note_head_style_harmonic(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \override NoteHead.style = #'harmonic
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert NoteHead.style
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="style",
        value="#'harmonic",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_style_harmonic_function(
    argument, *, tags: list[abjad.Tag] = None
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
        "NoteHead",
        "style",
        "#'harmonic",
        first_tag,
        final_tag,
    )


def note_head_style_harmonic_black(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides note-head style to harmonic-black.
    """
    return OverrideCommand(
        attribute="style",
        value="#'harmonic-black",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_transparent(
    selector=lambda _: _select.pleaves(_),
):
    """
    Overrides note-head transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def note_head_x_extent_zero(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides note-head X-extent.

    ..  todo:: Set note-head X-extent to zero rather than false.

    """
    return OverrideCommand(
        attribute="X_extent",
        grob="NoteHead",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=(0, 0),
    )


def ottava_bracket_shorten_pair(
    pair: tuple[int | float, int | float] = (-0.8, -0.6),
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides ottava bracket shorten pair.
    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides ottava bracket staff padding.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides rehearsal mark direction.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides rehearsal mark extra offset.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides rehearsal mark padding.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides rehearsal mark self-alignment-X.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides rehearsal mark Y offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_down(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides repeat tie direction.

    ..  container:: example

        Overrides repeat tie direction on pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.repeat_tie(selector=lambda _: baca.select.pleaves(_)[1:]),
        ...         map=lambda _: baca.select.qruns(_),
        ...     ),
        ...     baca.repeat_tie_down(),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 5/4
                        r8
                        \override RepeatTie.direction = #down
                        \override Stem.direction = #up
                        b'16
                        [
                        b'16
                        ]
                        \repeatTie
                        c''4
                        ~
                        c''16
                        \repeatTie
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        b'16
                        [
                        b'16
                        ]
                        \repeatTie
                        b'4
                        \repeatTie
                        ~
                        b'16
                        \repeatTie
                        r16
                    }
                    \times 4/5
                    {
                        b'16
                        \revert RepeatTie.direction
                        \revert Stem.direction
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides repeat tie extra-offset.
    """
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
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides repeat tie stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def repeat_tie_transparent(
    selector=lambda _: _select.pleaves(_),
):
    """
    Overrides repeat tie transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def repeat_tie_up(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides repeat tie direction.

    ..  container:: example

        Overrides repeat tie direction on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.repeat_tie(
        ...             selector=lambda _: baca.select.pleaves(_)[1:],
        ...         ),
        ...         map=lambda _: baca.select.qruns(_),
        ...     ),
        ...     baca.repeat_tie_up(),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 5/4
                        r8
                        \override RepeatTie.direction = #up
                        \override Stem.direction = #down
                        b'16
                        [
                        b'16
                        ]
                        \repeatTie
                        c''4
                        ~
                        c''16
                        \repeatTie
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        b'16
                        [
                        b'16
                        ]
                        \repeatTie
                        b'4
                        \repeatTie
                        ~
                        b'16
                        \repeatTie
                        r16
                    }
                    \times 4/5
                    {
                        b'16
                        \revert RepeatTie.direction
                        \revert Stem.direction
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="RepeatTie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_color(
    color: str,
    selector=lambda _: _select.rest(_, 0),
) -> OverrideCommand:
    """
    Overrides rest extra offset.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_down(
    selector=lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    r"""
    Overrides rest direction.

    ..  container:: example

        Down-overrides direction of rests:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.rest_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Rest.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert Rest.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: _select.rest(_, 0),
) -> OverrideCommand:
    """
    Overrides rest extra offset.
    """
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
    selector=lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    r"""
    Overrides rest position.

    ..  container:: example

        Overrides rest position:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.rest_position(-6),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Rest.staff-position = -6
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert Rest.staff-position
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="staff_position",
        value=n,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_transparent(
    selector=lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    r"""
    Overrides rest transparency.

    ..  container:: example

        Makes rests transparent:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.rest_transparent(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Rest.transparent = ##t
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert Rest.transparent
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_up(
    selector=lambda _: abjad.select.rests(_),
) -> OverrideCommand:
    r"""
    Overrides rest direction.

    ..  container:: example

        Up-overrides rest direction:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.rest_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Rest.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert Rest.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def rest_x_extent_zero(
    selector=lambda _: _select.rest(_, 0),
) -> OverrideCommand:
    """
    Overrides rest X-extent.

    Note that overriding Rest.X-extent = ##f generates LilyPond warnings.

    But overriding Rest.X-extent = #'(0 . 0) does not generate warnings.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Rest",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=(0, 0),
    )


def script_color(
    color: str = "#red",
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides script color.

    ..  container:: example

        Overrides script color on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...     baca.script_color("#red"),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Script.color = #red
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \accent
                        [
                        d'16
                        - \accent
                        ]
                        bf'4
                        - \accent
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \accent
                        [
                        e''16
                        - \accent
                        ]
                        ef''4
                        - \accent
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent
                        [
                        g''16
                        - \accent
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \accent
                        r4
                        \revert Script.color
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_down(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides script direction.

    ..  container:: example

        Down-overrides script direction on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...     baca.script_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Script.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \accent
                        [
                        d'16
                        - \accent
                        ]
                        bf'4
                        - \accent
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \accent
                        [
                        e''16
                        - \accent
                        ]
                        ef''4
                        - \accent
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent
                        [
                        g''16
                        - \accent
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \accent
                        r4
                        \revert Script.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    r"""
    Overrides script extra offset.

    ..  container:: example

        Overrides script extra offset on leaf 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...     baca.script_extra_offset(
        ...         (-1.5, 0),
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \once \override Script.extra-offset = #'(-1.5 . 0)
                        c'16
                        - \accent
                        [
                        d'16
                        - \accent
                        ]
                        bf'4
                        - \accent
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \accent
                        [
                        e''16
                        - \accent
                        ]
                        ef''4
                        - \accent
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent
                        [
                        g''16
                        - \accent
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \accent
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_padding(
    number: int | float,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides script padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=number,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_staff_padding(
    n: int | float,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides script staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_up(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides script direction.

    ..  container:: example

        Up-overrides script direction on all leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(selector=lambda _: baca.select.pheads(_)),
        ...     baca.script_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Script.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \accent
                        [
                        d'16
                        - \accent
                        ]
                        bf'4
                        - \accent
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \accent
                        [
                        e''16
                        - \accent
                        ]
                        ef''4
                        - \accent
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent
                        [
                        g''16
                        - \accent
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \accent
                        r4
                        \revert Script.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def script_x_extent_zero(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides script X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="Script",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def slur_down(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Overrides slur direction on leaves:

        >>> def selector(argument):
        ...     selection = abjad.select.tuplets(argument)
        ...     items = [baca.tleaves(_) for _ in selection]
        ...     selection = abjad.select.nontrivial(items)
        ...     return selection
        ...
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.slur(map=selector),
        ...     baca.slur_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Slur.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        (
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        )
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        (
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        )
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert Slur.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.DOWN,
        grob="Slur",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def slur_up(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Up-overrides slur direction on leaves:

        >>> def selector(argument):
        ...     selection = abjad.select.tuplets(argument)
        ...     items = [baca.tleaves(_) for _ in selection]
        ...     selection = abjad.select.nontrivial(items)
        ...     return selection
        ...
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.slur(map=selector),
        ...     baca.slur_up(),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.tuplet_bracket_down(),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Slur.direction = #up
                        \override TupletBracket.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \override Stem.direction = #down
                        c'16
                        [
                        (
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        )
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        (
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        )
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert Stem.direction
                        r4
                        \revert Slur.direction
                        \revert TupletBracket.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.UP,
        grob="Slur",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def span_bar_color(
    color: str,
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    after: bool = False,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides span bar color.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
    *,
    after: bool = False,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides span bar extra offset.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides span bar transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="SpanBar",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_color(
    color: str = "#red",
    selector=lambda _: _select.pleaves(_),
    *,
    context: str = None,
) -> OverrideCommand:
    r"""
    Overrides stem color.

    ..  container:: example

        Overrides stem color on pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_color(color="#red"),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \override Stem.color = #red
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert Stem.color
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        context=context,
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_down(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides stem direction.

    ..  container:: example

        Down-overrides stem direction pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \override Stem.direction = #down
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert Stem.direction
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides stem extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_stencil_false(
    selector=lambda _: _select.pleaf(_, 0),
) -> OverrideCommand:
    """
    Overrides stem stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def stem_transparent(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    """
    Overrides stem transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Stem",
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_tremolo_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides stem tremolo extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="StemTremolo",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_up(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides stem direction.

    ..  container:: example

        Up-overrides stem direction on pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \override Stem.direction = #up
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \revert Stem.direction
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
        abjad.UP,
        first_tag,
        final_tag,
    )


def strict_note_spacing_off(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides spacing spanner strict note spacing.
    """
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
    selector=lambda _: _select.leaves(_),
    *,
    context: str = "Staff",
) -> OverrideCommand:
    r"""
    Overrides sustain pedal staff padding.

    ..  container:: example

        Overrides sustain pedal staff padding on leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=lambda _: baca.select.rleaves(_)),
        ...         map=lambda _: abjad.select.tuplets(_),
        ...     ),
        ...     baca.sustain_pedal_staff_padding(4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Staff.SustainPedalLineSpanner.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \sustainOn
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                        \sustainOff
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        \sustainOn
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        \sustainOff
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \sustainOn
                        r4
                        \sustainOff
                        \revert Staff.SustainPedalLineSpanner.staff-padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: _select.mmrests(_),
):
    """
    Colors multimeasure rests.
    """
    command = mmrest_color(color, selector=selector)
    _command.tag(_tags.TACET_COLORING, command)
    _command.tag(_tags.function_name(_frame()), command)
    command_ = _command.new(command, measures=measures)
    assert isinstance(command_, OverrideCommand)
    return command_


def text_script_color(
    color: str = "#red",
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script color.

    ..  container:: example

        Overrides text script color on all leaves:

        >>> def selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r'\markup "più mosso"'),
        ...     baca.markup(
        ...         r'\markup "lo stesso tempo"',
        ...         selector=selector,
        ...     ),
        ...     baca.text_script_color("#red"),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TextScript.color = #red
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup "più mosso"
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        ^ \markup "lo stesso tempo"
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TextScript.color
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.text_script_color("#red"),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script direction.

    ..  container:: example

        Down-overrides text script direction on leaves:

        >>> def selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r'\markup "più mosso"'),
        ...     baca.markup(
        ...         r'\markup "lo stesso tempo"',
        ...         selector=selector,
        ...     ),
        ...     baca.text_script_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TextScript.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup "più mosso"
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        ^ \markup "lo stesso tempo"
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TextScript.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.text_script_down()
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script extra offset.

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.text_script_extra_offset((0, 2)),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script font size.
    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script padding.

    ..  container:: example

        Overrides text script padding on leaves:

        >>> def selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r'\markup "più mosso"'),
        ...     baca.markup(
        ...         r'\markup "lo stesso tempo"',
        ...         selector=selector,
        ...     ),
        ...     baca.text_script_padding(4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TextScript.padding = 4
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup "più mosso"
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        ^ \markup "lo stesso tempo"
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TextScript.padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.text_script_padding(2),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script parent-alignment-X.
    """
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


def text_script_self_alignment_x(
    n: int | float,
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script self-alignment-X.
    """
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


def text_script_staff_padding(
    n: int | float,
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script staff padding.

    ..  container:: example

        Overrides text script staff padding on leaves:

        >>> def selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r'\markup "più mosso"'),
        ...     baca.markup(
        ...         r'\markup "lo stesso tempo"',
        ...         selector=selector,
        ...     ),
        ...     baca.text_script_staff_padding(n=4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TextScript.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup "più mosso"
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        ^ \markup "lo stesso tempo"
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TextScript.staff-padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markkup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.text_script_staff_padding(2)
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
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


def text_script_up(
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script direction.

    ..  container:: example

        Up-overrides text script direction on leaves:

        >>> def selector(argument):
        ...     result = abjad.select.tuplet(argument, 1)
        ...     result = baca.select.phead(result, 0)
        ...     return result
        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(r'\markup "più mosso"'),
        ...     baca.markup(
        ...         r'\markup "lo stesso tempo"',
        ...         selector=selector,
        ...     ),
        ...     baca.text_script_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TextScript.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        ^ \markup "più mosso"
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        ^ \markup "lo stesso tempo"
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TextScript.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_mmrests(accumulator.get(), head="Music")
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=lambda _: abjad.select.leaf(_, 1),
        ...     ),
        ...     baca.text_script_up()
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script X-offset.
    """
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
    selector=lambda _: _select.leaves(_),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script Y-offset.
    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides text spanner left padding.
    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides text spanner right padding.
    """
    return OverrideCommand(
        attribute="bound_details__right__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def text_spanner_staff_padding(
    n: int | float,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides text spanner staff padding.

    ..  container:: example

        Overrides text spanner staff padding on all trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.text_spanner_staff_padding(6),
        ...     baca.text_script_staff_padding(6),
        ...     baca.text_spanner(
        ...         "pont. => ord.",
        ...         selector=lambda _: baca.select.tleaves(_),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TextScript.staff-padding = 6
                        \override TextSpanner.staff-padding = 6
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        - \abjad-dashed-line-with-arrow
                        - \baca-text-spanner-left-text "pont."
                        - \baca-text-spanner-right-text "ord."
                        \startTextSpan
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        \stopTextSpan
                        r4
                        \revert TextScript.staff-padding
                        \revert TextSpanner.staff-padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides text spanner stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def text_spanner_transparent(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides text spanner transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TextSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )


def text_spanner_y_offset(
    n: int | float,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides text spanner Y-offset.
    """
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
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides tie direction.

    ..  container:: example

        Overrides tie direction on pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_up(),
        ...     baca.tie(
        ...         selector=lambda _: baca.select.pleaf(_, 0),
        ...     ),
        ...     baca.tie_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 5/4
                        r8
                        \override Stem.direction = #up
                        \override Tie.direction = #down
                        b'16
                        [
                        ~
                        b'16
                        ]
                        c''4
                        ~
                        c''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        b'16
                        [
                        b'16
                        ]
                        b'4
                        ~
                        b'16
                        r16
                    }
                    \times 4/5
                    {
                        b'16
                        \revert Stem.direction
                        \revert Tie.direction
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="Tie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.DOWN,
    )


def tie_up(
    selector=lambda _: _select.pleaves(_),
) -> OverrideCommand:
    r"""
    Overrides tie direction.

    ..  container:: example

        Overrides tie direction on pitched leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_down(),
        ...     baca.tie_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 5/4
                        r8
                        \override Stem.direction = #down
                        \override Tie.direction = #up
                        b'16
                        [
                        b'16
                        ]
                        c''4
                        ~
                        c''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8
                    {
                        b'16
                        [
                        b'16
                        ]
                        b'4
                        ~
                        b'16
                        r16
                    }
                    \times 4/5
                    {
                        b'16
                        \revert Stem.direction
                        \revert Tie.direction
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="Tie",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.UP,
    )


def time_signature_extra_offset(
    pair: tuple[int | float, int | float],
    selector: typing.Callable = lambda _: _select.hleaf(_, 0),
) -> OverrideCommand:
    r"""
    Overrides time signature extra offset.

    ..  container:: example

        Overrides time signature extra offset on leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.time_signature_extra_offset((-6, 0)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector: typing.Callable = lambda _: _select.hleaves(_),
) -> OverrideCommand:
    """
    Overrides time signature stencil property.
    """
    return OverrideCommand(
        attribute="stencil",
        context="Score",
        grob="TimeSignature",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=False,
    )


def time_signature_transparent(
    selector: typing.Callable = lambda _: _select.hleaves(_),
) -> OverrideCommand:
    r"""
    Overrides time signature transparency.

    ..  container:: example

        Makes all time signatures transparent:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.time_signature_transparent(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override Score.TimeSignature.transparent = ##t
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert Score.TimeSignature.transparent
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides trill spanner staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        grob="TrillSpanner",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def tuplet_bracket_down(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides tuplet bracket direction.

    ..  container:: example

        Overrides tuplet bracket direction on leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.tuplet_bracket_down(),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.direction = #down
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.DOWN,
    )


def tuplet_bracket_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    r"""
    Overrides tuplet bracket extra offset.

    ..  container:: example

        Overrides tuplet bracket extra offset on leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_extra_offset((-1, 0)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \once \override TupletBracket.extra-offset = #'(-1 . 0)
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_outside_staff_priority(
    n: int | float,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides tuplet bracket outside-staff-priority.
    """
    return OverrideCommand(
        attribute="outside_staff_priority",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=n,
    )


def tuplet_bracket_padding(
    n: int | float,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides tuplet bracket padding.
    """
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
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    """
    Overrides tuplet bracket shorten pair.
    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides tuplet bracket staff padding.

    ..  container:: example

        Overrides tuplet bracket staff padding on leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides tuplet bracket transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )


def tuplet_bracket_up(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    r"""
    Overrides tuplet bracket direction.

    ..  container:: example

        Override tuplet bracket direction on leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.tuplet_bracket_up(),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="TupletBracket",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=abjad.UP,
    )


def tuplet_number_denominator(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value="#tuplet-number::calc-denominator-text",
    )


def tuplet_number_extra_offset(
    pair: tuple[int | float, int | float],
    selector=lambda _: abjad.select.leaf(_, 0),
) -> OverrideCommand:
    r"""
    Overrides tuplet number extra offset.

    ..  container:: example

        Overrides tuplet number extra offset on leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.tuplet_number_extra_offset((-1, 0)),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \once \override TupletNumber.extra-offset = #'(-1 . 0)
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_number_text(
    string: str,
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    assert isinstance(string, str), repr(string)
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=string,
    )


def tuplet_number_transparent(
    selector=lambda _: _select.leaves(_),
) -> OverrideCommand:
    """
    Overrides tuplet number transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TupletNumber",
        selector=selector,
        tags=[_tags.function_name(_frame())],
        value=True,
    )
