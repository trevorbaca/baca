from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class PerformerSpecifier(ParameterSpecifier):

    def __init__(self, description=None, name=None, performer=None):
        ParameterSpecifier.__init__(self, description=description, name=name)
        self.performer = performer

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        if self.name:
            return self.name
        elif self.performer:
            return self.performer.name
