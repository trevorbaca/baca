"""
Override library.
"""
import abjad
import typing
from . import scoping
from . import typings


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
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaves()",
        tag_measure_number: bool = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
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
        if attribute == "color" and value not in abjad.ly.colors:
            raise Exception(f"{repr(value)} is not a LilyPond color.")
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
            context = (
                abjad.inspect(leaves[0]).parentage().get(context) or context()
            )
            lilypond_type = context.lilypond_type
            assert isinstance(lilypond_type, str), repr(lilypond_type)
        grob = self.grob
        attribute = self.attribute
        value = self.value
        if attribute == "color" and value not in abjad.ly.normal_colors:
            value = f"#(x11-color '{value})"
        once = bool(len(leaves) == 1)
        string = abjad.LilyPondFormatManager.make_lilypond_override_string(
            grob, attribute, value, context=lilypond_type, once=once
        )
        format_slot = "before"
        if self.after is True:
            format_slot = "after"
        literal = abjad.LilyPondLiteral(string, format_slot)
        tag = self.get_tag(leaves[0])
        if tag:
            tag = tag.append("OverrideCommand(1)")
        else:
            tag = abjad.Tag("OverrideCommand(1)")
        abjad.attach(literal, leaves[0], deactivate=self.deactivate, tag=tag)
        if once:
            return
        string = abjad.LilyPondFormatManager.make_lilypond_revert_string(
            grob, attribute, context=lilypond_type
        )
        literal = abjad.LilyPondLiteral(string, "after")
        tag = self.get_tag(leaves[-1])
        if tag:
            tag = tag.append("OverrideCommand(2)")
        else:
            tag = abjad.Tag("OverrideCommand(2)")
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
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.accidental_extra_offset",
) -> OverrideCommand:
    """
    Overrides accidental stencil.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="accidental",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def accidental_stencil_false(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.accidental_stencil_false",
) -> OverrideCommand:
    """
    Overrides accidental stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="accidental",
        selector=selector,
        tags=[tag],
        value=False,
    )


def accidental_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.accidental_transparent",
):
    """
    Overrides accidental transparency on.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="accidental",
        selector=selector,
        tags=[tag],
    )


def accidental_x_extent_false(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.accidental_x_extent_false",
) -> OverrideCommand:
    """
    Overrides accidental X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        grob="accidental",
        selector=selector,
        tags=[tag],
        value=False,
    )


def bar_line_color(
    color: str,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    after: bool = None,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.bar_line_color",
) -> OverrideCommand:
    """
    Overrides bar line color.
    """
    return OverrideCommand(
        after=after,
        attribute="color",
        value=color,
        context=context,
        grob="bar_line",
        selector=selector,
        tags=[tag],
    )


def bar_line_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    after: bool = None,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.bar_line_extra_offset",
) -> OverrideCommand:
    """
    Overrides bar line extra offset.
    """
    return OverrideCommand(
        after=after,
        attribute="extra_offset",
        value=pair,
        context=context,
        grob="bar_line",
        selector=selector,
        tags=[tag],
    )


def bar_line_transparent(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.bar_line_transparent",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
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
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override Score.BarLine.transparent = ##t                                %! baca.bar_line_transparent:OverrideCommand(1)
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
                            \revert Score.BarLine.transparent                                        %! baca.bar_line_transparent:OverrideCommand(2)
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
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
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    c'1 * 1/4                                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="bar_line",
        selector=selector,
        tags=[tag],
    )


def bar_line_x_extent(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    after: bool = None,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.bar_line_x_extent",
) -> OverrideCommand:
    """
    Overrides bar line X extent.
    """
    return OverrideCommand(
        after=after,
        attribute="X_extent",
        value=pair,
        context=context,
        grob="bar_line",
        selector=selector,
        tags=[tag],
    )


def beam_positions(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.beam_positions",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP
        
        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Beam.positions = #'(6 . 6)                                         %! baca.beam_positions:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #4                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override Stem.direction = #up                                               %! baca.stem_up:OverrideCommand(1)
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
                        \revert Stem.direction                                                       %! baca.stem_up:OverrideCommand(2)
                        r4
                        \revert Beam.positions                                                       %! baca.beam_positions:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    if not isinstance(n, (int, float)):
        message = f"beam position must be number (not {n})."
        raise Exception(message)
    return OverrideCommand(
        attribute="positions",
        value=(n, n),
        grob="beam",
        selector=selector,
        tags=[tag],
    )


def beam_stencil_false(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.beam_stencil_false",
) -> OverrideCommand:
    """
    Overrides beam stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="beam",
        selector=selector,
        tags=[tag],
        value=False,
    )


def beam_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.beam_transparent",
) -> OverrideCommand:
    """
    Overrides beam transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="beam",
        selector=selector,
        tags=[tag],
    )


def clef_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.clef_extra_offset",
) -> OverrideCommand:
    """
    Overrides clef extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        context="Staff",
        grob="clef",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def clef_shift(
    clef: typing.Union[str, abjad.Clef],
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.clef_shift",
) -> scoping.Suite:
    """
    Shifts clef to left by width of clef.
    """
    if isinstance(clef, str):
        clef = abjad.Clef(clef)
    if isinstance(clef, (int, float)):
        extra_offset_x = clef
    else:
        assert isinstance(clef, abjad.Clef)
        width = clef._to_width[clef.name]
        extra_offset_x = -width
    suite = scoping.suite(
        clef_x_extent_false(tag=tag),
        clef_extra_offset((extra_offset_x, 0), tag=tag),
    )
    scoping.tag(abjad.tags.SHIFTED_CLEF, suite, tag_measure_number=True)
    return suite


def clef_x_extent_false(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.clef_x_extent_false",
) -> OverrideCommand:
    """
    Overrides clef x-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        context="Staff",
        grob="clef",
        selector=selector,
        tags=[tag],
        value=False,
    )


