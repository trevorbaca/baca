from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServerRequest(AbjadObject):

    ### INITIALIZER ###
    
    def __init__(self, server, count=None, index=None):
        self.server = server
        self.count = count
        self.index = index

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.server(self)
