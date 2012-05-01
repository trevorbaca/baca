from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator


class AttributeRetrievalRequest(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, attribute_retrieval_indicator, count=None, offset=None):
        assert isinstance(attribute_retrieval_indicator, AttributeRetrievalIndicator)
        self.attribute_retrieval_indicator = attribute_retrieval_indicator
        self.count = count
        self.offset = offset

    ### SPECIAL METHODS ###

    def __call__(self):
        raise NotImplementedError