def dls_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.dls_padding",
) -> OverrideCommand:
    """
    Overrides dynamic line spanner padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="dynamic_line_spanner",
        selector=selector,
        tags=[tag],
    )


def dls_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.dls_staff_padding",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override DynamicLineSpanner.staff-padding = #4                              %! baca.dls_staff_padding:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        \p                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(1)
                        \<                                                                           %! baca.hairpin:PiecewiseCommand(1)
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        \f                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(2)
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        \p                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(1)
                        \<                                                                           %! baca.hairpin:PiecewiseCommand(1)
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
                        \f                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(2)
                        ]
                    }
                    \times 4/5 {
                        a'16
                        \p                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(1)
                        r4
                        \revert DynamicLineSpanner.staff-padding                                     %! baca.dls_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="dynamic_line_spanner",
        selector=selector,
        tags=[tag],
    )


def dls_up(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.dls_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override DynamicLineSpanner.direction = #up                                 %! baca.dls_up:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        \p                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(1)
                        \<                                                                           %! baca.hairpin:PiecewiseCommand(1)
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        \f                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(2)
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        \p                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(1)
                        \<                                                                           %! baca.hairpin:PiecewiseCommand(1)
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
                        \f                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(2)
                        ]
                    }
                    \times 4/5 {
                        a'16
                        \p                                                                           %! SPANNER_STOP:baca.hairpin:PiecewiseCommand(1)
                        r4
                        \revert DynamicLineSpanner.direction                                         %! baca.dls_up:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="dynamic_line_spanner",
        selector=selector,
        tags=[tag],
    )


def dots_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.dots_extra_offset",
) -> OverrideCommand:
    """
    Overrides dots extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="dots",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def dots_stencil_false(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.dots_stencil_false",
) -> OverrideCommand:
    """
    Overrides dots stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="dots",
        selector=selector,
        tags=[tag],
        value=False,
    )


def dots_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.dots_transparent",
) -> OverrideCommand:
    """
    Overrides dots transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="dots",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_color(
    color: str = "red",
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_color",
) -> OverrideCommand:
    """
    Overrides dynamic text color.
    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_extra_offset",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \once \override DynamicText.extra-offset = #'(-3 . 0)                        %! baca.dynamic_text_extra_offset:OverrideCommand(1)
                        c'16
                        \p                                                                           %! baca.dynamic:IndicatorCommand
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
                        \f                                                                           %! baca.dynamic:IndicatorCommand
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        raise Exception(
            f"dynamic text extra offset must be pair (not {pair})."
        )
    if len(pair) != 2:
        raise Exception(
            f"dynamic text extra offset must be pair (not {pair})."
        )
    return OverrideCommand(
        attribute="extra_offset",
        value=pair,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_parent_alignment_x(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_parent_alignment_x",
) -> OverrideCommand:
    """
    Overrides dynamic text parent alignment X to ``n``.
    """
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=n,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_self_alignment_x(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_self_alignment_x",
) -> OverrideCommand:
    """
    Overrides dynamic text self-alignment-X to ``n``.
    """
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_stencil_false(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_stencil_false",
) -> OverrideCommand:
    """
    Overrides dynamic text stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_transparent(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_transparent",
) -> OverrideCommand:
    """
    Overrides dynamic text transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_x_extent_zero(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_x_extent_zero",
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_x_offset(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_x_offset",
) -> OverrideCommand:
    """
    Overrides dynamic text X-extent.
    """
    return OverrideCommand(
        attribute="X_offset",
        value=n,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def dynamic_text_y_offset(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.dynamic_text_y_offset",
) -> OverrideCommand:
    """
    Overrides dynamic text Y-extent.
    """
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        grob="dynamic_text",
        selector=selector,
        tags=[tag],
    )


def flag_stencil_false(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.flag_stencil_false",
) -> OverrideCommand:
    """
    Overrides flag stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="flag",
        selector=selector,
        tags=[tag],
        value=False,
    )


def flag_transparent(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.flag_transparent",
) -> OverrideCommand:
    """
    Overrides flag transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="flag",
        selector=selector,
        tags=[tag],
    )


def glissando_thickness(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.glissando_thickness",
) -> OverrideCommand:
    """
    Overrides glissando thickness.
    """
    return OverrideCommand(
        attribute="thickness",
        value=str(n),
        grob="glissando",
        selector=selector,
        tags=[tag],
    )


def hairpin_shorten_pair(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.hairpin_shorten_pair",
) -> OverrideCommand:
    """
    Overrides hairpin shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        value=pair,
        grob="hairpin",
        selector=selector,
        tags=[tag],
    )


def hairpin_start_shift(
    dynamic: typing.Union[str, abjad.Dynamic],
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.hairpin_start_shift",
) -> scoping.Suite:
    """
    Shifts hairpin start dynamic to left by width of dynamic.
    """
    dynamic = abjad.Dynamic(dynamic)
    width = dynamic._to_width[dynamic.name]
    extra_offset_x = -width
    hairpin_shorten_left = width - 1.25
    return scoping.suite(
        dynamic_text_extra_offset((extra_offset_x, 0), tag=tag),
        dynamic_text_x_extent_zero(tag=tag),
        hairpin_shorten_pair((hairpin_shorten_left, 0), tag=tag),
    )


def hairpin_stencil_false(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.hairpin_stencil_false",
) -> OverrideCommand:
    """
    Overrides hairpin stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        value=False,
        grob="hairpin",
        selector=selector,
        tags=[tag],
    )


def hairpin_to_barline(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.hairpin_to_barline",
) -> OverrideCommand:
    """
    Overrides hairpin to-barline to true.
    """
    return OverrideCommand(
        attribute="to_barline",
        value=True,
        grob="hairpin",
        selector=selector,
        tags=[tag],
    )


def hairpin_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.hairpin_transparent",
) -> OverrideCommand:
    """
    Overrides hairpin transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="hairpin",
        selector=selector,
        tags=[tag],
    )


