from abjad.tools import pitchtools
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.ListEditor import ListEditor
from scf.editors.PitchRangeEditor import PitchRangeEditor
from scf.editors.TargetManifest import TargetManifest
from scf.menuing.UserInputGetter import UserInputGetter


class PitchRangeInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_getter_configuration_method = UserInputGetter.append_symbolic_pitch_range_string
    item_class = pitchtools.PitchRange
    item_editor_class = PitchRangeEditor
    item_identifier = 'pitch range'
    target_manifest = TargetManifest(pitchtools.PitchRangeInventory,
        target_name_attribute='inventory_name',
        )

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def target_summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result
