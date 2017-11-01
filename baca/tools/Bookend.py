import abjad
import baca
import collections


class Bookend(abjad.AbjadObject):
    r'''Bookend.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_indicators',
        '_selector',
        '_spanner',
        )

    ### INITIALIZER ###

    def __init__(self, indicators, selector, spanner):
        assert isinstance(indicators, collections.Iterable), repr(indicators)
        self._indicators = indicators
        assert isinstance(selector, abjad.Expression), repr(selector)
        self._selector = selector
        assert issubclass(spanner, abjad.Spanner), repr(spanner)
        self._spanner = spanner

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if not self.indicators:
            return
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        indicators = abjad.CyclicTuple(self.indicators)
        for i, item in enumerate(argument):
            start_indicator = indicators[i]
            start_leaf = baca.select(item).leaf(0)
            start_spanner = abjad.inspect(start_leaf).get_spanner(self.spanner)
            assert start_spanner is not None
            start_spanner.attach(start_indicator, start_leaf)
            if len(item) <= 1:
                continue
            stop_indicator = indicators[i + 1]
            stop_leaf = baca.select(item).leaf(-1)
            stop_spanner = abjad.inspect(stop_leaf).get_spanner(self.spanner)
            assert stop_spanner is not None
            assert start_spanner is stop_spanner
            stop_spanner.attach(stop_indicator, stop_leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def indicators(self):
        r'''Gets indicators.
        '''
        return self._indicators

    @property
    def selector(self):
        r'''Gets selector.
        '''
        return self._selector

    @property
    def spanner(self):
        r'''Gets spanner.
        '''
        return self._spanner
