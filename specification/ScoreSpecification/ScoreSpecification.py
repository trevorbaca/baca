from baca.specification.ScoreSegmentSpecification import ScoreSegmentSpecification


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

    # TODO: implement
    def interpret_segments(self, segments=None):
        segments = segments or self[:]
        for segment in segments:
            pass

    # TODO: implement
    def make_score(self):
        pass
