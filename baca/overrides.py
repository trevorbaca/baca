"""
Overrides.
"""
import typing
from inspect import currentframe as _frame

import abjad

from . import scoping as _scoping
from . import selectors as _selectors
from . import tags as _tags
from . import typings


class OverrideCommand(_scoping.Command):
    r"""
    Override command.

    ..  container:: example

        >>> baca.OverrideCommand()
        OverrideCommand()

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_after",
        "_allowlist",
        "_attribute",
        "_blocklist",
        "_context",
        "_grob",
        "_tags",
        "_value",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        after: bool = None,
        allowlist: typing.Tuple[type] = None,
        attribute: str = None,
        blocklist: typing.Tuple[type] = None,
        context: str = None,
        deactivate: bool = None,
        grob: str = None,
        map=None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: _scoping.ScopeTyping = None,
        selector=_selectors.leaves(),
        tag_measure_number: bool = None,
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
        value: typing.Any = None,
    ) -> None:
        _scoping.Command.__init__(
            self,
            deactivate=deactivate,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tag_measure_number=tag_measure_number,
            tags=tags,
        )
        if after is not None:
            after = bool(after)
        self._after = after
        if allowlist is not None:
            assert isinstance(allowlist, tuple), repr(allowlist)
            assert all(issubclass(_, abjad.Leaf) for _ in allowlist)
        self._allowlist = allowlist
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if blocklist is not None:
            assert isinstance(blocklist, tuple), repr(blocklist)
            assert all(issubclass(_, abjad.Leaf) for _ in blocklist)
        self._blocklist = blocklist
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        self._value = value

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves()
        if self.blocklist:
            for leaf in leaves:
                if isinstance(leaf, self.blocklist):
                    raise Exception(f"{type(leaf).__name__} is forbidden.")
        if self.allowlist:
            for leaf in leaves:
                if not isinstance(leaf, self.allowlist):
                    names = ",".join(_.__name__ for _ in self.allowlist)
                    violator = type(leaf).__name__
                    raise Exception(f"only {names} (not {violator}) allowed.")
        lilypond_type = self.context
        if lilypond_type is not None:
            assert isinstance(lilypond_type, (str)), repr(lilypond_type)
        if lilypond_type in dir(abjad):
            context = getattr(abjad, lilypond_type)
            assert issubclass(context, abjad.Context), repr(context)
            context = abjad.get.parentage(leaves[0]).get(context) or context()
            lilypond_type = context.lilypond_type
            assert isinstance(lilypond_type, str), repr(lilypond_type)
        grob = self.grob
        attribute = self.attribute
        value = self.value
        once = bool(len(leaves) == 1)
        string = abjad.overrides.make_lilypond_override_string(
            grob, attribute, value, context=lilypond_type, once=once
        )
        format_slot = "before"
        if self.after is True:
            format_slot = "after"
        literal = abjad.LilyPondLiteral(string, format_slot)
        tag = self.get_tag(leaves[0])
        site = _scoping.site(_frame(), self, n=1)
        if tag:
            tag = tag.append(site)
        else:
            tag = site
        abjad.attach(literal, leaves[0], deactivate=self.deactivate, tag=tag)
        if once:
            return
        string = abjad.overrides.make_lilypond_revert_string(
            grob, attribute, context=lilypond_type
        )
        literal = abjad.LilyPondLiteral(string, "after")
        tag = self.get_tag(leaves[-1])
        site = _scoping.site(_frame(), self, n=2)
        if tag:
            tag = tag.append(site)
        else:
            tag = site
        abjad.attach(literal, leaves[-1], deactivate=self.deactivate, tag=tag)

    ### PUBLIC PROPERTIES ###

    @property
    def after(self) -> typing.Optional[bool]:
        """
        Is true if command positions LilyPond command after selection.
        """
        return self._after

    @property
    def allowlist(self) -> typing.Optional[typing.Tuple[type]]:
        """
        Gets allowlist leaves.
        """
        return self._allowlist

    @property
    def attribute(self) -> typing.Optional[str]:
        """
        Gets attribute name.
        """
        return self._attribute

    @property
    def blocklist(self) -> typing.Optional[typing.Tuple[type]]:
        """
        Gets blocklist leaves.
        """
        return self._blocklist

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context name.
        """
        return self._context

    @property
    def grob(self) -> typing.Optional[str]:
        """
        Gets grob name.
        """
        return self._grob

    @property
    def value(self) -> typing.Any:
        """
        Gets attribute value.
        """
        return self._value


