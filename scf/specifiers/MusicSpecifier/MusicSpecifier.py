from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from scf.specifiers.MusicContributionSpecifier import MusicContributionSpecifier
from scf.specifiers.Specifier import Specifier


class MusicSpecifier(Specifier, ObjectInventory):

    ### CLASS ATTRIBUTES ###

    storage_module_import_statements = [
        'from abjad import *',
        'from abjad.tools import contexttools',
        'from abjad.tools import durationtools',
        'from scf import specifiers',
        ]

    ### INITIALIZER ### 

    def __init__(self, *args, **kwargs):
        Specifier.__init__(self)
        ObjectInventory.__init__(self, *args)
        self.music_specifier_name = kwargs.get('music_specifier_name', None)

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _item_class(self):
        return MusicContributionSpecifer
    
    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.music_specifier_name or 'music specifier'
