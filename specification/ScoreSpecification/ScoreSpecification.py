from baca.specification.ScoreSegmentSpecification import ScoreSegmentSpecification


class ScoreSpecification(object):

   ### INITIALIZER ###

    def __init__(self, segment_specification_class=None, segments=None):
        self.segment_specification_class = segment_specification_class or ScoreSegmentSpecification
        self.segments = segments or []

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.segments)

    ### PUBLIC METHODS ###
    
    def append_segment(self, name=None):
        segment = self.segment_specification_class(name=name)     
        self.segments.append(segment)
        return segment
