# -*- encoding: utf-8 -*-
from abjad import *


class LabelSpecifier(abctools.AbjadObject):
    r'''Label specifier.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_label_logical_ties',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        label_logical_ties=True,
        ):
        self._label_logical_ties = bool(label_logical_ties)

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan):
        logical_tie_count = len(logical_ties)
        for index, logical_tie in enumerate(logical_ties):
            markup = Markup(str(index), direction=Up)
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