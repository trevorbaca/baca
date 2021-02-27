"""
Override library.
"""
import inspect
import typing

import ide

import abjad

from . import classes, scoping, typings


def _site(frame):
    prefix = "baca"
    return scoping.site(frame, prefix)


### CLASSES ###


class OverrideCommand(scoping.Command):
    r"""
    Override command.

    ..  container:: example

        >>> baca.OverrideCommand()
        OverrideCommand(selector=baca.leaves(), tags=[])

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_after",
        "_attribute",
        "_blacklist",
        "_context",
        "_grob",
        "_tags",
        "_value",
        "_whitelist",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        after: bool = None,
        attribute: str = None,
        blacklist: typing.Tuple[type] = None,
        context: str = None,
        deactivate: bool = None,
        grob: str = None,
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = classes.select().leaves(),
        tag_measure_number: bool = None,
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
        value: typing.Any = None,
        whitelist: typing.Tuple[type] = None,
    ) -> None:
        scoping.Command.__init__(
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
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if blacklist is not None:
            assert isinstance(blacklist, tuple), repr(blacklist)
            assert all(issubclass(_, abjad.Leaf) for _ in blacklist)
        self._blacklist = blacklist
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        self._value = value
        if whitelist is not None:
            assert isinstance(whitelist, tuple), repr(whitelist)
            assert all(issubclass(_, abjad.Leaf) for _ in whitelist)
        self._whitelist = whitelist

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
        if self.blacklist:
            for leaf in leaves:
                if isinstance(leaf, self.blacklist):
                    message = f"{type(leaf).__name__} is forbidden."
                    raise Exception(message)
        if self.whitelist:
            for leaf in leaves:
                if not isinstance(leaf, self.whitelist):
                    names = ",".join(_.__name__ for _ in self.whitelist)
                    violator = type(leaf).__name__
                    message = f"only {names} (not {violator}) allowed."
                    raise Exception(message)
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
        if tag:
            tag = tag.append(abjad.Tag("baca.OverrideCommand._call(1)"))
        else:
            tag = abjad.Tag(abjad.Tag("baca.OverrideCommand._call(1)"))
        abjad.attach(literal, leaves[0], deactivate=self.deactivate, tag=tag)
        if once:
            return
        string = abjad.overrides.make_lilypond_revert_string(
            grob, attribute, context=lilypond_type
        )
        literal = abjad.LilyPondLiteral(string, "after")
        tag = self.get_tag(leaves[-1])
        if tag:
            tag = tag.append(abjad.Tag("baca.OverrideCommand._call(2)"))
        else:
            tag = abjad.Tag(abjad.Tag("baca.OverrideCommand._call(2)"))
        abjad.attach(literal, leaves[-1], deactivate=self.deactivate, tag=tag)

    ### PUBLIC PROPERTIES ###

    @property
    def after(self) -> typing.Optional[bool]:
        """
        Is true if command positions LilyPond command after selection.
        """
        return self._after

    @property
    def attribute(self) -> typing.Optional[str]:
        """
        Gets attribute name.
        """
        return self._attribute

    @property
    def blacklist(self) -> typing.Optional[typing.Tuple[type]]:
        """
        Gets blacklist leaves.
        """
        return self._blacklist

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

    @property
    def whitelist(self) -> typing.Optional[typing.Tuple[type]]:
        """
        Gets whitelist leaves.
        """
        return self._whitelist


### FACTORY FUNCTIONS ###


def accidental_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def accidental_font_size(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental font size.
    """
    return OverrideCommand(
        attribute="font_size",
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def accidental_stencil_false(
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def accidental_transparent(
    selector: abjad.Expression = classes.select().leaves(),
):
    """
    Overrides accidental transparency on.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def accidental_x_extent_false(
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def accidental_x_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental X-offset.
    """
    return OverrideCommand(
        attribute="X_offset",
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def accidental_y_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides accidental Y-offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        grob="Accidental",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def bar_line_color(
    color: str,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def bar_line_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def bar_line_transparent(
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    r"""
    Overrides bar line transparency.

    ..  container:: example

        Makes bar line before measure 1 transparent:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.rhythm(
        ...         rmakers.talea([1, 1, 1, -1], 8),
        ...         rmakers.beam(),
        ...         rmakers.extract_trivial(),
        ...     ),
        ...     baca.bar_line_transparent(selector=baca.group_by_measure()[1]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \override Score.BarLine.transparent = ##t
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
                            \revert Score.BarLine.transparent
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="BarLine",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def bar_line_x_extent(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def beam_positions(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selections)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 3/4
                    s1 * 3/4
                }
                \new Staff
                {
                    \times 4/5 {
                        \override Beam.positions = #'(6 . 6)
                        \override TupletBracket.staff-padding = 4
                        r8
                        \override Stem.direction = #up
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \times 4/5 {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def beam_stencil_false(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides beam stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Beam",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def beam_transparent(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides beam transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Beam",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def clef_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides clef extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def clef_shift(
    clef: typing.Union[str, abjad.Clef],
    selector: abjad.Expression = classes.select().leaf(0),
) -> scoping.Suite:
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
    suite = scoping.suite(clef_x_extent_false(), clef_extra_offset((extra_offset_x, 0)))
    scoping.tag(_site(inspect.currentframe()), suite)
    scoping.tag(ide.tags.SHIFTED_CLEF, suite, tag_measure_number=True)
    return suite


def clef_whiteout(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides clef whiteout.
    """
    return OverrideCommand(
        attribute="whiteout",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def clef_x_extent_false(
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides clef x-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        context="Staff",
        grob="Clef",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def dls_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides dynamic line spanner padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="DynamicLineSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dls_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        ...             'p < f',
        ...             remove_length_1_spanner_start=True,
        ...             selector=baca.tleaves(),
        ...             ),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override DynamicLineSpanner.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def dls_up(
    selector: abjad.Expression = classes.select().leaves(),
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
        ...             'p < f',
        ...             remove_length_1_spanner_start=True,
        ...             selector=baca.tleaves(),
        ...             ),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override DynamicLineSpanner.direction = #up
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def dots_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides dots extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Dots",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def dots_stencil_false(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides dots stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Dots",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def dots_transparent(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides dots transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Dots",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dots_x_extent_false(
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides dots X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="Dots",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def dynamic_text_color(
    color: str = "#red",
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text color.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().pleaf(0),
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
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].pleaf(0)),
        ...     baca.dynamic_text_extra_offset((-3, 0)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_parent_alignment_x(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text parent alignment X to ``n``.
    """
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_self_alignment_x(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text self-alignment-X to ``n``.
    """
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_stencil_false(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_transparent(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_x_extent_zero(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_x_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_text_y_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides dynamic text Y-extent.
    """
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        grob="DynamicText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def flag_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides flag extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Flag",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def flag_stencil_false(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides flag stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Flag",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def flag_transparent(
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    """
    Overrides flag transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Flag",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def glissando_thickness(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    """
    Overrides glissando thickness.
    """
    return OverrideCommand(
        attribute="thickness",
        value=str(n),
        grob="Glissando",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def hairpin_shorten_pair(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="Hairpin",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def hairpin_start_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    selector: abjad.Expression = classes.select().leaf(0),
) -> scoping.Suite:
    """
    Shifts hairpin start dynamic to left by width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    suite = scoping.suite(
        dynamic_text_extra_offset((extra_offset_x, 0)),
        dynamic_text_x_extent_zero(),
        hairpin_shorten_pair((hairpin_shorten_left, 0)),
    )
    scoping.tag(_site(inspect.currentframe()), suite)
    return suite


def hairpin_stencil_false(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="Hairpin",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def hairpin_to_barline(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin to-barline to true.
    """
    return OverrideCommand(
        attribute="to_barline",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def hairpin_transparent(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides hairpin transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Hairpin",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def laissez_vibrer_tie_down(
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def laissez_vibrer_tie_up(
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="LaissezVibrerTie",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def mmrest_color(
    color: str = "#red",
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest color.


    ..  container:: example

        REGRESSION. Coerces X11 color names:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.mmrest_color("#(x11-color 'DarkOrchid)"),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override MultiMeasureRest.color = #(x11-color 'DarkOrchid)
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \revert MultiMeasureRest.color
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_transparent(
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRest",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_color(
    color: str = "#red",
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text color.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r"\baca-boxed-markup still",
        ...         literal=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_color("#red"),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override MultiMeasureRestText.color = #red
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            ^ \baca-boxed-markup still
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \revert MultiMeasureRestText.color
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    ..  container:: example exception

        Raises exception when called on leaves other than multimeasure
        rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_color("#red", selector=baca.leaves()),
        ...     baca.pitches([2, 4]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: only MultimeasureRest (not Note) allowed.

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text extra offset.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_extra_offset((0, 2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override MultiMeasureRestText.extra-offset = #'(0 . 2)
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            ^ \baca-boxed-markup still
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \revert MultiMeasureRestText.extra-offset
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        value=f"#'({pair[0]} . {pair[1]})",
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text padding.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_padding(2),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override MultiMeasureRestText.padding = 2
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            ^ \baca-boxed-markup still
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \revert MultiMeasureRestText.padding
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_parent_center(
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text parent alignment X to center.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_parent_center(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override MultiMeasureRestText.parent-alignment-X = 0
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            ^ \baca-boxed-markup still
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \revert MultiMeasureRestText.parent-alignment-X
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=0,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest text staff padding.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_staff_padding(2),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override MultiMeasureRestText.staff-padding = 2
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            R1 * 3/8
                            ^ \baca-boxed-markup still
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            R1 * 4/8
                            %@% ^ \baca-duration-multiplier-markup #"4" #"8"
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            R1 * 3/8
                            %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                            \revert MultiMeasureRestText.staff-padding
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_transparent(
    selector: abjad.Expression = classes.select().mmrests(),
) -> OverrideCommand:
    """
    Overrides script transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="MultiMeasureRestText",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        whitelist=(abjad.MultimeasureRest,),
    )


def no_ledgers(
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def note_column_shift(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides note column force hshift.
    """
    return OverrideCommand(
        attribute="force_hshift",
        value=n,
        grob="NoteColumn",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def note_head_color(
    color: str,
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="color",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=color,
    )


def note_head_duration_log(
    n: int,
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    """
    Overrides note-head duration-log property.
    """
    return OverrideCommand(
        attribute="duration_log",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def note_head_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def note_head_font_size(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head font size.
    """
    return OverrideCommand(
        attribute="font_size",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def note_head_no_ledgers(
    value: bool,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers property.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=value,
    )


def note_head_stencil_false(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def note_head_style(
    string: str,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head style property.
    """
    return OverrideCommand(
        attribute="style",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=string,
    )


def note_head_style_cross(
    selector: abjad.Expression = classes.select().pleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        value="cross",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def note_head_style_harmonic(
    selector: abjad.Expression = classes.select().pleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        value="harmonic",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def note_head_style_harmonic_black(
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    r"""
    Overrides note-head style to harmonic-black.
    """
    return OverrideCommand(
        attribute="style",
        value="harmonic-black",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def note_head_transparent(
    selector: abjad.Expression = classes.select().pleaves(),
):
    """
    Overrides note-head transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def note_head_x_extent_zero(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides note-head X-extent.

    ..  todo:: Set note-head X-extent to zero rather than false.

    """
    return OverrideCommand(
        attribute="X_extent",
        grob="NoteHead",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=(0, 0),
    )


def ottava_bracket_shorten_pair(
    pair: abjad.NumberPair = (-0.8, -0.6),
    selector: abjad.Expression = classes.select().leaves(),
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
        tags=[_site(inspect.currentframe())],
    )


def ottava_bracket_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        tags=[_site(inspect.currentframe())],
    )


def rehearsal_mark_down(
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def rehearsal_mark_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def rehearsal_mark_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def rehearsal_mark_self_alignment_x(
    n: typings.HorizontalAlignmentTyping,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def rehearsal_mark_y_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def repeat_tie_down(
    selector: abjad.Expression = classes.select().pleaves(),
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
        ...         baca.repeat_tie(selector=baca.pleaves()[1:]),
        ...         map=baca.qruns(),
        ...         ),
        ...     baca.repeat_tie_down(),
        ...     baca.stem_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 7/8 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def repeat_tie_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides repeat tie extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="RepeatTie",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def repeat_tie_stencil_false(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides repeat tie stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="RepeatTie",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def repeat_tie_transparent(
    selector: abjad.Expression = classes.select().pleaves(),
):
    """
    Overrides repeat tie transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="RepeatTie",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def repeat_tie_up(
    selector: abjad.Expression = classes.select().pleaves(),
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
        ...         baca.repeat_tie(selector=baca.pleaves()[1:]),
        ...         map=baca.qruns(),
        ...         ),
        ...     baca.repeat_tie_up(),
        ...     baca.stem_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 7/8 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def rest_color(
    color: str,
    selector: abjad.Expression = classes.select().rest(0),
) -> OverrideCommand:
    """
    Overrides rest extra offset.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="Rest",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def rest_down(
    selector: abjad.Expression = classes.select().rests(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Rest.direction = #down
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def rest_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().rest(0),
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
        tags=[_site(inspect.currentframe())],
    )


def rest_position(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().rests(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Rest.staff-position = -6
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def rest_transparent(
    selector: abjad.Expression = classes.select().rests(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Rest.transparent = ##t
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def rest_up(
    selector: abjad.Expression = classes.select().rests(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Rest.direction = #up
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def rest_x_extent_zero(
    selector: abjad.Expression = classes.select().rest(0),
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
        tags=[_site(inspect.currentframe())],
        value=(0, 0),
    )


def script_color(
    color: str = "#red",
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.script_color("#red"),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Script.color = #red
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def script_down(
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.script_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Script.direction = #down
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def script_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.script_extra_offset((-1.5, 0), selector=baca.leaf(1)),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def script_padding(
    number: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides script padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=number,
        grob="Script",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def script_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides script staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="Script",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def script_up(
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.accent(selector=baca.pheads()),
        ...     baca.script_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Script.direction = #up
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def script_x_extent_zero(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides script X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="Script",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def slur_down(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Overrides slur direction on leaves:

        >>> selector = baca.tuplets().map(baca.tleaves()).nontrivial()
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Slur.direction = #down
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def slur_up(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    r"""
    Overrides slur direction.

    ..  container:: example

        Up-overrides slur direction on leaves:

        >>> selector = baca.tuplets().map(baca.tleaves()).nontrivial()
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Slur.direction = #up
                        \override TupletBracket.staff-padding = 2
                        \override TupletBracket.direction = #down
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def span_bar_color(
    color: str,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def span_bar_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def span_bar_transparent(
    selector: abjad.Expression = classes.select().leaf(0),
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
        tags=[_site(inspect.currentframe())],
    )


def stem_color(
    color: str = "#red",
    selector: abjad.Expression = classes.select().pleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def stem_down(
    selector: abjad.Expression = classes.select().pleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def stem_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides stem extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="Stem",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_stencil_false(
    selector: abjad.Expression = classes.select().pleaf(0),
) -> OverrideCommand:
    """
    Overrides stem stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="Stem",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def stem_transparent(
    selector: abjad.Expression = classes.select().pleaves(),
) -> OverrideCommand:
    """
    Overrides stem transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="Stem",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def stem_tremolo_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides stem tremolo extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="StemTremolo",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def stem_up(
    selector: abjad.Expression = classes.select().pleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def strict_note_spacing_off(
    selector: abjad.Expression = classes.select().leaves(),
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
        tags=[_site(inspect.currentframe())],
    )


def sustain_pedal_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        ...         baca.sustain_pedal(selector=baca.rleaves()),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Staff.SustainPedalLineSpanner.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def text_script_color(
    color: str = "#red",
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.text_script_color("#red"),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextScript.color = #red
                        \override TupletBracket.staff-padding = 2
                        r8
                        c'16
                        ^ \markup { più mosso }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        ^ \markup { lo stesso tempo }
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
                    \times 4/5 {
                        a'16
                        r4
                        \revert TextScript.color
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_color("#red"),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="color",
        blacklist=blacklist,
        value=color,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def text_script_down(
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.text_script_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextScript.direction = #down
                        \override TupletBracket.staff-padding = 2
                        r8
                        c'16
                        ^ \markup { più mosso }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        ^ \markup { lo stesso tempo }
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
                    \times 4/5 {
                        a'16
                        r4
                        \revert TextScript.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_down()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="direction",
        blacklist=blacklist,
        value=abjad.Down,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def text_script_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    r"""
    Overrides text script extra offset.

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_extra_offset((0, 2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="extra_offset",
        blacklist=blacklist,
        value=f"#'({pair[0]} . {pair[1]})",
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def text_script_font_size(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script font size.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="font_size",
        blacklist=blacklist,
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def text_script_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.text_script_padding(4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextScript.padding = 4
                        \override TupletBracket.staff-padding = 2
                        r8
                        c'16
                        ^ \markup { più mosso }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        ^ \markup { lo stesso tempo }
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
                    \times 4/5 {
                        a'16
                        r4
                        \revert TextScript.padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_padding(2),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="padding",
        blacklist=blacklist,
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def text_script_parent_alignment_x(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script parent-alignment-X.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="parent_alignment_X",
        blacklist=blacklist,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def text_script_self_alignment_x(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script self-alignment-X.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="self_alignment_X",
        blacklist=blacklist,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def text_script_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.text_script_staff_padding(n=4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextScript.staff-padding = 4
                        \override TupletBracket.staff-padding = 2
                        r8
                        c'16
                        ^ \markup { più mosso }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        ^ \markup { lo stesso tempo }
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
                    \times 4/5 {
                        a'16
                        r4
                        \revert TextScript.staff-padding
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markkup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_staff_padding(2)
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="staff_padding",
        blacklist=blacklist,
        value=n,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def text_script_up(
    selector: abjad.Expression = classes.select().leaves(),
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
        ...     baca.markup('più mosso'),
        ...     baca.markup(
        ...         'lo stesso tempo',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.text_script_up(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextScript.direction = #up
                        \override TupletBracket.staff-padding = 2
                        r8
                        c'16
                        ^ \markup { più mosso }
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        ^ \markup { lo stesso tempo }
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
                    \times 4/5 {
                        a'16
                        r4
                        \revert TextScript.direction
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example exception

        Raises exception when called on multimeasure rests:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.markup(
        ...         r'\baca-boxed-markup still',
        ...         literal=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_up()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: MultimeasureRest is forbidden.

    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="direction",
        blacklist=blacklist,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=abjad.Up,
    )


def text_script_x_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script X-offset.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="X_offset",
        blacklist=blacklist,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def text_script_y_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
    *,
    allow_mmrests: bool = False,
) -> OverrideCommand:
    """
    Overrides text script Y-offset.
    """
    if allow_mmrests is True:
        blacklist = None
    else:
        blacklist = (abjad.MultimeasureRest,)
    return OverrideCommand(
        attribute="Y_offset",
        blacklist=blacklist,
        grob="TextScript",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def text_spanner_left_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner left padding.
    """
    return OverrideCommand(
        attribute="bound_details__left__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def text_spanner_right_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner right padding.
    """
    return OverrideCommand(
        attribute="bound_details__right__padding",
        grob="TextSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def text_spanner_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        ...         'pont. => ord.',
        ...         selector=baca.tleaves(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> string = abjad.LilyPondFormatManager.align_tags(string, 89)
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextSpanner.staff-padding = 6
                        \override TextScript.staff-padding = 6
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
    )


def text_spanner_stencil_false(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="TextSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def text_spanner_transparent(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TextSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=True,
    )


def text_spanner_y_offset(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides text spanner Y-offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        grob="TextSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def tie_down(
    selector: abjad.Expression = classes.select().pleaves(),
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
        ...     baca.tie(selector=baca.pleaf(0)),
        ...     baca.tie_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[11, 11, 12], [11, 11, 11], [11]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 7/8 {
                        b'16
                        [
                        b'16
                        ]
                        b'4
                        ~
                        b'16
                        r16
                    }
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=abjad.Down,
    )


def tie_up(
    selector: abjad.Expression = classes.select().pleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 5/4
                    s1 * 5/4
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 7/8 {
                        b'16
                        [
                        b'16
                        ]
                        b'4
                        ~
                        b'16
                        r16
                    }
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=abjad.Up,
    )


def time_signature_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().hleaf(0),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def time_signature_stencil_false(
    selector: abjad.Expression = classes.select().hleaves(),
) -> OverrideCommand:
    """
    Overrides time signature stencil property.
    """
    return OverrideCommand(
        attribute="stencil",
        context="Score",
        grob="TimeSignature",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=False,
    )


def time_signature_transparent(
    selector: abjad.Expression = classes.select().hleaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Score.TimeSignature.transparent = ##t
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=True,
    )


def trill_spanner_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides trill spanner staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        grob="TrillSpanner",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def tuplet_bracket_down(
    selector: abjad.Expression = classes.select().leaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        \override TupletBracket.direction = #down
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=abjad.Down,
    )


def tuplet_bracket_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \once \override TupletBracket.extra-offset = #'(-1 . 0)
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_outside_staff_priority(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet bracket outside-staff-priority.
    """
    return OverrideCommand(
        attribute="outside_staff_priority",
        grob="TupletBracket",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def tuplet_bracket_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet bracket padding.
    """
    return OverrideCommand(
        attribute="padding",
        grob="TupletBracket",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def tuplet_bracket_shorten_pair(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
) -> OverrideCommand:
    """
    Overrides tuplet bracket shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        grob="TupletBracket",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_bracket_staff_padding(
    n: abjad.Number,
    selector: abjad.Expression = classes.select().leaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=n,
    )


def tuplet_bracket_transparent(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet bracket transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TupletBracket",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=True,
    )


def tuplet_bracket_up(
    selector: abjad.Expression = classes.select().leaves(),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        \override TupletBracket.direction = #up
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=abjad.Up,
    )


def tuplet_number_denominator(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value="tuplet-number::calc-denominator-text",
    )


def tuplet_number_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.Expression = classes.select().leaf(0),
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
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = 2
                        \once \override TupletNumber.extra-offset = #'(-1 . 0)
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
                    \times 9/10 {
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
                    \times 4/5 {
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
        tags=[_site(inspect.currentframe())],
        value=f"#'({pair[0]} . {pair[1]})",
    )


def tuplet_number_text(
    markup: abjad.Markup,
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    assert isinstance(markup, abjad.Markup), repr(markup)
    return OverrideCommand(
        attribute="text",
        grob="TupletNumber",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=markup,
    )


def tuplet_number_transparent(
    selector: abjad.Expression = classes.select().leaves(),
) -> OverrideCommand:
    """
    Overrides tuplet number transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="TupletNumber",
        selector=selector,
        tags=[_site(inspect.currentframe())],
        value=True,
    )
