from scf.specifiers.ParameterSpecifier import ParameterSpecifier


class RhythmSpecifier(ParameterSpecifier):

    def __init__(self, kaleid_package_importable_name=None, description=None, name=None):
        ParameterSpecifier.__init__(self)
        self.kaleid_package_importable_name = kaleid_package_importable_name
        self.description = description
        self.name = name

    ### READ-ONLY ATTRIBUTES ###
    
    @property
    def one_line_menuing_summary(self):
        if self.name:
            return self.name
        else:
            self.kaleid_package_importable_name
        
