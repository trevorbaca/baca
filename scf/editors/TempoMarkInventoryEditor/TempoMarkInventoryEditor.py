from abjad.tools import contexttools
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.ListEditor import ListEditor
from scf.editors.TempoMarkEditor import TempoMarkEditor
from scf.menuing.UserInputGetter import UserInputGetter


class TempoMarkInventoryEditor(ListEditor):

    target_class = contexttools.TempoMarkInventory
    target_item_getter_configuration_method = UserInputGetter.append_tempo
    target_item_class = contexttools.TempoMark
    target_item_editor_class = TempoMarkEditor
    target_item_identifier = 'tempo mark'
    target_items_identifier = 'tempo marks'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_summary_lines(self):
        result = []
        for tempo_mark in self.target:
            result.append(repr(tempo_mark))
        return result
