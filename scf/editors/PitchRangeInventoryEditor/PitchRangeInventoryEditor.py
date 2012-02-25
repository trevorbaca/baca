from abjad.tools import pitchtools
from baca.scf.editors.InteractiveEditor import InteractiveEditor
from baca.scf.editors.ListEditor import ListEditor
from baca.scf.editors.PitchRangeEditor import PitchRangeEditor
from baca.scf.menuing.UserInputGetter import UserInputGetter


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
    def breadcrumb(self):
        return 'pitch-range inventory'

    @property
    def summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result
