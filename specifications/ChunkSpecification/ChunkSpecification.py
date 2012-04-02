from baca.handlers.composites.CompositeRhythmHandler import CompositeRhythmHandler
from baca.specifications.Directive import Directive
from baca.specifications.DuratedStatalServerRequest import DuratedStatalServerRequest
from baca.specifications.DurationSpecification import DurationSpecification
from baca.specifications.RelativeReference import RelativeReference
from baca.specifications.StatalServerRequest import StatalServerRequest


class ChunkSpecification(object):

    ### CLASS ATTRIBUTES ###
    
    attribute_names = (
        'duration_in_seconds',
        'time_signatures',
        'name',
        'score_template',
        'tempo',
        'written_duration',
        )

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
        pass

    @property
    def relative_references(self):
        result = []
        for attribute_name in self.attribute_names:
            attribute_value = getattr(self, attribute_name)
            if isinstance(attribute_value, RelativeReference):
                result.append(attribute_value)
        return result

    ### PUBLIC METHODS ###

    def append_directive(self):
        directive = Directive(chunk_name=self.name)
        self.directives.append(directive)
        return directive

    def request_time_signatures(self, server, n, position=None):
        self.time_signatures = StatalServerRequest(server, n, level=-1, position=position) 

    def request_time_signatures_from_next_n_complete_nodes_at_level(self, server, n, level, position=None):
        self.time_signatures = StatalServerRequest(server, n, complete=True, level=level, position=position)

    def request_time_signatures_from_next_n_nodes_at_level(self, server, n, level, position=None):
        self.time_signatures = StatalServerRequest(server, n, complete=False, level=level, position=position)

    def request_time_signatures_not_less_than_duration_in_seconds(self, server, duration_in_seconds):
        self.time_signatures = DurationStatalServerRequest(server, duration_in_seconds, criterion='not less')

    def request_time_signatures_not_less_than_written_duration(self, server, written_duration):
        self.time_signatures = DuratedStatalServerRequest(server, written_duration, criterion='not less')

    def request_time_signatures_not_more_than_duration_in_seconds(self, server, duration_in_seconds):
        self.time_signatures = DurationStatalServerRequest(server, duration_in_seconds, criterion='not more')

    def request_time_signatures_not_more_than_written_duration(self, server, written_duration):
        self.time_signatures = DuratedStatalServerRequest(server, written_duration, criterion='not more')
    
    def set_chords_for_voice(self, voice_name, chord_handler):
        selection = Selection(voice_name)
        directive = Directive(selection, chord_handler)
        self.append_directive(directive)

    def set_rhythm_for_voice(self, voice_name, division_handler, rhythm_handler):
        selection = Selection(voice_name)
        composite_rhythm_handler = CompositeRhythmHandler(division_handler, rhythm_handler)
        directive = Directive(selection, composite_rhythm_handler)
        self.append_directive(directive)

    def set_time_signatures(self, time_signatures):
        self.time_signatures = time_signatures

    def set_duration_in_seconds(self, duration_in_seconds):
        self.duration = DurationSpecification(duration_in_seconds, is_written=False)

    def set_score_template(self, score_template):
        self.score_template = score_template

    def set_tempo(self, tempo):
        self.tempo = tempo

    def set_tempo_relative_to_chunk(self, chunk_name):
        self.tempo = RelativeReference(chunk_name, 'tempo')

    def set_written_duration(self, written_duration):
        self.duration = DurationSpecification(written_duration, is_written=True)
