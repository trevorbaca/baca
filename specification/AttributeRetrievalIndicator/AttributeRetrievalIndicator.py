from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection


class AttributeRetrievalIndicator(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, attribute_name, segment_name, context_name=None, scope=None):
        assert isinstance(segment_name, str)
        assert isinstance(attribute_name, str)
        assert isinstance(context_name, (str, type(None)))
        assert isinstance(scope, (Scope, type(None)))
        self.attribute_name = attribute_name
        self.segment_name = segment_name
        self.context_name = context_name
        self.scope = scope
