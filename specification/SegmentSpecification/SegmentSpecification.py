from abjad.tools import chordtools
from abjad.tools import contexttools
from abjad.tools import notetools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate
from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.handlers.pitch.TimewisePitchClassHandler import TimewisePitchClassHandler
from baca.specification.Directive import Directive
from baca.specification.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specification.HandlerRequest import HandlerRequest
from baca.specification.Scope import Scope
from baca.specification.Selection import Selection
from baca.specification.StatalServer import StatalServer
from baca.specification.StatalServerRequest import StatalServerRequest
from handlers.Handler import Handler


class SegmentSpecification(AbjadObject):

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

    def annotate_source(self, source, count=None, seed=None):
        if isinstance(source, StatalServer):
            source = StatalServerRequest(source, count=count, seed=seed)
        elif isinstance(source, Handler):
            assert count is None
            source = HandlerRequest(source, offset=seed)
        elif count is not None or seed is not None:
            raise ValueError("'count' or 'seed' set on nonstatal source: {!r}.".format(source))
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
            selection = self.select()
        elif selection_token in self.context_names:
            selection = self.select(context_names=[selection_token])
        elif self.all_are_context_names(selection_token):
            selection = self.select(context_names=selection_token)
        else:
            raise ValueError('invalid selection token: {!r}.'.format(selection_token))
        return selection

    def select(self, context_names=None, segment_name=None, scope=None):
        assert context_names is None or self.all_are_context_names(context_names)
        assert isinstance(segment_name, (str, type(None)))
        assert isinstance(scope, (Scope, type(None)))
        segment_name = segment_name or self.name
        selection = Selection(segment_name, context_names=context_names, scope=scope)
        return selection

    def select_divisions(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'divisions'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection

    def select_measures(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = 'measures'
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, segment_name=segment_name, scope=scope)
        return selection
    
    def select_notes_and_chords(self, context_token=None, part=None, segment_name=None, start=None, stop=None):
        criterion = (chordtools.Chord, notetools.Note)
        context_names = self.parse_context_token(context_token)
        scope = Scope(criterion=criterion, part=part, start=start, stop=stop)
        selection = self.select(context_names=context_names, scope=scope)
        return selection

    def set_aggregate(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'aggregate'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_articulations(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'articulations'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_attribute(self, attribute_name, target_token, source, count=None, persistent=True, seed=None):
        assert isinstance(attribute_name, str)
        assert isinstance(persistent, type(True))
        target_selection = self.parse_selection_token(target_token)
        source = self.annotate_source(source, count=count, seed=seed)
        directive = Directive(target_selection, attribute_name, source, persistent=persistent)
        self.directives.append(directive)

    def set_chord_treatment(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'chord_treatment'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_divisions(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'divisions'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_duration_in_seconds(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'duration_in_seconds'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_dynamics(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'dynamcis'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_marks(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'marks'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_markup(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'markup'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_pitch_classes(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'pitch_classes'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_pitch_class_application(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'pitch_class_application'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_pitch_class_transform(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'pitch_class_transform'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_register(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'register'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_rhythm(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'rhythm'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_tempo(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'tempo'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_time_signatures(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'time_signatures'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)

    def set_written_duration(self, target_token, source, count=None, persistent=True, seed=None):
        attribute_name = 'written_duration'
        self.set_attribute(attribute_name, target_token, source, count=count, persistent=persistent, seed=seed)
