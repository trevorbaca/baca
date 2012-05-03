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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        body = []
        for attribute_name in ('segment_name', 'context_name', 'scope'):
            attribute_value = getattr(self.attribute_retrieval_indicator.selection, attribute_name, None)
            if attribute_value is not None:
                body.append(attribute_value)
        body.append(self.attribute_retrieval_indicator.attribute_name)
        body = ', '.join(body)
        return '({}, count={}, offset={})'.format(body, self.count, self.offset)
