from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.Selection import Selection


class AttributeRetrievalIndicator(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, selection, attribute_name):
        assert isinstance(selection, Selection)
        assert isinstance(attribute_name, str)
        self.selection = selection
        self.attribute_name = attribute_name
