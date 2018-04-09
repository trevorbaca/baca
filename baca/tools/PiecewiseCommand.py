import abjad
import baca
import collections
import copy
from .Command import Command


class PiecewiseCommand(Command):
    r'''Piecewise command.
    '''

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
        bookend=None,
        indicators=None,
        selector=None,
        spanner=None,
        spanner_selector=None,
        ):
        Command.__init__(self, selector=selector)
        if bookend is not None:
            bookend = bool(bookend)
        self._bookend = bookend
        if indicators is not None:
            indicators = abjad.CyclicTuple(indicators)
        self._indicators = indicators
        if spanner is not None:
            assert isinstance(spanner, (abjad.Spanner, baca.SpannerCommand))
        self._spanner = spanner
        if isinstance(spanner_selector, str):
            spanner_selector = eval(spanner_selector)
        if spanner_selector is not None:
            prototype = (abjad.Expression, baca.MapCommand)
            assert isinstance(spanner_selector, prototype)
        self._spanner_selector = spanner_selector
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.spanner is None:
            return
        if not self.indicators:
            return
        spanner_argument = argument
        if self.spanner_selector is not None:
            spanner_argument = self.spanner_selector(spanner_argument)
        if isinstance(self.spanner, abjad.Spanner):
            spanner = copy.copy(self.spanner)
            leaves = abjad.select(spanner_argument).leaves()
            abjad.attach(
                spanner,
                leaves,
                tag=self.tag.prepend('PWC1'),
                )
        else:
            spanner = self.spanner(spanner_argument)
        if self.selector is not None:
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
    def bookend(self):
        r'''Is true when command bookend-attaches indicators.

        Returns true, false or none.
        '''
        return self._bookend

    @property
    def indicators(self):
        r'''Gets indicators.

        Returns cyclic tuple or none.
        '''
        return self._indicators

    @property
    def selector(self):
        r'''Gets selector.

        Returns selector or none.
        '''
        return self._selector

    @property
    def spanner(self):
        r'''Gets spanner command.

        Returns spanner command or none.
        '''
        return self._spanner

    @property
    def spanner_selector(self):
        r'''Gets spanner selector.

        Returns selector or none.
        '''
        return self._spanner_selector
