from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class PerformerSpecifier(ParameterSpecifier):

    def __init__(self, performer=None):
        ParameterSpecifier.__init__(self)
        self.performer = performer

    ### READ-ONLY ATTRIBUTES ###

    @property
    def one_line_menuing_summary(self):
        if self.performer:
            return self.performer.performer_name
