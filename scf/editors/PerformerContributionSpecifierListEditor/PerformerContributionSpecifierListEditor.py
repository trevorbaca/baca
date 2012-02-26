from scf.specifiers.PerformerContributionSpecifierList import PerformerContributionSpecifierList
from scf.specifiers.PerformerContributionSpecifier import PerformerContributionSpecifier
from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerContributionSpecifierEditor import PerformerContributionSpecifierEditor


class PerformerContributionSpecifierListEditor(ListEditor):

    target_class = PerformerContributionSpecifierList
    target_item_getter_configuration_method = None
    target_item_class = PerformerContributionSpecifier
    target_item_editor_class = PerformerContributionSpecifierEditor
    target_item_identifier = 'performer contribution'
    target_items_identifier = 'performer contributions'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'performer contributions'
