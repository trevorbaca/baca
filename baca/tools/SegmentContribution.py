import abjad


class SegmentContribution(abjad.AbjadValueObject):
    r'''Segment contribution.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(2) Makers'

    __slots__ = (
        '_payload',
        '_start_offset',
        )

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None):
        self._payload = payload
        self._start_offset = start_offset

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Gets payload.

        Returns selection or voice.
        '''
        return self._payload

    @property
    def start_offset(self):
        r'''Gets start offset.

        Returns offset.
        '''
        return self._start_offset
