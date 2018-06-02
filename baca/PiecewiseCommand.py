import abjad
import baca
import collections
import copy
import typing
from .Command import Command
from .MapCommand import MapCommand
from .SpannerCommand import SpannerCommand
from .Typing import Selector


class PiecewiseCommand(Command):
    """
    Piecewise command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookend',
        '_indicators',
        '_pieces',
        '_selector',
        '_spanner',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        indicators: typing.Iterable = None,
        pieces: typing.Union[MapCommand, Selector] = 'baca.leaves()',
        spanner: abjad.Spanner = None,
        selector: Selector = 'baca.leaves()',
        tweaks: typing.List[typing.Tuple] = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        if indicators is not None:
            indicators = abjad.CyclicTuple(indicators)
        self._indicators = indicators
        if isinstance(pieces, str):
            pieces = eval(pieces)
        if pieces is not None:
            prototype = (abjad.Expression, MapCommand)
            assert isinstance(pieces, prototype), repr(pieces)
        self._pieces = pieces
        if spanner is not None:
            assert isinstance(spanner, (abjad.Spanner, SpannerCommand))
        self._spanner = spanner
        self._tags = []
        if tweaks is not None:
            assert isinstance(tweaks, list), repr(tweaks)
            assert all(isinstance(_, tuple) for _ in tweaks), repr(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.

        ..  note:: IMPORTANT: spanner ``selector`` applies before ``pieces``
            selector.

        """
        if argument is None:
            return
        if self.spanner is None:
            return
        if not self.indicators:
            return
        if self.selector is not None:
            assert not isinstance(self.selector, str)
            argument = self.selector(argument)
        if isinstance(self.spanner, abjad.Spanner):
            spanner = copy.copy(self.spanner)
            leaves = abjad.select(argument).leaves()
            abjad.attach(
                spanner,
                leaves,
                tag=self.tag.prepend('PWC1'),
                )
        else:
            assert isinstance(self.spanner, SpannerCommand)
            spanner = self.spanner(argument)
        self._apply_tweaks(spanner)
        argument = abjad.select(spanner).leaves()
        if self.pieces is not None:
            assert not isinstance(self.pieces, str)
            pieces = self.pieces(argument)
        else:
            pieces = argument
        length = len(pieces)
        for leaf in abjad.select(pieces).leaves():
            if leaf not in spanner:
                message = f'\n  Leaf {leaf!s} not in {spanner!s}'
                message += "\n  Do pieces contradict spanner selector?"
                raise Exception(message)
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
            self._attach_indicators(spanner, indicator, first_leaf)
            if not pattern.matches_index(i, piece_count):
                continue
            if len(piece) <= 1:
                continue
            last_leaf = baca.select(piece).leaf(-1)
            if last_leaf not in spanner:
                continue
            indicator = self.indicators[i + 1]
            if i == length - 1:
                last = True
            else:
                last = False
            self._attach_indicators(spanner, indicator, last_leaf, last=last)

    ### PRIVATE METHODS ###

    def _attach_indicators(self, spanner, argument, leaf, last=False):
        if not isinstance(argument, tuple):
            argument = (argument,)
        for argument_ in argument:
            if argument_ is None:
                pass
            elif isinstance(argument_, abjad.ArrowLineSegment) and last:
                pass
            elif isinstance(argument_, baca.IndicatorCommand):
                for indicator in argument_.indicators:
                    spanner.attach(
                        indicator,
                        leaf,
                        tag=self.tag.prepend('PWC2'),
                        )
            else:
                reapplied = Command._remove_reapplied_wrappers(leaf, argument_)
                wrapper = spanner.attach(
                    argument_,
                    leaf,
                    tag=self.tag.prepend('PWC3'),
                    wrapper=True,
                    )
                if argument_ == reapplied:
                    baca.SegmentMaker._treat_persistent_wrapper(
                        self.manifests,
                        wrapper,
                        'redundant',
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
    def pieces(self) -> typing.Optional[
        typing.Union[abjad.Expression, MapCommand]
        ]:
        """
        Gets piece selector.
        """
        return self._pieces

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets spanner selector.
        """
        return self._selector

    @property
    def spanner(self) -> typing.Optional[abjad.Spanner]:
        """
        Gets spanner.
        """
        return self._spanner

    @property
    def tweaks(self) -> typing.Optional[typing.List[typing.Tuple]]:
        """
        Gets tweaks.
        """
        return self._tweaks
