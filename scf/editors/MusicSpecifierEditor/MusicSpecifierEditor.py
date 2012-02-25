from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.PerformerContributionSpecifierListEditor import PerformerContributionSpecifierListEditor
from scf.editors.TempoMarkEditor import TempoMarkEditor
from scf.specifiers.MusicSpecifier import MusicSpecifier
from scf.editors.TargetManifest import TargetManifest
from scf import getters
from scf import predicates


class MusicSpecifierEditor(InteractiveEditor):

    target_class = MusicSpecifier
    target_manifest = TargetManifest(MusicSpecifier,
        ('music_specifier_name', 'nm', getters.get_string),
        ('tempo', 'tp', TempoMarkEditor),
        ('performer_contribution_specifiers', 'pc', PerformerContributionSpecifierListEditor),
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or self.human_readable_class_name
        
    @property
    def target_name(self):
        if self.target is not None:
            return self.target.music_specifier_name
