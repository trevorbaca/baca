from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from scf.specifiers.Specifier import Specifier


class PerformerContributionSpecifierInventory(Specifier, ObjectInventory):
    
    def __init__(self, *args):
        Specifier.__init__(self)
        ObjectInventory.__init__(self, *args)

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        pieces = [performer.performer_label for performer in self]
        if pieces:
            return ', '.join(pieces)
