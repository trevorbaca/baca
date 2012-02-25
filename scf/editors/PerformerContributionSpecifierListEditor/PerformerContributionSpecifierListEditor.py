from scf.specifiers.PerformerContributionSpecifierList import PerformerContributionSpecifierList
from scf.specifiers.PerformerContributionSpecifier import PerformerContributionSpecifier
from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerContributionSpecifierEditor import PerformerContributionSpecifierEditor


class PerformerContributionSpecifierListEditor(ListEditor):

    target_class = PerformerContributionSpecifierList
    target_item_getter_configuration_method = None
    target_item_class = PerformerContributionSpecifier
    target_item_editor_class = PerformerContributionSpecifierEditor
    target_item_identifier = 'performer contribution specifier'
    target_items_identifier = 'performer contribution specifiers'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'performer contribution specifier editor'
