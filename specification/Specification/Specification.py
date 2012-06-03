from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.ContextDictionary import ContextDictionary
from baca.specification.SettingInventory import SettingInventory
from baca.specification.ValueRetrievalIndicator import ValueRetrievalIndicator


class Specification(AbjadObject):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, score_template):
        self._score_template = score_template
        self._context_dictionary = ContextDictionary(self.score_template())
        self._initialize_context_name_abbreviations()
        self._payload = ContextDictionary(self.score_template())
        self._settings = SettingInventory()

    ### PRIVATE METHODS ###

    def _initialize_context_name_abbreviations(self):
        self.context_name_abbreviations = getattr(self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
        score = self.score_template()
        self._score_name = score.name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_dictionary(self):
        return self._context_dictionary

    @property
    def payload(self):
        return self._payload

    @property
    def score_name(self):
        return self._score_name

    @property
    def score_template(self):
        return self._score_template

    @property
    def settings(self):
        return self._settings

    ### PUBLIC METHODS ###

    def retrieve(self, attribute_name, segment_name, context_name=None, scope=None):
        return AttributeRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)

    def retrieve_resolved_value(self, attribute_name, segment_name, context_name=None, scope=None):
        return ValueRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)
