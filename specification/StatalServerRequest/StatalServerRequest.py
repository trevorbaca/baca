from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServerRequest(AbjadObject):

    ### INITIALIZER ###
    
    def __init__(self, server, complete=False, level=None, n=None, position=None):
        self.server = server
        self.n = n
        self.complete = complete
        self.level = level
        self.position = position

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.server(self)
