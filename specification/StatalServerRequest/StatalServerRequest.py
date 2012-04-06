from abjad.tools.abctools.AbjadObject import AbjadObject
from baca.specification.StatalServer import StatalServer


class StatalServerRequest(AbjadObject):

    ### INITIALIZER ###
    
    #def __init__(self, server, count=None, offset=None):
    def __init__(self, server, count=None, seed=None):
        assert isinstance(server, StatalServer)
        self.server = server
        self.count = count
        self.seed = seed

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.server(self)
