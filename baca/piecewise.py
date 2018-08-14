"""
Piecewise library.
"""
import abjad
import typing
from . import classes
from . import commands
from . import scoping
from . import typings


### CLASSES ###

# TODO: change __init__ / __repr__ so indicators are visible in interpreter
class IndicatorBundle(abjad.AbjadObject):
    """
    IndicatorBundle.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookended_spanner_start',
        '_enchained',
        '_indicator',
        '_spanner_start',
        '_spanner_stop',
        )

    _publish_storage_format=True

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments: typing.Any,
        bookended_spanner_start: typing.Any = None,
        enchained: bool = None,
        ) -> None:
        assert len(arguments) <= 3, repr(arguments)
        self._indicator = None
        self._spanner_start = None
        self._spanner_stop = None
        for argument in arguments:
            if argument is None:
                continue
            elif getattr(argument, 'spanner_start', False) is True:
                self._spanner_start = argument
            elif getattr(argument, 'spanner_stop', False) is True:
                self._spanner_stop = argument
            else:
                self._indicator = argument
        self._bookended_spanner_start = bookended_spanner_start
        if enchained is not None:
            enchained = bool(enchained)
        self._enchained = enchained

    ### SPECIAL METHODS ###

    def __iter__(self) -> typing.Iterator:
        """
        Iterates bundle.
        """
        return iter(self.indicators)

    def __len__(self) -> int:
        """
        Gets length.
        """
        return len(self.indicators)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        class_ = type(self).__name__
        string = ', '.join([repr(_) for _ in self.indicators])
        return f'{class_}({string})'

    ### PUBLIC PROPERTIES ###

    @property
    def bookended_spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets bookended start text span indicator.
        """
        return self._bookended_spanner_start

    @property
    def enchained(self) -> typing.Optional[bool]:
        """
        Is true when bundle contributes to enchained spanner.
        """
        return self._enchained

    @property
    def indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets indicator.
        """
        return self._indicator

    @property
    def indicators(self) -> typing.List:
        """
        Gets indicators.
        """
        result: typing.List = []
        if self.spanner_stop:
            result.append(self.spanner_stop)
        if self.indicator:
            result.append(self.indicator)
        if self.spanner_start:
            result.append(self.spanner_start)
        return result

    @property
    def spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner start.
        """
        return self._spanner_start

    @property
    def spanner_stop(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner stop.
        """
        return self._spanner_stop

    ### PUBLIC METHODS ###

    def compound(self) -> bool:
        """
        Is true when bundle has both indicator and spanner_start.
        """
        return bool(self.indicator) and bool(self.spanner_start)

    def indicator_only(self) -> bool:
        """
        Is true when bundle has indicator only.
        """
        if self.indicator and not self.spanner_start:
            return True
        return False

    def simple(self) -> bool:
        """
        Is true when bundle has indicator or spanner start but not both.
        """
        return len(self) == 1

    def spanner_start_only(self) -> bool:
        """
        Is true when bundle has spanner start only.
        """
        if not self.indicator and self.spanner_start:
            return True
        return False

    def with_indicator(self, indicator) -> 'IndicatorBundle':
        """
        Makes new bundle with indicator.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.Dynamic('p'),
            ...     abjad.DynamicTrend('<'),
            ...     )

            >>> bundle.with_indicator(abjad.Dynamic('f'))
            IndicatorBundle(Dynamic('f'), DynamicTrend(shape='<'))

            >>> bundle.with_indicator(None)
            IndicatorBundle(DynamicTrend(shape='<'))

        """
        if indicator is None:
            return type(self)(self.spanner_start)
        return type(self)(
            self.spanner_stop,
            indicator,
            self.spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

    def with_spanner_start(self, spanner_start) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner start.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.Dynamic('p'),
            ...     abjad.DynamicTrend('<'),
            ...     )

            >>> bundle.with_spanner_start(abjad.DynamicTrend('>'))
            IndicatorBundle(Dynamic('p'), DynamicTrend(shape='>'))

            >>> bundle.with_spanner_start(None)
            IndicatorBundle(Dynamic('p'))

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.StopTextSpan(),
            ...     abjad.StartTextSpan(left_text=abjad.Markup('pont.')),
            ...     )

            >>> bundle.with_spanner_start(
            ...     abjad.StartTextSpan(command=r'\startTextSpanOne')
            ...     )
            IndicatorBundle(StopTextSpan(command='\\stopTextSpan'), StartTextSpan(command='\\startTextSpanOne', concat_hspace_left=0.5))

            >>> bundle.with_spanner_start(None)
            IndicatorBundle(StopTextSpan(command='\\stopTextSpan'))

        """
        if (spanner_start is not None and
            getattr(spanner_start, 'spanner_start', False) is not True):
            raise Exception(spanner_start)
        return type(self)(
            self.spanner_stop,
            self.indicator,
            spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

    def with_spanner_stop(self, spanner_stop) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner stop.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.StopTextSpan(),
            ...     abjad.StartTextSpan(left_text=abjad.Markup('pont.')),
            ...     )

            >>> string = r'\stopTextSpanOne'
            >>> bundle.with_spanner_stop(abjad.StopTextSpan(command=string))
            IndicatorBundle(StopTextSpan(command='\\stopTextSpanOne'), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, left_text=Markup(contents=['pont.'])))

            >>> bundle.with_spanner_stop(None)
            IndicatorBundle(StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, left_text=Markup(contents=['pont.'])))

        """
        if (spanner_stop is not None and
            getattr(spanner_stop, 'spanner_stop', False) is not True):
            raise Exception(spanner_stop)
        return type(self)(
            spanner_stop,
            self.indicator,
            self.spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

class PiecewiseCommand(scoping.Command):
    """
    Piecewise indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookend',
        '_bundles',
        '_final_piece_spanner',
        '_leak',
        '_piece_selector',
        '_remove_length_1_spanner_start',
        '_right_broken',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        bundles: typing.List[IndicatorBundle] = None,
        final_piece_spanner: typing.Any = None,
        leak: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        piece_selector: typings.Selector = 'baca.leaves()',
        remove_length_1_spanner_start: bool = None,
        right_broken: typing.Any = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaves()',
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        ) -> None:
        # for selector evaluation
        import baca
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
            )
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        bundles_ = None
        if bundles is not None:
            bundles_ = abjad.CyclicTuple(bundles)
        self._bundles = bundles_
        if final_piece_spanner not in (None, False):
            assert getattr(final_piece_spanner, 'spanner_start', False)
        self._final_piece_spanner = final_piece_spanner
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if isinstance(piece_selector, str):
            piece_selector = eval(piece_selector)
        if piece_selector is not None:
            assert isinstance(piece_selector, abjad.Expression), repr(
                piece_selector)
        self._piece_selector = piece_selector
        if remove_length_1_spanner_start is not None:
            remove_length_1_spanner_start = bool(remove_length_1_spanner_start)
        self._remove_length_1_spanner_start = remove_length_1_spanner_start
        self._right_broken = right_broken

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.bundles:
            return
        if self.selector is not None:
            assert not isinstance(self.selector, str)
            argument = self.selector(argument)
        if self.piece_selector is not None:
            assert not isinstance(self.piece_selector, str)
            pieces = self.piece_selector(argument)
        else:
            pieces = argument
        assert pieces is not None
        piece_count = len(pieces)
        assert 0 < piece_count, repr(piece_count)
        if self.bookend in (False, None):
            bookend_pattern = abjad.Pattern()
        elif self.bookend is True:
            bookend_pattern = abjad.index([0], 1)
        else:
            assert isinstance(self.bookend, int), repr(self.bookend)
            bookend_pattern = abjad.index([self.bookend], period=piece_count)
        previous_had_bookend = None
        for i, piece in enumerate(pieces):
            start_leaf = classes.Selection(piece).leaf(0)
            stop_leaf = classes.Selection(piece).leaf(-1)
            if i == 0:
                is_first_piece = True
            else:
                is_first_piece = False
            if i == piece_count - 1:
                is_final_piece = True
            else:
                is_final_piece = False
            if is_final_piece and self.right_broken:
                bundle = IndicatorBundle(self.right_broken)
                self._attach_indicators(
                    bundle,
                    stop_leaf,
                    tag=str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS),
                    )
            if (bookend_pattern.matches_index(i, piece_count) and
                1 < len(piece)):
                should_bookend = True
            else:
                should_bookend = False
            if is_final_piece and self.right_broken:
                should_bookend = False
            bundle = self.bundles[i]
            if should_bookend and bundle.bookended_spanner_start:
                bundle = bundle.with_spanner_start(
                    bundle.bookended_spanner_start
                    )
            if (len(piece) == 1 and
                bundle.compound() and
                self.remove_length_1_spanner_start):
                bundle = bundle.with_spanner_start(None)
            if is_final_piece and bundle.compound():
                if self.final_piece_spanner:
                    bundle = bundle.with_spanner_start(
                        self.final_piece_spanner)
                elif self.final_piece_spanner is False:
                    bundle = bundle.with_spanner_start(None)
            if is_first_piece or previous_had_bookend:
                bundle = bundle.with_spanner_stop(None)
            self._attach_indicators(
                bundle,
                start_leaf,
                tag='PiecewiseCommand(1)',
                )
            next_bundle = self.bundles[i + 1]
            if should_bookend:
                if bundle.bookended_spanner_start is not None:
                    next_bundle = next_bundle.with_spanner_start(None)
                if next_bundle.compound():
                    next_bundle = next_bundle.with_spanner_start(None)
                if self.leak:
                    indicators_ = []
                    for indicator in next_bundle.indicators:
                        indicator_ = abjad.new(indicator, leak=True)
                        indicators_.append(indicator_)
                    next_bundle = IndicatorBundle(*indicators_)
                self._attach_indicators(
                    next_bundle,
                    stop_leaf,
                    tag='PiecewiseCommand(2)',
                    )
            elif is_final_piece and next_bundle.spanner_stop:
                spanner_stop = next_bundle.spanner_stop
                if self.leak:
                    spanner_stop = abjad.new(spanner_stop, leak=True)
                bundle = IndicatorBundle(spanner_stop)
                self._attach_indicators(
                    bundle,
                    stop_leaf,
                    tag='PiecewiseCommand(3)',
                    )
            previous_had_bookend = should_bookend

    ### PRIVATE METHODS ###

    def _attach_indicators(
        self,
        bundle,
        leaf,
        tag=None,
        ):
        # TODO: factor out late import
        from .segmentmaker import SegmentMaker
        assert isinstance(tag, str), repr(tag)
        for indicator in bundle:
            reapplied = scoping.Command._remove_reapplied_wrappers(
                leaf,
                indicator,
                )
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=self.tag.append(tag),
                wrapper=True,
                )
            if scoping.compare_persistent_indicators(
                indicator,
                reapplied,
                ):
                status = 'redundant'
                SegmentMaker._treat_persistent_wrapper(
                    self.runtime['manifests'],
                    wrapper,
                    status,
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def bookend(self) -> typing.Optional[typing.Union[bool, int]]:
        """
        Gets bookend token.

        Command attaches indicator to first leaf in each group of
        selector output when ``bookend`` is false.

        Command attaches indicator to both first leaf and last
        leaf in each group of selector output when ``bookend`` is true.

        When ``bookend`` equals integer ``n``, command attaches indicator to
        first leaf and last leaf in group ``n`` of selector output and attaches
        indicator to only first leaf in other groups of selector output.
        """
        return self._bookend

    @property
    def bundles(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets bundles.
        """
        return self._bundles

    @property
    def final_piece_spanner(self) -> typing.Optional[typing.Any]:
        """
        Gets last piece spanner start.
        """
        return self._final_piece_spanner

    @property
    def leak(self) -> typing.Optional[bool]:
        """
        Is true when command leaks final spanner stop.
        """
        return self._leak

    @property
    def piece_selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets piece selector.
        """
        return self._piece_selector

    @property
    def remove_length_1_spanner_start(self) -> typing.Optional[bool]:
        """
        Is true when command removes spanner start from length-1 pieces.
        """
        return self._remove_length_1_spanner_start

    @property
    def right_broken(self) -> typing.Optional[typing.Any]:
        """
        Gets right-broken indicator.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets (first-order) selector.
        """
        return self._selector

### FACTORY FUNCTIONS ###

def dynamic(
    dynamic: typing.Union[str, abjad.Dynamic],
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.phead(0)',
    redundant: bool = None,
    tag: typing.Optional[str] = 'baca_dynamic',
    ) -> commands.IndicatorCommand:
    r"""
    Attaches dynamic.

    ..  container:: example

        Attaches dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('f'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            \f                                                                       %! baca_dynamic:IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches dynamic to pitched head 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \f                                                                       %! baca_dynamic:IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches effort dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('"f"'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            \baca-effort-f                                                           %! baca_dynamic:IndicatorCommand
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
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Works with dynamic trends:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 13)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('<'),
        ...     baca.dynamic('f', selector=baca.pleaf(-1)),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #13                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #13                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #13                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #13                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_dynamic:IndicatorCommand
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_dynamic:IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_dynamic:IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Works with tweaks:        

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.dynamic('p', abjad.tweak('red').color),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_dynamic:IndicatorCommand
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    if isinstance(dynamic, str):
        indicator = make_dynamic(dynamic)
    else:
        indicator = dynamic
    prototype = (abjad.Dynamic, abjad.DynamicTrend)
    assert isinstance(indicator, prototype), repr(indicator)
    return commands.IndicatorCommand(
        *tweaks,
        context='Voice',
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[tag],
        )

def hairpin(
    dynamics: typing.Union[str, typing.List],
    *,
    bookend: typing.Union[bool, int] = -1,
    final_hairpin: typing.Union[bool, str, abjad.DynamicTrend] = None,
    leak: bool = None,
    left_broken: bool = None,
    piece_selector: typings.Selector = 'baca.group()',
    remove_length_1_spanner_start: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.leaves()',
    tag: typing.Optional[str] = 'baca_hairpin',
    ) -> PiecewiseCommand:
    r"""
    Attaches hairpin.

    ..  container:: example

        Conventional dynamics:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin('p < f', bookend=-1),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Effort dynamic al niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('"ff" >o niente'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-ff                                                          %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak to-barline ##t                                                  %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak circled-tip ##t                                                 %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \!                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Effort dynamic dal niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('niente o< "ff"'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \!                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak circled-tip ##t                                                 %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-ff                                                          %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Effort dynamic constante:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('"p" -- f'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-p                                                           %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak stencil #constante-hairpin                                      %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Effort dynamics crescendo subito, decrescendo subito:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin(
        ...         '"mp" <| "f"',
        ...         selector=baca.leaves()[:7],
        ...         ),
        ...     baca.hairpin(
        ...         '"mf" |> "p"',
        ...         selector=baca.leaves()[7:],
        ...         ),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-mp                                                          %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak stencil #abjad-flared-hairpin                                   %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-f                                                           %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-mf                                                          %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak stencil #abjad-flared-hairpin                                   %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \baca-effort-p                                                           %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Piece selector groups leaves by measures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         'p f',
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         'p < f >',
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Bookends each piece:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         'p f',
        ...         bookend=True,
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'DeepPink1)                                   %! REDUNDANT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'DeepPink1)                                   %! REDUNDANT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! REDUNDANT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! REDUNDANT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'DeepPink1)                                   %! REDUNDANT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'DeepPink1)                                   %! REDUNDANT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! REDUNDANT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         'p -- f >',
        ...         bookend=True,
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak stencil #constante-hairpin                                      %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak stencil #constante-hairpin                                      %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \p                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Leaks conventional dynamic one leaf to the right:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         'f > p',
        ...         leak=True,
        ...         piece_selector=baca.cmgroups([2])[:1],
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            <> \p                                                                    %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Leaks niente one leaf to the right:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         'f >o niente',
        ...         leak=True,
        ...         piece_selector=baca.cmgroups([2])[:1],
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            - \tweak to-barline ##t                                                  %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            - \tweak circled-tip ##t                                                 %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            \>                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            <> \!                                                                    %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(2)
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        REGRESSION. Works with lone dynamic:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('f', bookend=False),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        REGRESSION. Works with lone hairpin:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     baca.suite(
        ...         baca.hairpin('<', bookend=False),
        ...         baca.dynamic('f', selector=baca.pleaf(-1)),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \<                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_hairpin:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            - \tweak color #(x11-color 'blue)                                        %! EXPLICIT_DYNAMIC_COLOR:_treat_persistent_wrapper(1)
                            \f                                                                       %! EXPLICIT_DYNAMIC:_set_status_tag:baca_dynamic:IndicatorCommand
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    if isinstance(dynamics, str):
        bundles = parse_hairpin_descriptor(dynamics)
    else:
        bundles = dynamics
    for item in bundles:
        assert isinstance(item, IndicatorBundle), repr(dynamic)
    final_hairpin_: typing.Union[bool, abjad.DynamicTrend, None] = None
    if isinstance(final_hairpin, bool):
        final_hairpin_ = final_hairpin
    elif isinstance(final_hairpin, str):
        final_hairpin_ = abjad.DynamicTrend(final_hairpin)
    if left_broken is not None:
        left_broken = bool(left_broken)
    if left_broken is True:
        bundle = bundles[0]
        assert bundle.spanner_start_only()
        dynamic_trend = abjad.new(bundle.spanner_start, left_broken=True)
        bundle = IndicatorBundle(dynamic_trend)
        bundles[0] = bundle
    if remove_length_1_spanner_start is not None:
        remove_length_1_spanner_start = bool(remove_length_1_spanner_start)
    right_broken_: typing.Any = False
    if bool(right_broken) is True:
        right_broken_ = abjad.LilyPondLiteral(r'\!', format_slot='after')
    return PiecewiseCommand(
        bookend=bookend,
        bundles=bundles,
        final_piece_spanner=final_hairpin_,
        leak=leak,
        piece_selector=piece_selector,
        remove_length_1_spanner_start=remove_length_1_spanner_start,
        right_broken=right_broken_,
        selector=selector,
        tags=[tag],
        )

def make_dynamic(string: str) -> typing.Union[
    abjad.Dynamic, abjad.DynamicTrend
    ]:
    r"""
    Makes dynamic.

    ..  container:: example

        >>> baca.make_dynamic('p')
        Dynamic('p')

        >>> baca.make_dynamic('sffz')
        Dynamic('ff', command='\\baca-sffz', name_is_textual=False, sforzando=True)

        >>> baca.make_dynamic('niente')
        Dynamic('niente', command='\\!', direction=Down, name_is_textual=True)

        >>> baca.make_dynamic('<')
        DynamicTrend(shape='<')

        >>> baca.make_dynamic('o<|')
        DynamicTrend(shape='o<|')

        >>> baca.make_dynamic('appena-udibile')
        Dynamic('appena udibile', command='\\baca-appena-udibile', name_is_textual=True, sforzando=False)

    ..  container:: example

        Ancora dynamics:

        >>> baca.make_dynamic('p-ancora')
        Dynamic('p', command='\\baca-p-ancora')

        >>> baca.make_dynamic('f-ancora')
        Dynamic('f', command='\\baca-f-ancora')

    ..  container:: example

        Effort dynamics:

        >>> baca.make_dynamic('"p"')
        Dynamic('"p"', command='\\baca-effort-p', direction=Down)

        >>> baca.make_dynamic('"f"')
        Dynamic('"f"', command='\\baca-effort-f', direction=Down)

    ..  container:: example

        Possibile dynamics:

        >>> baca.make_dynamic('p-poss')
        Dynamic('p', command='\\baca-p-poss')

        >>> baca.make_dynamic('f-poss')
        Dynamic('f', command='\\baca-f-poss')

    ..  container:: example

        Sempre dynamics:

        >>> baca.make_dynamic('p-sempre')
        Dynamic('p', command='\\baca-p-sempre')

        >>> baca.make_dynamic('f-sempre')
        Dynamic('f', command='\\baca-f-sempre')

    ..  container:: example

        Subito dynamics:

        >>> baca.make_dynamic('p-sub')
        Dynamic('p', command='\\baca-p-sub')

        >>> baca.make_dynamic('f-sub')
        Dynamic('f', command='\\baca-f-sub')

    ..  container:: example

        Al niente hairpins are special-cased to carry to-barline tweaks:

        >>> baca.make_dynamic('>o')
        DynamicTrend(shape='>o', tweaks=LilyPondTweakManager(('to_barline', True)))

        >>> baca.make_dynamic('|>o')
        DynamicTrend(shape='|>o', tweaks=LilyPondTweakManager(('to_barline', True)))

    """
    assert isinstance(string, str), repr(string)
    scheme_manifest = classes.SchemeManifest()
    known_shapes = abjad.DynamicTrend('<').known_shapes
    indicator: typing.Union[abjad.Dynamic, abjad.DynamicTrend]
    if '_' in string:
        raise Exception(f'use hyphens instead of underscores ({string!r}).')
    if string == 'niente':
        indicator = abjad.Dynamic('niente', command=r'\!')
    elif string.endswith('-ancora'):
        dynamic = string.split('-')[0]
        command = rf'\baca-{dynamic}-ancora'
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith('-poss'):
        dynamic = string.split('-')[0]
        command = rf'\baca-{dynamic}-poss'
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith('-sempre'):
        dynamic = string.split('-')[0]
        command = rf'\baca-{dynamic}-sempre'
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith('-sub'):
        dynamic = string.split('-')[0]
        command = rf'\baca-{dynamic}-sub'
        indicator = abjad.Dynamic(dynamic, command=command)
    elif 'baca-' + string in scheme_manifest.dynamics:
        name = scheme_manifest.dynamic_to_steady_state(string)
        command = '\\baca-' + string
        pieces = string.split('-')
        if pieces[0] in ('sfz', 'sffz', 'sfffz'):
            sforzando = True
        else:
            sforzando = False
        name_is_textual = not(sforzando)
        indicator = abjad.Dynamic(
            name,
            command=command,
            name_is_textual=name_is_textual,
            sforzando=sforzando,
            )
    elif string.startswith('"'):
        assert string.endswith('"')
        stripped_string = string.strip('"')
        command = rf'\baca-effort-{stripped_string}'
        indicator = abjad.Dynamic(f'{string}', command=command)
    elif string in known_shapes:
        indicator = abjad.DynamicTrend(string)
        if string.endswith('>o'):
            abjad.tweak(indicator).to_barline = True
    else:
        indicator = abjad.Dynamic(string)
    return indicator

def parse_hairpin_descriptor(
    descriptor: str
    ) -> typing.List[IndicatorBundle]:
    r"""
    Parses hairpin descriptor.

    ..  container:: example

        >>> for item in baca.parse_hairpin_descriptor('f'):
        ...     item
        IndicatorBundle(Dynamic('f'))

        >>> for item in baca.parse_hairpin_descriptor('"f"'):
        ...     item
        IndicatorBundle(Dynamic('"f"', command='\\baca-effort-f', direction=Down))

        >>> for item in baca.parse_hairpin_descriptor('niente'):
        ...     item
        IndicatorBundle(Dynamic('niente', command='\\!', direction=Down, name_is_textual=True))

        >>> for item in baca.parse_hairpin_descriptor('<'):
        ...     item
        IndicatorBundle(DynamicTrend(shape='<'))

        >>> for item in baca.parse_hairpin_descriptor('o<|'):
        ...     item
        IndicatorBundle(DynamicTrend(shape='o<|'))

        >>> for item in baca.parse_hairpin_descriptor('--'):
        ...     item
        IndicatorBundle(DynamicTrend(shape='--'))

        >>> for item in baca.parse_hairpin_descriptor('< f'):
        ...     item
        IndicatorBundle(DynamicTrend(shape='<'))
        IndicatorBundle(Dynamic('f'))

        >>> for item in baca.parse_hairpin_descriptor('o< f'):
        ...     item
        IndicatorBundle(DynamicTrend(shape='o<'))
        IndicatorBundle(Dynamic('f'))

        >>> for item in baca.parse_hairpin_descriptor('niente o<| f'):
        ...     item
        IndicatorBundle(Dynamic('niente', command='\\!', direction=Down, name_is_textual=True), DynamicTrend(shape='o<|'))
        IndicatorBundle(Dynamic('f'))

        >>> for item in baca.parse_hairpin_descriptor('f >'):
        ...     item
        IndicatorBundle(Dynamic('f'), DynamicTrend(shape='>'))

        >>> for item in baca.parse_hairpin_descriptor('f >o'):
        ...     item
        IndicatorBundle(Dynamic('f'), DynamicTrend(shape='>o', tweaks=LilyPondTweakManager(('to_barline', True))))

        >>> for item in baca.parse_hairpin_descriptor('p mp mf f'):
        ...     item
        IndicatorBundle(Dynamic('p'))
        IndicatorBundle(Dynamic('mp'))
        IndicatorBundle(Dynamic('mf'))
        IndicatorBundle(Dynamic('f'))

        >>> for item in baca.parse_hairpin_descriptor('p < f f > p'):
        ...     item
        IndicatorBundle(Dynamic('p'), DynamicTrend(shape='<'))
        IndicatorBundle(Dynamic('f'))
        IndicatorBundle(Dynamic('f'), DynamicTrend(shape='>'))
        IndicatorBundle(Dynamic('p'))

    """
    assert isinstance(descriptor, str), repr(descriptor)
    indicators: typing.List[
        typing.Union[abjad.Dynamic, abjad.DynamicTrend]] = []
    bundles: typing.List[IndicatorBundle] = []
    for string in descriptor.split():
        indicator = make_dynamic(string)
        indicators.append(indicator)
    if len(indicators) == 1:
        bundle = IndicatorBundle(indicators[0])
        bundles.append(bundle)
        return bundles
    if isinstance(indicators[0], abjad.DynamicTrend):
        result = indicators.pop(0)
        assert isinstance(result, abjad.DynamicTrend)
        bundle = IndicatorBundle(result)
        bundles.append(bundle)
    if len(indicators) == 1:
        bundle = IndicatorBundle(indicators[0])
        bundles.append(bundle)
        return bundles
    for left, right in classes.Sequence(indicators).nwise():
        if (isinstance(left, abjad.DynamicTrend) and
            isinstance(right, abjad.DynamicTrend)):
            raise Exception('consecutive dynamic trends')
        elif (isinstance(left, abjad.Dynamic) and
            isinstance(right, abjad.Dynamic)):
            bundle = IndicatorBundle(left)
            bundles.append(bundle)
        elif (isinstance(left, abjad.Dynamic) and
            isinstance(right, abjad.DynamicTrend)):
            bundle = IndicatorBundle(left, right)
            bundles.append(bundle)
    if indicators and isinstance(indicators[-1], abjad.Dynamic):
        bundle = IndicatorBundle(indicators[-1])
        bundles.append(bundle)
    return bundles

def text_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.LilyPondTweakManager,
    bookend: typing.Union[bool, int] = -1,
    boxed: bool = None,
    leak: bool = None,
    lilypond_id: int = None,
    piece_selector: typings.Selector = 'baca.group()',
    selector: typings.Selector = 'baca.leaves()',
    tag: typing.Optional[str] = 'baca_text_spanner',
    ) -> PiecewiseCommand:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single-segment spanners.

        Dashed line with arrow:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. => ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-dashed-line-with-arrow                                          %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "pont."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "ord."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Dashed line with hook:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. =| ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-dashed-line-with-hook                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "pont."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.text \markup {                              %! baca_text_spanner:PiecewiseCommand(1)
                                \concat                                                              %! baca_text_spanner:PiecewiseCommand(1)
                                    {                                                                %! baca_text_spanner:PiecewiseCommand(1)
                                        \raise                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            #-1                                                      %! baca_text_spanner:PiecewiseCommand(1)
                                            \draw-line                                               %! baca_text_spanner:PiecewiseCommand(1)
                                                #'(0 . -1)                                           %! baca_text_spanner:PiecewiseCommand(1)
                                        \hspace                                                      %! baca_text_spanner:PiecewiseCommand(1)
                                            #0.75                                                    %! baca_text_spanner:PiecewiseCommand(1)
                                        \general-align                                               %! baca_text_spanner:PiecewiseCommand(1)
                                            #Y                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            #1                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            \upright                                                 %! baca_text_spanner:PiecewiseCommand(1)
                                                ord.                                                 %! baca_text_spanner:PiecewiseCommand(1)
                                    }                                                                %! baca_text_spanner:PiecewiseCommand(1)
                                }                                                                    %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #1.25                               %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Solid line with arrow:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. -> ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "pont."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "ord."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Solid line with hook:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. -| ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-solid-line-with-hook                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "pont."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.text \markup {                              %! baca_text_spanner:PiecewiseCommand(1)
                                \concat                                                              %! baca_text_spanner:PiecewiseCommand(1)
                                    {                                                                %! baca_text_spanner:PiecewiseCommand(1)
                                        \raise                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            #-1                                                      %! baca_text_spanner:PiecewiseCommand(1)
                                            \draw-line                                               %! baca_text_spanner:PiecewiseCommand(1)
                                                #'(0 . -1)                                           %! baca_text_spanner:PiecewiseCommand(1)
                                        \hspace                                                      %! baca_text_spanner:PiecewiseCommand(1)
                                            #0.75                                                    %! baca_text_spanner:PiecewiseCommand(1)
                                        \general-align                                               %! baca_text_spanner:PiecewiseCommand(1)
                                            #Y                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            #1                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            \upright                                                 %! baca_text_spanner:PiecewiseCommand(1)
                                                ord.                                                 %! baca_text_spanner:PiecewiseCommand(1)
                                    }                                                                %! baca_text_spanner:PiecewiseCommand(1)
                                }                                                                    %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #1.25                               %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Invisible lines:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. || ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "pont."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "ord."                                   %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Piece selector groups leaves by measures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A || B',
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "A"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        With spanners:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A -> B ->',
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "A"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Bookends each piece:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A || B',
        ...         bookend=True,
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "B"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "A"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "B"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            - \abjad-invisible-line                                                  %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "A"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        With spanners:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A -> B ->',
        ...         bookend=True,
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "B"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "A"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "B"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            - \abjad-solid-line-with-arrow                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-right-text "A"                                      %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #0.5                                %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        REGRESSION. Backslashed markup is handled correctly:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         r'\baca-damp-markup =|',
        ...         bookend=False,
        ...         selector=baca.rmleaves(2),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-dashed-line-with-hook                                           %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-markup \baca-damp-markup                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(3)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        REGRESSION. Bookended hooks are kerned:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A -| B -|',
        ...         piece_selector=baca.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \override DynamicLineSpanner.staff-padding = #'5                         %! baca_dls_staff_padding:OverrideCommand(1)
                            \override TextSpanner.staff-padding = #4.5                               %! baca_text_spanner_staff_padding:OverrideCommand(1)
                            e'8                                                                      %! baca_make_even_divisions
                            - \abjad-solid-line-with-hook                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-solid-line-with-hook                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-solid-line-with-hook                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "A"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \abjad-solid-line-with-hook                                            %! baca_text_spanner:PiecewiseCommand(1)
                            - \baca-text-spanner-left-text "B"                                       %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.text \markup {                              %! baca_text_spanner:PiecewiseCommand(1)
                                \concat                                                              %! baca_text_spanner:PiecewiseCommand(1)
                                    {                                                                %! baca_text_spanner:PiecewiseCommand(1)
                                        \raise                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            #-1                                                      %! baca_text_spanner:PiecewiseCommand(1)
                                            \draw-line                                               %! baca_text_spanner:PiecewiseCommand(1)
                                                #'(0 . -1)                                           %! baca_text_spanner:PiecewiseCommand(1)
                                        \hspace                                                      %! baca_text_spanner:PiecewiseCommand(1)
                                            #0.75                                                    %! baca_text_spanner:PiecewiseCommand(1)
                                        \general-align                                               %! baca_text_spanner:PiecewiseCommand(1)
                                            #Y                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            #1                                                       %! baca_text_spanner:PiecewiseCommand(1)
                                            \upright                                                 %! baca_text_spanner:PiecewiseCommand(1)
                                                A                                                    %! baca_text_spanner:PiecewiseCommand(1)
                                    }                                                                %! baca_text_spanner:PiecewiseCommand(1)
                                }                                                                    %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.padding #1.25                               %! baca_text_spanner:PiecewiseCommand(1)
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! baca_text_spanner:PiecewiseCommand(1)
                            \startTextSpan                                                           %! baca_text_spanner:PiecewiseCommand(1)
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \stopTextSpan                                                            %! baca_text_spanner:PiecewiseCommand(2)
                            ]                                                                        %! baca_make_even_divisions
                            \revert DynamicLineSpanner.staff-padding                                 %! baca_dls_staff_padding:OverrideCommand(2)
                            \revert TextSpanner.staff-padding                                        %! baca_text_spanner_staff_padding:OverrideCommand(2)
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    shape_to_style = {
        '=>': 'dashed-line-with-arrow',
        '=|': 'dashed-line-with-hook',
        '||': 'invisible-line',
        '->': 'solid-line-with-arrow',
        '-|': 'solid-line-with-hook',
        }
    if isinstance(items, str):
        items_: typing.List[typing.Union[str, abjad.Markup]] = []
        current_item: typing.List[str] = []
        for word in items.split():
            if word in shape_to_style:
                if current_item:
                    item_ = ' '.join(current_item)
                    if boxed:
                        markup = abjad.Markup.from_literal(item_)
                        markup = markup.box().override(('box-padding', 0.5))
                        items_.append(markup)
                    else:
                        items_.append(item_)
                    current_item = []
                items_.append(word)
            else:
                current_item.append(word)
        if current_item:
            item_ = ' '.join(current_item)
            if boxed:
                markup = abjad.Markup.from_literal(item_)
                markup = markup.box().override(('box-padding', 0.5))
                items_.append(markup)
            else:
                items_.append(item_)
        items = items_
    bundles = []
    if len(items) == 1:
        raise NotImplementedError('implement lone item')
    if lilypond_id is None:
        command = r'\stopTextSpan'
    elif lilypond_id == 1:
        command = r'\stopTextSpanOne'
    elif lilypond_id == 2:
        command = r'\stopTextSpanTwo'
    elif lilypond_id == 3:
        command = r'\stopTextSpanThree'
    else:
        raise ValueError(lilypond_id)
    stop_text_span = abjad.StopTextSpan(command=command)
    cyclic_items = abjad.CyclicTuple(items)
    for i, item in enumerate(cyclic_items):
        if item in shape_to_style:
            continue
        if isinstance(item, str) and item.startswith('\\'):
            item_markup = rf'- \baca-text-spanner-left-markup {item}'
        elif isinstance(item, str):
            item_markup = rf'- \baca-text-spanner-left-text "{item}"'
        else:
            item_markup = item
            assert isinstance(item_markup, abjad.Markup)
            item_markup = item_markup.upright()
        prototype = (str, abjad.Markup)
        assert isinstance(item_markup, prototype)
        style = 'invisible-line'
        if cyclic_items[i + 1] in shape_to_style:
            style = shape_to_style[cyclic_items[i + 1]]
            right_text = cyclic_items[i + 2]
        else:
            right_text = cyclic_items[i + 1]
        right_markup: typing.Union[str, abjad.Markup]
        if isinstance(right_text, str):
            if 'hook' not in style:
                if right_text.startswith('\\'):
                    right_markup = rf'- \baca-text-spanner-right-markup'
                    right_markup += rf' {right_text}'
                else:
                    right_markup = rf'- \baca-text-spanner-right-text'
                    right_markup += rf' "{right_text}"'
            else:
                right_markup = abjad.Markup.from_literal(right_text)
                assert isinstance(right_markup, abjad.Markup)
                right_markup = right_markup.upright()
        else:
            assert isinstance(right_text, abjad.Markup)
            right_markup = right_text.upright()
        if lilypond_id is None:
            command = r'\startTextSpan'
        elif lilypond_id == 1:
            command = r'\startTextSpanOne'
        elif lilypond_id == 2:
            command = r'\startTextSpanTwo'
        elif lilypond_id == 3:
            command = r'\startTextSpanThree'
        else:
            raise ValueError(lilypond_id)
        start_text_span = abjad.StartTextSpan(
            command=command,
            left_text=item_markup,
            style=style,
            )
        if tweaks:
            PiecewiseCommand._apply_tweaks(start_text_span, tweaks)
        # kerns bookended hook
        if 'hook' in style:
            assert isinstance(right_markup, abjad.Markup)
            line = abjad.Markup.draw_line(0, -1)
            line = line.raise_(-1)
            hspace = abjad.Markup.hspace(0.75)
            right_markup = right_markup.general_align('Y', 1)
            right_markup = abjad.Markup.concat([line, hspace, right_markup])
        bookended_spanner_start = abjad.new(
            start_text_span,
            right_text=right_markup,
            )
        # TODO: find some way to make these tweaks explicit to composer
        manager = abjad.tweak(bookended_spanner_start)
        manager.bound_details__right__stencil_align_dir_y = abjad.Center
        if 'hook' in style:
            manager.bound_details__right__padding = 1.25
        else:
            manager.bound_details__right__padding = 0.5
        bundle = IndicatorBundle(
            stop_text_span,
            start_text_span,
            bookended_spanner_start=bookended_spanner_start,
            enchained=True,
            )
        bundles.append(bundle)
    return PiecewiseCommand(
        bookend=bookend,
        bundles=bundles,
        leak=leak,
        piece_selector=piece_selector,
        selector=selector,
        tags=[tag],
        )
