from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class PitchClassSpecifier(ParameterSpecifier):

    def __init__(self, 
        description=None,
        name=None,
        pitch_class_reservoir=None, 
        pitch_class_reservoir_helper=None,
        pitch_class_transform=None
        ):
        ParameterSpecifier.__init__(self)
        self.description = description
        self.name = name
        self.pitch_class_reservoir = pitch_class_reservoir
        self.pitch_class_reservoir_helper = pitch_class_reservoir_helper
        self.pitch_class_transform = pitch_class_transform

    ### READ-ONLY ATTRIBUTES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.get_one_line_menuing_summary(self.pitch_class_reservoir)
