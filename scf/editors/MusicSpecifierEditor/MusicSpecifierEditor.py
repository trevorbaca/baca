from scf import getters
from scf import specifiers
from scf.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scf.editors.MusicContributionSpecifierEditor import MusicContributionSpecifierEditor
from scf.editors.TargetManifest import TargetManifest


class MusicSpecifierEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = specifiers.MusicContributionSpecifier
    item_creator_class = MusicContributionSpecifierEditor
    item_editor_class = MusicContributionSpecifierEditor
    item_identifier = 'performer contribution'
    target_manifest = TargetManifest(specifiers.MusicSpecifier,
        #('inventory_name', 'name', 'nm', getters.get_string, False),
        #target_attribute_name='inventory_name',
        )

    ### PUBLIC METHODS ###

    # TODO: abstract up to ListEditor after all tests pass
    def conditionally_initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self.target_class([])
