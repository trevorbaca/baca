from abjad.tools.abctools.AbjadObject import AbjadObject
from collections import OrderedDict


class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self):
        OrderedDict.__init__(self)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return OrderedDict.__repr__(self)