def laissez_vibrer_tie_down(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.laissez_vibrer_tie_down",
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="laissez_vibrer_tie",
        selector=selector,
        tags=[tag],
    )


def laissez_vibrer_tie_up(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.laissez_vibrer_tie_up",
) -> OverrideCommand:
    r"""
    Overrides laissez-vibrer-tie direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="laissez_vibrer_tie",
        selector=selector,
        tags=[tag],
    )


def mmrest_color(
    color: str = "red",
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_text_color",
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
        ...     baca.mmrest_color('DarkOrchid'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override MultiMeasureRest.color = #(x11-color 'DarkOrchid)              %! baca.mmrest_text_color:OverrideCommand(1)
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            \revert MultiMeasureRest.color                                           %! baca.mmrest_text_color:OverrideCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="multi_measure_rest",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_transparent(
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_transparent",
) -> OverrideCommand:
    r"""
    Overrides multimeasure rest transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="multi_measure_rest",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_color(
    color: str = "red",
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_text_color",
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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_color('red'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override MultiMeasureRestText.color = #red                              %! baca.mmrest_text_color:OverrideCommand(1)
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            ^ \markup {                                                              %! baca.markup:IndicatorCommand
                                \override                                                            %! baca.markup:IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! baca.markup:IndicatorCommand
                                    \box                                                             %! baca.markup:IndicatorCommand
                                        still                                                        %! baca.markup:IndicatorCommand
                                }                                                                    %! baca.markup:IndicatorCommand
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            \revert MultiMeasureRestText.color                                       %! baca.mmrest_text_color:OverrideCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.mmrest_text_color('red', selector=baca.leaves()),
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
        grob="multi_measure_rest_text",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_text_extra_offset",
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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_extra_offset((0, 2)),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override MultiMeasureRestText.extra-offset = #'(0 . 2)                  %! baca.mmrest_text_extra_offset:OverrideCommand(1)
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            ^ \markup {                                                              %! baca.markup:IndicatorCommand
                                \override                                                            %! baca.markup:IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! baca.markup:IndicatorCommand
                                    \box                                                             %! baca.markup:IndicatorCommand
                                        still                                                        %! baca.markup:IndicatorCommand
                                }                                                                    %! baca.markup:IndicatorCommand
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            \revert MultiMeasureRestText.extra-offset                                %! baca.mmrest_text_extra_offset:OverrideCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return OverrideCommand(
        attribute="extra_offset",
        value=pair,
        grob="multi_measure_rest_text",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_text_padding",
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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_padding(2),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override MultiMeasureRestText.padding = #2                              %! baca.mmrest_text_padding:OverrideCommand(1)
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            ^ \markup {                                                              %! baca.markup:IndicatorCommand
                                \override                                                            %! baca.markup:IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! baca.markup:IndicatorCommand
                                    \box                                                             %! baca.markup:IndicatorCommand
                                        still                                                        %! baca.markup:IndicatorCommand
                                }                                                                    %! baca.markup:IndicatorCommand
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            \revert MultiMeasureRestText.padding                                     %! baca.mmrest_text_padding:OverrideCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        grob="multi_measure_rest_text",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_parent_center(
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_text_parent_center",
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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_parent_center(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override MultiMeasureRestText.parent-alignment-X = #0                   %! baca.mmrest_text_parent_center:OverrideCommand(1)
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            ^ \markup {                                                              %! baca.markup:IndicatorCommand
                                \override                                                            %! baca.markup:IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! baca.markup:IndicatorCommand
                                    \box                                                             %! baca.markup:IndicatorCommand
                                        still                                                        %! baca.markup:IndicatorCommand
                                }                                                                    %! baca.markup:IndicatorCommand
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            \revert MultiMeasureRestText.parent-alignment-X                          %! baca.mmrest_text_parent_center:OverrideCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return OverrideCommand(
        attribute="parent_alignment_X",
        value=0,
        grob="multi_measure_rest_text",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.mmrest_text_staff_padding",
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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.mmrest(1),
        ...         ),
        ...     baca.mmrest_text_staff_padding(2),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:baca.SegmentMaker._attach_color_literal(2)
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                        \baca-bar-line-visible                                                       %! baca.SegmentMaker._attach_final_bar_line()
                        \bar "|"                                                                     %! baca.SegmentMaker._attach_final_bar_line()
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):baca.SegmentMaker._comment_measure_numbers()
                        \time 1/4                                                                    %! PHANTOM:baca.SegmentMaker._style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:baca.SegmentMaker._make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:baca.SegmentMaker._style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:baca.SegmentMaker._make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \override MultiMeasureRestText.staff-padding = #2                        %! baca.mmrest_text_staff_padding:OverrideCommand(1)
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            ^ \markup {                                                              %! baca.markup:IndicatorCommand
                                \override                                                            %! baca.markup:IndicatorCommand
                                    #'(box-padding . 0.5)                                            %! baca.markup:IndicatorCommand
                                    \box                                                             %! baca.markup:IndicatorCommand
                                        still                                                        %! baca.markup:IndicatorCommand
                                }                                                                    %! baca.markup:IndicatorCommand
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                                 %! _call_rhythm_commands
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                                 %! _call_rhythm_commands
                            \revert MultiMeasureRestText.staff-padding                               %! baca.mmrest_text_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \baca-invisible-music                                            %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._make_multimeasure_rest_container()
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
                                {                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:baca.SegmentMaker._style_phantom_measures(5):baca.SegmentMaker._comment_measure_numbers()
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:baca.SegmentMaker._style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:baca.SegmentMaker._style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                                }                                                                    %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:baca.SegmentMaker._make_multimeasure_rest_container()
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="multi_measure_rest_text",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def mmrest_text_transparent(
    selector: abjad.SelectorTyping = "baca.mmrests()",
    *,
    tag: typing.Optional[str] = "baca.script_transparent",
) -> OverrideCommand:
    """
    Overrides script transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="multi_measure_rest_text",
        selector=selector,
        tags=[tag],
        whitelist=(abjad.MultimeasureRest,),
    )


def no_ledgers(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.no_ledgers",
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        value=True,
        grob="note_head",
        selector=selector,
        tags=[tag],
    )


def note_column_shift(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.note_colun_shift",
) -> OverrideCommand:
    """
    Overrides note column force hshift.
    """
    return OverrideCommand(
        attribute="force_hshift",
        value=n,
        grob="note_column",
        selector=selector,
        tags=[tag],
    )


def note_head_color(
    color: str,
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.note_head_color",
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="color",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=color,
    )


def note_head_duration_log(
    n: int,
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.note_head_color",
) -> OverrideCommand:
    """
    Overrides note-head duration-log property.
    """
    return OverrideCommand(
        attribute="duration_log",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=n,
    )


def note_head_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.note_head_extra_offset",
) -> OverrideCommand:
    """
    Overrides note-head color.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def note_head_no_ledgers(
    value: bool,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.note_head_extra_offset",
) -> OverrideCommand:
    """
    Overrides note-head no-ledgers property.
    """
    return OverrideCommand(
        attribute="no_ledgers",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=value,
    )


def note_head_stencil_false(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.note_head_stencil_false",
) -> OverrideCommand:
    """
    Overrides note-head stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=False,
    )


def note_head_style(
    string: str,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.note_head_stencil_false",
) -> OverrideCommand:
    """
    Overrides note-head style property.
    """
    return OverrideCommand(
        attribute="style",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=string,
    )


def note_head_style_cross(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.note_head_style_cross",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override NoteHead.style = #'cross                                           %! baca.note_head_style_cross:OverrideCommand(1)
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
                        \revert NoteHead.style                                                       %! baca.note_head_style_cross:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="style",
        value="cross",
        grob="note_head",
        selector=selector,
        tags=[tag],
    )


def note_head_style_harmonic(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.note_head_style_harmonic",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override NoteHead.style = #'harmonic                                        %! baca.note_head_style_harmonic:OverrideCommand(1)
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
                        \revert NoteHead.style                                                       %! baca.note_head_style_harmonic:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="style",
        value="harmonic",
        grob="note_head",
        selector=selector,
        tags=[tag],
    )


def note_head_style_harmonic_black(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.note_head_style_harmonic_black",
) -> OverrideCommand:
    r"""
    Overrides note-head style to harmonic-black.
    """
    return OverrideCommand(
        attribute="style",
        value="harmonic-black",
        grob="note_head",
        selector=selector,
        tags=[tag],
    )


def note_head_transparent(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.note_head_transparent",
):
    """
    Overrides note-head transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="note_head",
        selector=selector,
        tags=[tag],
    )


def note_head_x_extent_zero(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.note_head_x_extent_zero",
) -> OverrideCommand:
    """
    Overrides note-head X-extent.

    ..  todo:: Set note-head X-extent to zero rather than false.

    """
    return OverrideCommand(
        attribute="X_extent",
        grob="note_head",
        selector=selector,
        tags=[tag],
        value=(0, 0),
    )


def ottava_bracket_shorten_pair(
    pair: abjad.NumberPair = (-0.8, -0.6),
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.ottava_bracket_shorten_pair",
) -> OverrideCommand:
    """
    Overrides ottava bracket shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        context="Staff",
        value=pair,
        grob="ottava_bracket",
        selector=selector,
        tags=[tag],
    )


def ottava_bracket_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.ottava_bracket_staff_padding",
) -> OverrideCommand:
    """
    Overrides ottava bracket staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        context="Staff",
        value=n,
        grob="ottava_bracket",
        selector=selector,
        tags=[tag],
    )


def rehearsal_mark_down(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.rehearsal_mark_down",
) -> OverrideCommand:
    """
    Overrides rehearsal mark direction.
    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        context=context,
        grob="rehearsal_mark",
        selector=selector,
        tags=[tag],
    )


def rehearsal_mark_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.rehearsal_mark_extra_offset",
) -> OverrideCommand:
    """
    Overrides rehearsal mark extra offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        value=pair,
        context=context,
        grob="rehearsal_mark",
        selector=selector,
        tags=[tag],
    )


def rehearsal_mark_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.rehearsal_padding",
) -> OverrideCommand:
    """
    Overrides rehearsal mark padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=n,
        context=context,
        grob="rehearsal_mark",
        selector=selector,
        tags=[tag],
    )


def rehearsal_mark_self_alignment_x(
    n: typings.HorizontalAlignmentTyping,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.rehearsal_mark_self_alignment_x",
) -> OverrideCommand:
    """
    Overrides rehearsal mark self-alignment-X.
    """
    return OverrideCommand(
        attribute="self_alignment_X",
        value=n,
        context=context,
        grob="rehearsal_mark",
        selector=selector,
        tags=[tag],
    )


def rehearsal_mark_y_offset(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.rehearsal_mark_y_offset",
) -> OverrideCommand:
    """
    Overrides rehearsal mark Y offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        value=n,
        context=context,
        grob="rehearsal_mark",
        selector=selector,
        tags=[tag],
    )


