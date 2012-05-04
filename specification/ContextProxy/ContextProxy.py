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

    def get_value(self, attribute_name=None, scope=None):
        values = self.get_values(attribute_name=attribute_name, scope=scope)
        if not values:
            raise Exception('no values for {!r} found.'.format(attribute_name))
        elif 1 < len(values):
            raise Exception('multiple values for {!r} found.'.format(attribute_name))
        assert len(values) == 1
        return values[0]

    def get_values(self, attribute_name=None, scope=None):
        values = []
        for key, value in self.iteritems():
            if ((attribute_name is None or key == attribute_name) and
                (scope is None or value.scope == scope)
                ):
                values.append(value)
        return values
