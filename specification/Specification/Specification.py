from abjad.tools import *
from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration
from baca.specification.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from baca.specification.ContextTree import ContextTree
from baca.specification.SettingReservoir import SettingReservoir
from baca.specification.ValueRetrievalIndicator import ValueRetrievalIndicator


class Specification(SettingReservoir):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, settings=None):
        SettingReservoir.__init__(self, settings=settings)

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def score_template():
        def fget(self):
            return self._score_template
        def fset(self, score_template):
            assert isinstance(score_template, (scoretemplatetools.ScoreTemplate, type(None)))
            self._score_template = score_template
            self._context_tree = ContextTree(self.score_template())
            self.initialize_context_name_abbreviations()
        return property(**locals())

    ### PUBLIC METHODS ###

    def initialize_context_name_abbreviations(self):
        self.context_name_abbreviations = getattr(self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
        score = self.score_template()
        self.score_name = score.name

    def retrieve(self, attribute_name, segment_name, context_name=None, scope=None):
        return AttributeRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)

    def retrieve_resolved_value(self, attribute_name, segment_name, context_name=None, scope=None):
        return ValueRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)
