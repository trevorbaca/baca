class Selection(object):

    ### INITIALIZER ###

    def __init__(self, context_name=None, criterion=None, score_segment_name=None, start=None, stop=None):
        self.score_segment_name = score_segment_name
        self.context_name = context_name
        self.criterion = criterion
        self.start = start
        self.stop = stop

    ### SPECIAL METHODS ###

    def __repr__(self):
        result = []
        keyword_argument_names = ('context_name', 'criterion', 'score_segment_name', 'start', 'stop')
        for keyword_argument_name in keyword_argument_names:
            value = getattr(self, keyword_argument_name)
            if value is not None:
                result.append('{}={!r}'.format(keyword_argument_name, value))
        result = ', '.join(result)
        return '{}({})'.format(type(self).__name__, result)
