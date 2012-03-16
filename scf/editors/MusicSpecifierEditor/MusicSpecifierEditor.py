from scf import getters
from scf import specifiers
from scf.editors.ListEditor import ListEditor
from scf.editors.MusicContributionSpecifierEditor import MusicContributionSpecifierEditor
from scf.editors.TargetManifest import TargetManifest


class MusicSpecifierEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_class = specifiers.MusicContributionSpecifier
    item_creator_class = MusicContributionSpecifierEditor
    item_editor_class = MusicContributionSpecifierEditor
    item_identifier = 'performer contribution'
    target_manifest = TargetManifest(specifiers.MusicSpecifier,
        ('music_specifier_name', 'nm', getters.get_string),
        target_attribute_name='music_specifier_name',
        )

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.music_specifier_name