def accidental_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def accidental_font_size(
    n: abjad.Number,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental font size.
    """
    return OverrideCommand(
        attribute="font_size",
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def accidental_stencil_false(
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def accidental_transparent(
    selector=_selectors.leaves(),
):
    """
    Overrides accidental transparency on.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def accidental_x_extent_false(
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def accidental_x_offset(
    n: abjad.Number,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental X-offset.
    """
    return OverrideCommand(
        attribute="X_offset",
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def accidental_y_offset(
    n: abjad.Number,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental Y-offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        grob="Accidental",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def bar_line_color(
    color: str,
    selector=_selectors.leaf(0),
    *,
    after: bool = None,
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
        tags=[_scoping.site(_frame())],
    )


def bar_line_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
    *,
    after: bool = None,
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
        tags=[_scoping.site(_frame())],
    )


def bar_line_transparent(
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    r"""
    Overrides bar line transparency.

    ..  container:: example

        Makes bar line before measure 1 transparent:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.rhythm(
        ...         rmakers.talea([1, 1, 1, -1], 8),
        ...         rmakers.beam(),
        ...         rmakers.extract_trivial(),
        ...     ),
        ...     baca.bar_line_transparent(
        ...         selector=lambda _: baca.Selection(_).group_by_measure()[1]
        ...     ),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
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
        tags=[_scoping.site(_frame())],
    )


def bar_line_x_extent(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
    *,
    after: bool = None,
    context: str = "Score",
    measures: typings.SliceTyping = None,
) -> OverrideCommand:
    """
    Overrides bar line X extent.
    """
    return OverrideCommand(
        after=after,
        attribute="X_extent",
        value=f"#'({pair[0]} . {pair[1]})",
        context=context,
        measures=measures,
        grob="BarLine",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def beam_positions(
    n: abjad.Number,
    selector=_selectors.leaves(),
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
    if not isinstance(n, (int, float)):
        message = f"beam position must be number (not {n})."
        raise Exception(message)
    return OverrideCommand(
        attribute="positions",
        value=f"#'({n} . {n})",
        grob="Beam",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def beam_stencil_false(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides beam stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Beam",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def beam_transparent(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides beam transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Beam",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def clef_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides clef extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def clef_shift(
    clef: typing.Union[str, abjad.Clef],
    selector=_selectors.leaf(0),
) -> _scoping.Suite:
    """
    Shifts clef to left by width of clef.
    """
    extra_offset_x: typing.Union[int, float]
    if isinstance(clef, str):
        clef = abjad.Clef(clef)
    if isinstance(clef, (int, float)):
        extra_offset_x = clef
    else:
        assert isinstance(clef, abjad.Clef)
        width = clef._to_width[clef.name]
        extra_offset_x = -width
    suite = _scoping.suite(
        clef_x_extent_false(), clef_extra_offset((extra_offset_x, 0))
    )
    _scoping.tag(_scoping.site(_frame()), suite)
    _scoping.tag(_tags.SHIFTED_CLEF, suite, tag_measure_number=True)
    return suite


def clef_whiteout(
    n: abjad.Number,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides clef whiteout.
    """
    return OverrideCommand(
        attribute="whiteout",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def clef_x_extent_false(
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides clef x-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def dls_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides dynamic line spanner padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dls_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
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
        ...             selector=baca.selectors.tleaves(),
        ...             ),
        ...         map=baca.selectors.tuplets(),
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
                        \<
                        [
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
                        \<
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
        tags=[_scoping.site(_frame())],
    )


def dls_up(
    selector=_selectors.leaves(),
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
        ...             selector=baca.selectors.tleaves(),
        ...             ),
        ...         map=baca.selectors.tuplets(),
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
                        \<
                        [
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
                        \<
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
        value=abjad.Up,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dots_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides dots extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Dots",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def dots_stencil_false(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides dots stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Dots",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def dots_transparent(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides dots transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Dots",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dots_x_extent_false(
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides dots X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Dots",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def dynamic_text_color(
    color: str = "#red",
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text color.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    r"""
    Overrides dynamic text extra offset.

    ..  container:: example

        Overrides dynamic text extra offset on pitched leaf 0:

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
        ...     baca.dynamic(
        ...         "f",
        ...         selector=lambda _: baca.Selection(_).tuplets()[1:2].pleaf(0),
        ...     ),
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
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_parent_alignment_x(
    n: abjad.Number,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text parent alignment X to ``n``.
    """
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_self_alignment_x(
    n: abjad.Number,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text self-alignment-X to ``n``.
    """
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_stencil_false(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_transparent(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_x_extent_zero(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_x_offset(
    n: abjad.Number,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def dynamic_text_y_offset(
    n: abjad.Number,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text Y-extent.
    """
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def flag_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides flag extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Flag",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def flag_stencil_false(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides flag stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Flag",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def flag_transparent(
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    """
    Overrides flag transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Flag",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def glissando_thickness(
    n: abjad.Number,
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    """
    Overrides glissando thickness.
    """
    return OverrideCommand(
        attribute="thickness",
        value=str(n),
        grob="Glissando",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def hairpin_shorten_pair(
    pair: abjad.NumberPair,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Hairpin",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def hairpin_start_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    selector=_selectors.leaf(0),
) -> _scoping.Suite:
    """
    Shifts hairpin start dynamic to left by width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    suite = _scoping.suite(
        dynamic_text_extra_offset((extra_offset_x, 0)),
        dynamic_text_x_extent_zero(),
        hairpin_shorten_pair((hairpin_shorten_left, 0)),
    )
    _scoping.tag(_scoping.site(_frame()), suite)
    return suite


def hairpin_stencil_false(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="Hairpin",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def hairpin_to_barline(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin to-barline to true.
    """
    return OverrideCommand(
        attribute="to_barline",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def hairpin_transparent(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def laissez_vibrer_tie_down(
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def laissez_vibrer_tie_up(
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def mmrest_color(
    color: str = "#red",
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest color.


    ..  container:: example

        REGRESSION. Coerces X11 color names:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.mmrest_color("#(x11-color 'DarkOrchid)"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override MultiMeasureRest.color = #(x11-color 'DarkOrchid)
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
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
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_transparent(
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_color(
    color: str = "#red",
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text color.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.mmrest(1),
        ...     ),
        ...     baca.mmrest_text_color("#red"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override MultiMeasureRestText.color = #red
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.make_notes(),
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.mmrest_text_color("#red", selector=baca.selectors.leaves()),
        ...     baca.pitches([2, 4]),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
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
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text extra offset.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.mmrest(1),
        ...     ),
        ...     baca.mmrest_text_extra_offset((0, 2)),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override MultiMeasureRestText.extra-offset = #'(0 . 2)
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
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
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_padding(
    n: abjad.Number,
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text padding.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.mmrest(1),
        ...     ),
        ...     baca.mmrest_text_padding(2),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override MultiMeasureRestText.padding = 2
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
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
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_parent_center(
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text parent alignment X to center.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.mmrest(1),
        ...     ),
        ...     baca.mmrest_text_parent_center(),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override MultiMeasureRestText.parent-alignment-X = 0
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
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
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_staff_padding(
    n: abjad.Number,
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text staff padding.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.mmrest(1),
        ...     ),
        ...     baca.mmrest_text_staff_padding(2),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.make_lilypond_file(
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
                \context Staff = "Music_Staff"
                <<
                    \context Voice = "Global_Skips"
                    {
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 1/2
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override MultiMeasureRestText.staff-padding = 2
                        R1 * 4/8
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                        R1 * 3/8
                        ^ \baca-boxed-markup still
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                        R1 * 4/8
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
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def mmrest_text_transparent(
    selector=_selectors.mmrests(),
) -> OverrideCommand:
    """
    Overrides script transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_scoping.site(_frame())],
        allowlist=(abjad.MultimeasureRest,),
    )


def no_ledgers(
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def note_column_shift(
    n: abjad.Number,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides note column force hshift.
    """
    return OverrideCommand(
        attribute="force_hshift",
        value=n,
        grob="NoteColumn",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def note_head_color(
    color: str,
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="color",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=color,
    )


def note_head_duration_log(
    n: int,
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    """
    Overrides note-head duration-log property.
    """
    return OverrideCommand(
        attribute="duration_log",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def note_head_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def note_head_font_size(
    n: abjad.Number,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head font size.
    """
    return OverrideCommand(
        attribute="font_size",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def note_head_no_ledgers(
    value: bool,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers property.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=value,
    )


def note_head_stencil_false(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def note_head_style(
    string: str,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head style property.
    """
    return OverrideCommand(
        attribute="style",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=string,
    )


def note_head_style_cross(
    selector=_selectors.pleaves(),
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
        tags=[_scoping.site(_frame())],
    )


def note_head_style_harmonic(
    selector=_selectors.pleaves(),
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
        tags=[_scoping.site(_frame())],
    )


def note_head_style_harmonic_black(
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    r"""
    Overrides note-head style to harmonic-black.
    """
    return OverrideCommand(
        attribute="style",
        value="#'harmonic-black",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def note_head_transparent(
    selector=_selectors.pleaves(),
):
    """
    Overrides note-head transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def note_head_x_extent_zero(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head X-extent.

    ..  todo:: Set note-head X-extent to zero rather than false.

    """
    return OverrideCommand(
        attribute="X_extent",
        grob="NoteHead",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=(0, 0),
    )


def ottava_bracket_shorten_pair(
    pair: abjad.NumberPair = (-0.8, -0.6),
    selector=_selectors.leaves(),
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
        tags=[_scoping.site(_frame())],
    )


def ottava_bracket_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
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
        tags=[_scoping.site(_frame())],
    )


def rehearsal_mark_down(
    selector=_selectors.leaf(0),
    *,
    context: str = "Score",
) -> OverrideCommand:
    """
    Overrides rehearsal mark direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        context=context,
        grob="RehearsalMark",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def rehearsal_mark_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
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
        tags=[_scoping.site(_frame())],
    )


def rehearsal_mark_padding(
    n: abjad.Number,
    selector=_selectors.leaf(0),
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
        tags=[_scoping.site(_frame())],
    )


def rehearsal_mark_self_alignment_x(
    n: typings.HorizontalAlignmentTyping,
    selector=_selectors.leaf(0),
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
        tags=[_scoping.site(_frame())],
    )


def rehearsal_mark_y_offset(
    n: abjad.Number,
    selector=_selectors.leaf(0),
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
        tags=[_scoping.site(_frame())],
    )


def repeat_tie_down(
    selector=_selectors.pleaves(),
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
        ...         baca.repeat_tie(selector=baca.selectors.pleaves((1, None))),
        ...         map=baca.selectors.qruns(),
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
                        \repeatTie
                        ]
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
                        \repeatTie
                        ]
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
        value=abjad.Down,
        grob="RepeatTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def repeat_tie_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides repeat tie extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="RepeatTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def repeat_tie_stencil_false(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides repeat tie stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="RepeatTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def repeat_tie_transparent(
    selector=_selectors.pleaves(),
):
    """
    Overrides repeat tie transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="RepeatTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def repeat_tie_up(
    selector=_selectors.pleaves(),
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
        ...             selector=baca.selectors.pleaves((1, None)),
        ...         ),
        ...         map=baca.selectors.qruns(),
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
                        \repeatTie
                        ]
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
                        \repeatTie
                        ]
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
        value=abjad.Up,
        grob="RepeatTie",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def rest_color(
    color: str,
    selector=_selectors.rest(0),
) -> OverrideCommand:
    """
    Overrides rest extra offset.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="Rest",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def rest_down(
    selector=_selectors.rests(),
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
        value=abjad.Down,
        grob="Rest",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def rest_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.rest(0),
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
        tags=[_scoping.site(_frame())],
    )


def rest_position(
    n: abjad.Number,
    selector=_selectors.rests(),
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
        tags=[_scoping.site(_frame())],
    )


def rest_transparent(
    selector=_selectors.rests(),
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
        tags=[_scoping.site(_frame())],
    )


def rest_up(
    selector=_selectors.rests(),
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
        value=abjad.Up,
        grob="Rest",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def rest_x_extent_zero(
    selector=_selectors.rest(0),
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
        tags=[_scoping.site(_frame())],
        value=(0, 0),
    )


def script_color(
    color: str = "#red",
    selector=_selectors.leaves(),
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
        ...     baca.accent(selector=baca.selectors.pheads()),
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
        tags=[_scoping.site(_frame())],
    )


def script_down(
    selector=_selectors.leaves(),
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
        ...     baca.accent(selector=baca.selectors.pheads()),
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
        value=abjad.Down,
        grob="Script",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def script_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
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
        ...     baca.accent(selector=baca.selectors.pheads()),
        ...     baca.script_extra_offset((-1.5, 0), selector=baca.selectors.leaf(1)),
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
        tags=[_scoping.site(_frame())],
    )


def script_padding(
    number: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides script padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=number,
        grob="Script",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def script_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides script staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="Script",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def script_up(
    selector=_selectors.leaves(),
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
        ...     baca.accent(selector=baca.selectors.pheads()),
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
        value=abjad.Up,
        grob="Script",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def script_x_extent_zero(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides script X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="Script",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def slur_down(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Overrides slur direction on leaves:

        >>> def selector(argument):
        ...     selection = baca.Selection(argument).tuplets()
        ...     items = [baca.Selection(_).tleaves() for _ in selection]
        ...     selection = baca.Selection(items).nontrivial()
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
        value=abjad.Down,
        grob="Slur",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def slur_up(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Up-overrides slur direction on leaves:

        >>> def selector(argument):
        ...     selection = baca.Selection(argument).tuplets()
        ...     items = [baca.Selection(_).tleaves() for _ in selection]
        ...     selection = baca.Selection(items).nontrivial()
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
                        \override TupletBracket.staff-padding = 2
                        \override TupletBracket.direction = #down
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
                        \revert TupletBracket.staff-padding
                        \revert TupletBracket.direction
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="Slur",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def span_bar_color(
    color: str,
    selector=_selectors.leaf(0),
    *,
    after: bool = None,
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
        tags=[_scoping.site(_frame())],
    )


def span_bar_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
    *,
    after: bool = None,
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
        tags=[_scoping.site(_frame())],
    )


def span_bar_transparent(
    selector=_selectors.leaf(0),
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
        tags=[_scoping.site(_frame())],
    )


def stem_color(
    color: str = "#red",
    selector=_selectors.pleaves(),
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
        tags=[_scoping.site(_frame())],
    )


def stem_down(
    selector=_selectors.pleaves(),
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
        value=abjad.Down,
        grob="Stem",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def stem_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides stem extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Stem",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_stencil_false(
    selector=_selectors.pleaf(0),
) -> OverrideCommand:
    """
    Overrides stem stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Stem",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def stem_transparent(
    selector=_selectors.pleaves(),
) -> OverrideCommand:
    """
    Overrides stem transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Stem",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def stem_tremolo_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides stem tremolo extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="StemTremolo",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_up(
    selector=_selectors.pleaves(),
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
        value=abjad.Up,
        grob="Stem",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def strict_note_spacing_off(
    selector=_selectors.leaves(),
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
        tags=[_scoping.site(_frame())],
    )


def sustain_pedal_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
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
        ...         baca.sustain_pedal(selector=baca.selectors.rleaves()),
        ...         map=baca.selectors.tuplets(),
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
        tags=[_scoping.site(_frame())],
    )


def text_script_color(
    color: str = "#red",
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script color.

    ..  container:: example

        Overrides text script color on all leaves:

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
        ...         selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0),
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.text_script_color("#red"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="color",
        blocklist=blocklist,
        value=color,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def text_script_down(
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script direction.

    ..  container:: example

        Down-overrides text script direction on leaves:

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
        ...         selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0),
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.text_script_down()
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="direction",
        blocklist=blocklist,
        value=abjad.Down,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def text_script_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script extra offset.

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.text_script_extra_offset((0, 2)),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="extra_offset",
        blocklist=blocklist,
        value=f"#'({pair[0]} . {pair[1]})",
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def text_script_font_size(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script font size.
    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="font_size",
        blocklist=blocklist,
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def text_script_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script padding.

    ..  container:: example

        Overrides text script padding on leaves:

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
        ...         selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0),
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.text_script_padding(2),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="padding",
        blocklist=blocklist,
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def text_script_parent_alignment_x(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script parent-alignment-X.
    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="parent_alignment_X",
        blocklist=blocklist,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def text_script_self_alignment_x(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script self-alignment-X.
    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="self_alignment_X",
        blocklist=blocklist,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def text_script_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script staff padding.

    ..  container:: example

        Overrides text script staff padding on leaves:

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
        ...         selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0),
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markkup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.text_script_staff_padding(2)
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="staff_padding",
        blocklist=blocklist,
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def text_script_up(
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script direction.

    ..  container:: example

        Up-overrides text script direction on leaves:

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
        ...         selector=lambda _: baca.Selection(_).tuplets()[1:2].phead(0),
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
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         selector=baca.selectors.leaf(1),
        ...     ),
        ...     baca.text_script_up()
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="direction",
        blocklist=blocklist,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=abjad.Up,
    )


def text_script_x_offset(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script X-offset.
    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="X_offset",
        blocklist=blocklist,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def text_script_y_offset(
    n: abjad.Number,
    selector=_selectors.leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script Y-offset.
    """
    if allow_mmrests is True:
        blocklist = None
    else:
        blocklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="Y_offset",
        blocklist=blocklist,
        grob="TextScript",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def text_spanner_left_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner left padding.
    """
    return OverrideCommand(
        attribute="bound_details__left__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def text_spanner_right_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner right padding.
    """
    return OverrideCommand(
        attribute="bound_details__right__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def text_spanner_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
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
        ...         selector=baca.selectors.tleaves(),
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
                        \override TextSpanner.staff-padding = 6
                        \override TextScript.staff-padding = 6
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        - \abjad-dashed-line-with-arrow
                        - \baca-text-spanner-left-text "pont."
                        - \baca-text-spanner-right-text "ord."
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
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
                        \revert TextSpanner.staff-padding
                        \revert TextScript.staff-padding
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
        tags=[_scoping.site(_frame())],
    )


def text_spanner_stencil_false(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="TextSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def text_spanner_transparent(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TextSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=True,
    )


def text_spanner_y_offset(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner Y-offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        grob="TextSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def tie_down(
    selector=_selectors.pleaves(),
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
        ...         selector=baca.selectors.pleaf(0),
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
        tags=[_scoping.site(_frame())],
        value=abjad.Down,
    )


def tie_up(
    selector=_selectors.pleaves(),
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
        tags=[_scoping.site(_frame())],
        value=abjad.Up,
    )


def time_signature_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.hleaf(0),
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
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def time_signature_stencil_false(
    selector=_selectors.hleaves(),
) -> OverrideCommand:
    """
    Overrides time signature stencil property.
    """
    return OverrideCommand(
        attribute="stencil",
        context="Score",
        grob="TimeSignature",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=False,
    )


def time_signature_transparent(
    selector=_selectors.hleaves(),
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
        tags=[_scoping.site(_frame())],
        value=True,
    )


def trill_spanner_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides trill spanner staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        grob="TrillSpanner",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def tuplet_bracket_down(
    selector=_selectors.leaves(),
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
                        \override TupletBracket.staff-padding = 2
                        \override TupletBracket.direction = #down
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
                        \revert TupletBracket.direction
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="TupletBracket",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=abjad.Down,
    )


def tuplet_bracket_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
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
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_outside_staff_priority(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet bracket outside-staff-priority.
    """
    return OverrideCommand(
        attribute="outside_staff_priority",
        grob="TupletBracket",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def tuplet_bracket_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet bracket padding.
    """
    return OverrideCommand(
        attribute="padding",
        grob="TupletBracket",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=n,
    )


def tuplet_bracket_shorten_pair(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
) -> OverrideCommand:
    """
    Overrides tuplet bracket shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        grob="TupletBracket",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_staff_padding(
    n: abjad.Number,
    selector=_selectors.leaves(),
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
        tags=[_scoping.site(_frame())],
        value=n,
    )


def tuplet_bracket_transparent(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet bracket transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TupletBracket",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=True,
    )


def tuplet_bracket_up(
    selector=_selectors.leaves(),
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
                        \override TupletBracket.staff-padding = 2
                        \override TupletBracket.direction = #up
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
                        \revert TupletBracket.direction
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="TupletBracket",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=abjad.Up,
    )


def tuplet_number_denominator(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value="#tuplet-number::calc-denominator-text",
    )


def tuplet_number_extra_offset(
    pair: abjad.NumberPair,
    selector=_selectors.leaf(0),
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
                        \override TupletBracket.staff-padding = 2
                        \once \override TupletNumber.extra-offset = #'(-1 . 0)
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
        tags=[_scoping.site(_frame())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_number_text(
    markup: abjad.Markup,
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    assert isinstance(markup, abjad.Markup), repr(markup)
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=markup,
    )


def tuplet_number_transparent(
    selector=_selectors.leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet number transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TupletNumber",
        selector=selector,
        tags=[_scoping.site(_frame())],
        value=True,
    )
