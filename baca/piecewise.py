"""
Piecewise.
"""
import typing
from inspect import currentframe as _frame

import abjad

from . import classes as _classes
from . import commandclasses as _commandclasses
from . import const as _const
from . import scoping as _scoping
from . import selection as _selection
from . import selectors as _selectors
from . import sequence as _sequence
from . import tags as _tags
from . import typings


class Bundle:
    """
    Bundle.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_bookended_spanner_start",
        "_indicator",
        "_spanner_start",
        "_spanner_stop",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookended_spanner_start: typing.Any = None,
        indicator: typing.Any = None,
        spanner_start: typing.Any = None,
        spanner_stop: typing.Any = None,
    ) -> None:
        self._bookended_spanner_start = bookended_spanner_start
        self._indicator = indicator
        self._spanner_start = spanner_start
        self._spanner_stop = spanner_stop

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def bookended_spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets bookended start text span indicator.
        """
        return self._bookended_spanner_start

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


class PiecewiseCommand(_scoping.Command):
    """
    Piecewise indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_autodetect_right_padding",
        "_bookend",
        "_bundles",
        "_final_piece_spanner",
        "_leak_spanner_stop",
        "_left_broken",
        "_pieces",
        "_remove_length_1_spanner_start",
        "_right_broken",
        "_selector",
        "_tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        autodetect_right_padding: bool = None,
        bookend: typing.Union[bool, int] = None,
        bundles: typing.List[Bundle] = None,
        final_piece_spanner: typing.Any = None,
        leak_spanner_stop: bool = None,
        left_broken: bool = None,
        map=None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        pieces=_selectors.leaves(),
        remove_length_1_spanner_start: bool = None,
        right_broken: typing.Any = None,
        scope: _scoping.ScopeTyping = None,
        selector=_selectors.leaves(),
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
        tweaks: abjad.IndexedTweakManagers = None,
    ) -> None:
        _scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
        )
        if autodetect_right_padding is not None:
            autodetect_right_padding = bool(autodetect_right_padding)
        self._autodetect_right_padding = autodetect_right_padding
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        bundles_ = None
        if bundles is not None:
            bundles_ = abjad.CyclicTuple(bundles)
        self._bundles = bundles_
        if final_piece_spanner not in (None, False):
            assert getattr(final_piece_spanner, "spanner_start", False)
        self._final_piece_spanner = final_piece_spanner
        if leak_spanner_stop is not None:
            leak_spanner_stop = bool(leak_spanner_stop)
        self._leak_spanner_stop = leak_spanner_stop
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if pieces is not None:
            assert callable(pieces), repr(pieces)
        self._pieces = pieces
        if remove_length_1_spanner_start is not None:
            remove_length_1_spanner_start = bool(remove_length_1_spanner_start)
        self._remove_length_1_spanner_start = remove_length_1_spanner_start
        self._right_broken = right_broken
        _scoping.validate_indexed_tweaks(tweaks)
        self._tweaks = tweaks

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
        if self.pieces is not None:
            assert not isinstance(self.pieces, str)
            pieces = self.pieces(argument)
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
        just_backstole_right_text = None
        just_bookended_leaf = None
        previous_had_bookend = None
        total_pieces = len(pieces)
        for i, piece in enumerate(pieces):
            start_leaf = _selection.Selection(piece).leaf(0)
            stop_leaf = _selection.Selection(piece).leaf(-1)
            is_first_piece = i == 0
            is_penultimate_piece = i == piece_count - 2
            is_final_piece = i == piece_count - 1
            if is_final_piece and self.right_broken:
                bundle = Bundle(spanner_start=self.right_broken)
                tag = _scoping.site(_frame(), self, n=1)
                tag = tag.append(_tags.RIGHT_BROKEN)
                self._attach_indicators(bundle, stop_leaf, i, total_pieces, tag=tag)
            if bookend_pattern.matches_index(i, piece_count) and 1 < len(piece):
                should_bookend = True
            else:
                should_bookend = False
            if is_final_piece and self.final_piece_spanner is False:
                should_bookend = False
            bundle = self.bundles[i]
            if (
                is_final_piece
                and self.right_broken
                and not isinstance(bundle.spanner_start, abjad.StartTextSpan)
            ):
                should_bookend = False
            if is_final_piece and just_backstole_right_text:
                bundle = abjad.new(bundle, spanner_start=None)
            next_bundle = self.bundles[i + 1]
            if should_bookend and bundle.bookended_spanner_start:
                bundle = abjad.new(bundle, spanner_start=bundle.bookended_spanner_start)
            if (
                is_penultimate_piece
                and (len(pieces[-1]) == 1 or self.final_piece_spanner is False)
                and isinstance(next_bundle.spanner_start, abjad.StartTextSpan)
            ):
                bundle = abjad.new(bundle, spanner_start=bundle.bookended_spanner_start)
                just_backstole_right_text = True
            if (
                len(piece) == 1
                and bundle.compound()
                and self.remove_length_1_spanner_start
            ):
                bundle = abjad.new(bundle, spanner_start=None)
            if is_final_piece and bundle.spanner_start:
                if isinstance(bundle.spanner_start, abjad.StartHairpin):
                    if self.final_piece_spanner:
                        bundle = abjad.new(
                            bundle, spanner_start=self.final_piece_spanner
                        )
                    elif self.final_piece_spanner is False:
                        bundle = abjad.new(bundle, spanner_start=None)
                elif isinstance(bundle.spanner_start, abjad.StartTextSpan):
                    if self.final_piece_spanner is False:
                        bundle = abjad.new(bundle, spanner_start=None)
            tag = _scoping.site(_frame(), self, n=2)
            if is_first_piece or previous_had_bookend:
                bundle = abjad.new(bundle, spanner_stop=None)
                if self.left_broken:
                    tag = tag.append(_tags.LEFT_BROKEN)
            if is_final_piece and self.right_broken:
                tag = tag.append(_tags.RIGHT_BROKEN)
            autodetected_right_padding = None
            # solution is merely heuristic;
            # TextSpanner.bound-details.right.to-extent = ##t implementation
            # only 100% workable solution
            if is_final_piece and self.autodetect_right_padding:
                if abjad.get.annotation(stop_leaf, _const.PHANTOM) is True:
                    autodetected_right_padding = 2.5
                # stop leaf multiplied whole note on fermata measure downbeat
                elif (
                    isinstance(stop_leaf, abjad.Note)
                    and stop_leaf.written_duration == 1
                    and stop_leaf.multiplier == abjad.Multiplier(1, 4)
                ):
                    autodetected_right_padding = 3.25
                # stop leaf on normal measure downbeat
                else:
                    autodetected_right_padding = 2.75
                # there's probably a third case for normal midmeasure leaf
                # else:
                #    autodetected_right_padding = 1.25
            self._attach_indicators(
                bundle,
                start_leaf,
                i,
                total_pieces,
                autodetected_right_padding=autodetected_right_padding,
                just_bookended_leaf=just_bookended_leaf,
                tag=tag,
            )
            if should_bookend:
                tag = _scoping.site(_frame(), self, n=3)
                if is_final_piece and self.right_broken:
                    tag = tag.append(_tags.RIGHT_BROKEN)
                if bundle.bookended_spanner_start is not None:
                    next_bundle = abjad.new(next_bundle, spanner_start=None)
                if next_bundle.compound():
                    next_bundle = abjad.new(next_bundle, spanner_start=None)
                self._attach_indicators(
                    next_bundle, stop_leaf, i, total_pieces, tag=tag
                )
                just_bookended_leaf = stop_leaf
            elif (
                is_final_piece
                and not just_backstole_right_text
                and next_bundle.spanner_stop
                and ((start_leaf is not stop_leaf) or self.leak_spanner_stop)
            ):
                spanner_stop = abjad.new(next_bundle.spanner_stop)
                if self.leak_spanner_stop:
                    spanner_stop = abjad.new(spanner_stop, leak=True)
                bundle = Bundle(spanner_stop=spanner_stop)
                tag = _scoping.site(_frame(), self, n=4)
                if self.right_broken:
                    tag = tag.append(_tags.RIGHT_BROKEN)
                self._attach_indicators(bundle, stop_leaf, i, total_pieces, tag=tag)
            previous_had_bookend = should_bookend

    ### PRIVATE METHODS ###

    def _attach_indicators(
        self,
        bundle,
        leaf,
        i,
        total_pieces,
        autodetected_right_padding=None,
        just_bookended_leaf=None,
        tag=None,
    ):
        assert isinstance(tag, abjad.Tag), repr(tag)
        for indicator in bundle:
            if indicator in (True, False):
                pass
            else:
                indicator = abjad.new(indicator)
            if not getattr(indicator, "trend", False) and leaf is just_bookended_leaf:
                continue
            if autodetected_right_padding is not None and isinstance(
                indicator, abjad.StartTextSpan
            ):
                number = autodetected_right_padding
                abjad.tweak(
                    indicator,
                    tag=self.tag.append(tag)
                    .append(_tags.AUTODETECT)
                    .append(_tags.SPANNER_START),
                ).bound_details__right__padding = number
            if self.tweaks and hasattr(indicator, "_tweaks"):
                _scoping.apply_tweaks(indicator, self.tweaks, i=i, total=total_pieces)
            elif (
                self.tweaks
                and hasattr(indicator, "tweaks")
                and getattr(indicator, "_is_dataclass", False) is True
            ):
                _scoping.apply_tweaks(indicator, self.tweaks, i=i, total=total_pieces)
            reapplied = _scoping.remove_reapplied_wrappers(leaf, indicator)
            tag_ = self.tag.append(tag)
            if getattr(indicator, "spanner_start", None) is True:
                tag_ = tag_.append(_tags.SPANNER_START)
            if getattr(indicator, "spanner_stop", None) is True:
                tag_ = tag_.append(_tags.SPANNER_STOP)
            wrapper = abjad.attach(indicator, leaf, tag=tag_, wrapper=True)
            if _scoping.compare_persistent_indicators(indicator, reapplied):
                status = "redundant"
                _scoping.treat_persistent_wrapper(
                    self.runtime["manifests"], wrapper, status
                )

    ### PUBLIC PROPERTIES ###

    @property
    def autodetect_right_padding(self) -> typing.Optional[bool]:
        """
        Is true when (text) spanner autodetects right padding.
        """
        return self._autodetect_right_padding

    @property
    def bookend(self) -> typing.Optional[typing.Union[bool, int]]:
        """
        Gets bookend token.

        Command attaches indicator to first leaf in each group of selector output when
        ``bookend`` is false.

        Command attaches indicator to both first leaf and last leaf in each group of
        selector output when ``bookend`` is true.

        When ``bookend`` equals integer ``n``, command attaches indicator to first leaf
        and last leaf in group ``n`` of selector output and attaches indicator to only
        first leaf in other groups of selector output.
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
    def leak_spanner_stop(self) -> typing.Optional[bool]:
        """
        Is true when piecewise command leaks stop indicator.
        """
        return self._leak_spanner_stop

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when piecewise command is left-broken.
        """
        return self._left_broken

    @property
    def pieces(self):
        """
        Gets piece selector.
        """
        return self._pieces

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
    def selector(self):
        """
        Gets (first-order) selector.
        """
        return self._selector

    @property
    def tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        """
        Gets tweaks.
        """
        return self._tweaks


def bow_speed_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = True,
    bookend: typing.Union[bool, int] = False,
    final_piece_spanner: bool = None,
    left_broken: bool = None,
    left_broken_text: str = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes bow speed spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.BOW_SPEED_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="BowSpeed",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def circle_bow_spanner(
    *tweaks: abjad.IndexedTweakManager,
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-left-broken-circle-bowing-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    qualifier: str = None,
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes circle bow spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.CIRCLE_BOW_SPANNER)
    if qualifier is None:
        string = r"\baca-circle-markup =|"
    else:
        assert isinstance(qualifier, str), repr(qualifier)
        string = rf"\baca-circle-{qualifier}-markup =|"
    command = text_spanner(
        string,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="CircleBow",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def clb_spanner(
    string_number: int,
    *tweaks: abjad.IndexedTweakManager,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-left-broken-clb-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes clb spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.CLB_SPANNER)
    assert string_number in (1, 2, 3, 4), repr(string_number)
    if string_number == 1:
        markup = r"\baca-damp-clb-one-markup"
    elif string_number == 2:
        markup = r"\baca-damp-clb-two-markup"
    elif string_number == 3:
        markup = r"\baca-damp-clb-three-markup"
    elif string_number == 4:
        markup = r"\baca-damp-clb-four-markup"
    else:
        raise Exception(string_number)
    command = text_spanner(
        f"{markup} =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="CLB",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def covered_spanner(
    *tweaks: abjad.IndexedTweakManager,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    argument: str = r"\baca-covered-markup =|",
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-left-broken-covered-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes covered spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.COVERED_SPANNER)
    command = text_spanner(
        argument,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Covered",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def damp_spanner(
    *tweaks: abjad.IndexedTweakManager,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-left-broken-damp-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes damp spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.DAMP_SPANNER)
    command = text_spanner(
        r"\baca-damp-markup =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Damp",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def dynamic(
    dynamic: typing.Union[str, abjad.Dynamic],
    *tweaks: abjad.TweakInterface,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    selector=_selectors.phead(0),
    redundant: bool = None,
) -> _commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic.

    ..  container:: example

        Attaches dynamic to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic("f"),
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
                        \f
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

    ..  container:: example

        Works with effort dynamics:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('"f"'),
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
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        \baca-effort-f
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

    ..  container:: example

        Works with hairpins:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.dynamic("p"),
        ...     baca.dynamic("<"),
        ...     baca.dynamic(
        ...         "!",
        ...         selector=baca.selectors.pleaf(-1),
        ...     ),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 13)),
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
                        \baca-new-spacing-section #1 #13
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #13
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #13
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \!
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Works with tweaks:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.dynamic("p", abjad.tweak("#'(-4 . 0)").extra_offset),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak extra-offset #'(-4 . 0)
                        \p
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    """
    if isinstance(dynamic, str):
        indicator = make_dynamic(dynamic)
    else:
        indicator = dynamic
    prototype = (abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin)
    assert isinstance(indicator, prototype), repr(indicator)
    return _commandclasses.IndicatorCommand(
        context="Voice",
        indicators=[indicator],
        map=map,
        match=match,
        measures=measures,
        redundant=redundant,
        selector=selector,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )


