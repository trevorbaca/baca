from scf.specifiers.PerformerContributionSpecifierInventory import PerformerContributionSpecifierInventory
from scf.specifiers.Specifier import Specifier


class MusicSpecifier(Specifier):

    def __init__(self, 
        music_specifier_name=None, 
        performer_contribution_specifiers=None,
        tempo=None,
        ):
        Specifier.__init__(self)
        self.music_specifier_name = music_specifier_name
        self.performer_contribution_specifiers = \
            performer_contribution_specifiers or PerformerContributionSpecifierInventory()
        self.tempo = tempo

    ### CLASS ATTRIBUTES ###

    storage_module_import_statements = [
        'from abjad import *',
        'from abjad.tools import contexttools',
        'from abjad.tools import durationtools',
        'from scf import specifiers',
        ]

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.music_specifier_name or 'music specifier'
