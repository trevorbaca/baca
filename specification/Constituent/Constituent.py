class Constituent(object):

    ### INITIALIZER ###

    def __init__(self, chunk_name=None, context_name=None, criterion=None, start=None, stop=None):
        self.chunk_name = chunk_name
        self.context_name = context_name
        self.criterion = criterion
        self.start = start
        self.stop = stop
