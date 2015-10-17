# -*- coding: utf-8 -*-
from abjad import *


class LabelSpecifier(abctools.AbjadObject):
    r'''Label specifier.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_label_logical_ties',
        '_start_index',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        label_logical_ties=True,
        start_index=0,
        ):
        self._label_logical_ties = bool(label_logical_ties)
        self._start_index = int(start_index)

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        logical_tie_count = len(logical_ties)
        for index, logical_tie in enumerate(logical_ties):
            written_index = self.start_index + index
            markup = Markup(str(written_index), direction=Up)
            attach(markup, logical_tie.head)

    ### PUBLIC PROPERTIES ###

    @property
    def label_logical_ties(self):
        r'''Is true when logical ties should be labeled. Otherwise false.

        Defaults to true.

        Set to true or false.

        Returns true or false.
        '''
        return self._label_logical_ties

    @property
    def start_index(self):
        r'''Gets start index of label specifier.

        Defaults to 0.

        Set to integer.

        Returns integer.
        '''
        return self._start_index