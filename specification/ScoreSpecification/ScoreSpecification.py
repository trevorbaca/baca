from baca.specification.ScoreSegmentSpecification import ScoreSegmentSpecification
from baca.specification.Selection import Selection
from baca.specification.StatalServerRequest import StatalServerRequest
from baca.specification.SettingReservoirs import SettingReservoirs


class ScoreSpecification(object):

    ### INITIALIZER ###

    def __init__(self, score_template, score_segment_specification_class=None, segments=None):
        self.score_template = score_template
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
#        self.interpret_segment_attribute_directives(segment, 'tempo')
#        self.interpret_segment_attribute_directives(segment, 'time_signatures')
#        self.interpret_segment_attribute_directives(segment, 'aggregate')
#        self.interpret_segment_attribute_directives(segment, 'pitch_classes')
#        self.interpret_segment_attribute_directives(segment, 'transform')
        raise Exception

    def interpret_segment_attribute_directives(self, segment, attribute_name):
        directives = segment.get_directives(attribute_name=attribute_name)
        reservoir = getattr(self.reservoirs, attribute_name)
        for directive in directives:
            source_value = self.resolve_directive_source_value(directive.source)
            reservoir.store_settings(directive.target_selection, source_value, directive.is_persistent)

    def interpret_segments(self):
        self.reservoirs = SettingReservoirs(self.score_template())
        while any([segment.is_pending for segment in self.segments]):
            for segment in self.segments:
                self.interpret_segment(segment)

    def resolve_directive_source_value(self, directive_source):
        if isinstance(directive_source, Selection):
            raise NotImplementedError(repr(directive_source))
        elif isinstance(directive_source, StatalServerRequest):
            return directive_source()
        else:
            return directive_source