def repeat_tie_down(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.repeat_tie_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override RepeatTie.direction = #down                                        %! baca.repeat_tie_down:OverrideCommand(1)
                        \override Stem.direction = #up                                               %! baca.stem_up:OverrideCommand(1)
                        b'16
                        [
                        b'16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        ]
                        c''4
                        ~
                        c''16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        b'16
                        [
                        b'16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        ]
                        b'4
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        ~
                        b'16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        r16
                    }
                    \times 4/5 {
                        b'16
                        \revert RepeatTie.direction                                                  %! baca.repeat_tie_down:OverrideCommand(2)
                        \revert Stem.direction                                                       %! baca.stem_up:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="repeat_tie",
        selector=selector,
        tags=[tag],
    )


def repeat_tie_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.repeat_tie_extra_offset",
) -> OverrideCommand:
    """
    Overrides repeat tie extra-offset.
    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="repeat_tie",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def repeat_tie_stencil_false(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.repeat_tie_stencil_false",
) -> OverrideCommand:
    """
    Overrides repeat tie stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="repeat_tie",
        selector=selector,
        tags=[tag],
        value=False,
    )


def repeat_tie_transparent(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.repeat_tie_transparent",
):
    """
    Overrides repeat tie transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="repeat_tie",
        selector=selector,
        tags=[tag],
    )


def repeat_tie_up(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.repeat_tie_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override RepeatTie.direction = #up                                          %! baca.repeat_tie_up:OverrideCommand(1)
                        \override Stem.direction = #down                                             %! baca.stem_down:OverrideCommand(1)
                        b'16
                        [
                        b'16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        ]
                        c''4
                        ~
                        c''16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        b'16
                        [
                        b'16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        ]
                        b'4
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        ~
                        b'16
                        \repeatTie                                                                   %! baca.repeat_tie:IndicatorCommand
                        r16
                    }
                    \times 4/5 {
                        b'16
                        \revert RepeatTie.direction                                                  %! baca.repeat_tie_up:OverrideCommand(2)
                        \revert Stem.direction                                                       %! baca.stem_down:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="repeat_tie",
        selector=selector,
        tags=[tag],
    )


def rest_down(
    selector: abjad.SelectorTyping = "baca.rests()",
    *,
    tag: typing.Optional[str] = "baca.rest_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Rest.direction = #down                                             %! baca.rest_down:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert Rest.direction                                                       %! baca.rest_down:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="rest",
        selector=selector,
        tags=[tag],
    )


def rest_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.rest(0)",
    *,
    tag: typing.Optional[str] = "baca.rest_extra_offset",
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
        value=pair,
        grob="rest",
        selector=selector,
        tags=[tag],
    )


def rest_position(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.rests()",
    *,
    tag: typing.Optional[str] = "baca.rest_position",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Rest.staff-position = #-6                                          %! baca.rest_position:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert Rest.staff-position                                                  %! baca.rest_position:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="staff_position",
        value=n,
        grob="rest",
        selector=selector,
        tags=[tag],
    )


def rest_transparent(
    selector: abjad.SelectorTyping = "baca.rests()",
    *,
    tag: typing.Optional[str] = "baca.rest_transparent",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Rest.transparent = ##t                                             %! baca.rest_transparent:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert Rest.transparent                                                     %! baca.rest_transparent:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="rest",
        selector=selector,
        tags=[tag],
    )


def rest_up(
    selector: abjad.SelectorTyping = "baca.rests()",
    *,
    tag: typing.Optional[str] = "baca.rest_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Rest.direction = #up                                               %! baca.rest_up:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert Rest.direction                                                       %! baca.rest_up:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="rest",
        selector=selector,
        tags=[tag],
    )


def script_color(
    color: str = "red",
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.script_color",
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
        ...     baca.script_color('red'),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Script.color = #red                                                %! baca.script_color:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        d'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        bf'4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        e''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        ef''4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        g''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                    }
                    \times 4/5 {
                        a'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        r4
                        \revert Script.color                                                         %! baca.script_color:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        grob="script",
        selector=selector,
        tags=[tag],
    )


def script_down(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.script_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Script.direction = #down                                           %! baca.script_down:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        d'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        bf'4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        e''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        ef''4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        g''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                    }
                    \times 4/5 {
                        a'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        r4
                        \revert Script.direction                                                     %! baca.script_down:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="script",
        selector=selector,
        tags=[tag],
    )


def script_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.script_extra_offset",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \once \override Script.extra-offset = #'(-1.5 . 0)                           %! baca.script_extra_offset:OverrideCommand(1)
                        c'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        d'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        bf'4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        e''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        ef''4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        g''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                    }
                    \times 4/5 {
                        a'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        value=pair,
        grob="script",
        selector=selector,
        tags=[tag],
    )


def script_padding(
    number: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.script_padding",
) -> OverrideCommand:
    """
    Overrides script padding.
    """
    return OverrideCommand(
        attribute="padding",
        value=number,
        grob="script",
        selector=selector,
        tags=[tag],
    )


def script_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.script_staff_padding",
) -> OverrideCommand:
    """
    Overrides script staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="script",
        selector=selector,
        tags=[tag],
    )


