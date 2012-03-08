from abjad.tools import pitchtools
from scf import getters
from scf.editors.ListEditor import ListEditor
from scf.editors.OctaveTranspositionMappingEditor import OctaveTranspositionMappingEditor
from scf.editors.TargetManifest import TargetManifest


class OctaveTranspositionMappingInventoryEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    target_item_class = pitchtools.OctaveTranspositionMapping
    target_item_creator_class = OctaveTranspositionMappingEditor
    target_item_editor_class = OctaveTranspositionMappingEditor
    target_item_identifier = 'octave transposition mapping'
    target_manifest = TargetManifest(pitchtools.OctaveTranspositionMappingInventory,
        ('inventory_name', 'name', 'nm', getters.get_string),
        target_attribute_name='inventory_name',
        )
