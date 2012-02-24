from baca.scf.specifiers.PerformerContributionSpecifierList import PerformerContributionSpecifierList
from baca.scf.specifiers.Specifier import Specifier


class MusicSpecifier(Specifier):

    def __init__(self, 
        music_specifier_name=None, 
        performer_contribution_specifiers=None,
        tempo=None,
        ):
        Specifier.__init__(self)
        self.music_specifier_name = music_specifier_name
        self.performer_contribution_specifiers = \
            performer_contribution_specifiers or PerformerContributionSpecifierList()
        self.tempo = tempo

    ### READ-ONLY ATTRIBUTES ###

    storage_module_import_statements = [
        'from abjad import *',
        'from abjad.tools import contexttools',
        'from baca.scf.specifiers.MusicSpecifier import MusicSpecifier',
        'from baca.scf.specifiers.PerformerContributionSpecifierList import PerformerContributionSpecifierList',
        ]