def script_up(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.script_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Script.direction = #up                                             %! baca.script_up:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        d'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        bf'4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        e''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                        ef''4
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ~
                        ef''16
                        r16
                        af''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        [
                        g''16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        ]
                    }
                    \times 4/5 {
                        a'16
                        - \accent                                                                    %! baca.accent:IndicatorCommand
                        r4
                        \revert Script.direction                                                     %! baca.script_up:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="script",
        selector=selector,
        tags=[tag],
    )


def script_x_extent_zero(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.script_x_extent_zero",
) -> OverrideCommand:
    """
    Overrides script X-extent.
    """
    return OverrideCommand(
        attribute="X_extent",
        value=(0, 0),
        grob="script",
        selector=selector,
        tags=[tag],
    )


def slur_down(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.slur_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Slur.direction = #down                                             %! baca.slur_down:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        [
                        (                                                                            %! baca.slur:SpannerIndicatorCommand(1)
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        )                                                                            %! SPANNER_STOP:baca.slur:SpannerIndicatorCommand(2)
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        (                                                                            %! baca.slur:SpannerIndicatorCommand(1)
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        )                                                                            %! SPANNER_STOP:baca.slur:SpannerIndicatorCommand(2)
                        ]
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert Slur.direction                                                       %! baca.slur_down:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="slur",
        selector=selector,
        tags=[tag],
    )


