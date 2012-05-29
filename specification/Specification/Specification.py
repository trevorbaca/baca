from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.SettingReservoir import SettingReservoir
from baca.specification.ValueRetrievalIndicator import ValueRetrievalIndicator


class Specification(SettingReservoir):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, settings=None):
        SettingReservoir.__init__(self, settings=settings)

    ### PUBLIC METHODS ###

    def retrieve(self, attribute_name, segment_name, context_name=None, scope=None):
        return AttributeRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)

    def retrieve_resolved_value(self, attribute_name, segment_name, context_name=None, scope=None):
        return ValueRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)
