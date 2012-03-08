from scf import specifiers
from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerContributionSpecifierEditor import PerformerContributionSpecifierEditor
from scf.editors.TargetManifest import TargetManifest


class PerformerContributionSpecifierListEditor(ListEditor):

    target_item_getter_configuration_method = None
    target_item_class = specifiers.PerformerContributionSpecifier
    target_item_editor_class = PerformerContributionSpecifierEditor
    target_item_identifier = 'performer contribution'
    target_manifest = TargetManifest(specifiers.PerformerContributionSpecifierList,
        )