def slur_up(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.slur_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Slur.direction = #up                                               %! baca.slur_up:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \override TupletBracket.direction = #down                                    %! baca.tuplet_bracket_down:OverrideCommand(1)
                        r8
                        \override Stem.direction = #down                                             %! baca.stem_down:OverrideCommand(1)
                        c'16
                        [
                        (                                                                            %! baca.slur:SpannerIndicatorCommand(1)
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        )                                                                            %! SPANNER_STOP:baca.slur:SpannerIndicatorCommand(2)
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        (                                                                            %! baca.slur:SpannerIndicatorCommand(1)
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        )                                                                            %! SPANNER_STOP:baca.slur:SpannerIndicatorCommand(2)
                        ]
                    }
                    \times 4/5 {
                        a'16
                        \revert Stem.direction                                                       %! baca.stem_down:OverrideCommand(2)
                        r4
                        \revert Slur.direction                                                       %! baca.slur_up:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.direction                                              %! baca.tuplet_bracket_down:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="slur",
        selector=selector,
        tags=[tag],
    )


def span_bar_color(
    color: str,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    after: bool = None,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.span_bar_color",
) -> OverrideCommand:
    """
    Overrides span bar color.
    """
    return OverrideCommand(
        after=after,
        attribute="color",
        value=color,
        context=context,
        grob="span_bar",
        selector=selector,
        tags=[tag],
    )


def span_bar_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    after: bool = None,
    context: str = "Score",
    tag: typing.Optional[str] = "baca.span_bar_extra_offset",
) -> OverrideCommand:
    """
    Overrides span bar extra offset.
    """
    return OverrideCommand(
        after=after,
        attribute="extra_offset",
        value=pair,
        context=context,
        grob="span_bar",
        selector=selector,
        tags=[tag],
    )


def span_bar_transparent(
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.span_bar_transparent",
) -> OverrideCommand:
    """
    Overrides span bar transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        context="Score",
        grob="span_bar",
        selector=selector,
        tags=[tag],
    )


def stem_color(
    color: str = "red",
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    context: str = None,
    tag: typing.Optional[str] = "baca.stem_color",
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
        ...     baca.stem_color(color='red'),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override Stem.color = #red                                                  %! baca.stem_color:OverrideCommand(1)
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
                        \revert Stem.color                                                           %! baca.stem_color:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="color",
        value=color,
        context=context,
        grob="stem",
        selector=selector,
        tags=[tag],
    )


def stem_down(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.stem_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override Stem.direction = #down                                             %! baca.stem_down:OverrideCommand(1)
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
                        \revert Stem.direction                                                       %! baca.stem_down:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Down,
        grob="stem",
        selector=selector,
        tags=[tag],
    )


def stem_stencil_false(
    selector: abjad.SelectorTyping = "baca.pleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.stem_stencil_false",
) -> OverrideCommand:
    """
    Overrides stem stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="stem",
        selector=selector,
        tags=[tag],
        value=False,
    )