def hairpin(
    dynamics: typing.Union[str, typing.List],
    *tweaks: abjad.TweakInterface,
    bookend: typing.Union[bool, int] = -1,
    final_hairpin: typing.Union[bool, str, abjad.StartHairpin] = None,
    forbid_al_niente_to_bar_line: bool = None,
    left_broken: bool = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    remove_length_1_spanner_start: bool = None,
    right_broken: bool = None,
    selector=_selectors.leaves(),
) -> PiecewiseCommand:
    r"""
    Attaches hairpin.

    ..  container:: example

        Conventional dynamics:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin("p < f", bookend=-1),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        [
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \f
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Effort dynamic al niente:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('"ff" >o niente'),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \baca-effort-ff
                        - \tweak to-barline ##t
                        - \tweak circled-tip ##t
                        \>
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \!
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Effort dynamic dal niente:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('niente o< "ff"'),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \!
                        - \tweak circled-tip ##t
                        \<
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \baca-effort-ff
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Effort dynamic constante:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('"p" -- f'),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \baca-effort-p
                        - \tweak stencil #constante-hairpin
                        \<
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \f
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Effort dynamics crescendo subito, decrescendo subito:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin(
        ...         '"mp" <| "f"',
        ...         selector=baca.selectors.leaves((None, 7)),
        ...         ),
        ...     baca.hairpin(
        ...         '"mf" |> "p"',
        ...         selector=baca.selectors.leaves((7, None)),
        ...         ),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \baca-effort-mp
                        - \tweak stencil #abjad-flared-hairpin
                        \<
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        \baca-effort-f
                        ]
                        d''8
                        - \tweak color #(x11-color 'blue)
                        \baca-effort-mf
                        - \tweak stencil #abjad-flared-hairpin
                        \>
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \baca-effort-p
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Piece selector groups leaves by measures:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         "p f",
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        \p
                        [
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        \f
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        \p
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        \f
                        [
                        e'8
                        d''8
                        \p
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

        With hairpins:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         "p < f >",
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        [
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        - \tweak color #(x11-color 'blue)
                        \f
                        \>
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        - \tweak color #(x11-color 'blue)
                        \p
                        \<
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        - \tweak color #(x11-color 'blue)
                        \f
                        \>
                        [
                        e'8
                        d''8
                        \p
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

        Bookends each piece:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         "p f",
        ...         bookend=True,
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        \p
                        [
                        d''8
                        f'8
                        e''8
                        \f
                        ]
                        g'8
                        \f
                        [
                        f''8
                        e'8
                        \p
                        ]
                        d''8
                        \p
                        [
                        f'8
                        e''8
                        g'8
                        \f
                        ]
                        f''8
                        \f
                        [
                        e'8
                        d''8
                        \p
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

        With hairpins:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin(
        ...         "p -- f >",
        ...         bookend=True,
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \p
                        - \tweak stencil #constante-hairpin
                        \<
                        [
                        d''8
                        f'8
                        e''8
                        \f
                        ]
                        g'8
                        - \tweak color #(x11-color 'blue)
                        \f
                        \>
                        [
                        f''8
                        e'8
                        \p
                        ]
                        d''8
                        - \tweak color #(x11-color 'blue)
                        \p
                        - \tweak stencil #constante-hairpin
                        \<
                        [
                        f'8
                        e''8
                        g'8
                        \f
                        ]
                        f''8
                        - \tweak color #(x11-color 'blue)
                        \f
                        \>
                        [
                        e'8
                        d''8
                        \p
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Works with lone dynamic:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin("f", bookend=False),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        \f
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Works with lone hairpin:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpin("< !"),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 C5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        e'8
                        \<
                        [
                        d''8
                        f'8
                        c''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        c''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \!
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Works with to-barline tweak:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(4),
        ...     baca.hairpin(
        ...         "p -- niente",
        ...         abjad.tweak(True).to_barline,
        ...         selector=baca.selectors.leaves((None, 2)),
        ...     ),
        ...     baca.hairpin(
        ...         "f -- niente",
        ...         abjad.tweak(True).to_barline,
        ...         selector=baca.selectors.leaves((2, None)),
        ...     ),
        ...     baca.pitches("C4 D4"),
        ...     baca.skeleton("{ c2 r4. c2 r4. }"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        {
                            \override DynamicLineSpanner.staff-padding = 4
                            c'2
                            - \tweak color #(x11-color 'blue)
                            \p
                            - \tweak to-barline ##t
                            - \tweak stencil #constante-hairpin
                            \<
                            r4.
                            \!
                            d'2
                            - \tweak color #(x11-color 'blue)
                            \f
                            - \tweak to-barline ##t
                            - \tweak stencil #constante-hairpin
                            \<
                            r4.
                            \!
                            \revert DynamicLineSpanner.staff-padding
                        }
                    }
                >>
            }

    ..  container:: example

        Works with interposed niente dynamics:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(4),
        ...     baca.hairpin(
        ...         "mf niente o< p",
        ...         bookend=False,
        ...         pieces=baca.selectors.mgroups([1, 2, 1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 4
                        e'8
                        \mf
                        [
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        - \tweak color #(x11-color 'blue)
                        \!
                        - \tweak circled-tip ##t
                        \<
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        \p
                        [
                        e'8
                        d''8
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Works with parenthesized dynamics:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(4),
        ...     baca.hairpin("(mp) < mf"),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 4
                        e'8
                        - \tweak color #(x11-color 'blue)
                        \baca-mp-parenthesized
                        \<
                        [
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \mf
                        ]
                        \revert DynamicLineSpanner.staff-padding
                    }
                >>
            }

    """
    if isinstance(dynamics, str):
        bundles = parse_hairpin_descriptor(
            dynamics,
            *tweaks,
            forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line,
        )
    else:
        bundles = dynamics
    for item in bundles:
        assert isinstance(item, Bundle), repr(dynamic)
    final_hairpin_: typing.Union[bool, abjad.StartHairpin, None] = None
    if isinstance(final_hairpin, bool):
        final_hairpin_ = final_hairpin
    elif isinstance(final_hairpin, str):
        final_hairpin_ = abjad.StartHairpin(final_hairpin)
    if left_broken is not None:
        left_broken = bool(left_broken)
    if remove_length_1_spanner_start is not None:
        remove_length_1_spanner_start = bool(remove_length_1_spanner_start)
    right_broken_: typing.Any = False
    if bool(right_broken) is True:
        right_broken_ = abjad.LilyPondLiteral(r"\!", format_slot="after")
    return PiecewiseCommand(
        bookend=bookend,
        bundles=bundles,
        final_piece_spanner=final_hairpin_,
        left_broken=left_broken,
        match=match,
        map=map,
        measures=measures,
        pieces=pieces,
        remove_length_1_spanner_start=remove_length_1_spanner_start,
        right_broken=right_broken_,
        selector=selector,
        tags=[_scoping.site(_frame())],
    )


