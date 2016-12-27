# -*- coding: utf-8 -*-


class Shell(object):
    r'''Shell.

    ::

        >>> import abjad
        >>> import baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_payload',
        )

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = payload

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Gets payload.
        '''
        return self._payload
