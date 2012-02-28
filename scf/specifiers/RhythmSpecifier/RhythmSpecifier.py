from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class RhythmSpecifier(ParameterSpecifier):

    def __init__(self, kaleid=None):
        ParameterSpecifier.__init__(self)
        self.kaleid = kaleid

    ### READ-ONLY ATTRIBUTES ###
    
    @property
    def one_line_menuing_summary(self):
        try:
            return self.kaleid.kaleid_name
        except AttributeError:
            pass
