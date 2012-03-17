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
        ObjectInventory.__init__(self, *args)
        Specifier.__init__(self, **kwargs)

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        '''Is there a way to do this programmatically?
        '''
        return tuple(sorted([
            'description',
            'inventory_name',
            'name',
            ]))

    @property
    def _item_class(self):
        return MusicContributionSpecifer
    
    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.music_specifier_name or 'music specifier'
