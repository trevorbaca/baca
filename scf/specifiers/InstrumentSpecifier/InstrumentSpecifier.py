from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class InstrumentSpecifier(ParameterSpecifier):

    def __init__(self, instrument=None):
        ParameterSpecifier.__init__(self)
        self.instrument = instrument

    ### READ-ONLY ATTRIBUTES ###

    @property
    def one_line_menuing_summary(self):
        try:
            return self.instrument.instrument_name
        except AttributeError:
            pass