def stem_transparent(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.stem_transparent",
) -> OverrideCommand:
    """
    Overrides stem transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        value=True,
        grob="stem",
        selector=selector,
        tags=[tag],
    )


def stem_up(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.stem_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override Stem.direction = #up                                               %! baca.stem_up:OverrideCommand(1)
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
                        \revert Stem.direction                                                       %! baca.stem_up:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        value=abjad.Up,
        grob="stem",
        selector=selector,
        tags=[tag],
    )


def strict_note_spacing_off(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.strict_note_spacing_off",
) -> OverrideCommand:
    """
    Overrides spacing spanner strict note spacing.
    """
    return OverrideCommand(
        attribute="strict_note_spacing",
        value=False,
        context="Score",
        grob="spacing_spanner",
        selector=selector,
        tags=[tag],
    )


def sustain_pedal_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    context: str = "Staff",
    tag: typing.Optional[str] = "baca.sustain_pedal_staff_padding",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Staff.SustainPedalLineSpanner.staff-padding = #4                   %! baca.sustain_pedal_staff_padding:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \sustainOn                                                                   %! baca.sustain_pedal:SpannerIndicatorCommand(1)
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                        \sustainOff                                                                  %! SPANNER_STOP:baca.sustain_pedal:SpannerIndicatorCommand(2)
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        \sustainOn                                                                   %! baca.sustain_pedal:SpannerIndicatorCommand(1)
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        \sustainOff                                                                  %! SPANNER_STOP:baca.sustain_pedal:SpannerIndicatorCommand(2)
                        ]
                    }
                    \times 4/5 {
                        a'16
                        \sustainOn                                                                   %! baca.sustain_pedal:SpannerIndicatorCommand(1)
                        r4
                        \sustainOff                                                                  %! SPANNER_STOP:baca.sustain_pedal:SpannerIndicatorCommand(2)
                        \revert Staff.SustainPedalLineSpanner.staff-padding                          %! baca.sustain_pedal_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        context=context,
        grob="sustain_pedal_line_spanner",
        selector=selector,
        tags=[tag],
    )


def text_script_color(
    color: str = "red",
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_color",
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
        ...     baca.text_script_color('red'),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TextScript.color = #red                                            %! baca.text_script_color:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup:IndicatorCommand
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
                        ^ \markup { "lo stesso tempo" }                                              %! baca.markup:IndicatorCommand
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
                        \revert TextScript.color                                                     %! baca.text_script_color:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...         'still',
        ...         boxed=True,
        ...         selector=baca.leaf(1),
        ...         ),
        ...     baca.text_script_color('red'),
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
        grob="text_script",
        selector=selector,
        tags=[tag],
    )


def text_script_down(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TextScript.direction = #down                                       %! baca.text_script_down:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup:IndicatorCommand
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
                        ^ \markup { "lo stesso tempo" }                                              %! baca.markup:IndicatorCommand
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
                        \revert TextScript.direction                                                 %! baca.text_script_down:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...         'still',
        ...         boxed=True,
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
        grob="text_script",
        selector=selector,
        tags=[tag],
    )


def text_script_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_extra_offset",
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
        ...         'still',
        ...         boxed=True,
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
        value=pair,
        grob="text_script",
        selector=selector,
        tags=[tag],
    )


def text_script_font_size(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_font_size",
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
        grob="text_script",
        selector=selector,
        tags=[tag],
    )


def text_script_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "text.script_padding",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TextScript.padding = #4                                            %! text.script_padding:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup:IndicatorCommand
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
                        ^ \markup { "lo stesso tempo" }                                              %! baca.markup:IndicatorCommand
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
                        \revert TextScript.padding                                                   %! text.script_padding:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...         'still',
        ...         boxed=True,
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
        grob="text_script",
        selector=selector,
        tags=[tag],
    )


def text_script_parent_alignment_x(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_parent_alignment_x",
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
        grob="text_script",
        selector=selector,
        tags=[tag],
        value=n,
    )


def text_script_self_alignment_x(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_self_alignment_x",
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
        grob="text_script",
        selector=selector,
        tags=[tag],
        value=n,
    )


def text_script_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: str = "baca.text_script_staff_padding",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TextScript.staff-padding = #4                                      %! baca.text_script_staff_padding:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup:IndicatorCommand
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
                        ^ \markup { "lo stesso tempo" }                                              %! baca.markup:IndicatorCommand
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
                        \revert TextScript.staff-padding                                             %! baca.text_script_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...         'still',
        ...         boxed=True,
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
        grob="text_script",
        selector=selector,
        tags=[tag],
    )


def text_script_up(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TextScript.direction = #up                                         %! baca.text_script_up:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup:IndicatorCommand
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
                        ^ \markup { "lo stesso tempo" }                                              %! baca.markup:IndicatorCommand
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
                        \revert TextScript.direction                                                 %! baca.text_script_up:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
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
        ...         'still',
        ...         boxed=True,
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
        grob="text_script",
        selector=selector,
        tags=[tag],
        value=abjad.Up,
    )


def text_script_x_offset(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_x_offset",
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
        grob="text_script",
        selector=selector,
        tags=[tag],
        value=n,
    )


def text_script_y_offset(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    allow_mmrests: bool = False,
    tag: typing.Optional[str] = "baca.text_script_y_offset",
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
        grob="text_script",
        selector=selector,
        tags=[tag],
        value=n,
    )


def text_spanner_left_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.text_spanner_left_padding",
) -> OverrideCommand:
    """
    Overrides text spanner left padding.
    """
    return OverrideCommand(
        attribute="bound_details__left__padding",
        grob="text_spanner",
        selector=selector,
        tags=[tag],
        value=n,
    )


def text_spanner_right_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.text_spanner_right_padding",
) -> OverrideCommand:
    """
    Overrides text spanner right padding.
    """
    return OverrideCommand(
        attribute="bound_details__right__padding",
        grob="text_spanner",
        selector=selector,
        tags=[tag],
        value=n,
    )


def text_spanner_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: str = "baca.text_spanner_staff_padding",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TextSpanner.staff-padding = #6                                     %! baca.text_spanner_staff_padding:OverrideCommand(1)
                        \override TextScript.staff-padding = #6                                      %! baca.text_script_staff_padding:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        [
                        - \abjad-dashed-line-with-arrow                                              %! baca.text_spanner:PiecewiseCommand(1)
                        - \baca-text-spanner-left-text "pont."                                       %! baca.text_spanner:PiecewiseCommand(1)
                        - \baca-text-spanner-right-text "ord."                                       %! baca.text_spanner:PiecewiseCommand(1)
                        - \tweak bound-details.right.padding #0.5                                    %! baca.text_spanner:PiecewiseCommand(1)
                        - \tweak bound-details.right.stencil-align-dir-y #center                     %! baca.text_spanner:PiecewiseCommand(1)
                        \startTextSpan                                                               %! baca.text_spanner:PiecewiseCommand(1)
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
                        \stopTextSpan                                                                %! SPANNER_STOP:baca.text_spanner:PiecewiseCommand(2)
                        r4
                        \revert TextSpanner.staff-padding                                            %! baca.text_spanner_staff_padding:OverrideCommand(2)
                        \revert TextScript.staff-padding                                             %! baca.text_script_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="staff_padding",
        value=n,
        grob="text_spanner",
        selector=selector,
        tags=[tag],
    )


def text_spanner_stencil_false(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.text_spanner_stencil_false",
) -> OverrideCommand:
    """
    Overrides text spanner stencil.
    """
    return OverrideCommand(
        attribute="stencil",
        grob="text_spanner",
        selector=selector,
        tags=[tag],
        value=False,
    )


def text_spanner_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.text_spanner_transparent",
) -> OverrideCommand:
    """
    Overrides text spanner transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="text_spanner",
        selector=selector,
        tags=[tag],
        value=True,
    )


def text_spanner_y_offset(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.text_spanner_y_offset",
) -> OverrideCommand:
    """
    Overrides text spanner Y-offset.
    """
    return OverrideCommand(
        attribute="Y_offset",
        grob="text_spanner",
        selector=selector,
        tags=[tag],
        value=n,
    )


