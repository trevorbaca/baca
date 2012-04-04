from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.handlers.pitch.TimewisePitchClassHandler import TimewisePitchClassHandler
from baca.specification.Directive import Directive
from baca.specification.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specification.DurationSpecification import DurationSpecification
from baca.specification.RelativeReference import RelativeReference
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest


class ScoreSegmentSpecification(object):

    ### CLASS ATTRIBUTES ###

    class Attrs(object):
        aggregate = 'aggregate'
        articulations = 'articulations'
        duration_in_seconds = 'duration_in_seconds'
        chords = 'chords'
        dynamics = 'dynamics'
        marks = 'marks'
        markup = 'markup'
        pitch = 'pitch'
        pitch_classes = 'pitch_classes'
        register = 'register'
        rhythm = 'rhythm'
        tempo = 'tempo'
        time_signatures = 'time_signatures'
        transform = 'transform'
        written_duration = 'written_duration'

    attrs = Attrs()

    ### INITIALIZER ###

    def __init__(self, directives=None, name=None, score_template=None):
        self.directives = directives or []
        self.name = name
        self.score_template = score_template

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

    def select(self, score_segment_name=None, context_name=None, 
        criterion=None, selection_token=None, start=None, stop=None):
        #if selection_token is not None:
        #    raise NotImplementedError
        score_segment_name = score_segment_name or self.name
        selection = Selection(
            score_segment_name=score_segment_name, context_name=context_name,
            criterion=criterion, start=start, stop=stop)
        return selection

    def set_all_voice_directives_relative_to(self, voice_name, source_selection_token):
        target_selection = Selection(context_name=voice_name)
        source_selection = Selection(source_selection_token)
        directive = Directive(target_selection, 'everything', source_selection)
        self.directives.append(directive)

    def set_segment_aggregate(self, aggregate):
        target_selection = self.select()
        directive = Directive(target_selection, self.attrs.aggregate, aggregate)
        self.directives.append(directive)

    def set_segment_aggregate_to_aggregate_at_position(self, server, position):
        target_selection = self.select()
        handler = StatalServerRequest(server, position=position)
        directive = Directive(target_selection, self.attrs.aggregate, handler)
        self.directives.append(directive)

    def set_segment_aggregate_to_next_aggregate(self, server):
        target_selection = self.select()
        handler = StatalServerRequest(server, n=1, level=-1)
        directive = Directive(target_selection, self.attrs.aggregate, handler)
        self.directives.append(directive)

    def set_segment_duration_in_seconds(self, duration_in_seconds):
        target_selection = self.select()
        directive = Directive(target_selection, self.attrs.duration_in_seconds, duration_in_seconds)
        self.directives.append(directive)

    def set_segment_pitch_class_transform(self, transform):
        target_selection = self.select()
        directive = Directive(target_selection, self.attrs.transform, transform)
        self.directives.append(directive)

    def set_segment_pitch_classes_timewise(self, pitch_class_server, seed=None):
        target_selection = self.select()
        handler = TimewisePitchClassHandler(pitch_class_server)
        directive = Directive(target_selection, self.attrs.pitch_classes, handler, seed=seed)
        self.directives.append(directive)

    def set_segment_tempo(self, tempo):
        target_selection = self.select()
        directive = Directive(target_selection, self.attrs.tempo, tempo)
        self.directives.append(directive)

    def set_segment_tempo_relative_to_segment(self, source_segment_name):
        target_selection = self.select()
        source_selection = Selection(score_segment_name=source_segment_name)
        directive = Directive(target_selection, self.attrs.tempo, source_selection)
        self.directives.append(directive)

    def set_segment_time_signatures(self, time_signatures):
        target_selection = self.select()
        directive = Directive(target_selection, self.attrs.time_signatures, time_signatures)
        self.directives.append(directive)

    def set_segment_time_signatures_from_count(self, server, n, position=None):
        target_selection = self.select()
        handler = StatalServerRequest(server, n=1, level=-1, position=position) 
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_time_signatures_from_next_n_complete_nodes_at_level(self, server, n, level, position=None):
        target_selection = self.select()
        handler = StatalServerRequest(server, n=1, complete=True, level=level, position=position)
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_time_signatures_from_next_n_nodes_at_level(self, server, n, level, position=None):
        target_selection = self.select()
        handler = StatalServerRequest(server, n=1, complete=False, level=level, position=position)
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_time_signatures_not_less_than_duration_in_seconds(self, server, duration_in_seconds):
        target_selection = self.select()
        handler = DurationStatalServerRequest(server, duration_in_seconds, criterion='not less')
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_time_signatures_not_less_than_written_duration(self, server, written_duration):
        target_selection = self.select()
        handler = DuratedStatalServerRequest(server, written_duration, criterion='not less')
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_time_signatures_not_more_than_duration_in_seconds(self, server, duration_in_seconds):
        target_selection = self.select()
        handler = DurationStatalServerRequest(server, duration_in_seconds, criterion='not more')
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_time_signatures_not_more_than_written_duration(self, server, written_duration):
        target_selection = self.select()
        handler = DuratedStatalServerRequest(server, written_duration, criterion='not more')
        directive = Directive(target_selection, self.attrs.time_signatures, handler)

    def set_segment_written_duration(self, written_duration):
        target_selection = self.select()
        directive = Directive(target_selection, self.attrs.written_duration, written_duration)
        self.directives.append(directive)

    def set_voice_articulations(self, voice_name, handler, seed=None):
        target_selection = self.select(context_name=voice_name)
        directive = Directive(target_selection, self.attrs.articulations, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_chords(self, voice_name, handler, seed=None):
        target_selection = self.select(context_name=voice_name)
        directive = Directive(target_selection, self.attrs.chords, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_dynamics(self, voice_name, handler, seed=None):
        target_selection = self.select(context_name=voice_name)
        directive = Directive(target_selection, self.attrs.dynamics, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_dynamics_relative_to(self, voice_name, source_selection_token):
        target_selection = self.select(context_name=voice_name)
        source_selection = self.select(selection_token=source_selection_token)
        directive = Directive(target_selection, self.attrs.dynamics, source_selection)
        self.directives.append(directive)

    def set_voice_marks(self, voice_name, handler, seed=None):
        target_selection = self.select(context_name=voice_name)
        directive = Directive(target_selection, self.attrs.marks, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_markup(self, voice_name, handler, seed=None, **kwargs):
        target_selection = self.select(context_name=voice_name, **kwargs)
        directive = Directive(target_selection, handler, handler, seed=seed)
        self.directives.append(directive) 

    def set_voice_register(self, voice_name, handler, seed=None, **kwargs):
        target_selection = self.select(context_name=voice_name, **kwargs)
        directive = Directive(target_selection, self.attrs.register, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_rhythm(self, voice_name, handler_token, seed=None):
        target_selection = self.select(context_name=voice_name)
        division_handler, rhythm_handler = handler_token
        handler = CompositeRhythmHandler(division_handler, rhythm_handler)
        directive = Directive(target_selection, self.attrs.rhythm, handler, seed=seed)
        self.directives.append(directive)
