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
        ('inventory_name', 'name', 'nm', getters.get_string, False),
        target_attribute_name='inventory_name',
        )

    ### PUBLIC READ-ONLY PROPERTIES ###

    # TODO: abstract up to ObjectInventoryEditor
    @property
    def target_name(self):
        if self.target is not None:
            return self.target.inventory_name
