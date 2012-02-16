from baca.scf.editors.ListEditor import ListEditor
from baca.scf.PerformerContributionSpecifierList import PerformerContributionSpecifierList
from baca.scf.PerformerContributionSpecifier import PerformerContributionSpecifier


class PerformerContributionSpecifierListEditor(ListEditor):

    target_class = PerformerContributionSpecifierList
    #target_item_getter_configuration_method = None
    target_item_class = PerformerContributionSpecifier
    #target_item_editor_class = PerformerContributionEditor
    target_item_identifier = 'performer contribution specifier'
    target_items_identifier = 'performer contribution specifiers'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def breadcrumb(self):
        return 'performer contribution specifier editor'
