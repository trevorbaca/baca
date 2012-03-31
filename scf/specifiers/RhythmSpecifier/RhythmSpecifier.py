from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class RhythmSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, kaleid_package_importable_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.kaleid_package_importable_name = kaleid_package_importable_name

    ### READ-ONLY PROPERTIES ###
    
    @property
    def one_line_menuing_summary(self):
        return self.name or self.kaleid_package_importable_name
