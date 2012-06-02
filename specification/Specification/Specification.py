from abjad.tools import *
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.ContextTree import ContextTree
from baca.specification.SettingReservoir import SettingReservoir
from baca.specification.ValueRetrievalIndicator import ValueRetrievalIndicator


class Specification(SettingReservoir):

    ### INITIALIZER ###

    def __init__(self, score_template, settings=None):
        SettingReservoir.__init__(self, settings=settings)
        self._score_template = score_template
        self._context_tree = ContextTree(self.score_template())
        self._initialize_context_name_abbreviations()

    ### PRIVATE METHODS ###

    def _initialize_context_name_abbreviations(self):
        self.context_name_abbreviations = getattr(self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
        score = self.score_template()
        self.score_name = score.name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_tree(self):
        return self._context_tree

    @property
    def score_template(self):
        return self._score_template

    ### PUBLIC METHODS ###

    def retrieve(self, attribute_name, segment_name, context_name=None, scope=None):
        return AttributeRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)

    def retrieve_resolved_value(self, attribute_name, segment_name, context_name=None, scope=None):
        return ValueRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)
