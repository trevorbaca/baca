class Selection(object):

    ### INITIALIZER ###

    def __init__(self, constituents=None):
        self.constituents = constituents or []

    ### PUBLIC METHODS ###

    def append_constituent(self, component_name, start=None, stop=None):
        constituent = Constitutent(component_name, start=start, stop=stop)
        self.constituents.append(constituent)