def tie_down(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.tie_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override Stem.direction = #up                                               %! baca.stem_up:OverrideCommand(1)
                        \override Tie.direction = #down                                              %! baca.tie_down:OverrideCommand(1)
                        b'16
                        [
                        ~                                                                            %! baca.tie:IndicatorCommand
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
                        \revert Stem.direction                                                       %! baca.stem_up:OverrideCommand(2)
                        \revert Tie.direction                                                        %! baca.tie_down:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="tie",
        selector=selector,
        tags=[tag],
        value=abjad.Down,
    )


def tie_up(
    selector: abjad.SelectorTyping = "baca.pleaves()",
    *,
    tag: typing.Optional[str] = "baca.tie_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \override Stem.direction = #down                                             %! baca.stem_down:OverrideCommand(1)
                        \override Tie.direction = #up                                                %! baca.tie_up:OverrideCommand(1)
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
                        \revert Stem.direction                                                       %! baca.stem_down:OverrideCommand(2)
                        \revert Tie.direction                                                        %! baca.tie_up:OverrideCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="tie",
        selector=selector,
        tags=[tag],
        value=abjad.Up,
    )


def time_signature_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.hleaf(0)",
    *,
    tag: typing.Optional[str] = "baca.time_signature_extra_offset",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \once \override Score.TimeSignature.extra-offset = #'(-6 . 0)                %! baca.time_signature_extra_offset:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    assert isinstance(pair, tuple), repr(pair)
    return OverrideCommand(
        attribute="extra_offset",
        context="Score",
        grob="time_signature",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def time_signature_stencil_false(
    selector: abjad.SelectorTyping = "baca.hleaves()",
    *,
    tag: typing.Optional[str] = "baca.time_signature_stencil_false",
) -> OverrideCommand:
    """
    Overrides time signature stencil property.
    """
    return OverrideCommand(
        attribute="stencil",
        context="Score",
        grob="time_signature",
        selector=selector,
        tags=[tag],
        value=False,
    )


def time_signature_transparent(
    selector: abjad.SelectorTyping = "baca.hleaves()",
    *,
    tag: typing.Optional[str] = "baca.time_signature_transparent",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override Score.TimeSignature.transparent = ##t                              %! baca.time_signature_transparent:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert Score.TimeSignature.transparent                                      %! baca.time_signature_transparent:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="transparent",
        context="Score",
        grob="time_signature",
        selector=selector,
        tags=[tag],
        value=True,
    )


def trill_spanner_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.trill_spanner_staff_padding",
) -> OverrideCommand:
    """
    Overrides trill spanner staff padding.
    """
    return OverrideCommand(
        attribute="staff_padding",
        grob="trill_spanner",
        selector=selector,
        tags=[tag],
        value=n,
    )


def tuplet_bracket_down(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_down",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \override TupletBracket.direction = #down                                    %! baca.tuplet_bracket_down:OverrideCommand(1)
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.direction                                              %! baca.tuplet_bracket_down:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=abjad.Down,
    )


def tuplet_bracket_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_extra_offset",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \once \override TupletBracket.extra-offset = #'(-1 . 0)                      %! baca.tuplet_bracket_extra_offset:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def tuplet_bracket_outside_staff_priority(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_outside_staff_priority",
) -> OverrideCommand:
    """
    Overrides tuplet bracket outside-staff-priority.
    """
    return OverrideCommand(
        attribute="outside_staff_priority",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=n,
    )


def tuplet_bracket_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_down",
) -> OverrideCommand:
    """
    Overrides tuplet bracket padding.
    """
    return OverrideCommand(
        attribute="padding",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=n,
    )


def tuplet_bracket_shorten_pair(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_shorten_pair",
) -> OverrideCommand:
    """
    Overrides tuplet bracket shorten pair.
    """
    return OverrideCommand(
        attribute="shorten_pair",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def tuplet_bracket_staff_padding(
    n: abjad.Number,
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_staff_padding",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="staff_padding",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=n,
    )


def tuplet_bracket_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_transparent",
) -> OverrideCommand:
    """
    Overrides tuplet bracket transparency.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=True,
    )


def tuplet_bracket_up(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_bracket_up",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \override TupletBracket.direction = #up                                      %! baca.tuplet_bracket_up:OverrideCommand(1)
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.direction                                              %! baca.tuplet_bracket_up:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="direction",
        grob="tuplet_bracket",
        selector=selector,
        tags=[tag],
        value=abjad.Up,
    )


def tuplet_number_denominator(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_number_denominator",
) -> OverrideCommand:
    """
    Overrides tuplet number text.
    """
    return OverrideCommand(
        attribute="text",
        grob="tuplet_number",
        selector=selector,
        tags=[tag],
        value="tuplet-number::calc-denominator-text",
    )


def tuplet_number_extra_offset(
    pair: abjad.NumberPair,
    selector: abjad.SelectorTyping = "baca.leaf(0)",
    *,
    tag: typing.Optional[str] = "baca.tuplet_number_extra_offset",
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        \once \override TupletNumber.extra-offset = #'(-1 . 0)                       %! baca.tuplet_number_extra_offset:OverrideCommand(1)
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return OverrideCommand(
        attribute="extra_offset",
        grob="tuplet_number",
        selector=selector,
        tags=[tag],
        value=pair,
    )


def tuplet_number_transparent(
    selector: abjad.SelectorTyping = "baca.leaves()",
    *,
    tag: typing.Optional[str] = "baca.tuplet_number_transparent",
) -> OverrideCommand:
    """
    Overrides tuplet number transparent.
    """
    return OverrideCommand(
        attribute="transparent",
        grob="tuplet_number",
        selector=selector,
        tags=[tag],
        value=True,
    )
