from abjad.tools import contexttools
from scf import getters
from scf.editors.ListEditor import ListEditor
from scf.editors.TargetManifest import TargetManifest
from scf.editors.TempoMarkEditor import TempoMarkEditor
from scf.menuing.UserInputGetter import UserInputGetter


class TempoMarkInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_class = contexttools.TempoMarkInventory
    target_item_getter_configuration_method = UserInputGetter.append_tempo
    target_item_class = contexttools.TempoMark
    target_item_editor_class = TempoMarkEditor
    target_item_identifier = 'tempo mark'
    target_manifest = TargetManifest(contexttools.TempoMarkInventory,
        ('inventory_name', 'name', 'nm', getters.get_string),
        target_name_attribute='inventory name',
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_summary_lines(self):
        result = []
        for item in self.target:
            result.append(repr(item))
        return result
