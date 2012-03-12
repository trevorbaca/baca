from scf import specifiers
from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerContributionSpecifierEditor import PerformerContributionSpecifierEditor
from scf.editors.TargetManifest import TargetManifest


class PerformerContributionSpecifierListEditor(ListEditor):

    item_getter_configuration_method = None
    item_class = specifiers.PerformerContributionSpecifier
    item_editor_class = PerformerContributionSpecifierEditor
    item_identifier = 'performer contribution'
    target_manifest = TargetManifest(specifiers.PerformerContributionSpecifierList,
        )
