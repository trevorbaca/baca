from abjad.tools.abctools.AbjadObject import AbjadObject
from collections import OrderedDict


class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self):
        OrderedDict.__init__(self)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return OrderedDict.__repr__(self)

    ### PUBLIC METHODS ###

    def get_values(self, attribute_name=None, scope=None):
        values = []
        for key, value in self.iteritems():
            if ((attribute_name is None or key == attribute_name) and
                (scope is None or value.scope == scope)
                ):
                values.append(value)
        return values
