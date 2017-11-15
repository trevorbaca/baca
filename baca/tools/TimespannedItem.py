import abjad


class TimespannedItem(abjad.AbjadValueObject):
    r'''Timespanned item.

    ..  container:: example

        >>> baca.TimespannedItem()
        TimespannedItem()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(2) Makers'

    __slots__ = (
        '_item',
        '_timespan',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, item=None, timespan=None):
        self._item = item
        if timespan is not None:
            assert isinstance(timespan, abjad.Timespan)
        self._timespan = timespan

    ### PUBLIC PROPERTIES ###

    @property
    def item(self):
        r'''Gets item.

        Returns item or none.
        '''
        return self._item

    @property
    def timespan(self):
        r'''Gets timespan.

        Returns timespan or none.
        '''
        return self._timespan
