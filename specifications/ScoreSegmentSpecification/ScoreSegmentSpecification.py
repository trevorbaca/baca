from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.handlers.pitch.TimewisePitchClassHandler import TimewisePitchClassHandler
from baca.specifications.Directive import Directive
from baca.specifications.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specifications.DurationSpecification import DurationSpecification
from baca.specifications.ParameterEnumeration import ParameterEnumeration
from baca.specifications.RelativeReference import RelativeReference
from baca.specifications.Selection import Selection
from baca.specifications.StatalServerRequest import StatalServerRequest


class ChunkSpecification(object):

    ### CLASS ATTRIBUTES ###
    
    attribute_names = (
        'duration_in_seconds',
        'name',
        'score_template',
        'tempo',
        'time_signatures',
        'written_duration',
        )

    parameters = ParameterEnumeration()

    ### INITIALIZER ###

    def __init__(self,
        directives=None,
        duration=None,
        time_signatures=None,
        name=None,
        score_template=None,
        tempo=None,
        ):
        self.directives = directives or []
        self.duration = duration
        self.time_signatures = time_signatures
        self.name = name
        self.score_template = score_template
        self.tempo = tempo

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def has_relative_references(self):
        return not self.relative_references

    @property
    def relative_references(self):
        result = []
        for attribute_name in self.attribute_names:
            directive = getattr(self, attribute_name)
            if directive.is_relative:
                result.append(directive)
        return result

    ### PUBLIC METHODS ###

    def select(self, chunk_name=None, context_name=None, criterion=None, start=None, stop=None):
        chunk_name = chunk_name or self.name
        selection = Selection(
            chunk_name=chunk_name, context_name=context_name,
            criterion=criterion, start=start, stop=stop)
        return selection

    def set_all_voice_directives_relative_to(self, target_voice_name, source_selection_token):
        target_selection = Selection(context_name=target_voice_name)
        source_selection = Selection(source_selection_token)
        directive = Directive(target_selection, 'everything', source_selection)
        self.directives.append(directive)

    def set_segment_directive(self, handler):
        selection = Selection(['Score'])
        directive = Directive(selection, handler)
        self.directives.append(directive)

    def set_segment_duration_in_seconds(self, duration_in_seconds):
        self.duration = DurationSpecification(duration_in_seconds, is_written=False)

    def set_segment_pitch_classes_timewise(self, pitch_class_server, seed=None):
        selection = Selection(['segment'])
        handler = TimewisePitchClassHandler(pitch_class_server)
        directive = Directive(selection, handler, seed=seed)
        self.directives.append(directive)

    def set_segment_score_template(self, score_template):
        self.score_template = score_template

    def set_segment_tempo(self, tempo):
        self.tempo = tempo

    def set_segment_tempo_relative_to_segment(self, source_segment_name):
        source_selection = Selection(segment_name=source_segment_name)
        self.tempo = RelativeReference(source_selection, 'tempo')

    def set_segment_time_signatures(self, time_signatures):
        self.time_signatures = time_signatures

    def set_segment_time_signatures_from_count(self, server, n, position=None):
        self.time_signatures = StatalServerRequest(server, n, level=-1, position=position) 

    def set_segment_time_signatures_from_next_n_complete_nodes_at_level(self, server, n, level, position=None):
        self.time_signatures = StatalServerRequest(server, n, complete=True, level=level, position=position)

    def set_segment_time_signatures_from_next_n_nodes_at_level(self, server, n, level, position=None):
        self.time_signatures = StatalServerRequest(server, n, complete=False, level=level, position=position)

    def set_segment_time_signatures_not_less_than_duration_in_seconds(self, server, duration_in_seconds):
        self.time_signatures = DurationStatalServerRequest(server, duration_in_seconds, criterion='not less')

    def set_segment_time_signatures_not_less_than_written_duration(self, server, written_duration):
        self.time_signatures = DuratedStatalServerRequest(server, written_duration, criterion='not less')

    def set_segment_time_signatures_not_more_than_duration_in_seconds(self, server, duration_in_seconds):
        self.time_signatures = DurationStatalServerRequest(server, duration_in_seconds, criterion='not more')

    def set_segment_time_signatures_not_more_than_written_duration(self, server, written_duration):
        self.time_signatures = DuratedStatalServerRequest(server, written_duration, criterion='not more')

    def set_segment_written_duration(self, written_duration):
        self.duration = DurationSpecification(written_duration, is_written=True)

    def set_voice_directive(self, voice_name, handler, seed=None):
        selection = Selection([voice_name])
        directive = Directive(selection, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_directive_for_notes_and_chords(self, voice_name, handler, n=None, seed=None):
        selection = Selection([])
        if n is None:
            selection.append_note_and_chord_constituent(voice_name)
        elif 0 < n:
            selection.append_note_and_chord_constituent(voice_name, stop=n)
        else:
            selection.append_note_and_chord_constituent(voice_name, start=-n)
        directive = Directive(selection, handler, seed=seed)
        self.directives.append(directive)

    def set_voice_dynamics(self, voice_name, handler, seed=None):
        target_selection = self.select(context_name=voice_name)
        directive = Directive(target_selection, self.parameters.dynamics, handler, seed=seed)

    def set_voice_dynamics_relative_to(self, voice_name, selection_token):
        source, target = Selection(selection_token), Selection([voice_name])
        directive = Directive(target, self.parameters.dynamics, source)
        self.directives.append(directive)

    def set_voice_rhythm(self, voice_name, division_handler, rhythm_handler, seed=None):
        selection = Selection([voice_name])
        composite_rhythm_handler = CompositeRhythmHandler(division_handler, rhythm_handler)
        directive = Directive(selection, composite_rhythm_handler, seed=seed)
        self.directives.append(directive)
