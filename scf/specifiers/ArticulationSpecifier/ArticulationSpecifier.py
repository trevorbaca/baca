from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class ArticulationSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, articulation_handler_name=None, name=None):
        ParameterSpecifier.__init__(self, description=description, name=name)
        self.articulation_handler_name = articulation_handler_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.articulation_handler_name
