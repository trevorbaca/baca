class StatalServerRequest(object):

    ### INITIALIZER ###
    
    def __init__(self, server, complete=False, level=None, n=None, position=None):
        self.server = server
        self.n = n
        self.complete = complete
        self.level = level
        self.position = position

    ### SPECIAL METHODS ###

    def __repr__(self):
        result = [repr(self.server)]
        kwargs = ('complete', 'level', 'n', 'position')
        for kwarg in kwargs:
            value = getattr(self, kwarg)
            if value is not None:
                result.append('{}={!r}'.format(kwarg, value))
        result = ', '.join(result)
        return '{}({})'.format(type(self).__name__, result)
