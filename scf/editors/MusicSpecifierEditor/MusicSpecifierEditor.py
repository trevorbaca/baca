from scf import getters
from scf import predicates
from scf import specifiers
from scf.editors.InteractiveEditor import InteractiveEditor
#from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerContributionSpecifierInventoryEditor import PerformerContributionSpecifierInventoryEditor
from scf.editors.TargetManifest import TargetManifest
from scf.selectors.TempoMarkSelector import TempoMarkSelector
from scf.specifiers.MusicSpecifier import MusicSpecifier


class MusicSpecifierEditor(InteractiveEditor):
#class MusicSpecifierEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    #item_class = specifiers.PerformerContributionList
    target_manifest = TargetManifest(MusicSpecifier,
        ('music_specifier_name', 'nm', getters.get_string),
        ('tempo', 'tp', TempoMarkSelector),
        ('performer_contribution_specifiers', 'performer contributions', 'pc', 
            PerformerContributionSpecifierInventoryEditor),
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.music_specifier_name
