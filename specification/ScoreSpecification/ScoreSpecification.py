from baca.specification.ScoreSegmentSpecification import ScoreSegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.InterpretationSettings import InterpretationSettings


class ScoreSpecification(object):

    ### INITIALIZER ###

    def __init__(self, default_score_template=None, score_segment_specification_class=None, segments=None):
        self.default_score_template = default_score_template
        self.score_segment_specification_class = score_segment_specification_class or ScoreSegmentSpecification
        self.segments = segments or []

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return self.segments[arg]
        elif isinstance(arg, str):
            for segment in self.segments:
                if segment.name == arg:
                    return segment
                else:
                    raise KeyError

    def __getslice__(self, start, stop):
        return self.segments.__getslice__(start, stop)

    def __len__(self):
        return len(self.segments)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.segments)

    ### PUBLIC METHODS ###
    
    def append_segment(self, name=None):
        segment = self.score_segment_specification_class(name=name)     
        self.segments.append(segment)
        return segment

    def interpret_segment(self, segment):
        segment.instantiate_score()
        self.interpret_segment_attribute(segment, 'tempo')
        self.interpret_segment_attribute(segment, 'time_signatures')
        self.interpret_segment_attribute(segment, 'aggregate')
        raise Exception

    def interpret_segment_attribute(self, segment, attribute_name):
        selection = segment.select()
        directives = segment.get_directives(target_selection=selection, attribute_name=attribute_name)
        assert 1 <= len(directives)
        for directive in directives:
            self.resolve_source_and_store_value(directive, attribute_name) 

    def interpret_segments(self):
        self.settings = InterpretationSettings()
        while any([segment.is_pending for segment in self.segments]):
            for segment in self.segments:
                self.interpret_segment(segment)

    def resolve_source(self, source):
        if isinstance(source, Selection):
            raise NotImplementedError(repr(source))
        elif isinstance(source, StatalServerRequest):
            return source()
        else:
            return source

    def resolve_source_and_store_value(self, directive, attribute_name):
        value = self.resolve_source(directive.source)
        setting = getattr(self.settings, attribute_name)
        setting.store_value(value, directive.is_persistent)
