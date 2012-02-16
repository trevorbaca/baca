from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.editors.PerformerContributionSpecifierListEditor import PerformerContributionSpecifierListEditor
from baca.scf.editors.TempoMarkEditor import TempoMarkEditor
from baca.scf.MusicSpecifier import MusicSpecifier
from baca.scf.ObjectManifest import ObjectManifest
from baca.scf import getters
from baca.scf import predicates


class MusicSpecifierEditor(InteractiveEditor):

    target_class = MusicSpecifier
    target_manifest = ObjectManifest(MusicSpecifier,
        ('music_specifier_name', 'nm', getters.get_string),
        ('tempo', 'tp', TempoMarkEditor),
        ('performer_contribution_specifiers', 'pc', PerformerContributionSpecifierListEditor),
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'music specifier editor'
        
    @property
    def target_name(self):
        if self.target is not None:
            return self.target.music_specifier_name
