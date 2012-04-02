from baca.specifications.Constituent import Constituent


class Selection(object):

    ### INITIALIZER ###

    def __init__(self, constituents=None):
        self.constituents = constituents or []

    ### PUBLIC METHODS ###

    def append_constituent(self, component_name, start=None, stop=None):
        constituent = Constitutent(component_name, start=start, stop=stop)
        self.constituents.append(constituent)

    def append_note_and_chord_constituent(self, component_name, start=None, stop=None):
        constituent = Constituent(component_name, criterion='note and chord', start=start, stop=stop)
        self.constituents.append(constituent)
