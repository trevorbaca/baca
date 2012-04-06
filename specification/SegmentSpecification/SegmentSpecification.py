from abjad.tools import chordtools
from abjad.tools import contexttools
from abjad.tools import notetools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate
from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.handlers.pitch.TimewisePitchClassHandler import TimewisePitchClassHandler
from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration
from baca.specification.Directive import Directive
from baca.specification.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.TemporalScope import TemporalScope


class SegmentSpecification(AbjadObject):

    ### CLASS ATTRIBUTES ###

    attrs = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, score_template, directives=None, name=None):
        self.score_template = score_template
        self.directives = directives or []
        self.name = name

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        return self.directives.__getitem__(arg)

    def __getslice__(self, start, stop):
        return self.directives.__getslice__(start, stop)

    def __len__(self):
        return len(self.directives)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def has_relative_directives(self):
        return bool(self.relative_directives)

    @property
    def relative_directives(self):
        result = []
        for directive in self.directives:
            if directive.is_relative:
                result.append(directive)
        return result

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def score_template():
        def fget(self):
            return self._score_template
        def fset(self, score_template):
            assert isinstance(score_template, (ScoreTemplate, type(None)))
            self._score_template = score_template
            self.initialize_score()
            self.initialize_context_names()
        return property(**locals())

    ### PUBLIC METHODS ###

    def all_are_context_names(self, expr):
        try:
            return all([x in self.context_names for x in expr])
        except:
            return False

    def get_directives(self, target_selection=None, attribute_name=None):
        result = []
        for directive in self.directives:
            if target_selection is None or directive.target_selection == target_selection:
                if attribute_name is None or directive.attribute_name == attribute_name:
                    result.append(directive)
        return result

    def initialize_context_names(self):
        if self.score is not None:
            self.context_names = []
            for context in contexttools.iterate_contexts_forward_in_expr(self.score):
                assert context.context_name is not None
                self.context_names.append(context.name)
                self.context_names.sort()
        else:
            self.context_names = []

    def initialize_score(self):
        if self.score_template is not None:
            self.score = self.score_template()
        else:
            self.score = None

    def parse_context_token(self, context_token):
        if context_token in self.context_names:
            context_names = [context_token]
        elif self.all_are_context_names(context_token):
            context_names = context_token
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names
            
    def parse_selection_token(self, selection_token):
        if isinstance(selection_token, Selection):
            selection = selection_token
        elif isinstance(selection_token, type(self)):
            selection = self.select_by_count()
        elif selection_token in self.context_names:
            selection = self.select_by_count(context_names=[selection_token])
        elif self.all_are_context_names(selection_token):
            selection = self.select_by_count(context_names=selection_token)
        else:
            raise ValueError('what is {!r}?'.format(selection_token))
        return selection

    def select_by_count(self, context_names=None, segment_name=None, temporal_scope=None):
        assert context_names is None or self.all_are_context_names(context_names)
        assert isinstance(segment_name, (str, type(None)))
        assert isinstance(temporal_scope, (TemporalScope, type(None)))
        segment_name = segment_name or self.name
        selection = Selection(segment_name, context_names=context_names, temporal_scope=temporal_scope)
        return selection

    def select_divisions_by_count(self, context_token, part=None, start=None, stop=None):
        criterion = 'divisions'
        context_names = self.parse_context_token(context_token)
        temporal_scope = TemporalScope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select_by_count(context_names=context_names, temporal_scope=temporal_scope)
        return selection

    #def select_measures_by_count(self, context_token, part=None, start=None, stop=None):
    def select_measures_by_count(self, target_token, part=None, start=None, stop=None):
        criterion = 'measures'
        #context_names = self.parse_context_token(context_token)
        temporal_scope = TemporalScope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select_by_count(context_names=context_names, temporal_scope=temporal_scope)
        return selection
    
    def select_notes_and_chords_by_count(self, context_token, part=None, start=None, stop=None):
        criterion = (chordtools.Chord, notetools.Note)
        context_names = self.parse_context_token(context_token)
        temporal_scope = TemporalScope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select_by_count(context_names=context_names, temporal_scope=temporal_scope)
        return selection

    def set_aggregate(self, target_token, aggregate, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.aggregate, aggregate)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_aggregate_to_aggregate_at_index(self, target_token, server, index, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        source = StatalServerRequest(server, index=index)
        directive = Directive(target_selection, self.attrs.aggregate, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_aggregate_to_next_aggregate(self, target_token, server, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        source = StatalServerRequest(server, count=1)
        directive = Directive(target_selection, self.attrs.aggregate, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_articulations(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.articulations, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_chords(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.chords, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_divisions(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.divisions, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_duration_in_seconds(self, target_token, duration_in_seconds, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.duration_in_seconds, duration_in_seconds)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_dynamics(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.dynamics, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_marks(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.marks, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_markup(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, source, self.attrs.markup, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive) 

    def set_pitch_class_transform(self, target_token, transform, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.transform, transform)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_pitch_classes_timewise(self, target_token, pitch_class_server, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = TimewisePitchClassHandler(pitch_class_server)
        directive = Directive(target_selection, self.attrs.pitch_classes, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_register(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.register, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_rhythm(self, target_token, source_token, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        division_source, rhythm_source = source_token
        source = CompositeRhythmHandler(division_source, rhythm_source)
        directive = Directive(target_selection, self.attrs.rhythm, source, seed=seed)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_tempo(self, target_token, source, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.tempo, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_time_signatures(self, target_token, time_signatures, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.time_signatures, time_signatures)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_time_signatures_from_count(self, target_token, server, count, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        source = StatalServerRequest(server, count=count)
        directive = Directive(target_selection, self.attrs.time_signatures, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_written_duration(self, target_token, written_duration, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        directive = Directive(target_selection, self.attrs.written_duration, written_duration)
        directive.persistent = persistent
        self.directives.append(directive)
