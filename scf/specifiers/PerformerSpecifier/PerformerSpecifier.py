from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class PerformerSpecifier(ParameterSpecifier):

    def __init__(self, performer=None):
        Specifier.__init__(self)
        self.performer = performer
