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
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest


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

    def annotate_source(self, source, seed=None):
        if seed is not None:
            source = StatalServerRequest(source, seed=seed)
        return source

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
        elif isinstance(context_token, type(self)):
            context_names = None
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
            raise ValueError('invalid selection token: {!r}.'.format(selection_token))
        return selection

    def select_by_count(self, context_names=None, segment_name=None, scope=None):
        assert context_names is None or self.all_are_context_names(context_names)
        assert isinstance(segment_name, (str, type(None)))
        assert isinstance(scope, (Scope, type(None)))
        segment_name = segment_name or self.name
        selection = Selection(segment_name, context_names=context_names, scope=scope)
        return selection

    def select_divisions_by_count(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'divisions'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select_by_count(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection

    def select_measures_by_count(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'measures'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select_by_count(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection
    
    def select_notes_and_chords_by_count(self, 
        context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = (chordtools.Chord, notetools.Note)
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select_by_count(context_names=context_names, scope=scope)
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
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.articulations, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_chords(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.chords, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_divisions(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.divisions, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_duration_in_seconds(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.duration_in_seconds, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_dynamics(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.dynamics, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_marks(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.marks, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_markup(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.markup, source)
        directive.persistent = persistent
        self.directives.append(directive) 

    def set_pitch_class_transform(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.transform, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_pitch_classes(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.pitch_classes, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_pitch_class_application(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.pitch_class_application, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_register(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.register, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_rhythm(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.rhythm, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_tempo(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.tempo, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_time_signatures(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.time_signatures, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_time_signatures_from_count(self, target_token, server, count, persistent=True):
        target_selection = self.parse_selection_token(target_token)
        source = StatalServerRequest(server, count=count)
        directive = Directive(target_selection, self.attrs.time_signatures, source)
        directive.persistent = persistent
        self.directives.append(directive)

    def set_written_duration(self, target_token, source, persistent=True, seed=None):
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, seed=seed)
        directive = Directive(target_selection, self.attrs.written_duration, source)
        directive.persistent = persistent
        self.directives.append(directive)
