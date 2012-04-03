class Constituent(object):

    ### INITIALIZER ###

    def __init__(self, score_segment_name=None, context_name=None, criterion=None, start=None, stop=None):
        self.score_segment_name = score_segment_name
        self.context_name = context_name
        self.criterion = criterion
        self.start = start
        self.stop = stop
