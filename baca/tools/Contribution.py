# -*- coding: utf-8 -*-
from abjad.tools import abctools


class Contribution(abctools.AbjadValueObject):
    r'''Contribution.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-maker components'

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
        r'''Gets payload of contribution.
        
        Returns selection or voice.
        '''
        return self._payload

    @property
    def start_offset(self):
        r'''Gets start offset of contribution.

        Returns offset.
        '''
        return self._start_offset