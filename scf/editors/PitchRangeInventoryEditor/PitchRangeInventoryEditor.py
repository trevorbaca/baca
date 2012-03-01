from abjad.tools import pitchtools
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.ListEditor import ListEditor
from scf.editors.PitchRangeEditor import PitchRangeEditor
from scf.menuing.UserInputGetter import UserInputGetter


class PitchRangeInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_class = pitchtools.PitchRangeInventory
    target_item_getter_configuration_method = UserInputGetter.append_symbolic_pitch_range_string
    target_item_class = pitchtools.PitchRange
    target_item_editor_class = PitchRangeEditor
    target_item_identifier = 'pitch range'
    target_items_identifier = 'pitch ranges'

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result
