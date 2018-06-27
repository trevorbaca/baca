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
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        indicators: typing.Sequence = None,
        pieces: typings.Selector = 'baca.leaves()',
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
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.

        ..  note:: IMPORTANT: first-order ``selector`` applies before
            ``pieces`` selector.

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
        length = len(pieces)
        piece_count = len(pieces)
        if self.bookend in (False, None):
            pattern = abjad.Pattern()
        elif self.bookend is True:
            pattern = abjad.index([0], 1)
        else:
            assert isinstance(self.bookend, int)
            pattern = abjad.index([self.bookend], period=piece_count)
        for i, piece in enumerate(pieces):
            first_leaf = baca.select(piece).leaf(0)
            indicator = self.indicators[i]
            self._attach_indicators(indicator, first_leaf)
            if not pattern.matches_index(i, piece_count):
                continue
            if len(piece) <= 1:
                continue
            last_leaf = baca.select(piece).leaf(-1)
            indicator = self.indicators[i + 1]
            self._attach_indicators(indicator, last_leaf)

    ### PRIVATE METHODS ###

    def _attach_indicators(self, argument, leaf):
        if not isinstance(argument, tuple):
            argument = (argument,)
        for argument_ in argument:
            if argument_ is None:
                continue
            reapplied = Command._remove_reapplied_wrappers(leaf, argument_)
            wrapper = abjad.attach(
                argument_,
                leaf,
                tag=self.tag.prepend('PIC'),
                wrapper=True,
                )
            if argument_ == reapplied:
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
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets (first-order) selector.
        """
        return self._selector
