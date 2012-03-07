from abjad.tools import pitchtools
from scf.editors.ListEditor import ListEditor
from scf.editors.OctaveTranspositionMappingEditor import OctaveTranspositionMappingEditor
from scf.menuing.UserInputGetter import UserInputGetter


class OctaveTranspositionMappingInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_class = pitchtools.OctaveTranspositionMappingInventory
    target_item_class = pitchtools.OctaveTranspositionMapping
    target_item_creator_class = OctaveTranspositionMappingEditor
    target_item_editor_class = OctaveTranspositionMappingEditor
    target_item_identifier = 'octave transposition mapping'
