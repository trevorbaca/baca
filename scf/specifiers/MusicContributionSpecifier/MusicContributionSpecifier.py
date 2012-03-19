from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from scf.specifiers.Specifier import Specifier


class MusicContributionSpecifier(Specifier, ObjectInventory):

    def __init__(self, parameter_specifiers, description=None, name=None):
        ObjectInventory.__init__(self, parameter_specifiers)
        Specifier.__init__(self, description=description, name=name)

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        value = self.name or 'unknown contribution'
        return 'contribution: {}'.format(value)
