from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class InstrumentSpecifier(ParameterSpecifier):

    def __init__(self, description=None, instrument=None, name=None):
        ParameterSpecifier.__init__(self, description=description, name=name)
        self.instrument = instrument

    ### READ-ONLY ATTRIBUTES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.instrument.instrument_name
