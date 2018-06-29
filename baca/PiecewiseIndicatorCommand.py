import abjad
import baca
import collections
import copy
import typing
from . import typings
from .Command import Command
from .DynamicBundle import DynamicBundle
from .IndicatorCommand import IndicatorCommand


class PiecewiseIndicatorCommand(Command):
    """
    Piecewise indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookend',
        '_bundles',
        '_forbid_spanner_start',
        '_last_piece_spanner',
        '_piece_selector',
        '_right_broken',
        '_right_open',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        bundles: typing.List[DynamicBundle] = None,
        forbid_spanner_start: typing.Union[bool, int] = None,
        last_piece_spanner: typing.Any = None,
        piece_selector: typings.Selector = 'baca.leaves()',
        right_broken: typing.Any = None,
        right_open: bool = None,
        selector: typings.Selector = 'baca.leaves()',
        ) -> None:
        Command.__init__(self, selector=selector)
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        if forbid_spanner_start is not None:
            assert isinstance(forbid_spanner_start, (int, bool)), repr(forbid_spanner_start)
        self._forbid_spanner_start = forbid_spanner_start
        bundles_ = None
        if bundles is not None:
            bundles_ = abjad.CyclicTuple(bundles)
        self._bundles = bundles_
        if last_piece_spanner not in (None, False):
            assert getattr(last_piece_spanner, 'spanner_start', False)
        self._last_piece_spanner = last_piece_spanner
        if isinstance(piece_selector, str):
            piece_selector = eval(piece_selector)
        if piece_selector is not None:
            assert isinstance(piece_selector, abjad.Expression), repr(
                piece_selector)
        self._piece_selector = piece_selector
        self._right_broken = right_broken
        if right_open is not None:
            right_open = bool(right_open)
        self._right_open = right_open
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
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
        for i, piece in enumerate(pieces):
            start_leaf = baca.select(piece).leaf(0)
            stop_leaf = baca.select(piece).leaf(-1)
            if i == piece_count - 1:
                is_last_piece = True
            else:
                is_last_piece = False
            if is_last_piece and self.right_broken:
                bundle = DynamicBundle.from_indicator(self.right_broken)
                self._attach_indicators(
                    #self.right_broken,
                    bundle,
                    stop_leaf,
                    tag=str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS),
                    )
            if (bookend_pattern.matches_index(i, piece_count) and
                1 < len(piece)):
                should_bookend = True
            else:
                should_bookend = False
            bundle = self.bundles[i]
            if len(piece) == 1 and bundle.both():
                bundle = bundle.dynamic_only()
            if is_last_piece and bundle.both():
#                assert len(indicators) == 2
#                indicator, spanner_start = indicators
#                if getattr(spanner_start, 'spanner_start', False) is not True:
#                    raise Exception(indicators)
                if self.last_piece_spanner:
                    #indicators = (indicator, self.last_piece_spanner)
                    #bundle.dynamic_trend = self.last_piece_spanner
                    bundle = abjad.new(
                        bundle,
                        dynamic_trend=self.last_piece_spanner,
                        )
                elif self.last_piece_spanner is False:
                    #indicators = indicator
                    bundle = abjad.new(bundle, dynamic_trend=None)
            self._attach_indicators(
                #indicators,
                bundle,
                start_leaf,
                tag='PIC',
                )
            if should_bookend:
                #indicators = self.indicators[i + 1]
                bundle = self.bundles[i + 1]
                #if isinstance(indicators, tuple):
                if bundle.both():
#                    assert len(indicators) == 2
#                    indicator, spanner_start = indicators
#                    if getattr(spanner_start, 'spanner_start', False) is not True:
#                        raise Exception(indicators)
#                    indicators = indicator
                    bundle = abjad.new(bundle, dynamic_trend=None)
                self._attach_indicators(
                    #indicators,
                    bundle,
                    stop_leaf,
                    tag='PIC',
                    )

    ### PRIVATE METHODS ###

    def _attach_indicators(
        self,
        #indicators,
        bundle,
        leaf,
        tag=None,
        ):
        assert isinstance(tag, str), repr(tag)
        for indicator in bundle.indicators:
            reapplied = Command._remove_reapplied_wrappers(leaf, indicator)
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=self.tag.prepend(tag),
                wrapper=True,
                )
            if indicator == reapplied:
                if (isinstance(indicator, abjad.Dynamic) and
                    indicator.sforzando):
                    status = 'explicit'
                else:
                    status = 'redundant'
                baca.SegmentMaker._treat_persistent_wrapper(
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
    def forbid_spanner_start(self) -> typing.Optional[typing.Union[bool, int]]:
        """
        Gets forbid-spanner-start token.
        """
        return self._forbid_spanner_start

    @property
    def last_piece_spanner(self) -> typing.Optional[typing.Any]:
        """
        Gets last piece spanner start.
        """
        return self._last_piece_spanner

    @property
    def piece_selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets piece selector.
        """
        return self._piece_selector

    @property
    def right_broken(self) -> typing.Optional[typing.Any]:
        """
        Gets right-broken indicator.
        """
        return self._right_broken

    @property
    def right_open(self) -> typing.Optional[bool]:
        """
        Is true when command allows trend on last leaf.
        """
        return self._right_open

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets (first-order) selector.
        """
        return self._selector