def half_clt_spanner(
    *tweaks: abjad.IndexedTweakManager,
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-left-broken-half-clt-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes 1/2 clt spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.HALF_CLT_SPANNER)
    command = text_spanner(
        "½ clt =|",
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="HalfCLT",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def make_dynamic(
    string: str, *, forbid_al_niente_to_bar_line: bool = None
) -> typing.Union[abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin]:
    r"""
    Makes dynamic.

    ..  container:: example

        >>> baca.make_dynamic("p")
        Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("sffz")
        Dynamic(name='ff', command='\\baca-sffz', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=3, tweaks=None)

        >>> baca.make_dynamic("niente")
        Dynamic(name='niente', command='\\!', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity, tweaks=None)

        >>> baca.make_dynamic("<")
        StartHairpin(shape='<', direction=None, tweaks=None)

        >>> baca.make_dynamic("o<|")
        StartHairpin(shape='o<|', direction=None, tweaks=None)

        >>> baca.make_dynamic("appena-udibile")
        Dynamic(name='appena udibile', command='\\baca-appena-udibile', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=None, tweaks=None)

    ..  container:: example

        Stop hairpin:

        >>> baca.make_dynamic("!")
        StopHairpin(leak=None)

    ..  container:: example

        Ancora dynamics:

        >>> baca.make_dynamic("p-ancora")
        Dynamic(name='p', command='\\baca-p-ancora', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-ancora")
        Dynamic(name='f', command='\\baca-f-ancora', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Composite dynamics:

        >>> baca.make_dynamic("pf")
        Dynamic(name='f', command='\\baca-pf', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=2, tweaks=None)

        >>> baca.make_dynamic("pff")
        Dynamic(name='ff', command='\\baca-pff', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=3, tweaks=None)

    ..  container:: example

        Effort dynamics:

        >>> baca.make_dynamic('"p"')
        Dynamic(name='"p"', command='\\baca-effort-p', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic('"f"')
        Dynamic(name='"f"', command='\\baca-effort-f', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Effort dynamics (parenthesized):

        >>> baca.make_dynamic('("p")')
        Dynamic(name='p', command='\\baca-effort-p-parenthesized', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic('("f")')
        Dynamic(name='f', command='\\baca-effort-f-parenthesized', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Effort dynamics (ancora):

        >>> baca.make_dynamic('"p"-ancora')
        Dynamic(name='p', command='\\baca-effort-ancora-p', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic('"f"-ancora')
        Dynamic(name='f', command='\\baca-effort-ancora-f', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Effort dynamics (sempre):

        >>> baca.make_dynamic('"p"-sempre')
        Dynamic(name='p', command='\\baca-effort-p-sempre', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic('"f"-sempre')
        Dynamic(name='f', command='\\baca-effort-f-sempre', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Sub. effort dynamics:

        >>> baca.make_dynamic("p-effort-sub")
        Dynamic(name='p', command='\\baca-p-effort-sub', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-effort-sub")
        Dynamic(name='f', command='\\baca-f-effort-sub', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Mezzo:

        >>> baca.make_dynamic("m")
        Dynamic(name='m', command='\\baca-m', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=None, tweaks=None)

    ..  container:: example

        Parenthesized dynamics:

        >>> baca.make_dynamic("(p)")
        Dynamic(name='p', command='\\baca-p-parenthesized', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("(f)")
        Dynamic(name='f', command='\\baca-f-parenthesized', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Poco scratch dynamics:

        >>> baca.make_dynamic("p-poco-scratch")
        Dynamic(name='p', command='\\baca-p-poco-scratch', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-poco-scratch")
        Dynamic(name='f', command='\\baca-f-poco-scratch', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Possibile dynamics:

        >>> baca.make_dynamic("p-poss")
        Dynamic(name='p', command='\\baca-p-poss', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-poss")
        Dynamic(name='f', command='\\baca-f-poss', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Scratch dynamics:

        >>> baca.make_dynamic("p-scratch")
        Dynamic(name='p', command='\\baca-p-scratch', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-scratch")
        Dynamic(name='f', command='\\baca-f-scratch', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Sempre dynamics:

        >>> baca.make_dynamic("p-sempre")
        Dynamic(name='p', command='\\baca-p-sempre', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-sempre")
        Dynamic(name='f', command='\\baca-f-sempre', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Subito dynamics:

        >>> baca.make_dynamic("p-sub")
        Dynamic(name='p', command='\\baca-p-sub', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-sub")
        Dynamic(name='f', command='\\baca-f-sub', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Whiteout dynamics:

        >>> baca.make_dynamic("p-whiteout")
        Dynamic(name='p', command='\\baca-p-whiteout', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None)

        >>> baca.make_dynamic("f-whiteout")
        Dynamic(name='f', command='\\baca-f-whiteout', direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None)

    ..  container:: example

        Al niente hairpins are special-cased to carry to-barline tweaks:

        >>> baca.make_dynamic(">o")
        StartHairpin(shape='>o', direction=None, tweaks=TweakInterface(('_literal', None), ('to_barline', True)))

        >>> baca.make_dynamic("|>o")
        StartHairpin(shape='|>o', direction=None, tweaks=TweakInterface(('_literal', None), ('to_barline', True)))

    ..  container:: example exception

        Errors on nondynamic input:

        >>> baca.make_dynamic("text")
        Traceback (most recent call last):
            ...
        Exception: the string 'text' initializes no known dynamic.

    """
    assert isinstance(string, str), repr(string)
    scheme_manifest = _classes.SchemeManifest()
    known_shapes = abjad.StartHairpin("<").known_shapes
    indicator: typing.Union[abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin]
    if "_" in string:
        raise Exception(f"use hyphens instead of underscores ({string!r}).")
    if string == "niente":
        indicator = abjad.Dynamic("niente", command=r"\!")
    elif string.endswith("-ancora") and '"' not in string:
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-ancora"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-ancora") and '"' in string:
        dynamic = string.split("-")[0]
        dynamic = dynamic.strip('"')
        command = rf"\baca-effort-ancora-{dynamic}"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-effort-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-effort-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith('("') and string.endswith('")'):
        dynamic = string.strip('(")')
        command = rf"\baca-effort-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.startswith("(") and string.endswith(")"):
        dynamic = string.strip("()")
        command = rf"\baca-{dynamic}-parenthesized"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poco-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poco-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-poss"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-poss"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-scratch"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-scratch"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and not string.startswith('"'):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sempre") and string.startswith('"'):
        dynamic = string.split("-")[0].strip('"')
        command = rf"\baca-effort-{dynamic}-sempre"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-sub"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-sub"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif string.endswith("-whiteout"):
        dynamic = string.split("-")[0]
        command = rf"\baca-{dynamic}-whiteout"
        indicator = abjad.Dynamic(dynamic, command=command)
    elif "baca-" + string in scheme_manifest.dynamics:
        name = scheme_manifest.dynamic_to_steady_state(string)
        command = "\\baca-" + string
        pieces = string.split("-")
        if pieces[0] in ("sfz", "sffz", "sfffz"):
            sforzando = True
        else:
            sforzando = False
        name_is_textual = not (sforzando)
        indicator = abjad.Dynamic(
            name,
            command=command,
            name_is_textual=name_is_textual,
        )
    elif string.startswith('"'):
        assert string.endswith('"')
        stripped_string = string.strip('"')
        command = rf"\baca-effort-{stripped_string}"
        indicator = abjad.Dynamic(f"{string}", command=command)
    elif string in known_shapes:
        indicator = abjad.StartHairpin(string)
        if string.endswith(">o") and not forbid_al_niente_to_bar_line:
            abjad.tweak(indicator).to_barline = True
    elif string == "!":
        indicator = abjad.StopHairpin()
    elif string == "m":
        indicator = abjad.Dynamic("m", command=r"\baca-m")
    else:
        failed = False
        try:
            indicator = abjad.Dynamic(string)
        except Exception:
            failed = True
        if failed:
            raise Exception(f"the string {string!r} initializes no known dynamic.")
    return indicator


