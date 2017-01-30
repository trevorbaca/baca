# -*- coding: utf-8 -*-
import abjad


class FloatingSelection(abjad.abctools.AbjadValueObject):
    r'''Floating selection.

    ::

        >>> import baca

    ..  container:: example

        ::

            >>> baca.tools.FloatingSelection()
            FloatingSelection()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Figures'

    __slots__ = (
        '_selection',
        '_timespan',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, selection=None, timespan=None):
        if selection is not None:
            assert isinstance(selection, abjad.Selection)
        self._selection = selection
        if timespan is not None:
            assert isinstance(timespan, abjad.Timespan)
        self._timespan = timespan

    ### PUBLIC PROPERTIES ###

    @property
    def selection(self):
        r'''Gets selection.

        Returns selection or none.
        '''
        return self._selection

    @property
    def timespan(self):
        r'''Gets timespan.

        Returns timespan or none.
        '''
        return self._timespan
