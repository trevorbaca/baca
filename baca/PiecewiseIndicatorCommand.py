import abjad
import baca
import collections
import copy
import typing
from . import typings
from .Command import Command
from .IndicatorCommand import IndicatorCommand


class PiecewiseIndicatorCommand(Command):
    """
    Piecewise indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookend',
        '_indicators',
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
        indicators: typing.Sequence = None,
        piece_selector: typings.Selector = 'baca.leaves()',
        right_broken: typing.Any = None,
        right_open: bool = None,
        selector: typings.Selector = 'baca.leaves()',
        ) -> None:
        Command.__init__(self, selector=selector)
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        indicators_ = None
        if indicators is not None:
            indicators_ = abjad.CyclicTuple(indicators)
        self._indicators = indicators_
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
        if not self.indicators:
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
            if i == piece_count - 1:
                is_last_piece = True
            else:
                is_last_piece = False
            if (bookend_pattern.matches_index(i, piece_count) and
                1 < len(piece)):
                has_bookend = True
            else:
                has_bookend = False
            start_leaf = baca.select(piece).leaf(0)
            indicators = self.indicators[i]
            self._attach_indicators(
                indicators,
                start_leaf,
                has_bookend=has_bookend,
                is_last_piece=is_last_piece,
                is_start_leaf=True,
                tag='PIC',
                )
            if has_bookend:
                stop_leaf = baca.select(piece).leaf(-1)
                indicators = self.indicators[i + 1]
                self._attach_indicators(
                    indicators,
                    stop_leaf,
                    has_bookend=has_bookend,
                    is_last_piece=is_last_piece,
                    is_stop_leaf=True,
                    tag='PIC',
                    )
            if is_last_piece and self.right_broken:
                stop_leaf = baca.select(piece).leaf(-1)
                self._attach_indicators(
                    self.right_broken,
                    stop_leaf,
                    has_bookend=True,
                    is_last_piece=is_last_piece,
                    is_stop_leaf=True,
                    tag=str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS),
                    )

    ### PRIVATE METHODS ###

    def _attach_indicators(
        self,
        indicators,
        leaf,
        has_bookend=False,
        is_last_piece=False,
        is_start_leaf=False,
        is_stop_leaf=False,
        tag=None,
        ):
        assert isinstance(tag, str), repr(tag)
        if not isinstance(indicators, tuple):
            indicators = (indicators,)
        for indicator in indicators:
            if indicator is None:
                continue
            if getattr(indicator, 'left_broken', False):
                pass
            elif (is_stop_leaf and
                getattr(indicator, 'spanner_start', False) is True):
                continue
            elif (is_last_piece and
                is_start_leaf and
                getattr(indicator, 'spanner_start', False) is True and
                not (has_bookend or self.right_broken or self.right_open)):
                continue
            elif (is_last_piece and
                is_stop_leaf and
                getattr(indicator, 'spanner_start', False) is True and
                not (has_bookend or self.right_broken or self.right_open)):
                continue
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
    def indicators(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets indicators.
        """
        return self._indicators

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