def material_annotation_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    left_broken: bool = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner()
    selector=_selectors.rleaves(),
) -> PiecewiseCommand:
    """
    Makes material annotation spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.MATERIAL_ANNOTATION_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        lilypond_id="MaterialAnnotation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def metric_modulation_spanner(
    *tweaks: abjad.IndexedTweakManager,
    argument: str = r"MM =|",
    autodetect_right_padding: bool = True,
    left_broken: bool = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner()
    selector=_selectors.rleaves(),
) -> PiecewiseCommand:
    """
    Makes metric modulation spanner.
    """
    # TODO: tag red tweak with METRIC_MODULATION_SPANNER_COLOR
    # red_tweak = abjad.tweak("#red").color
    # tweaks = tweaks + (red_tweak,)
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.METRIC_MODULATION_SPANNER)
    command = text_spanner(
        argument,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        lilypond_id="MetricModulation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def parse_hairpin_descriptor(
    descriptor: str,
    *tweaks: abjad.TweakInterface,
    forbid_al_niente_to_bar_line: bool = None,
) -> typing.List[Bundle]:
    r"""
    Parses hairpin descriptor.

    ..  container:: example

        >>> for item in baca.parse_hairpin_descriptor("f"):
        ...     item
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor('"f"'):
        ...     item
        Bundle(indicator=Dynamic(name='"f"', command='\\baca-effort-f', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("niente"):
        ...     item
        Bundle(indicator=Dynamic(name='niente', command='\\!', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("<"):
        ...     item
        Bundle(spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("< !"):
        ...     item
        Bundle(spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))
        Bundle(indicator=StopHairpin(leak=None))

        >>> for item in baca.parse_hairpin_descriptor("o<|"):
        ...     item
        Bundle(spanner_start=StartHairpin(shape='o<|', direction=None, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("--"):
        ...     item
        Bundle(spanner_start=StartHairpin(shape='--', direction=None, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("p < f"):
        ...     item
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None), spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("p <"):
        ...     item
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None), spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("p < !"):
        ...     item
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None), spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))
        Bundle(indicator=StopHairpin(leak=None))

        >>> for item in baca.parse_hairpin_descriptor("< f"):
        ...     item
        Bundle(spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("o< f"):
        ...     item
        Bundle(spanner_start=StartHairpin(shape='o<', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("niente o<| f"):
        ...     item
        Bundle(indicator=Dynamic(name='niente', command='\\!', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity, tweaks=None), spanner_start=StartHairpin(shape='o<|', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("f >"):
        ...     item
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None), spanner_start=StartHairpin(shape='>', direction=None, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("f >o"):
        ...     item
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None), spanner_start=StartHairpin(shape='>o', direction=None, tweaks=TweakInterface(('_literal', None), ('to_barline', True))))

        >>> for item in baca.parse_hairpin_descriptor("p mp mf f"):
        ...     item
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None))
        Bundle(indicator=Dynamic(name='mp', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-1, tweaks=None))
        Bundle(indicator=Dynamic(name='mf', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=1, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("p < f f > p"):
        ...     item
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None), spanner_start=StartHairpin(shape='<', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None))
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None), spanner_start=StartHairpin(shape='>', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("f -- ! > p"):
        ...     item
        Bundle(indicator=Dynamic(name='f', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=2, tweaks=None), spanner_start=StartHairpin(shape='--', direction=None, tweaks=None))
        Bundle(indicator=StopHairpin(leak=None), spanner_start=StartHairpin(shape='>', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None))

        >>> for item in baca.parse_hairpin_descriptor("mf niente o< p"):
        ...     item
        Bundle(indicator=Dynamic(name='mf', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=1, tweaks=None))
        Bundle(indicator=Dynamic(name='niente', command='\\!', direction=Down, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=True, ordinal=NegativeInfinity, tweaks=None), spanner_start=StartHairpin(shape='o<', direction=None, tweaks=None))
        Bundle(indicator=Dynamic(name='p', command=None, direction=None, format_hairpin_stop=False, hide=False, leak=False, name_is_textual=False, ordinal=-2, tweaks=None))

    """
    assert isinstance(descriptor, str), repr(descriptor)
    indicators: typing.List[
        typing.Union[abjad.Dynamic, abjad.StartHairpin, abjad.StopHairpin]
    ] = []
    bundles: typing.List[Bundle] = []
    for string in descriptor.split():
        indicator = make_dynamic(
            string, forbid_al_niente_to_bar_line=forbid_al_niente_to_bar_line
        )
        if not isinstance(indicator, abjad.Dynamic):
            if tweaks and hasattr(indicator, "_tweaks"):
                _scoping.apply_tweaks(indicator, tweaks)
            elif (
                tweaks
                and hasattr(indicator, "tweaks")
                and getattr(indicator, "_is_dataclass", False) is True
            ):
                _scoping.apply_tweaks(indicator, tweaks)
        indicators.append(indicator)
    if len(indicators) == 1:
        if isinstance(indicators[0], abjad.StartHairpin):
            bundle = Bundle(spanner_start=indicators[0])
        else:
            assert isinstance(indicators[0], abjad.Dynamic)
            bundle = Bundle(indicator=indicators[0])
        bundles.append(bundle)
        return bundles
    if isinstance(indicators[0], abjad.StartHairpin):
        result = indicators.pop(0)
        assert isinstance(result, abjad.StartHairpin)
        bundle = Bundle(spanner_start=result)
        bundles.append(bundle)
    if len(indicators) == 1:
        if isinstance(indicators[0], abjad.StartHairpin):
            bundle = Bundle(spanner_start=indicators[0])
        else:
            bundle = Bundle(indicator=indicators[0])
        bundles.append(bundle)
        return bundles
    for left, right in _sequence.Sequence(indicators).nwise():
        if isinstance(left, abjad.StartHairpin) and isinstance(
            right, abjad.StartHairpin
        ):
            raise Exception("consecutive start hairpin commands.")
        elif isinstance(left, abjad.Dynamic) and isinstance(right, abjad.Dynamic):
            bundle = Bundle(indicator=left)
            bundles.append(bundle)
        elif isinstance(left, (abjad.Dynamic, abjad.StopHairpin)) and isinstance(
            right, abjad.StartHairpin
        ):
            bundle = Bundle(indicator=left, spanner_start=right)
            bundles.append(bundle)
    prototype = (abjad.Dynamic, abjad.StopHairpin)
    if indicators and isinstance(indicators[-1], prototype):
        bundle = Bundle(indicator=indicators[-1])
        bundles.append(bundle)
    return bundles


def pitch_annotation_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    left_broken: bool = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner()
    selector=_selectors.rleaves(),
) -> PiecewiseCommand:
    """
    Makes pitch annotation spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.PITCH_ANNOTATION_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        left_broken=left_broken,
        lilypond_id="PitchAnnotation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def pizzicato_spanner(
    *tweaks: abjad.IndexedTweakManager,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-pizz-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes pizzicato spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.PIZZICATO_SPANNER)
    command = text_spanner(
        r"\baca-pizz-markup =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Pizzicato",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def rhythm_annotation_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    left_broken: bool = None,
    leak_spanner_stop: bool = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner()
    selector=_selectors.rleaves(),
) -> PiecewiseCommand:
    """
    Makes rhythm command spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.RHYTHM_ANNOTATION_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=True,
        bookend=False,
        leak_spanner_stop=leak_spanner_stop,
        left_broken=left_broken,
        lilypond_id="RhythmAnnotation",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def scp_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = True,
    bookend: typing.Union[bool, int] = False,
    final_piece_spanner: bool = None,
    left_broken: bool = None,
    left_broken_text: str = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes SCP spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.SCP_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="SCP",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def spazzolato_spanner(
    *tweaks: abjad.IndexedTweakManager,
    # NOTE: autodetect default differs from text_spanner():
    autodetect_right_padding: bool = True,
    items: typing.Union[str, typing.List] = r"\baca-spazzolato-markup =|",
    left_broken: bool = None,
    left_broken_text: typing.Optional[str] = r"\baca-left-broken-spazz-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes spazzolato spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.SPAZZOLATO_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=False,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Spazzolato",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(command, PiecewiseCommand)
    return result


def string_number_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = True,
    bookend: typing.Union[bool, int] = False,
    final_piece_spanner: bool = None,
    left_broken: bool = None,
    left_broken_text: str = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes string number spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.STRING_NUMBER_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="StringNumber",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def tasto_spanner(
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = True,
    bookend: typing.Union[bool, int] = False,
    final_piece_spanner: bool = None,
    left_broken: bool = None,
    left_broken_text: str = r"\baca-left-broken-t-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes tasto spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.TASTO_SPANNER)
    command = text_spanner(
        "T =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="SCP",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def text_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = None,
    bookend: typing.Union[bool, int] = -1,
    boxed: bool = None,
    direction: typing.Union[int, str, abjad.enums.VerticalAlignment] = None,
    final_piece_spanner: bool = None,
    leak_spanner_stop: bool = None,
    left_broken: bool = None,
    left_broken_text: str = None,
    lilypond_id: typing.Union[int, str] = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    selector=_selectors.leaves(),
) -> PiecewiseCommand:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single-segment spanners.

        Dashed line with arrow:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner("pont. => ord."),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-dashed-line-with-arrow
                        - \baca-text-spanner-left-text "pont."
                        - \baca-text-spanner-right-text "ord."
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        Dashed line with hook:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner("pont. =| ord."),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-dashed-line-with-hook
                        - \baca-text-spanner-left-text "pont."
                        - \tweak bound-details.right.text \markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75 \general-align #Y #1 \upright ord. }
                        - \tweak bound-details.right.padding 1.25
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        Solid line with arrow:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner("pont. -> ord."),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "pont."
                        - \baca-text-spanner-right-text "ord."
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        Solid line with hook:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner("pont. -| ord."),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-solid-line-with-hook
                        - \baca-text-spanner-left-text "pont."
                        - \tweak bound-details.right.text \markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75 \general-align #Y #1 \upright ord. }
                        - \tweak bound-details.right.padding 1.25
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        Invisible lines:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner("pont. || ord."),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "pont."
                        - \baca-text-spanner-right-text "ord."
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Piece selector groups leaves by measures:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         "A || B",
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "A"
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        \stopTextSpan
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "B"
                        \startTextSpan
                        f''8
                        e'8
                        ]
                        d''8
                        \stopTextSpan
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "A"
                        \startTextSpan
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        \stopTextSpan
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "B"
                        - \baca-text-spanner-right-text "A"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert DynamicLineSpanner.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        With spanners:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         "A -> B ->",
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "A"
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        \stopTextSpan
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "B"
                        \startTextSpan
                        f''8
                        e'8
                        ]
                        d''8
                        \stopTextSpan
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "A"
                        \startTextSpan
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        \stopTextSpan
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "B"
                        - \baca-text-spanner-right-text "A"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert DynamicLineSpanner.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        Bookends each piece:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         "A || B",
        ...         bookend=True,
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "A"
                        - \baca-text-spanner-right-text "B"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        \stopTextSpan
                        ]
                        g'8
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "B"
                        - \baca-text-spanner-right-text "A"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f''8
                        e'8
                        \stopTextSpan
                        ]
                        d''8
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "A"
                        - \baca-text-spanner-right-text "B"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'8
                        e''8
                        g'8
                        \stopTextSpan
                        ]
                        f''8
                        [
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "B"
                        - \baca-text-spanner-right-text "A"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert DynamicLineSpanner.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

        With spanners:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         "A -> B ->",
        ...         bookend=True,
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "A"
                        - \baca-text-spanner-right-text "B"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        \stopTextSpan
                        ]
                        g'8
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "B"
                        - \baca-text-spanner-right-text "A"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f''8
                        e'8
                        \stopTextSpan
                        ]
                        d''8
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "A"
                        - \baca-text-spanner-right-text "B"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        f'8
                        e''8
                        g'8
                        \stopTextSpan
                        ]
                        f''8
                        [
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "B"
                        - \baca-text-spanner-right-text "A"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert DynamicLineSpanner.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        Indexes tweaks. No purple appears because tweakable indicators appear on pieces
        0, 1, 2 but piece 3 carries only a stop text span:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner(
        ...         "P -> T ->",
        ...         (abjad.tweak("#red").color, 0),
        ...         (abjad.tweak("#blue").color, 1),
        ...         (abjad.tweak("#green").color, 2),
        ...         (abjad.tweak("#purple").color, 3),
        ...         final_piece_spanner=False,
        ...         pieces=baca.selectors.plts(),
        ...     ),
        ...     baca.skeleton("{ c2 c4. c2 c4. }"),
        ...     baca.pitches("C4 D4 E4 F4"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        {
                            \override TextSpanner.staff-padding = 4.5
                            c'2
                            - \abjad-solid-line-with-arrow
                            - \baca-text-spanner-left-text "P"
                            - \tweak color #red
                            \startTextSpan
                            d'4.
                            \stopTextSpan
                            - \abjad-solid-line-with-arrow
                            - \baca-text-spanner-left-text "T"
                            - \tweak color #blue
                            \startTextSpan
                            e'2
                            \stopTextSpan
                            - \abjad-solid-line-with-arrow
                            - \baca-text-spanner-left-text "P"
                            - \baca-text-spanner-right-text "T"
                            - \tweak bound-details.right.padding 0.5
                            - \tweak bound-details.right.stencil-align-dir-y #center
                            - \tweak color #green
                            \startTextSpan
                            f'4.
                            \stopTextSpan
                            \revert TextSpanner.staff-padding
                        }
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Handles backslashed markup correctly:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         r"\baca-damp-markup =|",
        ...         bookend=False,
        ...         selector=baca.selectors.rmleaves(2),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-dashed-line-with-hook
                        - \baca-text-spanner-left-markup \baca-damp-markup
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        [
                        f''8
                        e'8
                        ]
                        d''8
                        \stopTextSpan
                        [
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        [
                        e'8
                        d''8
                        ]
                        \revert DynamicLineSpanner.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Kerns bookended hooks:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         "A -| B -|",
        ...         pieces=baca.selectors.cmgroups([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches("E4 D5 F4 E5 G4 F5"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override DynamicLineSpanner.staff-padding = 5
                        \override TextSpanner.staff-padding = 4.5
                        e'8
                        [
                        - \abjad-solid-line-with-hook
                        - \baca-text-spanner-left-text "A"
                        \startTextSpan
                        d''8
                        f'8
                        e''8
                        ]
                        g'8
                        \stopTextSpan
                        [
                        - \abjad-solid-line-with-hook
                        - \baca-text-spanner-left-text "B"
                        \startTextSpan
                        f''8
                        e'8
                        ]
                        d''8
                        \stopTextSpan
                        [
                        - \abjad-solid-line-with-hook
                        - \baca-text-spanner-left-text "A"
                        \startTextSpan
                        f'8
                        e''8
                        g'8
                        ]
                        f''8
                        \stopTextSpan
                        [
                        - \abjad-solid-line-with-hook
                        - \baca-text-spanner-left-text "B"
                        - \tweak bound-details.right.text \markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75 \general-align #Y #1 \upright A }
                        - \tweak bound-details.right.padding 1.25
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        e'8
                        d''8
                        \stopTextSpan
                        ]
                        \revert DynamicLineSpanner.staff-padding
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Backsteals left text from length-1 final piece:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner(
        ...         "P -> T -> P",
        ...         pieces=baca.selectors.plts(),
        ...     ),
        ...     baca.make_notes(),
        ...     baca.pitches("C4 D4 E4 F4 G4 A4"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        \override TextSpanner.staff-padding = 4.5
                        c'2
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "P"
                        \startTextSpan
                        d'4.
                        \stopTextSpan
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "T"
                        \startTextSpan
                        e'2
                        \stopTextSpan
                        - \abjad-invisible-line
                        - \baca-text-spanner-left-text "P"
                        \startTextSpan
                        f'4.
                        \stopTextSpan
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "P"
                        \startTextSpan
                        g'2
                        \stopTextSpan
                        - \abjad-solid-line-with-arrow
                        - \baca-text-spanner-left-text "T"
                        - \baca-text-spanner-right-text "P"
                        - \tweak bound-details.right.padding 0.5
                        - \tweak bound-details.right.stencil-align-dir-y #center
                        \startTextSpan
                        a'4.
                        \stopTextSpan
                        \revert TextSpanner.staff-padding
                    }
                >>
            }

    ..  container:: example

        REGRESSION. Backsteals left text from spannerless final piece:

        >>> score = baca.docs.make_empty_score(1)
        >>> commands = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> commands(
        ...     "Music_Voice",
        ...     baca.text_spanner(
        ...         "P -> T ->",
        ...         final_piece_spanner=False,
        ...         pieces=baca.selectors.plts(),
        ...     ),
        ...     baca.skeleton("{ c2 c4. c2 c4 ~ c8 }"),
        ...     baca.pitches("C4 D4 E4 F4"),
        ...     baca.text_spanner_staff_padding(4.5),
        ... )

        >>> _, _ = baca.interpreter(
        ...     score,
        ...     commands.commands,
        ...     commands.time_signatures,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
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
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        s1 * 3/8
                        \baca-new-spacing-section #1 #12
                        \time 4/8
                        s1 * 1/2
                        \baca-new-spacing-section #1 #4
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music_Voice"
                    {
                        {
                            \override TextSpanner.staff-padding = 4.5
                            c'2
                            - \abjad-solid-line-with-arrow
                            - \baca-text-spanner-left-text "P"
                            \startTextSpan
                            d'4.
                            \stopTextSpan
                            - \abjad-solid-line-with-arrow
                            - \baca-text-spanner-left-text "T"
                            \startTextSpan
                            e'2
                            \stopTextSpan
                            - \abjad-solid-line-with-arrow
                            - \baca-text-spanner-left-text "P"
                            - \baca-text-spanner-right-text "T"
                            - \tweak bound-details.right.padding 0.5
                            - \tweak bound-details.right.stencil-align-dir-y #center
                            \startTextSpan
                            f'4
                            \stopTextSpan
                            ~
                            f'8
                            \revert TextSpanner.staff-padding
                        }
                    }
                >>
            }

    ..  container:: example exception

        Errors on unknown LilyPond ID:

        >>> baca.text_spanner(
        ...     "T -> P",
        ...     lilypond_id=4,
        ... )
        Traceback (most recent call last):
            ...
        ValueError: lilypond_id must be 1, 2, 3, str or none (not 4).

    """
    original_items = items
    if autodetect_right_padding is not None:
        autodetect_right_padding = bool(autodetect_right_padding)
    if direction == abjad.Down:
        shape_to_style = {
            "=>": "dashed-line-with-arrow",
            "=|": "dashed-line-with-up-hook",
            "||": "invisible-line",
            "->": "solid-line-with-arrow",
            "-|": "solid-line-with-up-hook",
        }
    else:
        shape_to_style = {
            "=>": "dashed-line-with-arrow",
            "=|": "dashed-line-with-hook",
            "||": "invisible-line",
            "->": "solid-line-with-arrow",
            "-|": "solid-line-with-hook",
        }
    if isinstance(items, str):
        items_: typing.List[typing.Union[str, abjad.Markup]] = []
        current_item: typing.List[str] = []
        for word in items.split():
            if word in shape_to_style:
                if current_item:
                    item_ = " ".join(current_item)
                    if boxed:
                        string = rf'\baca-boxed-markup "{item_}"'
                        markup = abjad.Markup(string)
                        items_.append(markup)
                    else:
                        items_.append(item_)
                    current_item = []
                items_.append(word)
            else:
                current_item.append(word)
        if current_item:
            item_ = " ".join(current_item)
            if boxed:
                string = rf'\baca-boxed-markup "{item_}"'
                markup = abjad.Markup(string)
                items_.append(markup)
            else:
                items_.append(item_)
        items = items_
    bundles = []
    if len(items) == 1:
        message = f"lone item not yet implemented ({original_items!r})."
        raise NotImplementedError(message)
    if lilypond_id is None:
        command = r"\stopTextSpan"
    elif lilypond_id == 1:
        command = r"\stopTextSpanOne"
    elif lilypond_id == 2:
        command = r"\stopTextSpanTwo"
    elif lilypond_id == 3:
        command = r"\stopTextSpanThree"
    elif isinstance(lilypond_id, str):
        command = rf"\bacaStopTextSpan{lilypond_id}"
    else:
        message = "lilypond_id must be 1, 2, 3, str or none"
        message += f" (not {lilypond_id})."
        raise ValueError(message)
    stop_text_span = abjad.StopTextSpan(command=command)
    cyclic_items = abjad.CyclicTuple(items)
    for i, item in enumerate(cyclic_items):
        item_markup: typing.Union[str, abjad.Markup]
        if item in shape_to_style:
            continue
        if isinstance(item, str) and item.startswith("\\"):
            item_markup = rf"- \baca-text-spanner-left-markup {item}"
        elif isinstance(item, str):
            item_markup = rf'- \baca-text-spanner-left-text "{item}"'
        else:
            item_markup = item
            assert isinstance(item_markup, abjad.Markup)
            string = item_markup.string
            item_markup = abjad.Markup(r"\upright {string}")
            assert isinstance(item_markup, abjad.Markup)
        prototype = (str, abjad.Markup)
        assert isinstance(item_markup, prototype)
        style = "invisible-line"
        if cyclic_items[i + 1] in shape_to_style:
            style = shape_to_style[cyclic_items[i + 1]]
            right_text = cyclic_items[i + 2]
        else:
            right_text = cyclic_items[i + 1]
        right_markup: typing.Union[str, abjad.Markup]
        if isinstance(right_text, str):
            if "hook" not in style:
                if right_text.startswith("\\"):
                    right_markup = r"- \baca-text-spanner-right-markup"
                    right_markup += rf" {right_text}"
                else:
                    right_markup = r"- \baca-text-spanner-right-text"
                    right_markup += rf' "{right_text}"'
            else:
                right_markup = abjad.Markup(rf"\upright {right_text}")
        else:
            assert isinstance(right_text, abjad.Markup)
            string = right_text.string
            right_markup = abjad.Markup(r"\upright {string}")
        if lilypond_id is None:
            command = r"\startTextSpan"
        elif lilypond_id == 1:
            command = r"\startTextSpanOne"
        elif lilypond_id == 2:
            command = r"\startTextSpanTwo"
        elif lilypond_id == 3:
            command = r"\startTextSpanThree"
        elif isinstance(lilypond_id, str):
            command = rf"\bacaStartTextSpan{lilypond_id}"
        else:
            raise ValueError(lilypond_id)
        left_broken_markup = None
        if isinstance(left_broken_text, str):
            left_broken_markup = abjad.Markup(left_broken_text)
        elif isinstance(left_broken_text, abjad.Markup):
            left_broken_markup = left_broken_text
        start_text_span = abjad.StartTextSpan(
            command=command,
            left_broken_text=left_broken_markup,
            left_text=item_markup,
            style=style,
        )
        # kerns bookended hook
        if "hook" in style:
            assert isinstance(right_markup, abjad.Markup)
            content_string = right_markup.string
            string = r"\markup \concat { \raise #-1 \draw-line #'(0 . -1) \hspace #0.75"
            string += rf" \general-align #Y #1 {content_string} }}"
            right_markup = abjad.Markup(string)
        bookended_spanner_start = abjad.new(start_text_span, right_text=right_markup)
        # TODO: find some way to make these tweaks explicit to composer
        manager = abjad.tweak(bookended_spanner_start)
        manager.bound_details__right__stencil_align_dir_y = abjad.Center
        if "hook" in style:
            manager.bound_details__right__padding = 1.25
        else:
            manager.bound_details__right__padding = 0.5
        bundle = Bundle(
            bookended_spanner_start=bookended_spanner_start,
            spanner_start=start_text_span,
            spanner_stop=stop_text_span,
        )
        bundles.append(bundle)
    return PiecewiseCommand(
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        bundles=bundles,
        final_piece_spanner=final_piece_spanner,
        leak_spanner_stop=leak_spanner_stop,
        left_broken=left_broken,
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
        tags=[_scoping.site(_frame())],
        tweaks=tweaks,
    )


def vibrato_spanner(
    items: typing.Union[str, typing.List],
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = True,
    bookend: typing.Union[bool, int] = False,
    final_piece_spanner: bool = None,
    left_broken: bool = None,
    left_broken_text: str = None,
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes vibrato spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.VIBRATO_SPANNER)
    command = text_spanner(
        items,
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="Vibrato",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result


def xfb_spanner(
    *tweaks: abjad.IndexedTweakManager,
    autodetect_right_padding: bool = True,
    bookend: typing.Union[bool, int] = False,
    final_piece_spanner: bool = None,
    left_broken: bool = None,
    left_broken_text: str = r"\baca-left-broken-xfb-markup",
    map=None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    pieces=_selectors.group(),
    right_broken: bool = None,
    # NOTE: selector differs from text_spanner(), annotation spanners:
    selector=_selectors.ltleaves_rleak(),
) -> PiecewiseCommand:
    """
    Makes XFB spanner.
    """
    tag = _scoping.site(_frame())
    tag = tag.append(_tags.BOW_SPEED_SPANNER)
    command = text_spanner(
        "XFB =|",
        *tweaks,
        autodetect_right_padding=autodetect_right_padding,
        bookend=bookend,
        final_piece_spanner=final_piece_spanner,
        left_broken=left_broken,
        left_broken_text=left_broken_text,
        lilypond_id="BowSpeed",
        map=map,
        match=match,
        measures=measures,
        pieces=pieces,
        right_broken=right_broken,
        selector=selector,
    )
    result = abjad.new(command, tags=[tag])
    assert isinstance(result, PiecewiseCommand)
    return result
