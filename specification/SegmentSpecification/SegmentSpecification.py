from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.handlers.pitch.TimewisePitchClassHandler import TimewisePitchClassHandler
from baca.specification.AttributeNameEnumeration import AttributeNameEnumeration
from baca.specification.Directive import Directive
from baca.specification.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest


class SegmentSpecification(AbjadObject):

    ### CLASS ATTRIBUTES ###

    attrs = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, directives=None, name=None, score_template=None):
        self.directives = directives or []
        self.name = name
        self.score_template = score_template
        self.is_pending = True

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

    ### PUBLIC METHODS ###

    def get_directives(self, target_selection=None, attribute_name=None):
        result = []
        for directive in self.directives:
            if target_selection is None or directive.target_selection == target_selection:
                if attribute_name is None or directive.attribute_name == attribute_name:
                    result.append(directive)
        return result

    def select(self, context_name=None, criterion=None, selection_token=None, 
        score_segment_name=None, start=None, stop=None):
        score_segment_name = score_segment_name or self.name
        selection = Selection(
            score_segment_name=score_segment_name, context_name=context_name,
            criterion=criterion, start=start, stop=stop)
        return selection

    # TODO: implement
    def selection_token_to_selection(self, selection_token):
        pass

    def set_aggregate(self, target_token, aggregate):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.aggregate, aggregate)
        self.directives.append(directive)

    def set_aggregate_to_aggregate_at_index(self, target_token, server, index):
        target_selection = self.selection_token_to_selection(target_token)
        source = StatalServerRequest(server, index=index)
        directive = Directive(target_selection, self.attrs.aggregate, source)
        self.directives.append(directive)

    def set_aggregate_to_next_aggregate(self, target_token, server):
        target_selection = self.selection_token_to_selection(target_token)
        source = StatalServerRequest(server, count=1)
        directive = Directive(target_selection, self.attrs.aggregate, source)
        self.directives.append(directive)

    def set_articulations(self, target_token, source, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.articulations, source, seed=seed)
        self.directives.append(directive)

    def set_chords(self, target_token, source, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.chords, source, seed=seed)
        self.directives.append(directive)

    def set_duration_in_seconds(self, target_token, duration_in_seconds):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.duration_in_seconds, duration_in_seconds)
        self.directives.append(directive)

    def set_dynamics(self, target_token, source, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.dynamics, source, seed=seed)
        self.directives.append(directive)

    def set_marks(self, target_token, source, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.marks, source, seed=seed)
        self.directives.append(directive)

    def set_markup(self, target_token, source, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, source, self.attrs.markup, seed=seed)
        self.directives.append(directive) 

    def set_pitch_class_transform(self, target_token, transform):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.transform, transform)
        self.directives.append(directive)

    def set_pitch_classes_timewise(self, target_token, pitch_class_server, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        source = TimewisePitchClassHandler(pitch_class_server)
        directive = Directive(target_selection, self.attrs.pitch_classes, source, seed=seed)
        self.directives.append(directive)

    def set_register(self, target_token, source, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.register, source, seed=seed)
        self.directives.append(directive)

    def set_rhythm(self, target_token, source_token, seed=None):
        target_selection = self.selection_token_to_selection(target_token)
        division_source, rhythm_source = source_token
        source = CompositeRhythmHandler(division_source, rhythm_source)
        directive = Directive(target_selection, self.attrs.rhythm, source, seed=seed)
        self.directives.append(directive)

    def set_tempo(self, target_token, source):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.tempo, source)
        self.directives.append(directive)

    def set_time_signatures(self, target_token, time_signatures):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.time_signatures, time_signatures)
        self.directives.append(directive)

    def set_time_signatures_from_count(self, target_token, server, count):
        target_selection = self.selection_token_to_selection(target_token)
        source = StatalServerRequest(server, count=count)
        directive = Directive(target_selection, self.attrs.time_signatures, source)
        self.directives.append(directive)

    def set_written_duration(self, target_token, written_duration):
        target_selection = self.selection_token_to_selection(target_token)
        directive = Directive(target_selection, self.attrs.written_duration, written_duration)
        self.directives.append(directive)
