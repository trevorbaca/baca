# -*- coding: utf-8 -*-


class Wrapper(object):
    r'''Wrapper.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_payload',
        )

    __documentation_section__ = 'Utilities'

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = payload

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Gets payload.
        '''
        return self._payload
