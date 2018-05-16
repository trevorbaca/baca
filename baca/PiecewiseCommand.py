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
        '_selector',
        '_spanner',
        '_spanner_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        bookend: bool = None,
        indicators: typing.Iterable = None,
        selector: Selector = None,
        spanner: abjad.Spanner = None,
        spanner_selector: typing.Union[MapCommand, Selector] = 'baca.leaves()',
        ) -> None:
        Command.__init__(self, selector=selector)
        if bookend is not None:
            bookend = bool(bookend)
        self._bookend = bookend
        if indicators is not None:
            indicators = abjad.CyclicTuple(indicators)
        self._indicators = indicators
        if spanner is not None:
            assert isinstance(spanner, (abjad.Spanner, SpannerCommand))
        self._spanner = spanner
        if isinstance(spanner_selector, str):
            spanner_selector = eval(spanner_selector)
        if spanner_selector is not None:
            prototype = (abjad.Expression, MapCommand)
            assert isinstance(spanner_selector, prototype), repr(spanner_selector)
        self._spanner_selector = spanner_selector
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.

        ..  note:: IMPORTANT: ``spanner_selector`` applies before ``selector``.
        """
        if argument is None:
            return
        if self.spanner is None:
            return
        if not self.indicators:
            return
        if self.spanner_selector is not None:
            assert not isinstance(self.spanner_selector, str)
            argument = self.spanner_selector(argument)
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
        argument = abjad.select(spanner).leaves()
        if self.selector is not None:
            assert not isinstance(self.selector, str)
            argument = self.selector(argument)
        length = len(argument)
        for i, item in enumerate(argument):
            leaf = baca.select(item).leaf(0)
            indicator = self.indicators[i]
            self._attach_indicators(spanner, indicator, leaf)
            if not self.bookend:
                continue
            if len(item) <= 1:
                continue
            leaf = baca.select(item).leaf(-1)
            if leaf not in spanner:
                continue
            indicator = self.indicators[i + 1]
            if i == length - 1:
                last = True
            else:
                last = False
            self._attach_indicators(spanner, indicator, leaf, last=last)

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
    def bookend(self) -> typing.Optional[bool]:
        r"""Is true when command bookend-attaches indicators.
        """
        return self._bookend

    @property
    def indicators(self) -> typing.Optional[abjad.CyclicTuple]:
        r"""Gets indicators.
        """
        return self._indicators

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""Gets selector.
        """
        return self._selector

    @property
    def spanner(self) -> typing.Optional[abjad.Spanner]:
        r"""Gets spanner.
        """
        return self._spanner

    @property
    def spanner_selector(self) -> typing.Optional[
        typing.Union[abjad.Expression, MapCommand]
        ]:
        r"""Gets spanner selector.
        """
        return self._spanner_selector
