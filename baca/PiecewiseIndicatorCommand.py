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
        '_pieces',
        '_right_open',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        indicators: typing.Sequence = None,
        pieces: typings.Selector = 'baca.leaves()',
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
        if isinstance(pieces, str):
            pieces = eval(pieces)
        if pieces is not None:
            assert isinstance(pieces, abjad.Expression), repr(pieces)
        self._pieces = pieces
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
        if self.pieces is not None:
            assert not isinstance(self.pieces, str)
            pieces = self.pieces(argument)
        else:
            pieces = argument
        assert pieces is not None
        piece_count = len(pieces)
        if self.bookend in (False, None):
            bookend_pattern = abjad.Pattern()
        elif self.bookend is True:
            bookend_pattern = abjad.index([0], 1)
        else:
            assert isinstance(self.bookend, int)
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
        ):
        if not isinstance(indicators, tuple):
            indicators = (indicators,)
        for indicator in indicators:
            if indicator is None:
                continue
            if (is_stop_leaf and
                getattr(indicator, 'spanner_start', False) is True):
                continue
            if (is_last_piece and
                is_start_leaf and
                not has_bookend and
                getattr(indicator, 'spanner_start', False) is True and
                not self.right_open):
                continue
            if (is_last_piece and
                is_stop_leaf and
                getattr(indicator, 'spanner_start', False) is True and
                not self.right_open):
                continue
            reapplied = Command._remove_reapplied_wrappers(leaf, indicator)
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=self.tag.prepend('PIC'),
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
    def pieces(self) -> typing.Optional[abjad.Expression]:
        """
        Gets piece selector.
        """
        return self._pieces

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
