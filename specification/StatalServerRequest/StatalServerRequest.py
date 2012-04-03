class StatalServerRequest(object):

    ### INITIALIZER ###
    
    def __init__(self, server, n=None, complete=False, level=None, position=None):
        self.server = server
        self.n = n
        self.complete = complete
        self.level = level
        self.position = position
